import sys


class InternalSchedulerError(Exception):

    def __init__(self, ee):
        self.ee = ee
        __,  __, self.tb = sys.exc_info()

    def re_raise(self):
        raise self.ee.with_traceback(self.tb)


class SchedulerError(BaseException):
    pass


class ScheduleError(SchedulerError):
    pass


class JobError(SchedulerError):
    pass


class NoSuchSchedule(ScheduleError):
    pass


class JobStoreError(SchedulerError):
    pass


class NoSuchJob(JobStoreError):
    pass


class DuplicateJob(JobStoreError):
    pass


class NoSuchJobSet(JobStoreError):
    pass


class DuplicateJobSet(JobStoreError):
    pass


class NoSuchNode(JobStoreError):
    pass


class DuplicateNode(JobStoreError):
    pass


class TriggerError(SchedulerError):
    pass
