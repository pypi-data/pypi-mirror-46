import logging
from dataclasses import dataclass
from openbm.plugins import auth


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class User(auth.UserBase):
    email: str


class InsecureAuth(auth.SecurityBase):

    def test_plugin():
        return InsecureAuth({'email': None})

    def __init__(self, config):
        logger.warning('Use of insecure backend, as its name implies, is '
                       'insecure')
        if 'email' not in config:
            raise ValueError('email option not found in insecure_auth section')
        self.user = User(userid='root',
                         name='root',
                         email=config['email'],
                         groups=('root'))
        super().__init__()

    def check_credentials(self, userid, passwd):
        return ['r:admin', '/root']

    def create_user(self, userid, passwd, **kwargs):
        raise auth.NotImplemented()

    def create_group(self, group_path, desc):
        raise auth.NotImplemented()

    def delete_user(self, userid):
        raise auth.NotImplemented()

    def delete_group(self, group_path):
        raise auth.NotImplemented()

    def change_password(self, userid, oldpasswd, newpasswd):
        raise auth.NotImplemented()

    def get_all_users(self):
        return ['root']

    def get_user(self, userid):
        return self.user

    def get_group(self, group_path):
        return {'group': 'root',
                'path': '/root',
                'children': [],
                'group_description': 'root',
                'users': 'root'}

    def add_user_group(self, groupid, userid):
        raise auth.NotImplemented()

    def user_groups(self, userid):
        return ['root']

    def group_users(self, group_path):
        return [self.user]
