#!/usr/bin/env python
#
#  Copyright (C) 2016 Oscar Curero
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
from schema import (
    And,
    Forbidden,
    Optional,
    Or,
    Regex,
    Schema,
)


definitions = {'base_schedule': {
    Optional('type'): Or('hourly', 'daily', 'weekly',
                         'monthly', 'yearly'),
    Optional('festive'): Or('yes', 'no', 'only', 'day-before',
                            'day-after'),
    Optional('target'): str,
    Optional('start_date'): str,
    Optional('end_date'): str,
    Optional('timezone'): str,
    Optional('year'): int,
    Optional('month'): And(int, lambda m: 0 < m <= 12),
    Optional('day'): And(int, lambda d: 0 < d <= 31),
    Optional('week'): And(int, lambda w: 0 < w <= 52),
    Optional('day_of_week'): Or(str, int),
    Optional('hour'): And(int, lambda h: 0 <= h <= 23),
}, 'base_step': {
    Optional('id'): And(str, lambda s: s[0].isalpha()),
    Optional('params'): dict,
    Optional('runcond'): str,
    Optional('abdcond'): str,
}, 'base_prereq': {
    Optional('conditional'): bool,
},
    'valid_execs': [],
    'valid_resolvs': [],
}


stepschema = [
    And([Schema({**definitions['base_step'],
                 **{Optional('type'): lambda s:
                     s not in definitions['valid_execs']}},
         ignore_extra_keys=True)],
        lambda s: len(s) > 0)]


prereqsschema = []


job = {
    'name': str,
    'owner': str,
    'steps': Or(*stepschema),
    Optional('jobset'): And([str], lambda l: len(l) > 0),
    Optional('description'): str,
    Forbidden('scheduler'): object,
    Optional('host'): str,
    Optional('prereqs'): Or(*prereqsschema),
    Optional('provides'): And([str], lambda s: len(s) > 0),
    Optional('schedule'): Or(str,
                             And([Schema(
                                  {**definitions['base_schedule'],
                                   **{Optional('minute'): Regex('\*|/|-'),
                                      Optional('second'): Regex('\*|/|-'),
                                      }}, ignore_extra_keys=True)],
                                 lambda s: len(s) > 0),
                             And([Schema(
                                  {**definitions['base_schedule'],
                                   **{Optional('minute'): Regex('\*|/|-'),
                                      Optional('second'): int,
                                      }}, ignore_extra_keys=True)],
                                 lambda s: len(s) > 0),
                             And([Schema(
                                  {**definitions['base_schedule'],
                                   **{Optional('minute'): Regex('\*|/|-'),
                                      Optional('second'): int,
                                      }}, ignore_extra_keys=True)],
                                 lambda s: len(s) > 0),
                             And([Schema(
                                  {**definitions['base_schedule'],
                                   **{Optional('minute'): int,
                                      Optional('second'): int,
                                      }}, ignore_extra_keys=True)],
                                 lambda s: len(s) > 0),
                             )
}


jobschema = Schema(job, ignore_extra_keys=True)


def add_resolver_plugins(name, resolver_schema):
    if resolver_schema:
        if name == 'job':
            # Default resolver
            resolver_type = {Optional('type'): 'job'}
        else:
            resolver_type = {'type': lambda s: s == name}

        resolver_schema = And([Schema({**definitions['base_prereq'],
                                      **resolver_type,
                                      **resolver_schema},
                                      ignore_extra_keys=True)],
                              lambda s: len(s) > 0)
        prereqsschema.append(resolver_schema)
        global job
        job[Optional('prereqs')] = Or(*prereqsschema)
        global jobschema
        jobschema = Schema(job, ignore_extra_keys=True)
        definitions['valid_resolvs'].append(name)


def add_executor_plugins(name, executor_schema):
    if executor_schema:
        if name == 'cmd':
            # Default executor
            executor_type = {Optional('type'): 'cmd'}
        else:
            executor_type = {'type': name}

        executor_schema = And([Schema({**definitions['base_step'],
                                      **executor_type,
                                      **executor_schema},
                                      ignore_extra_keys=True)],
                              lambda s: len(s) > 0)
        stepschema.append(executor_schema)
        global job
        job['steps'] = Or(*stepschema)
        global jobschema
        jobschema = Schema(job, ignore_extra_keys=True)
        definitions['valid_execs'].append(name)
