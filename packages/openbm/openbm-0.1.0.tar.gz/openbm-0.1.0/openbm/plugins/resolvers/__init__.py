import abc


class ResolverBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial.
    """

    def init(self, jobid, runid, jobspec):
        pass

    @abc.abstractmethod
    def exec_step(self, step, env):
        pass

    def end_step(self, step):
        pass

    def end_job(self, job):
        pass

    def on_shutdown(self):
        pass
