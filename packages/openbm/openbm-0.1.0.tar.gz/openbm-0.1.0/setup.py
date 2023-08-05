# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['openbm',
 'openbm.major',
 'openbm.major.webapps',
 'openbm.minor',
 'openbm.plugins',
 'openbm.plugins.auth',
 'openbm.plugins.executors',
 'openbm.plugins.notifiers',
 'openbm.plugins.resolvers']

package_data = \
{'': ['*'],
 'openbm': ['.pytest_cache/*',
            '.pytest_cache/v/*',
            '.pytest_cache/v/cache/*',
            'bin/*',
            'dat a/*',
            'dat a/joblogs/*']}

install_requires = \
['aioprocessing>=1.0,<2.0',
 'apscheduler>=3.5.1,<4.0.0',
 'boolrule>=0.3.0,<0.4.0',
 'cheroot>=6.3,<7.0',
 'click>=6.7,<7.0',
 'coverage>=4,<5',
 'dataclasses>=0.6.0,<0.7.0',
 'decorator>=4.3,<5.0',
 'networkx>=2.1,<3.0',
 'notifiers>=0.7.4,<0.8.0',
 'pendulum>=2.0,<3.0',
 'psutil>=5.4,<6.0',
 'pydblite>=3.0,<4.0',
 'pyramid>=1.9,<2.0',
 'pyramid_exclog>=1.0,<2.0',
 'pysyncobj>=0.3.3,<0.4.0',
 'pytest-lazy-fixture>=0.5.1,<0.6.0',
 'pyyaml>=3.12,<4.0',
 'requests>=2.18,<3.0',
 'schema>=0.6.7,<0.7.0',
 'sqlalchemy-querybuilder>=0.1.2,<0.2.0',
 'stevedore>=1.28,<2.0',
 'tblib>=1.3,<2.0',
 'websockets>=5.0,<6.0',
 'zope.sqlalchemy>=1.0,<2.0']

entry_points = \
{'console_scripts': ['openbmd = openbm.openbmd:main'],
 'openbm.plugins.auth': ['insecure = openbm.plugins.auth.insecure:InsecureAuth',
                         'sqlalchemy = '
                         'openbm.plugins.auth.sqlalchemy:SQLAlchemyAuth'],
 'openbm.plugins.executors': ['cmd = openbm.plugins.executors.cmd:Command',
                              'null = openbm.plugins.executors.null:Null'],
 'openbm.plugins.notifiers': ['email = '
                              'openbm.plugins.notifiers.generic_notifiers:Email',
                              'pushbullet = '
                              'openbm.plugins.notifiers.generic_notifiers:Pushbullet',
                              'telegram = '
                              'openbm.plugins.notifiers.generic_notifiers:Telegram'],
 'openbm.plugins.resolvers': ['job = openbm.plugins.resolvers.job:Job',
                              'user = openbm.plugins.resolvers.user:User']}

setup_kwargs = {
    'name': 'openbm',
    'version': '0.1.0',
    'description': 'OpenBatchManager is a distributed, high performant, fault tolerant job scheduler',
    'long_description': None,
    'author': 'Oscar Curero',
    'author_email': 'oscar@curero.es',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
