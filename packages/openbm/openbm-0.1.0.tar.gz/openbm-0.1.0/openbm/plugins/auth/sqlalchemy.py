# import AuthnPlugin
# from yapsy.IPlugin import IPlugin
# from simpleplugins import Plugin
import itertools
# from pyramid_sqlalchemy import BaseObject
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import transaction
from sqlalchemy import Column, ForeignKey, engine_from_config
# , engine_from_config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import Integer, String, Time, Binary
# from pyramid_sqlalchemy import Session, metadata, init_sqlalchemy
from openbm.plugins import auth

Base = declarative_base()
Session = sessionmaker()


class OBMUser(Base):
    __tablename__ = 'obm_users'
    userid = Column(String(255), primary_key=True)
    passwd = Column(String(255))
    name = Column(String(255))
    # surname = Column(String(255))
    email = Column(String(255))
    phone1 = Column(String(15))
    phone2 = Column(String(15))
    phone3 = Column(String(15))
    photo = Binary()
    lang = Column(String(5))
    last_login = Time()


class OBMGroup(Base):
    __tablename__ = 'obm_groups'
    groupid = Column(Integer, primary_key=True)
    name = Column(String(255))
    parent = Column(Integer, ForeignKey('obm_groups.groupid'))
    description = Column(String(255))
    parent_rel = relationship('OBMGroup',
                              remote_side=[groupid], backref='children_rel')
    users_rel = relationship('OBMUserGroups')

    @hybrid_property
    def users(self):
        return [user.user for user in self.users_rel]

    @hybrid_property
    def childrens(self):
        if self.groupid == 0:
            name = '/'
        else:
            name = self.name
        if self.children_rel:
            path = '/'.join([group.childrens for group in self.children_rel])
            return [name, '/' + path]
        else:
            return name


class OBMUserGroups(Base):
    __tablename__ = 'obm_usergroups'
    groupid = Column(Integer, ForeignKey('obm_groups.groupid'),
                     primary_key=True)
    userid = Column(String(255), ForeignKey('obm_users.userid'),
                    primary_key=True)
    group_rel = relationship('OBMGroup', uselist=False)
    user = relationship('OBMUser')

    @hybrid_property
    def group(self):
        if int(self.groupid) == -2:
            return OBMGroup(groupid=0, name='root', parent=0)
        else:
            return self.group_rel


class SQLAlchemyAuth(auth.SecurityBase):

    def test_plugin():
        config = {'url': 'sqlite:///:memory:'}
        return SQLAlchemyAuth(config)

    def __init__(self, config):
        engine = engine_from_config(config, '')
        Session.configure(bind=engine, extension=ZopeTransactionExtension())
        Base.metadata.create_all(engine)
        self.session = Session()
        try:
            with transaction.manager:
                self.session.add(OBMUser(userid='root', passwd=''))
                self.session.add(OBMGroup(groupid=0, parent=-1, name='root',
                                          description='Root Group'))
                self.session.add(OBMUserGroups(groupid=0, userid='root'))
        except IntegrityError:
            pass
        super().__init__()

    def _user_exists(self, userid):
        return self.session.query(OBMUser).filter_by(userid=userid).first()

    def _group_exists(self, group_path):
        parent = 0
        if not group_path or group_path == ['root']:
            return self.session.query(OBMGroup).filter_by(groupid=0).first()
        for group_name in group_path:
            if group_name == '':
                continue
            group = self.session.query(OBMGroup).filter_by(name=group_name,
                                                           parent=parent
                                                           ).first()
            if not group:
                return False
            parent = group.groupid
        return group

    def check_credentials(self, userid, passwd):
        user = self.session.query(OBMUser).filter_by(userid=userid,
                                                     passwd=passwd).first()
        if user is not None:
            return itertools.chain(*self.user_groups(userid))
        else:
            return None

    def create_user(self, userid, passwd, **kwargs):
        try:
            with transaction.manager:
                self.session.add(OBMUser(userid=userid, passwd=passwd,
                                         **kwargs))
        except IntegrityError:
            raise auth.DuplicateUser(userid)

    def create_group(self, group, desc):
        group_path = group.split('/')
        group_name = group_path[-1]
        if self._group_exists(group_path):
            raise auth.DuplicateGroup(group)
        parent = self._group_exists(group_path[:-1])
        if not parent:
            raise auth.NoSuchGroup(group)
        with transaction.manager:
            self.session.add(OBMGroup(name=group_name, parent=parent.groupid,
                                      description=desc))

    def delete_user(self, userid):
        raise auth.NotImplemented()

    def delete_group(self, group_name):
        group_path = group_name.split('/')
        group = self._group_exists(group_path)
        if not group:
            raise auth.NoSuchGroup(group_name)
        try:
            self.session.query(OBMGroup).filter_by(parent=group.groupid).one()
            raise auth.DeleteGroupChildren('/'.join(group_path))
        except NoResultFound:
            with transaction.manager:
                self.session.delete(group)

    def change_password(self, userid, oldpasswd, newpasswd):
        if self.check_credentials(userid, oldpasswd):
            with transaction.manager:
                self.session.query(OBMUser).filter_by(
                    userid=userid).update({'passwd': newpasswd})
                return True
        else:
            return False

    def get_all_users(self):
        return [row.userid for row in self.session.query(OBMUser).all()]

    def get_user(self, userid):
        user = self._user_exists(userid)
        if not user:
            raise auth.NoSuchUser(userid)
        return {'userid': user.userid,
                'name': user.name,
                'email': user.email,
                'groups': self.user_groups(userid)}

    def get_group(self, group_name):
        group_path = group_name.split('/')
        group = self._group_exists(group_path)
        if not group:
            raise auth.NoSuchGroup(group_name)

        return {'group': group.name,
                'path': '/' + '/'.join(group_path),
                'children': [row.name for row in
                             self.session.query(OBMGroup).
                             filter_by(parent=group.groupid).all()],
                'group_description': group.description,
                'users': [user.userid for user in group.users]}

    def add_user_group(self, group_path, userid):
        if self._user_exists(userid):
            try:
                groupid = self._group_exists(group_path.split('/')).groupid
            except AttributeError:
                raise auth.NoSuchGroup(group_path)
            with transaction.manager:
                self.session.add(OBMUserGroups(groupid=groupid, userid=userid))
        else:
            raise auth.NoSuchUser(userid)

    def user_groups(self, userid):
        return [row.group.childrens for row in (
               self.session.query(OBMUserGroups).filter_by(userid=userid
                                                           ).all())]

    def group_users(self, group_name):
        group_path = group_name.split('/')
        group = self._group_exists(group_path)
        if not group:
            raise auth.NoSuchGroup(group_name)
        return group.users
