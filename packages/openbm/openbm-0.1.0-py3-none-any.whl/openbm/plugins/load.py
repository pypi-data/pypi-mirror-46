import logging
from stevedore import (dispatch,
                       driver,
                       enabled,
                       extension,
                       )


logger = logging.getLogger(__name__)


def _enabled_notifier(ext, config):
    if ((config.has_section(f'notify_{ext.name}') and
       not config.has_option(f'notify_{ext.name}', 'enabled')) or
       (config.has_option(f'notify_{ext.name}', 'enabled') and
       config.getboolean(f'notify_{ext.name}', 'enabled'))):
        logger.info(f'Initializing {ext.name} notifier')
        return True
    else:
        if (config.has_option(f'notify_{ext.name}', 'enabled') and
           not config.getboolean(f'notify_{ext.name}', 'enabled')):
            logger.warning(f'Notifier {ext.name} is disabled')
        return False


def load_auth_backend(config):
    name = config['major']['auth_backend']
    if f'{name}_auth' not in config:
        config[f'{name}_auth'] = {}
    return driver.DriverManager(
        namespace='openbm.plugins.auth',
        name=name,
        invoke_on_load=True,
        invoke_args=(config[f'{name}_auth'],),
    ).driver


def load_notifiers(config):
    return [notify.plugin(config[f'notify_{notify.name}'])
            for notify in enabled.EnabledExtensionManager(
            namespace='openbm.plugins.notifiers',
            check_func=lambda ext: _enabled_notifier(ext, config),
            invoke_on_load=False,
            invoke_args=(config,),
            )]


def load_executors(scheduler):
    return dispatch.DispatchExtensionManager(
        namespace=f'openbm.plugins.executors',
        check_func=lambda ext: True,
        invoke_on_load=True,
        propagate_map_exceptions=True,
        invoke_args=(scheduler.config, scheduler),
    )


def load_resolvers(config):
    return dispatch.DispatchExtensionManager(
        namespace=f'openbm.plugins.resolvers',
        check_func=lambda ext: True,
        invoke_on_load=True,
        propagate_map_exceptions=True,
        invoke_args=(config,),
    )


def load_schema(plugin_type):
    return extension.ExtensionManager(
        namespace=f'openbm.plugins.{plugin_type}',
        invoke_on_load=False,
    )
