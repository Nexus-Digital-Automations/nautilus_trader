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
News Microservice client for real-time news data integration.
"""

import asyncio
import logging
from typing import Any, Callable, Optional

import aiohttp

from nautilus_trader.adapters.news_microservice.config import NewsClientConfig, NewsEvent
from nautilus_trader.common.component import Component
from nautilus_trader.common.enums import LogLevel
from nautilus_trader.core.datetime import unix_nanos_to_dt
from nautilus_trader.core.datetime import utc_now


class NewsClient(Component):
    """
    Client for connecting to and retrieving data from the News Microservice.

    This client provides methods to:
    - Fetch real-time news events
    - Monitor economic calendar events
    - Deploy and manage news source agents
    - Handle webhook subscriptions for real-time updates
    """

    def __init__(
        self,
        config: NewsClientConfig,
        clock,
        logger_factory,
    ) -> None:
        """
        Initialize the News Microservice client.

        Parameters
        ----------
        config : NewsClientConfig
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
        self._news_handlers: list[Callable[[NewsEvent], None]] = []

        # Base headers for all requests
        self._headers = {"Content-Type": "application/json"}
        if config.api_key:
            self._headers["Authorization"] = f"Bearer {config.api_key}"

        # Webhook server
        self._webhook_app: Optional[Any] = None
        self._webhook_runner: Optional[Any] = None

    @property
    def is_connected(self) -> bool:
        """Return True if client is connected to the microservice."""
        return self._is_connected

    async def connect(self) -> None:
        """Connect to the News Microservice."""
        self._log.info("Connecting to News Microservice...")

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
            if health_response.get("status") == "healthy":
                self._is_connected = True
                self._log.info("Successfully connected to News Microservice")
            else:
                raise ConnectionError(f"News Microservice health check failed: {health_response}")

        except Exception as e:
            self._log.error(f"Failed to connect to News Microservice: {e}")
            if self._session:
                await self._session.close()
                self._session = None
            raise

        # Start webhook server if enabled
        if self._config.enable_webhooks:
            await self._start_webhook_server()

    async def disconnect(self) -> None:
        """Disconnect from the News Microservice."""
        self._log.info("Disconnecting from News Microservice...")

        self._is_connected = False

        # Stop webhook server
        if self._webhook_runner:
            await self._webhook_runner.cleanup()
            self._webhook_runner = None

        # Close HTTP session
        if self._session:
            await self._session.close()
            self._session = None

        self._log.info("Disconnected from News Microservice")

    def add_news_handler(self, handler: Callable[[NewsEvent], None]) -> None:
        """
        Add a handler for news events.

        Parameters
        ----------
        handler : Callable[[NewsEvent], None]
            The news event handler function.
        """
        self._news_handlers.append(handler)
        self._log.debug(f"Added news handler: {handler.__name__}")

    async def get_news_status(self) -> dict[str, Any]:
        """
        Get the status of deployed news agents.

        Returns
        -------
        dict[str, Any]
            Status information about deployed agents.
        """
        return await self._request("GET", "/v1/status")

    async def deploy_news_sources(
        self,
        categories: Optional[list[str]] = None,
        ai_engine_url: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Deploy news source agents.

        Parameters
        ----------
        categories : list[str], optional
            Categories of news sources to deploy.
        ai_engine_url : str, optional
            URL for AI engine webhook forwarding.

        Returns
        -------
        dict[str, Any]
            Deployment results.
        """
        payload = {}
        if categories:
            payload["categories"] = categories
        if ai_engine_url:
            payload["ai_engine_url"] = ai_engine_url

        return await self._request("POST", "/v1/deploy", json=payload)

    async def get_templates(self) -> list[dict[str, Any]]:
        """
        Get available news source templates.

        Returns
        -------
        list[dict[str, Any]]
            List of available news source templates.
        """
        return await self._request("GET", "/v1/templates")

    async def submit_raw_news(self, news_data: dict[str, Any]) -> dict[str, str]:
        """
        Submit raw news data to the microservice.

        Parameters
        ----------
        news_data : dict[str, Any]
            Raw news data payload.

        Returns
        -------
        dict[str, str]
            Submission response.
        """
        return await self._request("POST", "/v1/ingress/raw-news", json=news_data)

    async def _request(
        self,
        method: str,
        endpoint: str,
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

    async def _start_webhook_server(self) -> None:
        """Start the webhook server for receiving news events."""
        try:
            from aiohttp import web

            self._webhook_app = web.Application()
            self._webhook_app.router.add_post('/webhook/news', self._handle_webhook)

            runner = web.AppRunner(self._webhook_app)
            await runner.setup()

            site = web.TCPSite(runner, '0.0.0.0', self._config.webhook_port)
            await site.start()

            self._webhook_runner = runner
            self._log.info(f"Started webhook server on port {self._config.webhook_port}")

        except Exception as e:
            self._log.error(f"Failed to start webhook server: {e}")

    async def _handle_webhook(self, request) -> Any:
        """Handle incoming webhook requests."""
        try:
            from aiohttp import web

            payload = await request.json()

            # Convert webhook payload to NewsEvent
            news_event = self._create_news_event_from_payload(payload)

            # Notify all handlers
            for handler in self._news_handlers:
                try:
                    handler(news_event)
                except Exception as e:
                    self._log.error(f"Error in news handler {handler.__name__}: {e}")

            return web.json_response({"status": "received"})

        except Exception as e:
            self._log.error(f"Error handling webhook: {e}")
            return web.json_response({"error": str(e)}, status=500)

    def _create_news_event_from_payload(self, payload: dict[str, Any]) -> NewsEvent:
        """
        Create a NewsEvent from webhook payload.

        Parameters
        ----------
        payload : dict[str, Any]
            Webhook payload data.

        Returns
        -------
        NewsEvent
            Processed news event.
        """
        timestamp = utc_now()

        return NewsEvent(
            source=payload.get("source_name", "unknown"),
            headline=payload.get("headline") or payload.get("title", "No headline"),
            url=payload.get("url") or payload.get("link"),
            content=payload.get("content") or payload.get("summary") or payload.get("description"),
            timestamp=timestamp.timestamp_ns,
            category=payload.get("category"),
            importance=payload.get("importance"),
            country=payload.get("country"),
            sentiment=payload.get("sentiment"),
        )