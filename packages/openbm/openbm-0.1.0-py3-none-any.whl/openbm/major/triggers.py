import asyncio
import logging
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.combining import BaseCombiningTrigger
import pendulum
from openbm.major.nodestores import (RaftNodeStore, SimpleNodeStore)
# from openbm.major.catalogs import (SimpleCatalog)

logger = logging.getLogger(__name__)


class OBMTrigger(BaseCombiningTrigger):

    def __init__(self, tipology, node_name, job, schedule, tz):
        # triggers = [NodeTrigger(tipology, node_name, tz)]
        triggers = []
        if schedule:
            triggers.append(ScheduleTrigger(run_date=schedule, timezone=tz))
        # if jobdata['prepreq']:
        #    triggers.append(DepTrigger(jobdata['prereq']))

        super().__init__(triggers)

    def get_next_fire_time(self, previous_fire_time, now):
        fire_times = [trigger.get_next_fire_time(previous_fire_time, now)
                      for trigger in self.triggers]
        return max(fire_times)


class ScheduleTrigger(DateTrigger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_next_fire_time(self, previous_fire_time, now):
        fire_time = super().get_next_fire_time(previous_fire_time, now)
        if fire_time is not None:
            return fire_time
        else:
            return now


class NodeTrigger(BaseTrigger):

    def __init__(self, tipology, node, tz):
        if tipology == 'standalone':
            node_mgr = SimpleNodeStore()
        else:
            node_mgr = RaftNodeStore()
        self.ready = False
        if not node.startswith('@') and node not in node_mgr.get_nodes():
            self.tz = tz
            asyncio.get_event_loop().create_task(self.poll(node_mgr.condition))
        else:
            self.ready = True

    async def poll(self, node_ready):
        await node_ready.wait()
        self.ready = True

    def get_next_fire_time(self, previous_fire_time, now):
        if self.ready:
            return now
        else:
            return pendulum.instance(now).in_timezone(self.tz).add(minutes=1,
                                                                   seconds=2)
