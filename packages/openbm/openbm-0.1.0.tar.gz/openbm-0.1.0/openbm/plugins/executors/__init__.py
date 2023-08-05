import abc


class ExecutorBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial.
    """

    @abc.abstractmethod
    def exec_step(self, step, env):
        pass

    @abc.abstractmethod
    def abort_job(self, jobid):
        pass
