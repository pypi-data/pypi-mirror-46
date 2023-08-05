#!/usr/bin/env python
#
#  Copyright (C) 2016 Oscar Curero
#
#  This file is part of OpenBatchManager.
#
#  OpenBatchManager free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  OpenBatchManager is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied  warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with OpenBatchmanager.  If not, see <http://www.gnu.org/licenses/>.
#
import asyncio
# from collections import OrderedDict
from datetime import datetime
import logging
import pickle
import pytz
import re
# import sys
from aioprocessing import AioPipe, AioEvent
from multiprocessing import Process
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.memory import MemoryJobStore
# from apscheduler.schedulers.asyncio import AsyncIOScheduler ?
# from apscheduler.executors.pool import ProcessPoolExecutor ?
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
import networkx as nx
from networkx.algorithms.dag import descendants, ancestors
import pendulum
import tblib.pickling_support
import websockets
import yaml
from openbm.plugins.load import (load_notifiers,
                                 load_auth_backend,
                                 )
from openbm.minor import MinorScheduler
# from openbm.major.catalogs import (SimpleCatalog)
from openbm.major.catalogs import (ClusterCatalog, SimpleCatalog)
# from openbm.major.nodestores import (SimpleNodeStore)
from openbm.major.exceptions import (DuplicateJob,
                                     InternalSchedulerError,
                                     NoSuchJob,
                                     )
# from openbm.major.executors import NodePoolExecutor
from openbm.major.nodestores import (RaftNodeStore, SimpleNodeStore)
# from openbm.major import dist_logging
# from openbm.major.triggers import OBMTrigger
from openbm.major.utils import dsndate_fmt, dsntime_fmt
import openbm.major.jobview
from openbm.major.webapps import webserver


tblib.pickling_support.install()
loop = asyncio.get_event_loop()

logger = logging.getLogger(__name__)


class MajorScheduler(MinorScheduler):
    """Base class for Major scheduler"""
    cron_many = re.compile('\*|/|-')

    def __init__(self, config):
        # self.jobview_queue = []
        self.schid = config['major'].pop('default_scheduler', 1)
        self.tz = config['major']['timezone']
        logger.info(f'starting in {self.tz} timezone')
        self.ws_clients = dict()
        self.locks = dict()
        # self.node_pool = NodePoolExecutor(self, self.ws_clients)
        #                                  config['jobstores']['major'])
        super().__init__(config)
        user_dayshift = config['major']['reload_time'].split(':')
        self.dayshift = pendulum.now(self.tz
                                     ).replace(hour=int(user_dayshift[0]),
                                               minute=int(user_dayshift[1]),
                                               second=int(user_dayshift[2]))
        if self.dayshift < pendulum.now(self.tz):
            self.dayshift = self.dayshift.add(days=1)

        # self.major = self._jobstores['major']
        self.dep_mgr = nx.DiGraph()
        for jobset in self.catalog.get_jobsets():
            self.dep_mgr.add_node(f'JOBSET_{jobset.name}')
            logger.debug(f'Created jobset {jobset.name} dependency')
        super().add_job(self._update_scheduler, 'cron', jobstore='int',
                        hour=int(user_dayshift[0]),
                        minute=int(user_dayshift[1]),
                        second=int(user_dayshift[2]))

        self.notifiers = load_notifiers(config)
        self.auth = load_auth_backend(config)

    async def start(self, init):
        openbm.major.jobview.load(self.catalog.list, self.dayshift, self.tz)
        om_start = AioEvent()
        self.om_task = asyncio.ensure_future(self._run_om(self.config,
                                                          om_start))
        logger.debug('Waiting for Operation Manager to become active')
        await om_start.coro_wait()
        server = websockets.serve(self._ws_handler,
                                  self.config['major']['node_addr'],
                                  self.config['major']['node_port'])
        self.ws_server = await server
        await super().start()
        if init:
            await self._update_interval_jobs()
            logger.debug('interval jobs initialization complete')
            await self._update_scheduler()
            logger.warning('scheduler initialitzation complete')
        self.add_job(self._archive_jobview, trigger='interval',
                     jobstore='int', minutes=10)
        await self.om_task

    def shutdown(self):
        logger.info('Waiting for jobs to finish')
        super().shutdown()

    async def stop(self):
        self.om_task.cancel()

    def _configure(self, config):
        # threads = asint(config.pop('threads', 50))
        config['jobstores'] = {'major': MemoryJobStore()}
        # config['executors'] = {'node': self.node_pool}
        super()._configure(config)

    async def _ws_handle(self, major_ready):
        major_ready.set()

    async def _run_om(self, config, event):
        logger.debug('Launching OM in another process')
        ep_local, ep_remote = AioPipe()
        log_local, log_remote = AioPipe()
        # om_proc = AioProcess(target=webserver.run, daemon=True,
        #                      args=(config, ep_remote, log_remote, event))
        om_proc = Process(target=webserver.run,
                          args=(config, ep_remote, log_remote, event))
        om_proc.daemon = True
        om_proc.start()
        while True:
            try:
                msg = await ep_local.coro_recv()
            except asyncio.CancelledError as ex:
                logger.debug('Stopping OM task')
                om_proc.terminate()
                break
            if msg[0][0] is None:
                om_proc.terminate()
                raise RuntimeError
            try:
                func = self
                for method in msg[0][0].split('.'):
                    func = getattr(func, method)
                reply = func(*msg[0][1:], **msg[1])
                if asyncio.iscoroutine(reply):
                    reply = await reply
            except BaseException as e:
                reply = InternalSchedulerError(e)
            ep_local.send(reply)

    def schedule_job(self, jobname, datetime):
        """Schedule a registered job to the scheduler"""
        job = self.catalog.get_job_repo(jobname)
        jobid = self.create_jobid(job["name"], 'R', datetime)
        jobdata = self.create_job(jobid, 'R', datetime, job)
        return jobdata['jobid']

    def schedule_joboneshot(self, job, datetime):
        """Schedule a one-time job to the scheduler"""
        try:
            self.catalog.get_job_repo(job['name'])
            raise DuplicateJob()
        except NoSuchJob:
            pass
        jobid = self.create_jobid(job["name"], 'R', datetime)
        jobdata = self.create_job(jobid, 'R', datetime, job)
        return jobdata['jobid']

    async def abort_job(self, jobid):
        run = self.catalog.getjob_joblist(jobid)['jobdata']['runs'][-1]
        if run['node'] != self.name:
            pass
        else:
            await super().abort_job(jobid)

    def query_jobview(self, filters):
        return openbm.major.jobview.filter(filters)

    def get_descendants(self, prov_name):
        return list(descendants(self.dep_mgr, prov_name))

    def get_ancestors(self, prov_name):
        try:
            return self.dep_mgr.nodes[list(
                ancestors(self.dep_mgr, prov_name))[0]]
        except IndexError:
            return []

    def delete_schedule(self, jobname):
        try:
            return super().remove_job(jobname, jobstore='major')
        except JobLookupError:
            # avoid exception chainning by using "raise ... from none"
            raise openbm.exceptions.ScheduleLookupError(jobname) from None
        except Exception as e:
            raise e

    def cluster_status(self):
        return False

    def find_leader(self):
        return False

    async def send_notify(self, event, message, group, title=''):

        recipients = self.auth.group_users(group.split('/'))
        send = []
        for notifier in self.notifiers:
            if notifier.filter(event):
                send.append(loop.run_in_executor(None, notifier.notify,
                                                 recipients,
                                                 message,
                                                 title))
        await asyncio.gather(*send)

    def _manage_jobstatus(self, jobid, jobdata, rundata={}):
        self.catalog.modify_joblist(jobid, jobdata, rundata)
        openbm.major.jobview.modify(jobid, jobdata, rundata)
        if jobdata['status'] in ('ABD', 'NDF'):
            job = self.catalog.getjob_joblist(jobid)['jobdata']
            if jobdata['status'] == 'ABD':
                message = f'Job {jobid} has ended abnormally'
                title = f'Job {jobid} ended abnormally'
            elif jobdata['status'] == 'NDF':
                message = f'Job {jobid} has undefined dependencies'
                title = f'Job {jobid} has unidefined dependencies'
            loop.create_task(self.send_notify(jobdata['status'], message,
                                              job['owner'], title))
        if jobdata['status'] == 'FOK' and jobid[-9] == 'I':
            jobname = self.catalog.getjob_joblist(jobid)['jobdata']['jobname']
            job = self.catalog.get_job_repo(jobname)
            loop.create_task(self._update_interval_job(job))

    async def _ws_handler(self, ws, name):
        try:
            name, inits = name.lstrip('/').split('/')
            int(inits)
        except ValueError:
            await ws.close(code=4000)
            logger.error(f'Invalid URI from {ws.remote_address[0]}')
        logger.debug(f'New connection from {name} ({ws.remote_address[0]})')
        if name not in self.ws_clients and name != self.name:
            self.node_mgr.add_node(name, inits)
            self.ws_clients[name] = ws
            logger.info(f'node {name} initialized with {inits} inits')
        else:
            await ws.close(code=4001)
            logger.error(f'Duplicate node: {name}')
            return
        while True:
            try:
                data = await ws.recv()
            except websockets.exceptions.ConnectionClosed:
                self.node_mgr.modify_node(name, status='LST')
                del(self.ws_clients[name])
                break
            method, args, kwargs, need_response = pickle.loads(data)
            response = getattr(self, method)(*args, **kwargs)
            if need_response:
                rrr = pickle.dumps(response)
                print(rrr)
                await ws.send(pickle.dumps(response))

    async def _archive_jobview(self):
        print('JOB ARCHIVING IS RUNNING')

    async def _update_interval_jobs(self):
        logger.debug('scheduling jobs for the next 5min')
        for job in self.catalog.get_all_jobs_repo():
            await self._update_interval_job(job)

    async def _update_interval_job(self, job):
        for schedule in yaml.load(job['spec']).get('schedule', []):
            if (re.match(self.cron_many,
                         str(schedule.get('minute', '*'))) or
               re.match(self.cron_many, str(schedule.get('second', '*')))):
                await self._schedule_job('I', job, self.dayshift, **schedule)
        logger.debug('refresh ended OK')

    async def _update_scheduler(self):
        # self.dayshift = self.dayshift.add(days=1)
        logger.debug('Scheduling jobs for the next 24h')
        schedule_list = []
        for job in self.catalog.get_all_jobs_repo():
            for schedule in yaml.load(job['spec']).get('schedule', []):
                if (isinstance(schedule.get('minute', None), int) and
                   isinstance(schedule.get('second', None), int)):
                    schedule_list.append(self._schedule_job('D', job,
                                                            self.dayshift,
                                                            **schedule))
                    # schedule_list.append(self._schedule_interv_job(job,
                    #                                             **schedule))

            if len(schedule_list) == 100:
                await asyncio.gather(*schedule_list)
                schedule_list = []
        await asyncio.gather(*schedule_list)
        logger.debug('updating complete joblist')
        # openbm.major.jobview.load(self.catalog.list, self.dayshift, self.tz)
        logger.debug('refresh ended OK')

    async def _schedule_job(self, sch_type, job, date_limit, **triggerargs):
        schedule = datetime.now(tz=pytz.timezone(self.tz))
        triggerargs.setdefault('timezone', self.tz)
        # try:
        cron = CronTrigger(**triggerargs)
        # except ValueError as ex:
        #    raise ScheduleError(ex)
        while True:
            schedule = pendulum.instance(cron.get_next_fire_time(schedule,
                                                                 schedule))
            if schedule and schedule <= date_limit:
                jobid = (f'{job["name"]}{sch_type}'
                         f'{pendulum.instance(schedule).day_of_year}'
                         f'{(self.dayshift - schedule).in_seconds():05}')
                jobid = self.create_jobid(job["name"], sch_type, schedule)
                self.create_job(jobid, sch_type, schedule, job)
                if sch_type == 'I':
                    break
            else:
                break

    def create_jobid(self, jobname, schedule_type, schedule_datetime):
        """ Create a jobid string from a jobname, schedule type and
        schedule datetime """
        timestamp = schedule_datetime or pendulum.now(self.tz)
        offset = (self.dayshift - timestamp).in_seconds()
        return f'{jobname}{schedule_type}{timestamp.day_of_year}{offset:05}'

    def create_job(self, jobid, sch_type, schedule, job):
        # NOTE Here we add our job to the scheduler using the TZ from
        # the scheduler because DateTrigger does not get it from main
        # tz = self.tz
        # schedule = pendulum.instance(schedule)
        # jobid = f'{job.id}{pendulum.now(self.tz).day_of_year}{id(job)}'
        # runid = f'{jobid}:0'
        est_exec_time = job['exec_time'][-1]
        # est_sta_time = schedule
        jobdict = yaml.load(job['spec'])
        schedule_date = schedule or pendulum.now(self.tz)
        dsn_date = dsndate_fmt(schedule_date)
        dsn_time = dsntime_fmt(schedule_date)
        default_provider = f'{job["name"]}.{dsn_date}'
        if sch_type in ('R', 'I'):
            default_provider += dsn_time
        if 'provides' not in jobdict:
            jobdict['provides'] = []
        jobdict['provides'].append(default_provider)
        jobdata = {'jobname': job['name'],
                   'jobid': jobid,
                   'prio': 0,
                   'owner': jobdict['owner'],
                   'est_sta_time': None,
                   'est_exec_time': est_exec_time,
                   'scheduler': jobdict.get('scheduler',
                                            self.schid),
                   'prereq': [],
                   'provides': jobdict['provides'],
                   'source': jobdict.get('steps'),
                   'runs': []}
        for prereq in jobdict.get('prereqs', []):
            if 'type' in prereq and prereq['type'] == 'user':
                jobdata['status'] = 'USR'
            dep_name = prereq['name'].replace('%SCHDATE',
                                              dsn_date).replace('%SCHTIME',
                                                                dsn_time)
            jobdata['prereq'].append(dep_name)
        self.catalog.add_joblist(jobid, jobdata)
        openbm.major.jobview.insert_job(jobdata.copy(), self.dayshift, self.tz)
        if not jobdict.get('prereqs', []):
            self.create_run(jobdict, jobdata, schedule)
        return jobdata

    def create_run(self, jobdict, jobdata, schedule):
        # NOTE Here we add our job to the scheduler using the TZ from
        # the scheduler because DateTrigger does not get it from main
        jobid = jobdata['jobid']
        # runid = len(jobdata["runs"])
        jobdata['runs'].append({'sta_time': None,
                                'sto_time': None,
                                'node': jobdict.get('node', None),
                                'rc': None
                                })
        self.add_job(self._subjob, jobstore='major', id=jobid,
                     args=(jobid, jobdata), misfire_grace_time=None,
                     trigger=DateTrigger(schedule, self.tz))
        est_sta_time = self.get_job(jobid, 'major').next_run_time
        # est_time_stop = est_sta_time + timedelta(est_time_exec)
        self.catalog.modify_joblist(jobid,
                                    {'est_sta_time': est_sta_time}, {})
        openbm.major.jobview.modify(jobid,
                                    {'est_sta_time': est_sta_time},
                                    jobdata['runs'][-1])

    def set_dependencies(self, job_name, sch_type, run_date, job):
        date_req = run_date or pendulum.now(self.tz)
        dsn_date = dsndate_fmt(date_req)
        dsn_time = dsntime_fmt(date_req)
        prov_name = f'{job_name}.{dsn_date}'
        if sch_type in ('R', 'I'):
            prov_name += f'.{dsn_time}'
        job['provider'] = prov_name
        if not self.dep_mgr.has_node(prov_name):
            self.dep_mgr.add_node(prov_name, jobid=job['jobid'],
                                  defined=True)
        else:
            self.dep_mgr.node[prov_name]['defined'] = True
            self.dep_mgr.node[prov_name]['jobid'] = job['jobid']
        for num, dep in enumerate(job['prereqs']):
            dep_name = dep['name'].replace('%SCHDATE',
                                           dsn_date).replace('%SCHTIME',
                                                             dsn_time)
            job['prereqs'][num]['name'] = dep_name
            logger.debug(f'Dependency set to {dep_name} for job {job_name}')
            if ('cond' in dep and dep['cond']
               and not self.dep_mgr.has_node(dep_name)):
                continue
            if not self.dep_mgr.has_node(dep_name):
                self.dep_mgr.add_node(dep_name, jobid=None,
                                      defined=False)
            self.dep_mgr.add_edge(dep_name, prov_name)

    async def _subjob(self, jobid, jobspec):
        self._manage_jobstatus(jobid, {'status': 'RSB'}, {})
        while True:
            try:
                node = self.node_mgr.select_node(jobspec['runs'][-1]['node'])
                break
            except ValueError:
                self._manage_jobstatus(jobid, {'status': 'WSB'}, {})
                await self.node_mgr.condition.wait()
        self._manage_jobstatus(jobid, {'status': 'SBP'},
                               {'node': node['name']})
        if node['name'] == self.name:
            # to local node
            await self._execjob(jobid, jobspec)
        else:
            # submit job to node
            self.locks[jobid] = asyncio.Condition()
            await self.ws_clients[node['name']].send('hola')
        # self._manage_jobstatus(jobid, {'status': 'SUB'}, {})


class StandaloneMajorScheduler(MajorScheduler):

    def __init__(self, config):
        self.type = 'standalone'
        self.node_mgr = SimpleNodeStore(config)
        self.catalog = SimpleCatalog(config['minor']['data_dir'])
        super().__init__(config)


class ClusterMajorScheduler(MajorScheduler):

    def __init__(self, config):
        self.type = 'cluster'
        self.node = '{}:{}'.format(config['major']['cluster_addr'],
                                   config['major']['cluster_port'])
        self.node_mgr = RaftNodeStore(config)
        self.catalog = ClusterCatalog(config['minor']['data_dir'],
                                      self.node, config['cluster'])
        super().__init__(config)

    def _configure(self, config):
        self.node_mgr = RaftNodeStore(config)
        # cluster = RaftCatalog(node, config.pop('cluster'))
        logger.warning('Waitting for cluster to become ready')
        while not self.catalog.isReady():
            asyncio.sleep(1)
        # self.catalog.setaddr(self.node, config.pop('om_addr'),
        #                     config.pop('om_port'))
        super()._configure(config)
