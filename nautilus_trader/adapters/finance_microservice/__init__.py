# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2025 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------
"""
Finance Data & Indicators Microservice integration adapter.

This subpackage provides clients and configuration for connecting to and
interacting with the Finance Data & Indicators Microservice API. It provides
access to economic calendar data, portfolio monitoring, and financial indicators.

Features:
- Economic calendar events and indicators
- Country-specific economic data
- Central bank meeting schedules
- Portfolio performance monitoring
- Risk assessment analytics
- Economic alerts and notifications
"""

from nautilus_trader.adapters.finance_microservice.client import FinanceClient
from nautilus_trader.adapters.finance_microservice.config import FinanceClientConfig

__all__ = [
    "FinanceClient",
    "FinanceClientConfig",
]