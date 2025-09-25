# Finance Data & Indicators Microservice Integration

## Overview

This document describes the integration between Nautilus Trader and the Finance Data & Indicators Microservice, providing access to economic calendar data, portfolio monitoring, and financial indicators for enhanced trading strategies.

## Architecture

The Finance Data & Indicators Microservice integration is implemented as an adapter in `nautilus_trader.adapters.finance_microservice` and provides:

- Economic calendar events and indicators
- Country-specific economic data
- Central bank meeting schedules
- Portfolio performance monitoring
- Risk assessment analytics
- Economic alerts and notifications

## API Endpoints

### Base Configuration
- **Base URL**: `http://localhost:8080` (configurable)
- **Authentication**: Bearer token (optional)
- **Rate Limiting**: 100 requests per minute
- **Cache TTL**: 300 seconds (5 minutes)

### Available Endpoints

#### Service Information
- `GET /` - Service information and version
- `GET /health` - Basic health check endpoint
- `GET /system/health` - Comprehensive system health with service status
- `GET /api/v1/info` - API configuration and feature information

#### Monitoring (`/api/v1/monitoring`)
- `GET /monitoring/health` - System health with detailed checks
- `GET /monitoring/health/summary` - Health summary
- `GET /monitoring/metrics` - Comprehensive metrics including request counts, error rates
- `GET /monitoring/datetime-serialization` - DateTime handling validation

#### Performance Monitoring
- `GET /api/v1/performance/metrics` - Performance metrics with cache and database stats

#### Analytics Dashboard (`/api/analytics`)
- `GET /analytics/dashboard` - Full dashboard data with market overview
- `GET /analytics/financial-indicators/{symbol}` - Detailed financial indicators for symbols
- `GET /market` - Market overview data with indices and sectors

#### AI Insights
- `GET /ai/insights` - Comprehensive AI-powered portfolio analysis

#### Settings
- `GET /api/settings` - User preferences and configuration

#### Authentication (`/api/auth`)
- `POST /auth/login` - User authentication
- `GET /auth/profile` - User profile (requires authentication)
- `POST /auth/refresh` - Token refresh

#### Securities (`/api/v1/securities`)
- `GET /securities/search` - Search securities by symbol or name
- `GET /securities` - List available securities with pagination
- `GET /securities/{symbol}` - Get detailed security information
- `GET /securities/{symbol}/info` - Get basic security information
- `GET /securities/exchanges/list` - List available exchanges
- `GET /securities/sectors/list` - List available sectors

#### Data Providers
- `GET /fmp/health` - Financial Modeling Prep API health check
- `GET /api/v1/openbb/status` - OpenBB platform status
- `GET /api/v1/openbb/providers/list` - List of available OpenBB data providers

#### Economic Calendar (`/api/v1/economic`)
- `GET /economic/calendar` - Get economic calendar with filtering and pagination
- `GET /economic/calendar/today` - Today's economic releases
- `GET /economic/calendar/week` - Weekly economic events
- `GET /economic/events/{event_id}` - Specific event details with historical data
- `GET /economic/indicators/{country}` - Country-specific economic indicators
- `GET /economic/central-banks` - Central bank meetings and announcements
- `POST /economic/alerts` - Create economic event alerts

#### Portfolio Monitoring (`/api/v1/portfolio`)
- `GET /api/portfolio` - Portfolio summary with holdings and performance
- `GET /portfolio/` - List all portfolios with pagination
- `GET /portfolio/{portfolio_id}` - Get portfolio details and holdings
- `GET /portfolio/{portfolio_id}/performance` - Portfolio performance analytics
- `GET /portfolio/{portfolio_id}/risk` - Portfolio risk analysis and metrics

## Configuration

### FinanceClientConfig

```python
from nautilus_trader.adapters.finance_microservice import FinanceClientConfig

config = FinanceClientConfig(
    base_url="http://localhost:8080",
    api_key="your-api-key",  # Optional
    timeout_connect=5.0,
    timeout_request=10.0,
    max_retries=3,
    cache_ttl=300,
    default_country="united_states",
    default_indicators=["GDP", "CPI", "UNRATE"],
    importance_filter="medium",  # low, medium, high
    enable_portfolio_monitoring=True
)
```

### Configuration Parameters

- **base_url**: Finance Microservice API base URL
- **api_key**: Authentication token (if required)
- **timeout_connect**: Connection timeout in seconds
- **timeout_request**: Request timeout in seconds
- **max_retries**: Maximum retry attempts for failed requests
- **cache_ttl**: Cache time-to-live in seconds
- **default_country**: Default country for economic indicators
- **default_indicators**: Default economic indicators to monitor
- **importance_filter**: Minimum importance level for economic events
- **enable_portfolio_monitoring**: Enable portfolio monitoring features

## Usage Examples

### Basic Setup

```python
from nautilus_trader.adapters.finance_microservice import FinanceClient, FinanceClientConfig
from nautilus_trader.common.component import MessageBus, TestClock
from nautilus_trader.common.logging import TestLogger

# Configuration
config = FinanceClientConfig(
    base_url="http://localhost:8080",
    default_country="united_states",
    importance_filter="high"
)

# Initialize client
clock = TestClock()
logger = TestLogger()
client = FinanceClient(config, clock, logger)

# Add event handlers
def handle_economic_event(event):
    print(f"Economic Event: {event.name} ({event.country})")
    print(f"Importance: {event.importance}, Actual: {event.actual_value}")

def handle_indicator_update(indicator):
    print(f"Indicator Update: {indicator.indicator} = {indicator.value}")

client.add_economic_event_handler(handle_economic_event)
client.add_indicator_handler(handle_indicator_update)

# Connect to microservice
await client.connect()
```

### Economic Calendar Integration

```python
# Get today's economic releases
todays_events = await client.get_todays_economic_releases(
    country="united_states",
    importance="high"
)

print(f"Today's high-impact events: {len(todays_events['data'])}")
for event in todays_events['data']:
    print(f"- {event['name']} at {event['scheduled_time']}")

# Get weekly economic events
weekly_events = await client.get_weekly_economic_events(
    country="united_states",
    importance="medium"
)

print(f"This week's events: {len(weekly_events['data'])}")

# Get detailed event information
event_details = await client.get_event_details(
    event_id="event_123",
    include_historical=True
)

print(f"Event: {event_details['name']}")
print(f"Forecast: {event_details['forecast']}")
print(f"Previous: {event_details['previous_value']}")
```

### Economic Indicators

```python
# Get country-specific indicators
us_indicators = await client.get_country_indicators(
    country="united_states",
    indicators="GDP,CPI,UNRATE",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

print(f"US Indicators: {len(us_indicators['data'])} records")

# Get central bank meetings
fed_meetings = await client.get_central_bank_meetings(
    country="united_states",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

print(f"Fed meetings: {len(fed_meetings['data'])}")

# Create economic alert
alert_response = await client.create_economic_alert(
    event_types=["FOMC Meeting", "CPI Release", "GDP Report"],
    countries=["united_states", "united_kingdom"],
    importance="high",
    webhook_url="http://localhost:9001/economic-alerts"
)

print(f"Alert created: {alert_response['alert_id']}")
```

### Portfolio Monitoring

```python
# List available portfolios
portfolios = await client.list_portfolios(page=1, limit=10)
print(f"Found {len(portfolios['data'])} portfolios")

# Get portfolio details
if portfolios['data']:
    portfolio_id = portfolios['data'][0]['portfolio_id']

    # Get detailed portfolio information
    details = await client.get_portfolio_details(
        portfolio_id=portfolio_id,
        include_holdings=True
    )

    print(f"Portfolio: {details['name']}")
    print(f"Total Value: ${details['total_value']:,.2f}")
    print(f"Holdings: {len(details['holdings']) if details['holdings'] else 0}")

    # Get performance analytics
    performance = await client.get_portfolio_performance(
        portfolio_id=portfolio_id,
        timeframe="1M",
        benchmark="SPY"
    )

    metrics = performance['performance_metrics']
    print(f"Total Return: {metrics['total_return']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")

    # Get risk analysis
    risk_analysis = await client.get_portfolio_risk_analysis(
        portfolio_id=portfolio_id,
        analysis_type="var"
    )

    risk_metrics = risk_analysis['risk_metrics']
    print(f"Value at Risk (95%): {risk_metrics['value_at_risk_95']:.2%}")
    print(f"Portfolio Volatility: {risk_metrics['portfolio_volatility']:.2%}")
```

### Advanced Analytics and Monitoring Usage

```python
# System Health and Monitoring
api_info = await client.get_api_info()
print(f"API Version: {api_info.get('version')}")

system_health = await client.get_system_health()
print(f"System Status: {system_health.get('status')}")

metrics = await client.get_monitoring_metrics()
print(f"Request Count: {metrics.get('request_count')}")

# Analytics and Market Data
dashboard = await client.get_analytics_dashboard()
print(f"Market Overview: {dashboard.get('market_overview')}")

aapl_indicators = await client.get_financial_indicators('AAPL')
print(f"AAPL Financial Health: {aapl_indicators.get('financial_health')}")

market_data = await client.get_market_overview()
for index in market_data.get('indices', []):
    print(f"{index['name']}: {index['value']} ({index['change']}%)")

# AI Insights
ai_insights = await client.get_ai_insights()
for insight in ai_insights.get('recommendations', []):
    print(f"AI Recommendation: {insight['action']} - {insight['reason']}")

# Securities Management
search_results = await client.search_securities(query="AAPL")
for security in search_results.get('data', []):
    print(f"Found: {security['symbol']} - {security['name']}")

security_details = await client.get_security_details('AAPL')
print(f"AAPL Details: {security_details.get('company_name')}")

exchanges = await client.list_exchanges()
print(f"Available Exchanges: {[ex['name'] for ex in exchanges.get('data', [])]}")

sectors = await client.list_sectors()
print(f"Available Sectors: {[s['name'] for s in sectors.get('data', [])]}")

# Data Provider Health
fmp_health = await client.get_fmp_health()
print(f"FMP Status: {fmp_health.get('status')}")

openbb_status = await client.get_openbb_status()
print(f"OpenBB Status: {openbb_status.get('status')}")

openbb_providers = await client.get_openbb_providers()
for provider in openbb_providers.get('providers', []):
    print(f"Provider: {provider['name']} - {provider['status']}")

# User Settings
settings = await client.get_user_settings()
print(f"Theme: {settings.get('theme', {}).get('mode')}")
print(f"Currency: {settings.get('display', {}).get('currency')}")

# Performance Monitoring
perf_metrics = await client.get_performance_metrics()
print(f"Cache Hit Rate: {perf_metrics.get('cache', {}).get('hit_rate')}")
print(f"Database Response Time: {perf_metrics.get('database', {}).get('response_time')}ms")
```

### Authentication Usage

```python
# Login to get access token
login_response = await client.login(
    email="user@example.com",
    password="secure_password"
)
access_token = login_response.get('access_token')

# Get user profile with token
profile = await client.get_profile(access_token)
print(f"User: {profile.get('name')} ({profile.get('email')})")

# Refresh token when needed
refresh_response = await client.refresh_token(
    refresh_token=login_response.get('refresh_token')
)
new_access_token = refresh_response.get('access_token')
```

## Data Models

### EconomicEvent

Represents an economic event from the microservice:

```python
class EconomicEvent(Data):
    event_id: str                    # Unique event identifier
    name: str                        # Event name/title
    country: str                     # Associated country
    importance: str                  # Importance level (low/medium/high)
    category: Optional[str]          # Economic category
    scheduled_time: int              # Scheduled time (UNIX nanoseconds)
    previous_value: Optional[float]  # Previous indicator value
    forecast: Optional[float]        # Forecasted value
    actual_value: Optional[float]    # Actual reported value
```

### EconomicIndicator

Represents an economic indicator data point:

```python
class EconomicIndicator(Data):
    indicator: str           # Indicator code (GDP, CPI, UNRATE)
    country: str            # Country for the indicator
    value: float            # Indicator value
    period: Optional[str]   # Time period for the data
    timestamp: int          # Data timestamp (UNIX nanoseconds)
```

### PortfolioPerformance

Represents portfolio performance metrics:

```python
class PortfolioPerformance(Data):
    portfolio_id: str               # Portfolio identifier
    total_return: float             # Total portfolio return
    daily_return: float             # Daily return
    volatility: float               # Portfolio volatility
    sharpe_ratio: Optional[float]   # Sharpe ratio
    max_drawdown: Optional[float]   # Maximum drawdown
    timestamp: int                  # Performance timestamp (UNIX nanoseconds)
```

## Integration with Trading Strategies

### Economic Event-Based Strategy

```python
from nautilus_trader.trading.strategy import Strategy

class EconomicEventStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.finance_client = None
        self.pending_events = {}

    def on_start(self):
        # Initialize finance client
        config = FinanceClientConfig(importance_filter="high")
        self.finance_client = FinanceClient(config, self.clock, self.logger)
        self.finance_client.add_economic_event_handler(self.on_economic_event)
        await self.finance_client.connect()

        # Pre-load today's high-impact events
        await self.load_todays_events()

    async def load_todays_events(self):
        events = await self.finance_client.get_todays_economic_releases(
            importance="high"
        )

        for event_data in events['data']:
            event_id = event_data['event_id']
            self.pending_events[event_id] = event_data
            self.log.info(f"Scheduled: {event_data['name']} at {event_data['scheduled_time']}")

    def on_economic_event(self, event: EconomicEvent):
        # Process high-impact economic events
        if event.importance == "high":
            self.process_high_impact_event(event)

    def process_high_impact_event(self, event: EconomicEvent):
        # GDP release impact
        if "GDP" in event.name and event.actual_value is not None:
            self.handle_gdp_release(event)

        # CPI release impact
        elif "CPI" in event.name and event.actual_value is not None:
            self.handle_cpi_release(event)

        # FOMC decision impact
        elif "FOMC" in event.name:
            self.handle_fomc_decision(event)

    def handle_gdp_release(self, event: EconomicEvent):
        # Analyze GDP surprise vs forecast
        if event.forecast and event.actual_value:
            surprise = (event.actual_value - event.forecast) / event.forecast

            if abs(surprise) > 0.02:  # 2% surprise threshold
                if surprise > 0:
                    # Positive GDP surprise - bullish signal
                    self.generate_bullish_signal("GDP_SURPRISE", event)
                else:
                    # Negative GDP surprise - bearish signal
                    self.generate_bearish_signal("GDP_SURPRISE", event)

    def handle_cpi_release(self, event: EconomicEvent):
        # Analyze inflation surprise
        if event.forecast and event.actual_value:
            surprise = event.actual_value - event.forecast

            if abs(surprise) > 0.1:  # 0.1% surprise threshold
                if surprise > 0:
                    # Higher than expected inflation - hawkish signal
                    self.generate_hawkish_signal("CPI_SURPRISE", event)
                else:
                    # Lower than expected inflation - dovish signal
                    self.generate_dovish_signal("CPI_SURPRISE", event)
```

### Portfolio-Based Risk Management

```python
class PortfolioRiskStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.finance_client = None
        self.portfolio_id = "main_portfolio"
        self.risk_threshold = 0.02  # 2% VaR threshold

    def on_start(self):
        config = FinanceClientConfig(enable_portfolio_monitoring=True)
        self.finance_client = FinanceClient(config, self.clock, self.logger)
        await self.finance_client.connect()

        # Schedule periodic risk checks
        self.clock.set_timer("risk_check", timedelta(minutes=15), self.check_portfolio_risk)

    async def check_portfolio_risk(self):
        # Get current portfolio risk metrics
        risk_analysis = await self.finance_client.get_portfolio_risk_analysis(
            portfolio_id=self.portfolio_id,
            analysis_type="var"
        )

        var_95 = risk_analysis['risk_metrics']['value_at_risk_95']

        if abs(var_95) > self.risk_threshold:
            self.log.warning(f"Portfolio VaR exceeded threshold: {var_95:.2%}")
            await self.implement_risk_reduction()

    async def implement_risk_reduction(self):
        # Get detailed portfolio information
        portfolio = await self.finance_client.get_portfolio_details(
            portfolio_id=self.portfolio_id,
            include_holdings=True
        )

        # Identify high-risk positions for reduction
        if portfolio['holdings']:
            for holding in portfolio['holdings']:
                # Implement position reduction logic
                pass
```

## Error Handling and Resilience

### Connection Management

```python
class ResilientFinanceClient:
    def __init__(self, config: FinanceClientConfig):
        self.config = config
        self.client = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5

    async def ensure_connected(self):
        if not self.client or not self.client.is_connected:
            await self.reconnect()

    async def reconnect(self):
        while self.reconnect_attempts < self.max_reconnect_attempts:
            try:
                if self.client:
                    await self.client.disconnect()

                self.client = FinanceClient(self.config, clock, logger)
                await self.client.connect()

                self.reconnect_attempts = 0
                self.log.info("Reconnected to Finance Microservice")
                break

            except Exception as e:
                self.reconnect_attempts += 1
                wait_time = 2 ** self.reconnect_attempts
                self.log.error(f"Reconnection attempt {self.reconnect_attempts} failed: {e}")
                await asyncio.sleep(wait_time)

    async def safe_request(self, method, *args, **kwargs):
        await self.ensure_connected()

        try:
            return await getattr(self.client, method)(*args, **kwargs)
        except Exception as e:
            self.log.error(f"Request failed: {e}")
            await self.reconnect()
            raise
```

## Best Practices

1. **Caching Strategy**: Leverage built-in caching for frequently accessed data
2. **Rate Limiting**: Implement client-side rate limiting to prevent API overuse
3. **Error Handling**: Always handle network failures and timeouts gracefully
4. **Data Validation**: Validate economic data before using in trading decisions
5. **Performance**: Use pagination for large datasets to minimize memory usage
6. **Security**: Secure API keys and use HTTPS in production

## Troubleshooting

### Common Issues

**Connection Timeout**
- Increase `timeout_connect` and `timeout_request` values
- Check network connectivity to microservice
- Verify microservice is running and accessible

**Rate Limit Exceeded**
- Implement request throttling in your application
- Use caching to reduce API calls
- Contact administrator to increase rate limits

**Invalid Economic Data**
- Verify date formats (YYYY-MM-DD)
- Check country codes are supported
- Validate importance levels (low/medium/high)

**Portfolio Not Found**
- Ensure portfolio exists in the system
- Check portfolio_id format and permissions
- Verify portfolio monitoring is enabled

## Performance Optimization

- **Request Batching**: Combine multiple requests where possible
- **Async Processing**: Use async/await for all API calls
- **Caching**: Implement local caching for frequently accessed data
- **Connection Pooling**: Reuse HTTP connections for multiple requests
- **Pagination**: Use appropriate page sizes for large datasets

## Security Considerations

- **API Authentication**: Use secure API key management
- **HTTPS**: Always use HTTPS in production environments
- **Input Validation**: Validate all input parameters
- **Error Information**: Don't expose sensitive data in error messages
- **Access Control**: Implement proper authorization for portfolio data