import abc
import logging
from dataclasses import dataclass, field


auth_logger = logging.getLogger('auth_backend')


class SecurityError(BaseException):
    pass


class NotImplemented(SecurityError):
    def __init__(self):
        super().__init__(f'sorry, feature not implemented')


class NoSuchUser(SecurityError):
    def __init__(self, msg):
        super().__init__(f'user {msg} does not exists')


class NoSuchGroup(SecurityError):
    def __init__(self, msg):
        super().__init__(f'group /{msg} does not exists')


class DuplicateUser(SecurityError):
    def __init__(self, msg):
        super().__init__(f'user {msg} already exists')


class DuplicateGroup(SecurityError):
    def __init__(self, msg):
        super().__init__(f'group /{msg} already exists')


class DeleteGroupChildren(SecurityError):
    def __init__(self, msg):
        super().__init__(f'group /{msg} contains children')


@dataclass(frozen=True)
class UserBase:
    userid: str
    name: str
    groups: tuple
    preferredLanguage: str = field(init=False)


class RootGroup(object):
    name = 'root'
    description = 'Root group'


class SecurityBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial.
    """

    @abc.abstractmethod
    def test_plugin(self):
        """Used in tests"""

    @abc.abstractmethod
    def check_credentials(self, userid, password, domain=None):
        """Format the data and return unicode text.

        :param data: A dictionary with string keys and simple types as
                     values.
        :type data: dict(str:?)
        :returns: Iterable producing the formatted text.
        """

    @abc.abstractmethod
    def user_groups(self, userid, domain=None):
        """Format the data and return unicode text.

        :param data: A dictionary with string keys and simple types as
                     values.
        :type data: dict(str:?)
        :returns: Iterable producing the formatted text.
        """

    @abc.abstractmethod
    def delete_user(self, userid):
        """Format the data and return unicode text.

        :param data: A dictionary with string keys and simple types as
                     values.
        :type data: dict(str:?)
        :returns: Iterable producing the formatted text.
        """

    @abc.abstractmethod
    def delete_group(self):
        """Format the data and return unicode text.

        :param data: A dictionary with string keys and simple types as
                     values.
        :type data: dict(str:?)
        :returns: Iterable producing the formatted text.
        """
