import httpx
import json

payload = {
    "architecture": "monolith",
    "traffic": {
        "monthly_active_users": 100000,
        "daily_active_users": 50000,
        "requests_per_day": 500000,
        "average_response_time_ms": 200,
        "concurrent_users": 5000,
        "peak_requests_per_second": 2000,
        "cache_hit_rate": 0.7,
        "storage_per_user_mb": 1.5,
        "api_requests_per_user": 50
    },
    "currency": "USD",
    "database": {
        "type": "rds",
        "read_replicas": 0,
        "backup_enabled": False,
        "multi_az": False,
        "cache_type": None,
        "cache_size_gb": 0
    }
}

r = httpx.post('http://localhost:8000/estimate', json=payload, timeout=10)
print('Status:', r.status_code)
print('Response:', r.text[:1500])
