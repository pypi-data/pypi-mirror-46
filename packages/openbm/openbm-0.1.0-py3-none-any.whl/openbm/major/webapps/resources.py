#!/usr/bin/env python
#
#  Copyright (C) 2015 social2data S.A.
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


# from pyramid.security import Deny
from pyramid.security import Allow, Deny
# from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS
from pyramid.httpexceptions import (HTTPBadRequest,
                                    HTTPConflict,
                                    # HTTPCreated,
                                    HTTPForbidden,
                                    HTTPNotFound,
                                    HTTPNotImplemented,
                                    HTTPOk)
import json
# import jsonschema
# from jsonschema import validate
import yaml
import schema

# from plugins.auth import SecurityException
from openbm.plugins import auth
from openbm.major import exceptions
from openbm.minor import schemas


class Root(object):

    __name__ = ''
    __parent__ = None

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        if key == 'schedule':
            return ScheduleList(self, self.request)
        elif key == 'users':
            return UserList(self, self.request)
        elif key == 'groups':
            return Group(self, self.request, [], key)
        elif key == 'jobs':
            return JobList(self, self.request)
        elif key == 'nodes':
            return NodeList(self, self.request)
        elif key == 'jobsets':
            return JobSetList(self, self.request)
        elif key == 'calendars':
            return Calendars()
        elif key == 'cluster':
            return Cluster()
        raise KeyError


class Cluster(object):

    __name__ = 'cluster'
    __parent__ = Root

    def __init__(self):
        pass


class UserList(object):

    def __init__(self, parent, request):
        self.__name__ = 'users'
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler

    def __getitem__(self, key):
        return User(self, self.request, key)

    def get_list(self):
        return self.request.registry.auth.get_all_users()

    @property
    def __acl__(self):
        return [(Allow, 'root', ALL_PERMISSIONS),
                (Allow, 'admin', ALL_PERMISSIONS),
                (Allow, Authenticated, 'view_user')
                ]


class User(object):

    def __init__(self, parent, request, userid):
        self.__name__ = userid
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler
        self.userid = userid

    def get_user(self):
        try:
            return self.request.registry.auth.get_user(self.userid)
        except auth.NoSuchUser as e:
            raise HTTPNotFound(e)

    def add_user(self, password, **details):
        try:
            return self.request.registry.auth.create_user(self.userid,
                                                          password,
                                                          **details)
        except auth.DuplicateUser as e:
            raise HTTPConflict(e)
        except auth.NotImplemented as e:
            raise HTTPNotImplemented(e)

    def delete_user(self):
        try:
            self.request.registry.auth.delete_user(self.userid)
        except auth.NotImplemented as e:
            raise HTTPNotImplemented(e)

    @property
    def __acl__(self):
        acl = [(Allow, 'root', ALL_PERMISSIONS),
               (Allow, 'admin', ALL_PERMISSIONS),
               (Allow, self.userid, 'modify_user'),
               (Allow, self.userid, 'view_user'),
               ]

        if (any(group for group in
           self.request.registry.auth.user_groups(self.userid) if
           f'admin-{group}' in self.request.effective_principals[2:])):
            acl.append((Allow,
                        self.request.authenticated_userid, ALL_PERMISSIONS))
        return acl + [(Deny, Authenticated, ALL_PERMISSIONS)]


class Group(object):

    def __init__(self, parent, request, group, key):
        self.__name__ = key
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler
        if parent.__name__:
            self.group = group + [key]
        else:
            self.group = group

    def __getitem__(self, key):
        return Group(self, self.request, self.group, key)

    def create_group(self, desc):
        try:
            self.request.registry.auth.create_group(self.group, desc)
        except auth.NoSuchGroup as e:
            raise HTTPNotFound(e)
        except auth.DuplicateGroup as e:
            raise HTTPConflict(e)
        except auth.NotImplemented as e:
            raise HTTPNotImplemented(e)

    def get_group(self):
        try:
            return self.request.registry.auth.get_group(self.group)
        except auth.NoSuchGroup as e:
            raise HTTPNotFound(e)

    def delete_group(self):
        try:
            return self.request.registry.auth.delete_group(self.group)
        except auth.NoSuchGroup as e:
            raise HTTPNotFound(e)
        except auth.DeleteGroupChildren as e:
            raise HTTPConflict(e)
        except auth.NotImplemented as e:
            raise HTTPNotImplemented(e)

    @property
    def __acl__(self):
        return [(Allow, 'u:root', ALL_PERMISSIONS),
                (Allow, 'g:admin', ALL_PERMISSIONS),
                (Allow, f'g:admin-{self.__name__}', ALL_PERMISSIONS),
                (Allow, Authenticated, 'view_group')
                ]


class NodeGroups(object):

    __name__ = 'nodegroups'
    __parent__ = Root

    def __init__(self):
        """ TODO """


class Calendars(object):

    __name__ = 'calendars'
    __parent__ = Root

    def __init__(self):
        pass


class JobSetList(object):

    def __init__(self, parent, request):
        self.__name__ = 'jobsets'
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler

    def __getitem__(self, key):
        return JobSet(self, self.request, key)

    def get_list(self):
        raise HTTPOk([dict(node) for node
                     in self.scheduler('catalog.get_jobsets')])

    @property
    def __acl__(self):
        return [(Allow, 'u:root', ALL_PERMISSIONS),
                (Allow, 'r:admin', ALL_PERMISSIONS),
                (Allow, 'r:configurator', 'config_jobset'),
                (Allow, Authenticated, 'view_jobset')
                ]


class JobSet(object):

    def __init__(self, parent, request, jobsetname):
        self.__name__ = jobsetname
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler
        self.jobset = jobsetname

    def add_jobset(self, starttime, endtime, totalslots, timezone):
        try:
            self.scheduler('catalog.add_jobset', self.jobset,
                           starttime, endtime, totalslots, timezone)
        except exceptions.DuplicateJobSet:
            raise HTTPConflict(json_body={'status': 'error', 'code': 409,
                                          'message': f'job set <{self.jobset}>'
                                          ' already exists'}) from None

    def get_jobset(self):
        raise HTTPOk([dict(self.scheduler('catalog.get_jobset', self.jobset))])

    def modify_jobset(self, jobsetdata):
        try:
            self.scheduler('catalog.get_jobset', self.jobset)
        except exceptions.NoSuchJobSet:
            raise HTTPNotFound(f'job set <{self.jobset}> does not exists')

        self.scheduler('catalog.modify_jobset', self.jobset, jobsetdata)

    def delete_jobset(self):
        try:
            self.scheduler('catalog.delete_jobset', self.jobset)
        except exceptions.NoSuchJobSet:
            raise HTTPNotFound()

    @property
    def __acl__(self):
        return [(Allow, 'root', ALL_PERMISSIONS),
                (Allow, 'r:admin', ALL_PERMISSIONS),
                (Allow, f'r:admin-{self.jobset}', ALL_PERMISSIONS),
                (Allow, 'r:configurator', 'config_jobset'),
                (Allow, f'r:configurator-{self.jobset}', 'config_jobset'),
                (Allow, 'r:operator', 'oper_jobset'),
                (Allow, f'r:operator_{self.jobset}', 'oper_jobset'),
                ]


class NodeList(object):

    def __init__(self, parent, request):
        self.__name__ = 'nodes'
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler

    def __getitem__(self, key):
        return Node(self, self.request, key)

    def get_list(self):
        return self.scheduler('node_mgr.get_nodes')

    @property
    def __acl__(self):
        return [(Allow, Authenticated, 'view_node'),
                ]


class Node(object):

    def __init__(self, parent, request, nodename):
        self.__name__ = nodename
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler
        self.node = nodename
        # self.job = self.scheduler('get_job', jobname)

    def modify_node(self, inits):
        try:
            self.scheduler('node_mgr.modify_node', self.node, inits=inits)
        except IndexError:
            raise HTTPNotFound()

    @property
    def __acl__(self):
        perm = [(Allow, 'root', 'oper_node'),
                (Allow, 'opernode', 'oper_node'),
                (Allow, f'opernode_{self.node}', 'oper_node')
                ]
        for group in self.request.effective_principals[2:]:
            if (group != 'opernode' and group != f'opernode_{self.node}' and
               group.startswith('opernode')):
                perm.append((Allow, group, 'oper_node'))

        return perm


class ScheduleList(object):

    def __init__(self, parent, request):
        self.__name__ = 'schedules'
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler

    def __getitem__(self, key):
        return Schedule(self, self.request, key)
        # else:
        #    raise KeyError

    @property
    def __acl__(self):
        return [(Allow, 'r:operator', ('view_job', 'sched_job', 'start_job',
                                       'stop_job', 'comment_job')),
                (Allow, 'r:configurator', ('add_job', 'delete_job', 'view_job',
                                           'edit_job', 'comment_job')),
                (Allow, Authenticated, ('view_schedule')),
                ]

    def get_list(self, query):
        try:
            query = json.loads(query)
        except Exception as e:
            raise HTTPBadRequest('Malformed query string: ' + e.__str__())
        return self.scheduler('query_jobview', query)


class Schedule(object):

    def __init__(self, parent, request, jobid):
        self.__name__ = jobid
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler
        try:
            # self.job = self.scheduler('catalog.getjob_joblist',
            #                          jobid)['jobdata']
            self.job = self.scheduler('query_jobview',
                                      {'rules': [{'field': 'jobs.jobid',
                                                  'operator': 'equal',
                                                  'value': self.__name__}]})[0]
        except IndexError:
            raise HTTPNotFound() from None

    def abort(self):
        if self.job['status'] != 'EXE':
            raise HTTPBadRequest('Job is not in EXE status')
        return self.scheduler('abort_job', self.__name__)

    def details(self):
        job = self.scheduler('query_jobview',
                             {'rules': [{'field': 'jobs.jobid',
                                         'operator': 'equal',
                                         'value': self.__name__}]})[0]
        return job

    def delete_schedule(self):
        return self.scheduler('delete_schedule', self.__name__)

    def refresh_schedule(self):
        try:
            self.scheduler('refresh_schedule', self.__name__)
        except exceptions.NoSuchSchedule as e:
            raise HTTPNotFound(e)

    def source(self):
        return self.scheduler('catalog.getjob_joblist', self.__name__)

    @property
    def __acl__(self):
        return [(Allow, 'r:operator', ('view_job', 'sched_job', 'start_job',
                                       'stop_job', 'comment_job')),
                (Allow, 'r:configurator', ('add_job', 'delete_job', 'view_job',
                                           'edit_job', 'comment_job')),
                (Allow, Authenticated, ('view_job')),
                ]


class JobList(object):

    def __init__(self, parent, request):
        self.__name__ = 'jobs'
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler

    def __getitem__(self, key):
        return Job(self, self.request, key)

    def add_job(self, jobspec, replace=False):
        try:
            jobdict = yaml.load(jobspec)
            schemas.jobschema.validate(jobdict)
        except (yaml.YAMLError,
                schema.SchemaError) as e:
            raise HTTPBadRequest(e)
        if jobdict['owner'] not in self.request.effective_principals[2:]:
            raise HTTPForbidden(f'owner not authorized for job')
        try:
            self.scheduler('catalog.add_job_repo', jobdict['name'], jobspec)
        except exceptions.DuplicateJob as exc:
            if replace:
                self.delete_job(jobdict['name'])
                self.scheduler('catalog.add_job_repo', jobdict['name'],
                               jobspec)
            else:
                raise HTTPConflict(exceptions.DuplicateJob(exc))

        # FIXME falta la invocacion final!!!
        # raise HTTPCreated('job added')

    def validate_job(self, jobspec):
        try:
            jobdict = yaml.load(jobspec)
            schemas.jobschema.validate(jobdict)
        except (yaml.YAMLError,
                schema.SchemaError) as e:
            raise HTTPBadRequest(e)
        # raise HTTPOk('ok')

    def delete_job(self, jobname):
        try:
            self.scheduler('catalog.delete_job_repo', jobname)
        except exceptions.NoSuchJob as e:
            raise HTTPNotFound(e)

    def get_jobs(self):
        return [job['name'] for job in
                self.scheduler('catalog.get_all_jobs_repo')]

    @property
    def __acl__(self):
        return [(Allow, 'u:root', ALL_PERMISSIONS),
                (Allow, 'r:admin', ALL_PERMISSIONS),
                (Allow, 'r:configurator', 'config_jobs'),
                ]


class Job(object):

    def __init__(self, parent, request, jobname):
        self.__name__ = jobname
        self.__parent__ = parent
        self.request = request
        self.scheduler = request.scheduler

    def get_job(self):
        try:
            return self.scheduler('catalog.get_job_repo', self.__name__)
        except exceptions.NoSuchJob as e:
            raise HTTPNotFound(e)

    def add_schedule(self, when):
        try:
            # FIXME timeargs['now'] = '1' if timeargs['now'] else None
            return self.scheduler('schedule_job', self.__name__, when)

        except exceptions.NoSuchJob as e:
            raise HTTPNotFound(e)
        except exceptions.ScheduleError as e:
            raise HTTPBadRequest(e)

    def delete_job(self):
        try:
            return self.scheduler('catalog.delete_job_repo', self.__name__)
        except exceptions.NoSuchJob as e:
            raise HTTPNotFound(e)

    @property
    def __acl__(self):
        return [(Allow, 'u:root', ALL_PERMISSIONS),
                (Allow, 'r:admin', ALL_PERMISSIONS),
                (Allow, 'r:monitor', 'view_jobs'),
                (Allow, 'r:monitor-{self.jobname}', 'view_jobs'),
                (Allow, 'r:configurator', 'config_jobs'),
                (Allow, 'r:configurator-{self.jobname}', 'config_jobs'),
                (Allow, 'r:operator', 'oper_jobs'),
                (Allow, 'r:operator-{self.jobname}', 'oper_jobs'),
                ]
