import pkg_resources
from openbm.plugins import notifiers
# Create the fake entry point definition
ep = pkg_resources.EntryPoint.parse('dummy = openbm.plugins.notifiers.testing:'
                                    'TestNotifier')
# Create a fake distribution to insert into the global working_set
d = pkg_resources.Distribution('')
# Add the mapping to the fake EntryPoint
d._ep_map = {'openbm.plugins.notifiers': {'dummy': ep}}
# Add the fake distribution to the global working_set
pkg_resources.working_set.add(d, 'dummy')


class TestNotifier(notifiers.NotifierBase):
    def notify(self, recipients, message, title):
        pass
