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
# from datetime import datetime
import logging
import os
from pydblite import Base
from pysyncobj import SyncObj, SyncObjConf
# from singleton_decorator import singleton
from openbm.major.exceptions import (NoSuchJob,
                                     NoSuchJobSet,
                                     DuplicateJob,
                                     DuplicateJobSet,
                                     )
# import openbm.major.jobview


logger = logging.getLogger(__name__)


class SimpleCatalog(object):

    def __init__(self, path):
        self.repo = Base(os.path.join(path, 'jobs.db'))
        self.list = Base(os.path.join(path, 'list.db'))
        self.jobsets = Base(os.path.join(path, 'jobsets.db'))
        if self.repo.exists():
            self.repo.open()
        else:
            self.repo.create('name', 'spec', 'exec_time')
            self.repo.create_index('name')
        if self.list.exists():
            self.list.open()
        else:
            self.list.create('id', 'jobdata')
            self.list.create_index('id')
        if self.jobsets.exists():
            self.jobsets.open()
        else:
            self.jobsets.create('name', 'enabled', 'starttime', 'endtime',
                                'timezone', 'totalslots', 'usedslots')
            self.jobsets.create_index('name')

    def add_job_repo(self, jobname, jobspec):
        if jobname not in self.repo._name:
            self.repo.insert(name=jobname,
                             spec=jobspec, exec_time=[0, 0, 0, 0])
            self.repo.commit()
        else:
            raise DuplicateJob(f'jobname {jobname} already exists')

    def modify_job_repo(self, jobname, jobspec):
        record = self.repo._name[jobname]
        if record:
            self.repo.update(record, jobspec=jobspec)
            self.repo.commit()
        else:
            raise NoSuchJob(f'no such jobname: {jobname}')
        logger.debug(f'job {jobname} modified')

    def delete_job_repo(self, jobname):
        record = self.repo._name[jobname]
        if record:
            self.repo.delete(record)
            self.repo.commit()
        else:
            raise NoSuchJob(f'no such jobname: {jobname}')
        logger.debug(f'job {jobname} removed')

    def get_job_repo(self, jobname):
        record = self.repo._name[jobname]
        if record:
            return record[0]
        else:
            raise NoSuchJob(f'no such jobname: {jobname}')

    def get_all_jobs_repo(self):
        return self.repo

    def add_joblist(self, jobid, jobdict):
        assert jobid not in self.list._id
        self.list.insert(id=jobid, jobdata=jobdict)
        self.list.commit()

    def modify_joblist(self, jobid, jobdata, rundata):
        jobdict = self.list._id[jobid][0]['jobdata']
        jobdict.update(jobdata)
        if rundata is not None:
            jobdict['runs'][-1].update(rundata)

        record = self.list._id[jobid][0]
        self.list.update(record, jobdata=jobdict)
        self.list.commit()
        # openbm.major.jobview.modify(jobid, runid, jobdata, rundata)

    def delete_joblist(self, jobid):
        record = self.list._id[jobid]
        self.list.delete(record)
        self.list.commit()

    def getjob_joblist(self, jobid):
        return self.list._id[jobid][0]

    def add_jobset(self, name, starttime, endtime, totalslots, timezone):
        if name not in self.jobsets._name:
            self.jobsets.insert(name=name,
                                enabled=True,
                                starttime=starttime,
                                endtime=endtime,
                                timezone=timezone,
                                totalslots=totalslots,
                                usedslots=0
                                )
            self.jobsets.commit()
            logger.debug(f'job set {name} added')
        else:
            raise DuplicateJobSet(f'job set {name} already exists')

    def get_jobset(self, name):
        record = self.jobsets._name[name]
        if record:
            return record[0]
        else:
            raise NoSuchJobSet(f'no such job set: {name}')

    def get_jobsets(self, jobsets=None):
        if jobsets:
            return [jobset for jobset in self.jobsets._name
                    if jobset['name'] in jobsets]
        else:
            return self.jobsets

    def modify_jobset(self, name, jobsetdata):
        jobset = self.jobsets._name[name]
        if not jobset:
            raise NoSuchJobSet(f'no such job set: {name}')
        self.jobsets.update(jobset, **jobsetdata)
        self.jobsets.commit()

    def delete_jobset(self, name):
        record = self.jobsets._name[name]
        if record:
            self.jobsets.delete(record)
            self.jobsets.commit()
        else:
            raise NoSuchJobSet(f'no such job set: {name}')
        logger.debug(f'job set {name} removed')


class ClusterCatalog(SyncObj):

    def __init__(self, path, node, nodes):
        logger.debug([_[1] for _ in nodes])
        logger.debug(node)
        conf = SyncObjConf(dynamicMembershipChange=True,
                           fullDumpFile=os.path.join(path, f'dump'),
                           journalFile=os.path.join(path, f'journal'))

        SyncObj.__init__(self, node, [_[1] for _ in nodes], conf)
        self._offset = 0
        self._joboffsets = {}
        self._websrv = {}

    def get_jobsets(self, jobsets=None):
        return []
