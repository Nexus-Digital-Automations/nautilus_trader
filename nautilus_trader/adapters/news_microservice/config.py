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
Configuration for News Microservice adapter.
"""

from typing import Optional

import msgspec

from nautilus_trader.config import PositiveFloat
from nautilus_trader.config import PositiveInt
from nautilus_trader.core.data import Data


class NewsClientConfig(msgspec.Struct):
    """
    Configuration for News Microservice adapter.

    Parameters
    ----------
    base_url : str, default "http://localhost:8000"
        The base URL for the News Microservice API.
    api_key : str, optional
        API key for authentication if required.
    timeout_connect : PositiveFloat, default 5.0
        The connection timeout in seconds.
    timeout_request : PositiveFloat, default 10.0
        The request timeout in seconds.
    max_retries : PositiveInt, default 3
        Maximum number of retry attempts for failed requests.
    enable_webhooks : bool, default True
        Whether to enable webhook endpoints for real-time news.
    webhook_port : PositiveInt, default 9001
        Port for webhook server if enabled.
    news_categories : list[str], optional
        List of news categories to monitor (e.g., ['economics', 'politics', 'technology']).
    importance_filter : str, default "medium"
        Minimum importance level for news events ('low', 'medium', 'high').
    country_filter : list[str], optional
        List of countries to filter news by (e.g., ['US', 'GB', 'DE']).
    """

    base_url: str = "http://localhost:8000"
    api_key: Optional[str] = None
    timeout_connect: PositiveFloat = 5.0
    timeout_request: PositiveFloat = 10.0
    max_retries: PositiveInt = 3
    enable_webhooks: bool = True
    webhook_port: PositiveInt = 9001
    news_categories: Optional[list[str]] = None
    importance_filter: str = "medium"
    country_filter: Optional[list[str]] = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.importance_filter not in ["low", "medium", "high"]:
            raise ValueError("importance_filter must be 'low', 'medium', or 'high'")


class NewsEvent(Data):
    """
    Represents a news event from the microservice.

    Parameters
    ----------
    source : str
        The news source name.
    headline : str
        The news headline.
    url : str, optional
        Original news URL.
    content : str, optional
        News content/summary.
    timestamp : int
        Event timestamp (UNIX nanoseconds).
    category : str, optional
        News category.
    importance : str, optional
        Importance level ('low', 'medium', 'high').
    country : str, optional
        Country associated with the news.
    sentiment : float, optional
        Sentiment score (-1.0 to 1.0).
    """

    def __init__(
        self,
        source: str,
        headline: str,
        url: Optional[str] = None,
        content: Optional[str] = None,
        timestamp: int = 0,
        category: Optional[str] = None,
        importance: Optional[str] = None,
        country: Optional[str] = None,
        sentiment: Optional[float] = None,
    ):
        super().__init__(timestamp_ns=timestamp)
        self.source = source
        self.headline = headline
        self.url = url
        self.content = content
        self.category = category
        self.importance = importance
        self.country = country
        self.sentiment = sentiment

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"source={self.source}, "
            f"headline={self.headline[:50]}{'...' if len(self.headline) > 50 else ''}, "
            f"category={self.category}, "
            f"importance={self.importance}"
            f")"
        )