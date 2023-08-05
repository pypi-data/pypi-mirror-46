import abc


class NotifierBase(metaclass=abc.ABCMeta):

    def __init__(self, config):
        self.event_mask = config.get('events', 'ALL').split(',')
        self.config = config

    def notify(self, recipients, message, title, **kwargs):
        """to be overriden"""

    def filter(self, event):
        return True if (event in self.event_mask or
                        'ALL' in self.event_mask or
                        f'!{event}' not in self.event_mask) else False
