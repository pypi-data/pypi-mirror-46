import logging
# import notifiers as gnotifiers
from notifiers.providers.email import SMTP as SMTP_backend
from notifiers.providers.telegram import Telegram as Telegram_backend
from notifiers.providers.pushbullet import Pushbullet as Pushbullet_backend
from notifiers.core import Provider, Response
from openbm.plugins import notifiers


logger = logging.getLogger(__name__)


class DummyNotifier(Provider):
    site_url = '/dev/null'
    base_url = '/dev/null'
    name = 'dummy'
    _schema = {'type': 'object',
               'properties': {'message': {'type': 'string', 'title': ''}},
               'additionalProperties': True}
    _required = {'required': ['message']}

    def _send_notification(self, data: dict) -> Response:
        pass


class Notifiers(notifiers.NotifierBase):

    def __init__(self, notifier_to, recipient_field, config):
        super().__init__(config)
        config.pop('enabled')
        self.notifier_to = notifier_to
        self.to_attr = recipient_field

    def notify(self, recipients, **kwargs):
        kwargs.pop('events')
        for recipient in recipients:
            if hasattr(recipient, self.to_attr):
                logger.debug(f'notifing {getattr(recipient, self.to_attr)}')
                self.notifier.notify(**{**kwargs,
                                     self.notifier_to: getattr(recipient,
                                                               self.to_attr)})
            else:
                logger.debug(f'Notification not sent: user {recipient} does '
                             f'not has an attribute named {self.to_attr}')


class Email(Notifiers):

    def test_plugin():
        plugin = Email({'enabled': True, 'events': 'ALL',
                        'from_addr': 'noreply@localhost'})
        plugin.notifier = DummyNotifier()
        return plugin

    def __init__(self, config):
        self.notifier = SMTP_backend()
        super().__init__('to', 'email', config)

    def notify(self, recipients, message, title):
        super().notify(recipients, message=message, subject=title,
                       from_=self.config['from_addr'], **dict(self.config))


class Telegram(Notifiers):

    def test_plugin():
        plugin = Telegram({'enabled': True, 'events': 'ALL',
                           'token': 1234, 'user_field': 'phone1'})
        plugin.notifier = DummyNotifier()
        return plugin

    def __init__(self, config):
        self.notifier = Telegram_backend()
        self.token = config.pop('token')
        super().__init__('chat_id', config.get('user_field', 'email'), config)

    def notify(self, recipients, message, title):
        super().notify(recipients, message=message, token=self.token,
                       **dict(self.config))


class Pushbullet(Notifiers):

    def test_plugin():
        plugin = Pushbullet({'enabled': True, 'events': 'ALL', 'token': 1234,
                             'user_field': 'email'})
        plugin.notifier = DummyNotifier()
        return plugin

    def __init__(self, config):
        self.notifier = Pushbullet_backend()
        self.token = config.pop('token')
        super().__init__('email', config.get('user_field', 'email'), config)

    def notify(self, recipients, message, title):
        super().notify(recipients, message=message, title='',
                       token=self.token, **dict(self.config))
