#
# Copyright 2013 Xavier Bruhiere
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import copy

import logbook
import rethinkdb as rdb


# We will use these settings later in the code to
# connect to the RethinkDB server.
RDB_CONFIG = {
    'host': os.getenv('RDB_HOST', 'localhost'),
    'port': os.getenv('RDB_PORT', 28015),
    'db': os.getenv('RDB_DB', 'intuition')
}

log = logbook.Logger('intuition.modules.managers.database')


class RethinkdbBackend():
    '''
    This class adds database backend to the portfolio
    '''
    def __init__(self, name, reset=False):
        self.session = self._connection()
        self.pf_table = name + 'Portfolio'
        self.cmr_table = name + 'Risks'
        if reset:
            self._reset_data()

    def _reset_data(self):
        for table in [self.pf_table, self.cmr_table]:
            if table in rdb.table_list().run(self.session):
                result = rdb.table_drop(table).run(self.session)
                assert result['dropped'] == 1

            result = rdb.table_create(table).run(self.session)
            result = rdb.table(table).index_create('date').run(self.session)
        return result.get('created', 0) == 1

    def _connection(self):
        return rdb.connect(host=RDB_CONFIG['host'],
                           port=RDB_CONFIG['port'],
                           db=RDB_CONFIG['db'])

    def _to_dict(self, portfolio):
        json_pf = portfolio.__dict__
        if json_pf['positions']:
            for sid, infos in portfolio.positions.iteritems():
                json_pf['positions'][sid] = infos.__dict__
        return json_pf

    def save_portfolio(self, date, portfolio):
        '''
        Store in Rethinkdb a zipline.Portfolio object
        '''
        log.info('Saving portfolio in database')
        result = rdb.table(self.pf_table).insert(
            {'date': date,
             'portfolio': self._to_dict(
                 copy.deepcopy(portfolio))}).run(self.session)
        log.debug(result)

    def load_portfolio(self, name):
        '''
        Build zipline.Portfolio object from <name> stored in database
        '''
        pass

    def save_metrics(self, date, cmr):
        '''
        Stores in database zipline.perf_tracker.cumulative_risk_metrics
        '''
        result = rdb.table(self.cmr_table).insert(
            {'date': date,
             'cmr': cmr.to_dict()}).run(self.session)
        log.debug(result)

    def __del__(self):
        self.session.close()