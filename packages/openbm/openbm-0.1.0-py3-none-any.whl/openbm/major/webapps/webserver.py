import os
import logging
import threading
from cheroot import wsgi
import psutil
from pyramid.config import Configurator
from pyramid.renderers import JSON
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import BasicAuthAuthenticationPolicy as BasicAuth
from openbm.major.exceptions import InternalSchedulerError
# from openbm.major import dist_logging
from openbm.plugins.load import (load_auth_backend, load_schema)
from openbm.major.webapps.resources import Root
from openbm.minor import schemas

logger = logging.getLogger(__name__)


def send_cmd(request, *args, **kwargs):
    endpoint.send((args, kwargs))
    repl = endpoint.recv()
    if isinstance(repl, InternalSchedulerError):
        raise repl.re_raise()
    else:
        return repl


def check_credentials(backend):

    def check_credentials_backend(user, passwd, request):
        return backend.check_credentials(user, passwd)

    return check_credentials_backend


def wsgi_webapi(config):
    logger.debug(f'Creating webapi wsgi application')
    authz_policy = ACLAuthorizationPolicy()
    json_renderer = JSON()
    # json_renderer.add_adapter(apscheduler.job.Job, job_adapter)
    settings = Configurator()
    settings.set_root_factory(Root)
    auth_backend = load_auth_backend(config)
    # backend.load_pyramid(config, settings)
    settings.add_request_method(send_cmd, 'scheduler', reify=False)
    settings.add_renderer(None, json_renderer)
    settings.add_settings({'timezone': config['major']['timezone']})
    settings.registry.config = config
    settings.registry.auth = auth_backend
    authn_policy = BasicAuth(check_credentials(auth_backend))
    settings.set_authentication_policy(authn_policy)
    settings.set_authorization_policy(authz_policy)
    # config.add_settings({'exclog.extra_info': 'true'})
    settings.add_settings(
        {'exclog.ignore':
         """pyramid.httpexceptions.HTTPSuccessful
            pyramid.httpexceptions.HTTPRedirection
            pyramid.httpexceptions.HTTPClientError
            pyramid.httpexceptions.HTTPNotImplemented
            """})
    settings.include('pyramid_exclog')
    # config.include("pyramid_jwt")
    # config.include("pyramid_httpauth")
    # config.set_jwt_authentication_policy('secret')
    settings.scan("openbm.major.webapps")
    # faulthandler.dump_traceback_later(5)
    return settings.make_wsgi_app()


def parent_notifier():
    server = psutil.Process()
    parent = server.parent()
    logger.debug('Parent notifier thread is running')
    parent.wait()
    server.terminate()


def run(config, cmdpipe, logpipe, event):
    # logger.addHandler(dist_logging.PipeHandler(logpipe))
    notifier = threading.Thread(target=parent_notifier)
    notifier.start()
    logger.debug(f'Operation Manager PID: {os.getpid()}')
    address = config.get('major', 'om_address')
    port = config.getint('major', 'om_port')
    global endpoint
    endpoint = cmdpipe
    logger.debug(f'Operation Manager will listen on {address}:{port}')
    server = wsgi.Server((address, port),
                         wsgi_webapi(config),
                         numthreads=1)

    for executor in load_schema('executors'):
        logger.debug(f'Loading schema for executor {executor.name}')
        schemas.add_executor_plugins(executor.name, executor.plugin.SCHEMA)

    for resolver in load_schema('resolvers'):
        logger.debug(f'Loading schema for resolver {resolver.name}')
        schemas.add_resolver_plugins(resolver.name, resolver.plugin.SCHEMA)

    logger.info(f'Operation Manager is listening on {address}:{port}')
    try:
        event.set()
        server.start()
    except KeyboardInterrupt:
        logger.info('Stopping Operation Manager')
        send_cmd(None, None)
    except Exception as ex:
        logger.critical(ex)
        send_cmd(None, None)
