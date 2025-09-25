# Microservices API Reference

## Overview

This document provides a comprehensive reference for all API endpoints available in both the News Microservice and Finance Data & Indicators Microservice integrations with Nautilus Trader.

## News Microservice API Reference

### Base Configuration
- **Base URL**: `http://localhost:8000`
- **Authentication**: Bearer token (optional)
- **Rate Limiting**: 100 requests per minute

### Service Information Endpoints

#### Get Service Information
- **Endpoint**: `GET /`
- **Description**: Returns basic service information and version
- **Response**: Service metadata and status

#### Health Check
- **Endpoint**: `GET /health`
- **Description**: Health check endpoint for service monitoring
- **Response**: Service health status and Huginn integration status

### News Data Ingestion Endpoints

#### Receive Huginn Webhook
- **Endpoint**: `POST /v1/ingress/huginn`
- **Description**: Receive webhook payload from Huginn agents
- **Request Body**: WebhookPayload with news data
- **Response**: Receipt confirmation and queuing status

#### Submit Raw News
- **Endpoint**: `POST /v1/ingress/raw-news`
- **Description**: Submit raw news data directly to the microservice
- **Request Body**: Raw news data in compatible format
- **Response**: Submission status and processing confirmation

### Agent Management Endpoints

#### Get Agent Status
- **Endpoint**: `GET /v1/status`
- **Description**: Retrieve status of all deployed news agents
- **Response**: Agent statistics, active/disabled counts, deployment status

#### Deploy News Sources
- **Endpoint**: `POST /v1/deploy`
- **Description**: Deploy news source agents with optional AI integration
- **Request Body**: DeploymentRequest with categories and AI engine URL
- **Response**: Deployment results and agent creation summary

#### List Templates
- **Endpoint**: `GET /v1/templates`
- **Description**: List all available news source templates
- **Response**: Array of templates with descriptions and categories

### Webhook Payload Structure

```json
{
    "source_name": "string",
    "headline": "string",
    "title": "string",
    "url": "string",
    "link": "string",
    "content": "string",
    "summary": "string",
    "description": "string",
    "timestamp": "string",
    "created_at": "string",
    "category": "string",
    "raw_data": {}
}
```

## Finance Data & Indicators Microservice API Reference

### Base Configuration
- **Base URL**: `http://localhost:8080`
- **Authentication**: Bearer token (optional)
- **Rate Limiting**: 100 requests per minute
- **Cache TTL**: 300 seconds (5 minutes)

### Service Information Endpoints

#### Get Service Information
- **Endpoint**: `GET /`
- **Description**: Returns service information and version
- **Response**: Service metadata and running status

#### Health Check
- **Endpoint**: `GET /health`
- **Description**: Basic health check endpoint
- **Response**: Service health status

#### System Health Check
- **Endpoint**: `GET /system/health`
- **Description**: Comprehensive system health with service status
- **Response**: Detailed system health information

#### API Information
- **Endpoint**: `GET /api/v1/info`
- **Description**: API configuration and feature information
- **Response**: API configuration details and available features

### Economic Calendar Endpoints

#### Get Economic Calendar
- **Endpoint**: `GET /api/v1/economic/calendar`
- **Description**: Retrieve economic events with comprehensive filtering
- **Query Parameters**:
  - `country`: Country filter (optional)
  - `importance`: Event importance level (low/medium/high)
  - `start_date`: Start date (YYYY-MM-DD)
  - `end_date`: End date (YYYY-MM-DD)
  - `category`: Economic category filter
  - `format`: Response format (json/csv/excel)
  - `page`: Page number (default: 1)
  - `limit`: Items per page (default: 100, max: 1000)
- **Response**: Paginated economic events with metadata

#### Today's Economic Releases
- **Endpoint**: `GET /api/v1/economic/calendar/today`
- **Description**: Get today's economic releases and events
- **Query Parameters**:
  - `country`: Country filter (optional)
  - `importance`: Minimum importance level (default: medium)
  - `format`: Response format (default: json)
- **Response**: Today's economic events with metadata

#### Weekly Economic Events
- **Endpoint**: `GET /api/v1/economic/calendar/week`
- **Description**: Get this week's important economic events
- **Query Parameters**:
  - `country`: Country filter (optional)
  - `importance`: Minimum importance level (default: medium)
  - `format`: Response format (default: json)
- **Response**: Current week's economic events

#### Event Details
- **Endpoint**: `GET /api/v1/economic/events/{event_id}`
- **Description**: Get detailed information about a specific economic event
- **Path Parameters**:
  - `event_id`: Unique event identifier
- **Query Parameters**:
  - `include_historical`: Include historical data (default: false)
  - `format`: Response format (default: json)
- **Response**: Detailed event information with optional historical context

#### Country Indicators
- **Endpoint**: `GET /api/v1/economic/indicators/{country}`
- **Description**: Get country-specific economic indicators
- **Path Parameters**:
  - `country`: Country code or name
- **Query Parameters**:
  - `indicators`: Comma-separated list of indicators (optional)
  - `start_date`: Start date (YYYY-MM-DD)
  - `end_date`: End date (YYYY-MM-DD)
  - `format`: Response format (default: json)
  - `page`: Page number (default: 1)
  - `limit`: Items per page (default: 100, max: 1000)
- **Response**: Paginated economic indicators data

#### Central Bank Meetings
- **Endpoint**: `GET /api/v1/economic/central-banks`
- **Description**: Get central bank meeting schedules and announcements
- **Query Parameters**:
  - `country`: Country filter (optional)
  - `start_date`: Start date (YYYY-MM-DD)
  - `end_date`: End date (YYYY-MM-DD)
  - `format`: Response format (default: json)
- **Response**: Central bank meetings and policy announcements

#### Create Economic Alert
- **Endpoint**: `POST /api/v1/economic/alerts`
- **Description**: Create economic event alerts and notifications
- **Request Body**: AlertRequest with event types, countries, and notification preferences
- **Response**: Alert creation confirmation and configuration

### Monitoring Endpoints

#### Monitoring Health
- **Endpoint**: `GET /api/v1/monitoring/health`
- **Description**: System health with detailed checks
- **Response**: Comprehensive system health metrics

#### Monitoring Health Summary
- **Endpoint**: `GET /api/v1/monitoring/health/summary`
- **Description**: Get health summary
- **Response**: Condensed health status summary

#### Monitoring Metrics
- **Endpoint**: `GET /api/v1/monitoring/metrics`
- **Description**: Comprehensive metrics including request counts, error rates
- **Response**: Detailed system metrics and performance data

#### DateTime Serialization Test
- **Endpoint**: `GET /api/v1/monitoring/datetime-serialization`
- **Description**: Test datetime handling validation
- **Response**: DateTime serialization validation results

### Performance Monitoring Endpoints

#### Performance Metrics
- **Endpoint**: `GET /api/v1/performance/metrics`
- **Description**: Performance metrics with cache and database stats
- **Response**: Detailed performance metrics and resource usage

### Analytics Dashboard Endpoints

#### Analytics Dashboard
- **Endpoint**: `GET /api/analytics/dashboard`
- **Description**: Full dashboard data with market overview and analytics
- **Response**: Comprehensive dashboard data including market indices, performance, and insights

#### Financial Indicators
- **Endpoint**: `GET /api/analytics/financial-indicators/{symbol}`
- **Description**: Detailed financial indicators for a specific symbol
- **Path Parameters**:
  - `symbol`: Stock symbol (e.g., AAPL, MSFT)
- **Response**: Comprehensive financial indicators and analysis

#### Market Overview
- **Endpoint**: `GET /api/market`
- **Description**: Market overview data with indices and sector performance
- **Response**: Market overview with major indices, top performers, and sector data

### AI Insights Endpoints

#### AI Insights
- **Endpoint**: `GET /ai/insights`
- **Description**: Comprehensive AI-powered portfolio analysis
- **Response**: AI-generated portfolio insights, recommendations, and predictions

### Settings Endpoints

#### User Settings
- **Endpoint**: `GET /api/settings`
- **Description**: User preferences and configuration
- **Response**: User settings including themes, display preferences, and notifications

### Authentication Endpoints

#### Login
- **Endpoint**: `POST /api/auth/login`
- **Description**: User authentication
- **Request Body**: `{"email": "string", "password": "string"}`
- **Response**: Authentication token and user information

#### User Profile
- **Endpoint**: `GET /api/auth/profile`
- **Description**: Get user profile (requires authentication)
- **Headers**: `Authorization: Bearer <token>`
- **Response**: User profile information

#### Refresh Token
- **Endpoint**: `POST /api/auth/refresh`
- **Description**: Refresh access token
- **Request Body**: `{"refresh_token": "string"}`
- **Response**: New access token

### Securities Endpoints

#### Search Securities
- **Endpoint**: `GET /api/v1/securities/search`
- **Description**: Search securities by symbol or name
- **Query Parameters**:
  - `q`: Search query (optional)
  - `limit`: Maximum results (default: 100)
- **Response**: List of matching securities

#### List Securities
- **Endpoint**: `GET /api/v1/securities`
- **Description**: List available securities
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `limit`: Items per page (default: 100)
- **Response**: Paginated list of securities

#### Security Details
- **Endpoint**: `GET /api/v1/securities/{symbol}`
- **Description**: Get detailed security information
- **Path Parameters**:
  - `symbol`: Security symbol
- **Response**: Detailed security information

#### Security Info
- **Endpoint**: `GET /api/v1/securities/{symbol}/info`
- **Description**: Get basic security information
- **Path Parameters**:
  - `symbol`: Security symbol
- **Response**: Basic security information

#### List Exchanges
- **Endpoint**: `GET /api/v1/securities/exchanges/list`
- **Description**: List available exchanges
- **Response**: List of supported exchanges

#### List Sectors
- **Endpoint**: `GET /api/v1/securities/sectors/list`
- **Description**: List available sectors
- **Response**: List of market sectors

### Data Provider Endpoints

#### FMP Health
- **Endpoint**: `GET /fmp/health`
- **Description**: Financial Modeling Prep API health check
- **Response**: FMP service health status

#### OpenBB Status
- **Endpoint**: `GET /api/v1/openbb/status`
- **Description**: OpenBB platform status
- **Response**: OpenBB service status and configuration

#### OpenBB Providers
- **Endpoint**: `GET /api/v1/openbb/providers/list`
- **Description**: List of available OpenBB data providers
- **Response**: Available OpenBB data providers and their status

### Portfolio Monitoring Endpoints

#### Portfolio Summary
- **Endpoint**: `GET /api/portfolio`
- **Description**: Get portfolio summary with holdings and performance
- **Response**: Comprehensive portfolio data with holdings, performance, and risk metrics

#### List Portfolios
- **Endpoint**: `GET /api/v1/portfolio/`
- **Description**: List all portfolios with basic information
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `limit`: Items per page (default: 100, max: 1000)
- **Response**: Paginated list of portfolios

#### Portfolio Details
- **Endpoint**: `GET /api/v1/portfolio/{portfolio_id}`
- **Description**: Get detailed information about a specific portfolio
- **Path Parameters**:
  - `portfolio_id`: Portfolio identifier
- **Query Parameters**:
  - `include_holdings`: Include detailed holdings (default: false)
- **Response**: Comprehensive portfolio information

#### Portfolio Performance
- **Endpoint**: `GET /api/v1/portfolio/{portfolio_id}/performance`
- **Description**: Get portfolio performance analytics and benchmarking
- **Path Parameters**:
  - `portfolio_id`: Portfolio identifier
- **Query Parameters**:
  - `timeframe`: Performance timeframe (default: 1M)
  - `benchmark`: Benchmark for comparison (default: SPY)
- **Response**: Detailed performance metrics and benchmark comparison

#### Portfolio Risk Analysis
- **Endpoint**: `GET /api/v1/portfolio/{portfolio_id}/risk`
- **Description**: Get portfolio risk analysis and metrics
- **Path Parameters**:
  - `portfolio_id`: Portfolio identifier
- **Query Parameters**:
  - `analysis_type`: Risk analysis type (default: var)
- **Response**: Comprehensive risk analytics and exposure analysis

### Request/Response Models

#### Economic Event Filter
```json
{
    "country": "string",
    "importance": "low|medium|high",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "category": "string"
}
```

#### Economic Indicator Request
```json
{
    "indicator": "string",
    "country": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "provider": "string"
}
```

#### Alert Request
```json
{
    "event_types": ["string"],
    "countries": ["string"],
    "importance": "low|medium|high",
    "email": "string",
    "webhook_url": "string"
}
```

#### Economic Event Response
```json
{
    "event_id": "string",
    "name": "string",
    "country": "string",
    "importance": "low|medium|high",
    "category": "string",
    "scheduled_time": "string",
    "description": "string",
    "previous_value": "number",
    "forecast": "number",
    "actual_value": "number",
    "impact": "string",
    "currency_affected": "string",
    "market_sectors_affected": ["string"]
}
```

#### Portfolio Performance Response
```json
{
    "portfolio_id": "string",
    "timeframe": "string",
    "benchmark": "string",
    "performance_metrics": {
        "total_return": "number",
        "annualized_return": "number",
        "volatility": "number",
        "sharpe_ratio": "number",
        "max_drawdown": "number",
        "beta": "number",
        "alpha": "number"
    },
    "benchmark_comparison": {
        "outperformance": "number",
        "correlation": "number",
        "tracking_error": "number"
    }
}
```

## Response Formats and Pagination

### Standard Response Structure
```json
{
    "data": [],
    "pagination": {
        "page": "number",
        "limit": "number",
        "total": "number",
        "pages": "number"
    },
    "metadata": {
        "timestamp": "string",
        "source": "string",
        "count": "number"
    }
}
```

### Error Response Structure
```json
{
    "error": "string",
    "message": "string",
    "status_code": "number",
    "timestamp": "string"
}
```

## Country Code Mapping

Both microservices support standardized country codes:

- **US/USA/United States** → `united_states`
- **GB/UK/United Kingdom** → `united_kingdom`
- **DE/Germany** → `germany`
- **FR/France** → `france`
- **JP/Japan** → `japan`
- **CN/China** → `china`
- **CA/Canada** → `canada`
- **AU/Australia** → `australia`
- And many more...

## Common Query Parameters

### Pagination
- `page`: Page number (default: 1, minimum: 1)
- `limit`: Items per page (default: 100, maximum: 1000)

### Date Filtering
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format

### Output Formatting
- `format`: Response format (json, csv, excel)

### Importance Filtering
- `importance`: Event importance level (low, medium, high)

## Rate Limiting and Caching

### News Microservice
- **Rate Limit**: 100 requests per minute per client IP
- **Cache TTL**: 300 seconds for general data, 60 seconds for high-impact events

### Finance Microservice
- **Rate Limit**: 100 requests per minute per client IP
- **Cache TTL**: 300 seconds (5 minutes) for all endpoints

## Error Codes

### Common HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid parameters)
- **401**: Unauthorized (invalid API key)
- **404**: Not Found (resource doesn't exist)
- **429**: Too Many Requests (rate limit exceeded)
- **500**: Internal Server Error
- **503**: Service Unavailable

### Custom Error Scenarios
- Invalid country codes return standardized error messages
- Missing required parameters return validation errors
- Malformed date formats return parsing errors
- Rate limit exceeded returns retry-after headers

## Authentication

Both microservices support optional Bearer token authentication:

```
Authorization: Bearer your-api-key-here
```

Include this header in all requests when authentication is enabled.

## Best Practices

1. **Pagination**: Always use pagination for large datasets
2. **Caching**: Leverage built-in caching by using consistent parameters
3. **Error Handling**: Implement proper error handling for all HTTP status codes
4. **Rate Limiting**: Implement client-side rate limiting to stay within limits
5. **Data Validation**: Validate all input parameters before making requests
6. **Connection Management**: Reuse HTTP connections when possible
7. **Timeouts**: Set appropriate timeout values for your use case