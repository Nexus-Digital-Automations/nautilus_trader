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
Configuration for Finance Data & Indicators Microservice adapter.
"""

from typing import Optional

import msgspec

from nautilus_trader.config import PositiveFloat
from nautilus_trader.config import PositiveInt
from nautilus_trader.core.data import Data


class FinanceClientConfig(msgspec.Struct):
    """
    Configuration for Finance Data & Indicators Microservice adapter.

    Parameters
    ----------
    base_url : str, default "http://localhost:8080"
        The base URL for the Finance Microservice API.
    api_key : str, optional
        API key for authentication if required.
    timeout_connect : PositiveFloat, default 5.0
        The connection timeout in seconds.
    timeout_request : PositiveFloat, default 10.0
        The request timeout in seconds.
    max_retries : PositiveInt, default 3
        Maximum number of retry attempts for failed requests.
    cache_ttl : PositiveInt, default 300
        Cache time-to-live in seconds for API responses.
    default_country : str, default "united_states"
        Default country for economic indicators.
    default_indicators : list[str], default ["GDP", "CPI", "UNRATE"]
        Default economic indicators to monitor.
    importance_filter : str, default "medium"
        Minimum importance level for economic events ('low', 'medium', 'high').
    enable_portfolio_monitoring : bool, default True
        Whether to enable portfolio monitoring features.
    """

    base_url: str = "http://localhost:8080"
    api_key: Optional[str] = None
    timeout_connect: PositiveFloat = 5.0
    timeout_request: PositiveFloat = 10.0
    max_retries: PositiveInt = 3
    cache_ttl: PositiveInt = 300
    default_country: str = "united_states"
    default_indicators: list[str] = msgspec.field(default_factory=lambda: ["GDP", "CPI", "UNRATE"])
    importance_filter: str = "medium"
    enable_portfolio_monitoring: bool = True

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.importance_filter not in ["low", "medium", "high"]:
            raise ValueError("importance_filter must be 'low', 'medium', or 'high'")


class EconomicEvent(Data):
    """
    Represents an economic event from the microservice.

    Parameters
    ----------
    event_id : str
        Unique identifier for the event.
    name : str
        Event name/title.
    country : str
        Country associated with the event.
    importance : str
        Importance level ('low', 'medium', 'high').
    category : str, optional
        Economic category.
    scheduled_time : int
        Scheduled time (UNIX nanoseconds).
    previous_value : float, optional
        Previous value for the indicator.
    forecast : float, optional
        Forecasted value.
    actual_value : float, optional
        Actual reported value.
    """

    def __init__(
        self,
        event_id: str,
        name: str,
        country: str,
        importance: str,
        category: Optional[str] = None,
        scheduled_time: int = 0,
        previous_value: Optional[float] = None,
        forecast: Optional[float] = None,
        actual_value: Optional[float] = None,
    ):
        super().__init__(timestamp_ns=scheduled_time)
        self.event_id = event_id
        self.name = name
        self.country = country
        self.importance = importance
        self.category = category
        self.previous_value = previous_value
        self.forecast = forecast
        self.actual_value = actual_value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"event_id={self.event_id}, "
            f"name={self.name}, "
            f"country={self.country}, "
            f"importance={self.importance}"
            f")"
        )


class EconomicIndicator(Data):
    """
    Represents an economic indicator data point.

    Parameters
    ----------
    indicator : str
        Indicator code (e.g., GDP, CPI, UNRATE).
    country : str
        Country for the indicator.
    value : float
        Indicator value.
    period : str, optional
        Time period for the data.
    timestamp : int
        Data timestamp (UNIX nanoseconds).
    """

    def __init__(
        self,
        indicator: str,
        country: str,
        value: float,
        period: Optional[str] = None,
        timestamp: int = 0,
    ):
        super().__init__(timestamp_ns=timestamp)
        self.indicator = indicator
        self.country = country
        self.value = value
        self.period = period

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"indicator={self.indicator}, "
            f"country={self.country}, "
            f"value={self.value}, "
            f"period={self.period}"
            f")"
        )


class PortfolioPerformance(Data):
    """
    Represents portfolio performance metrics.

    Parameters
    ----------
    portfolio_id : str
        Portfolio identifier.
    total_return : float
        Total portfolio return.
    daily_return : float
        Daily return.
    volatility : float
        Portfolio volatility.
    sharpe_ratio : float, optional
        Sharpe ratio.
    max_drawdown : float, optional
        Maximum drawdown.
    timestamp : int
        Performance timestamp (UNIX nanoseconds).
    """

    def __init__(
        self,
        portfolio_id: str,
        total_return: float,
        daily_return: float,
        volatility: float,
        sharpe_ratio: Optional[float] = None,
        max_drawdown: Optional[float] = None,
        timestamp: int = 0,
    ):
        super().__init__(timestamp_ns=timestamp)
        self.portfolio_id = portfolio_id
        self.total_return = total_return
        self.daily_return = daily_return
        self.volatility = volatility
        self.sharpe_ratio = sharpe_ratio
        self.max_drawdown = max_drawdown

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"portfolio_id={self.portfolio_id}, "
            f"total_return={self.total_return:.4f}, "
            f"daily_return={self.daily_return:.4f}, "
            f"volatility={self.volatility:.4f}"
            f")"
        )