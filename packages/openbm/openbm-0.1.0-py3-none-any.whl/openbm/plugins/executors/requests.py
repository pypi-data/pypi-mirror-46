import asyncio
from concurrent.futures import ThreadPoolExecutor
import psutil
from subprocess import PIPE
from schema import Optional
from openbm.exceptions import JobAbend  # , JobError
from openbm.major import loop


class Command(object):
    SCHEMA = {'cmd': str,
              Optional('shell'): str,
              Optional('runas'): str,
              }

    def test_plugin():
        return Command(None, None)

    def __init__(self, config, scheduler):
        self.processes = {}

    @staticmethod
    def _create_rc_exception(return_code):
            class RCException(Exception):

                pass

            RCException.__name__ = f'RC{return_code}'

            return RCException()

    def start_job(self, jobid, runid, jobspec):
        pass

    async def exec_step(self, jobid, step, env):
        p = psutil.Popen(str(step['cmd']), stdout=PIPE, shell=True)
        with ThreadPoolExecutor() as thread_executor:
            process = loop.run_in_executor(thread_executor, p.wait)
            self.processes[jobid] = process
            try:
                await process
            except asyncio.CancelledError:
                p.kill()
                self.processes.pop(jobid)
                raise JobAbend() from RuntimeError('killed')
            self.processes.pop(jobid)
        if p.returncode > 0:
            raise JobAbend() from self._create_rc_exception(p.returncode)
        else:
            return {'stdout': p.stdout.read()}

    async def abort_job(self, jobid):
        task = self.processes[jobid]
        task.cancel()
        await asyncio.wait((task,))

    def end_job(self, job):
        pass

    def on_shutdown(self):
        pass
