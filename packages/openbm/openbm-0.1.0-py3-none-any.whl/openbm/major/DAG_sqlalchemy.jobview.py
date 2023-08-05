from datetime import timedelta
import networkx as nx
from networkx.algorithms.dag import ancestors, descendants
from sqlalchemy import (create_engine, Column, ForeignKey, select, orm,
                        DateTime, Unicode, Boolean, CHAR, Integer, PickleType)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (relationship,
                            sessionmaker,
                            scoped_session)
from sqlalchemy.orm.exc import FlushError, NoResultFound
from sqlalchemy.pool import StaticPool
from sqlalchemy_querybuilder import Filter
import pendulum
# from openbm.major.utils import decode_jobid, dsndate_fmt, dsntime_fmt


Base = declarative_base()


class Job(Base):
    __tablename__ = 'jobs'
    jobid = Column('jobid', Unicode(16), primary_key=True, nullable=False)
    scheduler = Column('sched', CHAR(1), nullable=False)
    status = Column('status', Unicode(3), index=True)
    jobname = Column('jobname', Unicode(16))
    provider = Column('provider', Unicode(512))
    est_sta_time = Column('est_sta_time', DateTime)
    est_exec_time = Column('est_exec_time', Integer)
    prio = Column('prio', Integer)
    wait = Column('wait', Unicode(16))
    owner = Column('owner', Unicode(64))
    steps = Column('steps', PickleType)

    runs = relationship('JobRun', lazy='subquery',
                        cascade='save-update, merge, delete')
    prereq = relationship('PreReq', lazy='subquery',
                          cascade='save-update, merge, delete')
    provider = relationship('Provider', lazy='subquery',
                            cascade='save-update, merge, delete')

    @orm.reconstructor
    def init_on_load(self):
        print(type(self.higher_neighbors()))
        print(type(self.lower_neighbors()))

    @hybrid_property
    def runid(self):
        return self.prio

    @runid.expression
    def runid1(cls):
        print(cls)
        # return select([JobRun.runid]).where(
        #        cls.jobid == JobRun.jobid).as_scalar()
        # return self.runs[0].runid if self.runs else None

    @hybrid_property
    def providesa(self):
        return self.prio

    @hybrid_property
    def rc(self):
        return self.runs[0].rc if self.runs else None

    @hybrid_property
    def node(self):
        return self.runs[0].node if self.runs else None

    @node.expression
    def node(cls):
        return select([JobRun.node]).where(cls.jobid ==
                                           JobRun.jobid).as_scalar()

    @hybrid_property
    def sta_time(self):
        return self.runs[0].sta_time if self.runs else None

    @hybrid_property
    def sto_time(self):
        return self.runs[0].sto_time if self.runs else None

    @hybrid_property
    def runtime(self):
        return self.runs[0].runtime if self.runs else 0

    def __json__(self, request):
        tz = request.registry.settings['timezone']
        # print(self.provider)
        # for r in self.provider:
        #    print('HOLLA')
        #    print(r)
        #    print(r.ancestors())

        return {'jobid': self.jobid,
                'scheduler': self.scheduler,
                'jobname': self.jobname,
                'prio': self.prio,
                'wait': self.wait,
                'owner': self.owner,
                'node': self.node,
                'runid': self.runid,
                'status': self.status,
                'rc': self.rc,
                'est_exec_time': self.est_exec_time or 0,
                'est_sta_time': pendulum.instance(self.est_sta_time,
                                                  tz).isoformat() if
                self.est_sta_time else None,
                'sta_time': pendulum.instance(self.sta_time,
                                              tz).isoformat() if
                self.sta_time else None,
                'est_sto_time': (pendulum.instance(self.est_sta_time, tz) +
                                 timedelta(self.est_exec_time)).isoformat() if
                self.est_sta_time else None,
                'sto_time': pendulum.instance(self.sto_time,
                                              tz).isoformat() if self.sto_time
                else None,
                'runtime': self.runtime,
                'runs': self.runs,
                'prereq': self.prereq,
                'provider': self.provider,
                }


class JobRun(Base):
    __tablename__ = 'run'
    jobid = Column('jobid', Unicode(16), ForeignKey('jobs.jobid'),
                   primary_key=True)
    runid = Column('runid', Integer)
    # status = Column('status', Unicode(3), nullable=False, index=True)
    node = Column('node', Unicode(64))
    rc = Column('rc', CHAR(6))
    # est_sta_time = Column('est_sta_time', DateTime)
    sta_time = Column('sta_time', DateTime, index=True)
    # est_sto_time = Column('est_sto_time', DateTime)
    sto_time = Column('sto_time', DateTime, index=True)

    @hybrid_property
    def runtime(self):
        if not self.sto_time or not self.sta_time:
            return None
        else:
            return (self.sto_time - self.sta_time).seconds / 60

    def __json__(self, request):
        tz = request.registry.settings['timezone']
        return {'jobid': self.jobid,
                'runid': self.runid,
                'node': self.node,
                # 'status': self.status,
                'rc': self.rc,
                # 'est_sta_time': pendulum.instance(self.est_sta_time,
                #                                   tz).isoformat() if
                # self.est_sta_time else None,
                'sta_time': pendulum.instance(self.sta_time,
                                              tz).isoformat() if
                self.sta_time else None,
                # 'est_sto_time': self.est_sto_time.isoformat() if
                # self.est_sto_time else None,
                # 'sto_time': self.sto_time.isoformat() if self.sto_time
                # else None,
                }


class PreReq(Base):
    __tablename__ = 'prereq'
    jobid = Column('jobid', Unicode(16), ForeignKey('jobs.jobid'),
                   primary_key=True)
    name = Column('name', Unicode(512), primary_key=True)
    cond = Column('cond', Boolean)
    status = Column('status', Boolean)

    def __json__(self, request):
        return {}


class Provider(Base):
    __tablename__ = 'provider'
    name = Column('name', Unicode(512), primary_key=True)
    jobid = Column('jobid', Unicode(16), ForeignKey('jobs.jobid'))
    job = relationship('Job', lazy='subquery')

    def __json__(self, request):
        return {'jobid': self.jobid,
                'ancestors': 't',
                'provider': self.name}


class JobDep(Base):
    __tablename__ = 'jobdep'
    waiter = Column('waiter', Unicode(16), ForeignKey('jobs.jobid'),
                    primary_key=True)
    resolver = Column('resolver', Unicode(16), ForeignKey('jobs.jobid'),
                      primary_key=True)
    _descendants = relationship(Job, primaryjoin=waiter == Job.jobid,
                                backref='descendants', lazy='joined')
    _ancestors = relationship(Job, primaryjoin=resolver == Job.jobid,
                              backref='ancestors', lazy='joined')

    def __init__(self, waiter, resolver):
        self.waiter = waiter.jobid
        self.resolver = resolver.jobid
        # TODO: use multi-provides
        # self.waiter = waiter.name
        # self.resolver = resolver.name

    def __json__(self, request):
        return {'name': self.name,
                'resolver': self.resolver,
                'status': self.status,
                }


engine = create_engine('sqlite://', connect_args={'check_same_thread': False},
                       poolclass=StaticPool, echo=False)

Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
query = Session.query()
jobfilter = Filter({'jobs': Job}, query)


def load(joblist, dayshift, tz):
    for job in joblist:
        insert_job(job['jobdata'].copy(), dayshift, tz)
    # print('@------@-----@')
    # for i in Session.query(JobDep).all():
    #    print(i.waiter + '< - >' + i.resolver)


def insert_job(jobdata, dayshift, tz):
    # schedule = decode_jobid(jobdata['jobid'], dayshift, tz)
    for runid, rundata in enumerate(jobdata['runs']):
        Session.add(JobRun(runid=runid, **rundata))
    providers = []
    for provider in jobdata['provider']:
        provider_obj = Provider(jobid=jobdata['jobid'], name=provider)
        Session.add(provider_obj)
        providers.append(provider_obj)

    for prereq in jobdata['prereq']:
        name = prereq['name']
        if 'type' not in prereq or prereq['type'] == 'job':
            dep = Session.query(Provider).filter_by(name=name).first()
            for provider in providers:
                Session.add(JobDep(provider, dep))
        Session.add(PreReq(jobid=jobdata['jobid'],
                           name=name,
                           cond=prereq.get('cond', False),
                           status=False))
    del jobdata['runs']
    del jobdata['provider']
    del jobdata['prereq']
    Session.add(Job(**jobdata))
    Session.commit()


def insert_run(jobid, runid, rundata):
    Session.add(JobRun(jobid=jobid,
                       runid=runid,
                       ))
    try:
        Session.commit()
    except (IntegrityError, FlushError):
        Session.rollback()


def modify(jobid, runid, jobdata, rundata):
    job = Session.query(Job).filter(Job.jobid == jobid).one()
    for key in jobdata:
        setattr(job, key, jobdata[key])
    try:
        run = Session.query(JobRun).filter(JobRun.jobid == jobid and
                                           JobRun.runid == runid).one()
        for key in rundata:
            setattr(run, key, rundata[key])
    except NoResultFound:
        insert_run(jobid, runid, rundata.copy())
    Session.commit()


def filter(filters):
    if 'condition' not in filters:
        filters['condition'] = 'AND'
    if not filters['rules']:
        # If no filters are passed, force at least one so there's a query
        filters['rules'].append({'field': 'jobs.jobname',
                                 'operator': 'contains',
                                 'value': ''})
    hola = jobfilter.querybuilder(filters).all()
    print(hola)
    print(hola[0].lower_neighbors())
    print(hola[0].ancestors)
    print(hola[0].descendants)
    return hola
