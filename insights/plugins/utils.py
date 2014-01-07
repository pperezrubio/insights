#
# Copyright 2014 Xavier Bruhiere
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

import logbook


log = logbook.Logger('intuition.plugins.utils')


def debug_portfolio(portfolio):
    print('\n' + 79 * '=')
    log.debug(portfolio)
    print(79 * '=' + '\n')


def debug_metrics(perf_tracker):
    if perf_tracker.progress != 0.0:
        print('\n' + 79 * '=')
        log.debug(perf_tracker.cumulative_risk_metrics.to_dict())
        print(79 * '=' + '\n')
