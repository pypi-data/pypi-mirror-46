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
# from asyncio import FIRST_COMPLETED
import itertools
import logging
import os
import pickle
# import pytz
# import time
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler import events
# from apscheduler.util import asint
from boolrule import BoolRule
import pendulum
import pydblite
import websockets
from openbm.exceptions import (JobError,
                               JobAbend,
                               )
from openbm.plugins.load import (load_executors)
# from websockets.exceptions import ConnectionClosed
# from openbm.utils import dsndate_fmt


loop = asyncio.get_event_loop()
logger = logging.getLogger('openbm')


# logging.getLogger('apscheduler.executors.node').addFilter(r)


class MinorScheduler(AsyncIOScheduler):

    def __init__(self, config, **options):
        logger.debug(f'Starting a {self.__class__.__name__} scheduler')
        self.config = config
        # executors = {'mgr': ThreadPoolExecutor(10)}

        self.name = config['minor'].pop('node_name')
        self.datadir = config['minor'].pop('data_dir')
        if not os.path.exists(os.path.join(self.datadir, 'joblogs')):
            os.mkdir(os.path.join(self.datadir, 'joblogs'))
        self.security = config['minor'].getboolean('security', 'on')
        self.cert = config['minor'].pop('certificate')
        self.usedinits = 0
        # self.addr = config.pop('address')
        # self.port = config.pop('port')
        # self.tz = config['timezone'] FIXME
        # logger.info(f'Scheduler starting in {self.tz} timezone')
        logging.getLogger('asyncio').setLevel(logging.DEBUG)
        logger.debug(f'Process PID {os.getpid()}')
        super().__init__(**options)
        local_jobs_path = os.path.join(self.datadir, 'localjobs.db')
        self.local_jobs = pydblite.Base(local_jobs_path)
        if self.local_jobs.exists():
            self.local_jobs.open()
        else:
            self.local_jobs.create('jobid', 'step', 'executor')
            self.local_jobs.create_index('jobid')

    async def start(self):
        # self.add_listener(self._event_subjob, mask=events.EVENT_JOB_ADDED)
        self.add_listener(self._event_execjob, mask=events.EVENT_JOB_SUBMITTED)
        # self.add_listener(self._event_abendjob, mask=events.EVENT_JOB_ERROR)
        # self.add_listener(self._event_endedjob, mask=even.EVENT_JOB_EXECUTED)
        major_ready = asyncio.Event()
        asyncio.get_event_loop().create_task(self._ws_handle(major_ready))
        await major_ready.wait()
        # await self._ws_handle()
        self.executors = load_executors(self)
        super().start()
        logger.info(f'OpenBatchManager is now active in node {self.name}')

    async def stop(self):
        pass

    def _configure(self, config):
        if 'executors' not in config:
            config['executors'] = {}
        if 'jobstores' not in config:
            config['jobstores'] = {}
        if 'triggers' not in config:
            config['triggers'] = {}

        config['jobstores']['int'] = MemoryJobStore()
        config['executors']['jobs'] = ProcessPoolExecutor(5)
        # config['timezone'] = self.tz FIXME
        config['job_defaults'] = {'coalesce': False}
        # self.mgr_sch.start()
        super()._configure(config)

    async def _ws_handle(self, major_ready):
        proto = 'wss://' if self.security else 'ws://'
        servers = self.config['minor']['servers'].split(',')
        for connection in itertools.cycle(servers):
            logger.debug(f'Connecting to {proto}{connection}')
            server = websockets.connect(f'{proto}{connection}/{self.name}')
            try:
                self.ws = await asyncio.wait_for(server, 5)
                # await self.ws.send('2')
                major_ready.set()
                logger.info(f'Connected to major node {connection}')
                await self._ws_recv()
            except websockets.exceptions.ConnectionClosed as ex:
                if ex.code == 4000:
                    logger.critical(f'Node {self.name} already'
                                    f' exist in server {connection}')
                    return

            except Exception as ex:
                # await server.close()
                if isinstance(ex, asyncio.TimeoutError):
                    ex = 'timeout'
                logger.error(f'Connection to {connection} failed: {ex}')
            await asyncio.sleep(5)

    async def _ws_recv(self):
        while True:
            message = await self.ws.recv()
            method, args, kwargs, need_response = pickle.loads(message)
            response = await self.dispatcher[method](*args, **kwargs)
            print('estamos en handler')
            if need_response:
                print('enviamos respuesta')
                print(response)
                rrr = pickle.dumps(response)
                print(rrr)
                await self.ws.send(pickle.dumps(response))

    def _event_subjob(self, event):
        if event.jobstore == 'major':
            logger.debug(f'Job {event.job_id} submitted')
            self._manage_jobstatus(event.job_id, {'status': 'SCH'})

    def _event_execjob(self, event):
        if event.jobstore == 'major':
            self.usedinits += 1
            logger.debug(f'Job {event.job_id} executed')
            self._manage_jobstatus(event.job_id, {'status': 'SUB'})
            if 'MajorScheduler' in self.__class__.mro():
                self.node_mgr.modify_node(self.name, usedinits=self.usedinits)

    def _event_abendjob(self, event):
        if event.jobstore == 'major':
            self.usedinits -= 1
            logger.debug(f'Job {event.job_id} as ended abnormally')
            self._manage_jobstatus(event.job_id, {'status': 'ABD'},
                                   {'rc': str(event.exception)})
            if 'MajorScheduler' in self.__class__.mro():
                self.node_mgr.modify_node(self.name, usedinits=self.usedinits)

    def _event_endedjob(self, event):
        if event.jobstore == 'major':
            self.usedinits -= 1
            logger.debug(f'Job {event.job_id} executed')
            if not event.retval:
                event.retval = 'END_OK'
            self._manage_jobstatus(event.job_id, {'status': 'FOK'},
                                   {'rc': event.retval})
            if 'MajorScheduler' in self.__class__.mro():
                self.node_mgr.modify_node(self.name, usedinits=self.usedinits)

    # @staticmethod
    async def _execjob(self, jobid, jobspec):
        self._manage_jobstatus(jobid, {'status': 'EXE'},
                               {'sta_time': pendulum.now('UTC')})
        logger.info(f'Job {jobid} is running')
        joblog = logging.getLogger(jobid)
        joblog_file = logging.FileHandler(os.path.join(self.datadir, 'joblogs',
                                                       f'{jobid}'))
        joblog_file.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))
        joblog.addHandler(joblog_file)
        joblog.info(f'Job {jobid} started on node {self.name}')
        env = {'params': {}, 'exception': None, 'steps': {}, 'vars': {}}
        for num, step in enumerate(jobspec['source']):
            name = step.get('id', f'step{num}')
            joblog.info(f'Step {name} started')
            runcond = BoolRule(step.get('runcond', 'exception is None'))
            abdrule = step.get('abdcond', f'steps.{name}.exception is None')
            if not runcond.test(env):
                env['steps'][name] = {'exception': 'Flush'}
                logger.info(f'Step {name} FLUSHed for job {jobid}')
                continue
            try:
                exec_name = step.get('type', 'cmd')  # default executor
                if exec_name not in self.executors.entry_points_names():
                    raise JobError() from \
                        ValueError(f'executor {exec_name} not found')

                self.local_jobs.insert(jobid, num, exec_name)
                self.local_jobs.commit()
                logger.info(f'Started {name} step for job {jobid}')
                executor = self.executors.map_method(lambda ext, *args:
                                                     exec_name == ext.name,
                                                     'exec_step', jobid,
                                                     step, env)[0]
                ret = await executor or {}
                env['steps'][name] = {'exception': None, **ret}
            except (JobAbend, JobError) as ex:
                exc_name = ex.__class__.__name__
                exc_info = repr(ex) if isinstance(repr(ex), dict) else {}
                env['steps'][name] = {'exception': exc_name, **exc_info}
                last_exc = ex
            finally:
                if not BoolRule(abdrule).test(env):
                    if env['steps'][name]['exception']:
                        env['exception'] = env['steps'][name]['exception']
                    else:
                        env['exception'] = ValueError('ABDCOND')
                        last_exc = env['exception']
                    logger.info(f'Step {name} failed at condition {abdrule}')
                else:
                    logger.info(f'Ended {name} step for job {jobid}')

        if env['exception']:
            logger.info(f'Job {jobid} ENDED ABNORMALLY')
            rc = str(last_exc)
            status = 'ABD'
        else:
            logger.info(f'Job {jobid} ended')
            rc = 'END_OK'
            status = 'FOK'
        self._manage_jobstatus(jobid, {'status': status}, {'rc': rc,
                               'sto_time': pendulum.now('UTC')})
        self.local_jobs.delete(self.local_jobs(jobid=jobid))

    async def abort_job(self, jobid):
        logger.debug(f'Abort task started for jobid {jobid}')
        job = self.local_jobs._jobid[jobid][0]
        executor = self.executors.map_method(lambda ext, *args:
                                             job['executor'] == ext.name,
                                             'abort_job', jobid)[0]
        await executor
        logger.info(f'Jobid {jobid} has been aborted')

    def _manage_jobstatus(self, jobid, status, rundata={}):
        print(status, '<--minor')
        # TODO: Use RPC to execute manage_jobstatus remotelly

    def recv_job_proc(self, coro=None):
        coro.set_daemon()
        logger.debug('receive job queue started')
        while True:
            jobid, runid, jobspec = yield coro.receive()
            super().add_job(self._execjob, jobstore='node',
                            id=f'{jobid}:{runid}',
                            args=(jobspec, jobid, runid),
                            executor='process')
