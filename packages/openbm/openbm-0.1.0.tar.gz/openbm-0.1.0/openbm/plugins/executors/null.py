class Null(object):
    SCHEMA = {}

    def test_plugin():
        return Null(None, None)

    def __init__(self, config, scheduler):
        pass

    def start_job(self, jobid, runid, jobspec):
        pass

    async def exec_step(self, jobid, step, env):
        pass

    async def abort_job(self, jobid):
        pass

    def end_job(self, runid):
        pass

    def on_shutdown(self):
        pass
