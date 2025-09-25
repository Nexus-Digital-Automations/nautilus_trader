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
News Microservice integration adapter.

This subpackage provides a client and configuration for connecting to and
interacting with the News Microservice API. It provides access to news data,
economic calendar events, and real-time news notifications.

Features:
- Real-time news data ingestion
- Economic calendar event monitoring
- News sentiment analysis integration
- Custom news alerts and filtering
- Support for multiple news sources and categories
"""

from nautilus_trader.adapters.news_microservice.client import NewsClient
from nautilus_trader.adapters.news_microservice.config import NewsClientConfig

__all__ = [
    "NewsClient",
    "NewsClientConfig",
]