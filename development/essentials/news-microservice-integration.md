# News Microservice Integration

## Overview

This document describes the integration between Nautilus Trader and the News Microservice, providing real-time news data, economic event monitoring, and sentiment analysis capabilities for trading strategies.

## Architecture

The News Microservice integration is implemented as an adapter in `nautilus_trader.adapters.news_microservice` and provides:

- Real-time news event ingestion
- Economic calendar monitoring
- News sentiment analysis
- Custom alerts and filtering
- Support for multiple news sources

## API Endpoints

### Base Configuration
- **Base URL**: `http://localhost:8000` (configurable)
- **Authentication**: Bearer token (optional)
- **Rate Limiting**: 100 requests per minute

### Available Endpoints

#### Service Information
- `GET /` - Service information and version
- `GET /health` - Health check endpoint

#### News Data Ingestion
- `POST /v1/ingress/huginn` - Receive webhook from Huginn agents
- `POST /v1/ingress/raw-news` - Submit raw news data directly

#### Agent Management
- `GET /v1/status` - Get status of deployed news agents
- `POST /v1/deploy` - Deploy news source agents
- `GET /v1/templates` - List available news source templates

## Configuration

### NewsClientConfig

```python
from nautilus_trader.adapters.news_microservice import NewsClientConfig

config = NewsClientConfig(
    base_url="http://localhost:8000",
    api_key="your-api-key",  # Optional
    timeout_connect=5.0,
    timeout_request=10.0,
    max_retries=3,
    enable_webhooks=True,
    webhook_port=9001,
    news_categories=["economics", "politics", "technology"],
    importance_filter="medium",  # low, medium, high
    country_filter=["US", "GB", "DE"]
)
```

### Configuration Parameters

- **base_url**: News Microservice API base URL
- **api_key**: Authentication token (if required)
- **timeout_connect**: Connection timeout in seconds
- **timeout_request**: Request timeout in seconds
- **max_retries**: Maximum retry attempts for failed requests
- **enable_webhooks**: Enable webhook server for real-time news
- **webhook_port**: Port for webhook server
- **news_categories**: List of news categories to monitor
- **importance_filter**: Minimum importance level for news events
- **country_filter**: List of countries to filter news by

## Usage Example

### Basic Setup

```python
from nautilus_trader.adapters.news_microservice import NewsClient, NewsClientConfig
from nautilus_trader.common.component import MessageBus, TestClock
from nautilus_trader.common.logging import TestLogger

# Configuration
config = NewsClientConfig(
    base_url="http://localhost:8000",
    importance_filter="high",
    country_filter=["US", "GB"]
)

# Initialize client
clock = TestClock()
logger = TestLogger()
client = NewsClient(config, clock, logger)

# Add news event handler
def handle_news_event(event):
    print(f"News: {event.headline} from {event.source}")
    print(f"Importance: {event.importance}, Category: {event.category}")

client.add_news_handler(handle_news_event)

# Connect and start monitoring
await client.connect()

# Get agent status
status = await client.get_news_status()
print(f"Active agents: {status['active_agents']}")

# Deploy news sources
deployment = await client.deploy_news_sources(
    categories=["economics", "politics"],
    ai_engine_url="http://localhost:8080/ai-webhook"
)
print(f"Deployed {deployment['total_agents']} agents")

# Cleanup
await client.disconnect()
```

### Advanced Usage with Custom Filtering

```python
# Get available templates
templates = await client.get_templates()
for template in templates:
    print(f"Template: {template['name']} - {template['description']}")

# Submit raw news data
news_data = {
    "headline": "Breaking: Federal Reserve announces rate decision",
    "content": "The Federal Reserve announced...",
    "source_name": "Financial News Network",
    "category": "economics",
    "importance": "high",
    "country": "US"
}

response = await client.submit_raw_news(news_data)
print(f"News submitted: {response['status']}")
```

## Data Models

### NewsEvent

Represents a news event from the microservice:

```python
class NewsEvent(Data):
    source: str              # News source name
    headline: str            # News headline
    url: Optional[str]       # Original news URL
    content: Optional[str]   # News content/summary
    timestamp: int           # Event timestamp (UNIX nanoseconds)
    category: Optional[str]  # News category
    importance: Optional[str] # Importance level
    country: Optional[str]   # Associated country
    sentiment: Optional[float] # Sentiment score (-1.0 to 1.0)
```

## Webhook Integration

The adapter can receive real-time news updates via webhooks:

1. **Enable Webhooks**: Set `enable_webhooks=True` in configuration
2. **Configure Port**: Set `webhook_port` (default: 9001)
3. **Register Endpoint**: Configure News Microservice to send webhooks to `http://your-host:9001/webhook/news`

### Webhook Payload Format

```json
{
    "source_name": "Reuters",
    "headline": "Market Update: Stocks rally on positive data",
    "url": "https://reuters.com/article/123",
    "content": "Financial markets showed strong gains...",
    "category": "economics",
    "importance": "medium",
    "country": "US",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## Error Handling

The client implements robust error handling:

- **Connection Failures**: Automatic reconnection with exponential backoff
- **Rate Limiting**: Built-in rate limiting compliance
- **Request Timeouts**: Configurable timeout handling
- **Webhook Errors**: Graceful handling of malformed webhook data

## Integration with Trading Strategies

### News-Based Signal Generation

```python
from nautilus_trader.trading.strategy import Strategy

class NewsBasedStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.news_client = None

    def on_start(self):
        # Initialize news client
        config = NewsClientConfig(importance_filter="high")
        self.news_client = NewsClient(config, self.clock, self.logger)
        self.news_client.add_news_handler(self.on_news_event)
        await self.news_client.connect()

    def on_news_event(self, event: NewsEvent):
        # Analyze news for trading signals
        if event.importance == "high" and event.category == "economics":
            if "federal reserve" in event.headline.lower():
                # Generate trading signal based on Fed news
                self.generate_fed_signal(event)

    def generate_fed_signal(self, event: NewsEvent):
        # Implement Fed-specific signal logic
        if event.sentiment and event.sentiment > 0.5:
            # Positive Fed news - consider long positions
            pass
        elif event.sentiment and event.sentiment < -0.5:
            # Negative Fed news - consider short positions
            pass
```

## Best Practices

1. **Error Handling**: Always implement proper error handling for network operations
2. **Rate Limiting**: Respect API rate limits to avoid service disruption
3. **Filtering**: Use appropriate filters to reduce noise and focus on relevant news
4. **Sentiment Analysis**: Combine news sentiment with technical analysis for better signals
5. **Backtesting**: Validate news-based strategies with historical data when available

## Troubleshooting

### Common Issues

**Connection Failed**
- Verify News Microservice is running on configured port
- Check firewall settings and network connectivity
- Validate API key if authentication is enabled

**No News Events Received**
- Check if news agents are deployed and active
- Verify webhook configuration and network accessibility
- Review importance and category filters

**High CPU Usage**
- Reduce webhook frequency by adjusting filters
- Optimize news event handlers for performance
- Consider implementing event batching

**Memory Leaks**
- Ensure proper client cleanup with `disconnect()`
- Implement proper exception handling in event handlers
- Monitor event handler execution time

## Performance Considerations

- **Webhook Processing**: News events are processed asynchronously
- **Memory Usage**: Events are not cached by default to prevent memory growth
- **Network Overhead**: Configure appropriate timeout and retry settings
- **Event Frequency**: High-frequency news feeds may impact performance

## Security Notes

- **API Keys**: Store API keys securely, never commit to version control
- **Webhook Security**: Implement webhook signature verification in production
- **Network Security**: Use HTTPS in production environments
- **Access Control**: Restrict webhook endpoint access to trusted sources