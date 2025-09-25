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
Finance Data & Indicators Microservice client for economic data and portfolio monitoring.
"""

import asyncio
import logging
from typing import Any, Callable, Optional

import aiohttp

from nautilus_trader.adapters.finance_microservice.config import (
    EconomicEvent,
    EconomicIndicator,
    FinanceClientConfig,
    PortfolioPerformance,
)
from nautilus_trader.common.component import Component
from nautilus_trader.core.datetime import unix_nanos_to_dt
from nautilus_trader.core.datetime import utc_now


class FinanceClient(Component):
    """
    Client for connecting to and retrieving data from the Finance Data & Indicators Microservice.

    This client provides methods to:
    - Fetch economic calendar events
    - Retrieve economic indicators by country
    - Monitor central bank meetings and announcements
    - Get portfolio performance and risk analytics
    - Create economic alerts and notifications
    """

    def __init__(
        self,
        config: FinanceClientConfig,
        clock,
        logger_factory,
    ) -> None:
        """
        Initialize the Finance Microservice client.

        Parameters
        ----------
        config : FinanceClientConfig
            The client configuration.
        clock : Clock
            The system clock.
        logger_factory : LoggerFactory
            The logger factory.
        """
        super().__init__(
            clock=clock,
            logger=logger_factory.create(name=type(self).__name__),
        )

        self._config = config
        self._session: Optional[aiohttp.ClientSession] = None
        self._is_connected = False
        self._cache: dict[str, Any] = {}

        # Event handlers
        self._economic_event_handlers: list[Callable[[EconomicEvent], None]] = []
        self._indicator_handlers: list[Callable[[EconomicIndicator], None]] = []
        self._portfolio_handlers: list[Callable[[PortfolioPerformance], None]] = []

        # Base headers for all requests
        self._headers = {"Content-Type": "application/json"}
        if config.api_key:
            self._headers["Authorization"] = f"Bearer {config.api_key}"

    @property
    def is_connected(self) -> bool:
        """Return True if client is connected to the microservice."""
        return self._is_connected

    async def connect(self) -> None:
        """Connect to the Finance Data & Indicators Microservice."""
        self._log.info("Connecting to Finance Data & Indicators Microservice...")

        # Create HTTP session
        timeout = aiohttp.ClientTimeout(
            connect=self._config.timeout_connect,
            total=self._config.timeout_request,
        )
        self._session = aiohttp.ClientSession(
            timeout=timeout,
            headers=self._headers,
        )

        # Test connection with health check
        try:
            health_response = await self._request("GET", "/health")
            if health_response.get("status") == "ok":
                self._is_connected = True
                self._log.info("Successfully connected to Finance Data & Indicators Microservice")
            else:
                raise ConnectionError(f"Finance Microservice health check failed: {health_response}")

        except Exception as e:
            self._log.error(f"Failed to connect to Finance Data & Indicators Microservice: {e}")
            if self._session:
                await self._session.close()
                self._session = None
            raise

    async def disconnect(self) -> None:
        """Disconnect from the Finance Data & Indicators Microservice."""
        self._log.info("Disconnecting from Finance Data & Indicators Microservice...")

        self._is_connected = False

        # Close HTTP session
        if self._session:
            await self._session.close()
            self._session = None

        # Clear cache
        self._cache.clear()

        self._log.info("Disconnected from Finance Data & Indicators Microservice")

    def add_economic_event_handler(self, handler: Callable[[EconomicEvent], None]) -> None:
        """Add a handler for economic events."""
        self._economic_event_handlers.append(handler)
        self._log.debug(f"Added economic event handler: {handler.__name__}")

    def add_indicator_handler(self, handler: Callable[[EconomicIndicator], None]) -> None:
        """Add a handler for economic indicators."""
        self._indicator_handlers.append(handler)
        self._log.debug(f"Added indicator handler: {handler.__name__}")

    def add_portfolio_handler(self, handler: Callable[[PortfolioPerformance], None]) -> None:
        """Add a handler for portfolio performance."""
        self._portfolio_handlers.append(handler)
        self._log.debug(f"Added portfolio handler: {handler.__name__}")

    # Core Information Methods
    async def get_api_info(self) -> dict[str, Any]:
        """Get API configuration and feature information."""
        return await self._request("GET", "/api/v1/info")

    async def get_system_health(self) -> dict[str, Any]:
        """Get comprehensive system health with service status."""
        return await self._request("GET", "/system/health")

    # Monitoring Methods
    async def get_monitoring_health(self) -> dict[str, Any]:
        """Get system health with detailed checks."""
        return await self._request("GET", "/api/v1/monitoring/health")

    async def get_monitoring_health_summary(self) -> dict[str, Any]:
        """Get health summary."""
        return await self._request("GET", "/api/v1/monitoring/health/summary")

    async def get_monitoring_metrics(self) -> dict[str, Any]:
        """Get comprehensive metrics including request counts, error rates."""
        return await self._request("GET", "/api/v1/monitoring/metrics")

    async def get_datetime_serialization_test(self) -> dict[str, Any]:
        """Test datetime handling validation."""
        return await self._request("GET", "/api/v1/monitoring/datetime-serialization")

    # Performance Monitoring Methods
    async def get_performance_metrics(self) -> dict[str, Any]:
        """Get performance metrics with cache and database stats."""
        return await self._request("GET", "/api/v1/performance/metrics")

    # Analytics Dashboard Methods
    async def get_analytics_dashboard(self) -> dict[str, Any]:
        """Get full dashboard data."""
        return await self._request("GET", "/api/analytics/dashboard")

    async def get_financial_indicators(self, symbol: str) -> dict[str, Any]:
        """Get detailed financial indicators for a symbol."""
        return await self._request("GET", f"/api/analytics/financial-indicators/{symbol}")

    async def get_market_overview(self) -> dict[str, Any]:
        """Get market overview data."""
        return await self._request("GET", "/api/market")

    # AI Insights Methods
    async def get_ai_insights(self) -> dict[str, Any]:
        """Get comprehensive AI-powered portfolio analysis."""
        return await self._request("GET", "/ai/insights")

    # Settings Methods
    async def get_user_settings(self) -> dict[str, Any]:
        """Get user preferences and configuration."""
        return await self._request("GET", "/api/settings")

    # Securities Methods
    async def search_securities(
        self,
        query: Optional[str] = None,
        limit: int = 100,
    ) -> dict[str, Any]:
        """Search securities."""
        params = {"limit": limit}
        if query:
            params["q"] = query
        return await self._request("GET", "/api/v1/securities/search", params=params)

    async def list_securities(
        self,
        page: int = 1,
        limit: int = 100,
    ) -> dict[str, Any]:
        """List securities."""
        params = {"page": page, "limit": limit}
        return await self._request("GET", "/api/v1/securities", params=params)

    async def get_security_details(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """Get security details."""
        return await self._request("GET", f"/api/v1/securities/{symbol}")

    async def get_security_info(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """Get security information."""
        return await self._request("GET", f"/api/v1/securities/{symbol}/info")

    async def list_exchanges(self) -> dict[str, Any]:
        """List available exchanges."""
        return await self._request("GET", "/api/v1/securities/exchanges/list")

    async def list_sectors(self) -> dict[str, Any]:
        """List available sectors."""
        return await self._request("GET", "/api/v1/securities/sectors/list")

    # Data Provider Methods
    async def get_fmp_health(self) -> dict[str, Any]:
        """Get FMP (Financial Modeling Prep) API health."""
        return await self._request("GET", "/fmp/health")

    async def get_openbb_status(self) -> dict[str, Any]:
        """Get OpenBB platform status."""
        return await self._request("GET", "/api/v1/openbb/status")

    async def get_openbb_providers(self) -> dict[str, Any]:
        """Get list of OpenBB providers."""
        return await self._request("GET", "/api/v1/openbb/providers/list")

    # Authentication Methods
    async def login(
        self,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        """Login to get access token."""
        payload = {"email": email, "password": password}
        return await self._request("POST", "/api/auth/login", json=payload)

    async def get_profile(self, token: str) -> dict[str, Any]:
        """Get user profile (requires authentication)."""
        headers = {"Authorization": f"Bearer {token}"}
        return await self._request("GET", "/api/auth/profile", headers=headers)

    async def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        """Refresh access token."""
        payload = {"refresh_token": refresh_token}
        return await self._request("POST", "/api/auth/refresh", json=payload)

    # Economic Calendar Methods
    async def get_economic_calendar(
        self,
        country: Optional[str] = None,
        importance: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        limit: int = 100,
    ) -> dict[str, Any]:
        """
        Get economic calendar events with filtering options.

        Parameters
        ----------
        country : str, optional
            Country filter.
        importance : str, optional
            Event importance level.
        start_date : str, optional
            Start date (YYYY-MM-DD).
        end_date : str, optional
            End date (YYYY-MM-DD).
        page : int, default 1
            Page number.
        limit : int, default 100
            Items per page.

        Returns
        -------
        dict[str, Any]
            Economic calendar data with pagination.
        """
        params = {"page": page, "limit": limit}
        if country:
            params["country"] = country
        if importance:
            params["importance"] = importance
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await self._request("GET", "/api/v1/economic/calendar", params=params)

    async def get_todays_economic_releases(
        self,
        country: Optional[str] = None,
        importance: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get today's economic releases."""
        params = {}
        if country:
            params["country"] = country
        if importance:
            params["importance"] = importance

        return await self._request("GET", "/api/v1/economic/calendar/today", params=params)

    async def get_weekly_economic_events(
        self,
        country: Optional[str] = None,
        importance: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get this week's important economic events."""
        params = {}
        if country:
            params["country"] = country
        if importance:
            params["importance"] = importance

        return await self._request("GET", "/api/v1/economic/calendar/week", params=params)

    async def get_event_details(
        self,
        event_id: str,
        include_historical: bool = False,
    ) -> dict[str, Any]:
        """
        Get detailed information about a specific economic event.

        Parameters
        ----------
        event_id : str
            The event ID.
        include_historical : bool, default False
            Whether to include historical data.

        Returns
        -------
        dict[str, Any]
            Detailed event information.
        """
        params = {"include_historical": include_historical}
        return await self._request("GET", f"/api/v1/economic/events/{event_id}", params=params)

    async def get_country_indicators(
        self,
        country: str,
        indicators: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        limit: int = 100,
    ) -> dict[str, Any]:
        """
        Get country-specific economic indicators.

        Parameters
        ----------
        country : str
            Country code or name.
        indicators : str, optional
            Comma-separated list of indicators.
        start_date : str, optional
            Start date (YYYY-MM-DD).
        end_date : str, optional
            End date (YYYY-MM-DD).
        page : int, default 1
            Page number.
        limit : int, default 100
            Items per page.

        Returns
        -------
        dict[str, Any]
            Economic indicators data.
        """
        params = {"page": page, "limit": limit}
        if indicators:
            params["indicators"] = indicators
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await self._request("GET", f"/api/v1/economic/indicators/{country}", params=params)

    async def get_central_bank_meetings(
        self,
        country: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get central bank meeting schedule and announcements."""
        params = {}
        if country:
            params["country"] = country
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await self._request("GET", "/api/v1/economic/central-banks", params=params)

    async def create_economic_alert(
        self,
        event_types: list[str],
        countries: list[str],
        importance: str = "high",
        email: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Create economic event alerts.

        Parameters
        ----------
        event_types : list[str]
            Types of events to monitor.
        countries : list[str]
            Countries to monitor.
        importance : str, default "high"
            Minimum importance level.
        email : str, optional
            Email for notifications.
        webhook_url : str, optional
            Webhook URL for notifications.

        Returns
        -------
        dict[str, Any]
            Alert creation response.
        """
        payload = {
            "event_types": event_types,
            "countries": countries,
            "importance": importance,
        }
        if email:
            payload["email"] = email
        if webhook_url:
            payload["webhook_url"] = webhook_url

        return await self._request("POST", "/api/v1/economic/alerts", json=payload)

    # Portfolio Monitoring Methods
    async def list_portfolios(self, page: int = 1, limit: int = 100) -> dict[str, Any]:
        """List all portfolios with basic information."""
        params = {"page": page, "limit": limit}
        return await self._request("GET", "/api/v1/portfolio/", params=params)

    async def get_portfolio_details(
        self,
        portfolio_id: str,
        include_holdings: bool = False,
    ) -> dict[str, Any]:
        """
        Get detailed information about a specific portfolio.

        Parameters
        ----------
        portfolio_id : str
            Portfolio identifier.
        include_holdings : bool, default False
            Include detailed holdings.

        Returns
        -------
        dict[str, Any]
            Portfolio details.
        """
        params = {"include_holdings": include_holdings}
        return await self._request("GET", f"/api/v1/portfolio/{portfolio_id}", params=params)

    async def get_portfolio_performance(
        self,
        portfolio_id: str,
        timeframe: str = "1M",
        benchmark: str = "SPY",
    ) -> dict[str, Any]:
        """
        Get portfolio performance analytics.

        Parameters
        ----------
        portfolio_id : str
            Portfolio identifier.
        timeframe : str, default "1M"
            Performance timeframe.
        benchmark : str, default "SPY"
            Benchmark for comparison.

        Returns
        -------
        dict[str, Any]
            Performance analytics.
        """
        params = {"timeframe": timeframe, "benchmark": benchmark}
        return await self._request("GET", f"/api/v1/portfolio/{portfolio_id}/performance", params=params)

    async def get_portfolio_risk_analysis(
        self,
        portfolio_id: str,
        analysis_type: str = "var",
    ) -> dict[str, Any]:
        """
        Get portfolio risk analysis and metrics.

        Parameters
        ----------
        portfolio_id : str
            Portfolio identifier.
        analysis_type : str, default "var"
            Risk analysis type.

        Returns
        -------
        dict[str, Any]
            Risk analysis results.
        """
        params = {"analysis_type": analysis_type}
        return await self._request("GET", f"/api/v1/portfolio/{portfolio_id}/risk", params=params)

    async def _request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[dict[str, str]] = None,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Make an HTTP request to the microservice.

        Parameters
        ----------
        method : str
            HTTP method.
        endpoint : str
            API endpoint path.
        headers : dict[str, str], optional
            Additional headers for the request.
        **kwargs
            Additional arguments for the request.

        Returns
        -------
        dict[str, Any]
            Response data.
        """
        if not self._session:
            raise RuntimeError("Client not connected")

        url = f"{self._config.base_url}{endpoint}"

        # Merge additional headers with default headers
        request_headers = self._headers.copy()
        if headers:
            request_headers.update(headers)

        # Add headers to kwargs
        kwargs["headers"] = request_headers

        for attempt in range(self._config.max_retries + 1):
            try:
                async with self._session.request(method, url, **kwargs) as response:
                    if response.status >= 400:
                        error_text = await response.text()
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=error_text,
                        )

                    return await response.json()

            except Exception as e:
                if attempt == self._config.max_retries:
                    self._log.error(f"Request failed after {self._config.max_retries + 1} attempts: {e}")
                    raise

                self._log.warning(f"Request attempt {attempt + 1} failed, retrying: {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff