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


class JobException(Exception):

    def __str__(self):
        return f'{self.__class__.__name__}({self.__cause__})'


class JobError(JobException):
    """An error prevented the execution of the job"""


class JobAbend(JobException):
    """A job abnormally ended"""


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
