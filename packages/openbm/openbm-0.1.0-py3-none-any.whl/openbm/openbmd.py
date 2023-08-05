#!/usr/bin/env python
#
#  Copyright (C) 2015 social2data S.A.
#
#  This file is part of OpenBatchManager.
#
#  OpenBatchManager free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  OpenBatchManager is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied  warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with OpenBatchmanager.  If not, see <http://www.gnu.org/licenses/>.
#

import asyncio
import configparser
import logging
import click
from openbm import (minor,
                    major
                    )


loop = asyncio.get_event_loop()


@click.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--initialize', 'init', is_flag=True, default=False,
              help='initialize job scheduling')
@click.option('--loglevel', '-l', 'log_level',
              type=click.Choice(['critical', 'error',
                                 'warning', 'info', 'debug']),
              default='info', help='set verbose level (default "info")')
def main(config_file, init, log_level):
    """Execute an openbm scheduler"""
    logformat = '%(asctime)s%(msecs)d %(name)s:%(levelname)s:%(message)s'
    log_level = getattr(logging, log_level.upper())
    logging.basicConfig(level=log_level, format=logformat)
    logger = logging.getLogger('openbm')
    if logging.getLogger().level > logging.DEBUG:
        logging.getLogger('apscheduler').setLevel(logging.ERROR)
    logger.info(f'Starting OpenBatchManager version 0.1')

    config = configparser.ConfigParser()
    config.read(config_file)
    if (config.has_section('major') and
       config.getboolean('major', 'server', fallback=False)):
        if config.getboolean('major', 'cluster'):
            scheduler = major.ClusterMajorScheduler(config)
        else:
            scheduler = major.StandaloneMajorScheduler(config)
    else:
        scheduler = minor.MinorScheduler(config)
    logger.debug('Initialitation completed')
    loop.run_until_complete(scheduler.start(init))
