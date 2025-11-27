# ArchCost Observability Guide

This document explains how to monitor and observe the ArchCost application in different environments.

## Current Implementation

### 1. **Structured Logging** (Implemented)
- **Format**: JSON structured logs for easy parsing
- **Fields**: timestamp, level, logger, message, module, function, line
- **Location**: All logs are sent to stdout

### 2. **Health Checks** (Implemented)
- **Endpoint**: `GET /health`
- **Docker**: Health checks configured for all services in `docker-compose.yml`
- **Response**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2025-11-25T17:00:00Z",
    "version": "0.1.0"
  }
  ```

### 3. **Service Dependencies**
- Backend → MongoDB, Redis
- Frontend → Backend

---

## Cloud-Native Observability

### AWS Deployment

#### **CloudWatch Logs**
No code changes needed! AWS container services automatically capture stdout logs.

**Setup:**
1. Deploy to ECS/EKS/App Runner
2. Enable CloudWatch Logs in task definition
3. JSON logs are automatically parsed and searchable

**Log Insights Queries:**
```
fields @timestamp, level, message, module
| filter level = "ERROR"
| sort @timestamp desc
| limit 20
```

#### **AWS X-Ray** (Optional - Distributed Tracing)
Add to `requirements.txt`:
```
aws-xray-sdk
```

Add to `main.py`:
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_recorder.configure(service='ArchCost')
XRayMiddleware(app, xray_recorder)
```

#### **CloudWatch Metrics**
Use CloudWatch agent or ECS/EKS built-in metrics for:
- CPU/Memory usage
- Request count
- Error rates

---

### Azure Deployment

#### **Azure Monitor**
Automatically ingests container stdout logs.

**Setup:**
1. Deploy to Azure Container Apps/AKS
2. Enable Application Insights integration
3. JSON logs are parsed automatically

**Kusto Queries:**
```kusto
traces
| where severityLevel >= 3  // Errors and above
| project timestamp, message, customDimensions
| order by timestamp desc
```

#### **Application Insights** (Optional - APM)
Add to `requirements.txt`:
```
opencensus-ext-azure
opencensus-ext-fastapi
```

Add to `main.py`:
```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.fastapi import FastAPIMiddleware

# Add instrumentation
FastAPIMiddleware(app)
logger.addHandler(AzureLogHandler(connection_string="<YOUR_CONN_STRING>"))
```

---

### GCP Deployment

#### **Cloud Logging**
Automatically captures stdout from Cloud Run/GKE.

**Setup:**
1. Deploy to Cloud Run/GKE
2. JSON logs are automatically structured
3. View in Cloud Logging console

**Log Filters:**
```
severity >= WARNING
jsonPayload.module = "pricing_fetcher"
```

#### **Cloud Trace** (Optional - Distributed Tracing)
Add to `requirements.txt`:
```
google-cloud-trace
opentelemetry-exporter-gcp-trace
```

---

## Local Development Monitoring (Optional)

### Prometheus + Grafana

Uncomment in `docker-compose.yml`:
```yaml
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
```

Create `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
```

**Access:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

---

## Recommended Metrics to Monitor

### Application Metrics
- Request count and latency (`/estimate` endpoint)
- Currency rate fetch success/failure
- Cloud pricing data age
- Database connection pool status

### Infrastructure Metrics
- Container CPU/Memory usage
- HTTP response codes (2xx, 4xx, 5xx)
- Request queue depth
- Database query performance

### Business Metrics
- Number of estimates calculated
- Popular architectures selected
- Average traffic patterns input

---

## Alerting Recommendations

1. **Critical Alerts**
   - Health check failures (3+ consecutive)
   - Error rate > 5%
   - Database connection failures

2. **Warning Alerts**
   - Currency rate fetch failures
   - Response time > 2s (p95)
   - Memory usage > 80%

---

## Performance Monitoring

### Key Endpoints
| Endpoint | Expected Latency |
|----------|------------------|
| GET /health | < 50ms |
| GET / | < 100ms |
| POST /estimate | < 500ms |
| POST /admin/refresh-prices | < 10s |

### Optimization Tips
1. Monitor MongoDB query performance
2. Cache frequently requested estimates
3. Use CDN for frontend static assets
4. Enable HTTP/2 for API calls

---

## Cost Optimization

### Cloud Costs
- **Logs**: Set retention policies (7-30 days)
- **Metrics**: Use sampling for high-cardinality data
- **Traces**: Sample 10-20% of requests in production

### Log Volume Reduction
```python
# In production, reduce log level
logging.root.setLevel(logging.WARNING)  # Only warnings and errors
```

---

## Troubleshooting

### High Memory Usage
Check logs for:
```
fields @timestamp, message
| filter message like /memory/
```

### Slow Requests
Query p99 latency:
```
fields @timestamp, duration
| stats avg(duration), percentile(duration, 99)
```

### Database Issues
```
fields @timestamp, message
| filter logger = "database"
| filter level = "ERROR"
```
