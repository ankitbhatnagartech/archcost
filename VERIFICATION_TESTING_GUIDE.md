# Verification Checklist & Testing Guide

## ✅ Pre-Deployment Verification

### Code Verification
```bash
# Check for syntax errors (should be none)
python -m py_compile backend/main.py
python -m py_compile backend/schemas.py  
python -m py_compile backend/estimation_service.py
# All should complete without errors ✅
```

### Import Verification
```python
# Should work without errors
from fastapi.middleware.gzip import GZIPMiddleware
from pydantic import field_validator
import hashlib

# Check validators are accessible
from schemas import TrafficInput
traffic = TrafficInput(daily_active_users=1000)
# Should work fine ✅
```

---

## 🧪 Testing Guide

### Test 1: Input Validation
```bash
# Test 1a: Valid input (should succeed)
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "monolith",
    "traffic": {"daily_active_users": 1000},
    "currency": "USD"
  }'
# Expected: 200 OK with estimate

# Test 1b: DAU too high (should fail)
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "monolith",
    "traffic": {"daily_active_users": 2000000000},
    "currency": "USD"
  }'
# Expected: 422 Validation Error

# Test 1c: Negative revenue (should fail)
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "monolith",
    "traffic": {
      "daily_active_users": 1000,
      "revenue_per_user_monthly": -100
    },
    "currency": "USD"
  }'
# Expected: 422 Validation Error
```

### Test 2: Caching Headers
```bash
# Test 2a: Check ETag header
RESPONSE=$(curl -I http://localhost:8000/estimate)
echo "$RESPONSE" | grep -i "etag"
# Expected: ETag: "hash_value"

# Test 2b: Check Cache-Control header
echo "$RESPONSE" | grep -i "cache-control"
# Expected: Cache-Control: public, max-age=300, must-revalidate

# Test 2c: Check Vary header
echo "$RESPONSE" | grep -i "vary"
# Expected: Vary: Accept-Encoding, Content-Type

# Test 2d: Admin dashboard cache
curl -I http://localhost:8000/admin/dashboard \
  -H "Authorization: Bearer <JWT>"
# Expected: Cache-Control: private, max-age=60, must-revalidate
```

### Test 3: GZIP Compression
```bash
# Test 3a: Request without compression preference
curl -I http://localhost:8000/estimate
# Expected: Content-Type: application/json

# Test 3b: Request with gzip preference
curl -I -H "Accept-Encoding: gzip" http://localhost:8000/estimate
# Expected: Content-Encoding: gzip

# Test 3c: Check response size (with vs without gzip)
SIZE_UNCOMPRESSED=$(curl -s http://localhost:8000/estimate | wc -c)
SIZE_COMPRESSED=$(curl -s -H "Accept-Encoding: gzip" http://localhost:8000/estimate | wc -c)
echo "Uncompressed: $SIZE_UNCOMPRESSED bytes"
echo "Compressed: $SIZE_COMPRESSED bytes"
echo "Ratio: $(echo "scale=2; $SIZE_COMPRESSED * 100 / $SIZE_UNCOMPRESSED" | bc)%"
# Expected: Compressed ~30% of uncompressed (70% reduction)
```

### Test 4: Edge Cases
```bash
# Test 4a: Zero DAU (should be rejected by validator)
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "monolith",
    "traffic": {"daily_active_users": 0}
  }'
# Expected: 422 Validation Error

# Test 4b: Zero revenue per user (should work fine)
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "monolith",
    "traffic": {
      "daily_active_users": 1000,
      "revenue_per_user_monthly": 0
    }
  }'
# Expected: 200 OK (with profitability showing as "N/A" or skipped)

# Test 4c: Very high storage (should work)
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "monolith",
    "traffic": {
      "daily_active_users": 100,
      "storage_per_user_mb": 999999
    }
  }'
# Expected: 200 OK with large storage estimate

# Test 4d: Storage exceeds limit (should fail)
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "architecture": "monolith",
    "traffic": {
      "daily_active_users": 100,
      "storage_per_user_mb": 1000001
    }
  }'
# Expected: 422 Validation Error
```

### Test 5: MongoDB Verification
```javascript
// MongoDB commands to verify pricing update strategy

// Check 1: Verify only one pricing document
db.pricing.countDocuments({})
// Expected: 1

// Check 2: Verify pricing document has correct ID
db.pricing.findOne()
// Expected: { "_id": "latest_pricing", ... }

// Check 3: Verify history limit
db.pricing_history.countDocuments({})
// Expected: 0-2 (not unlimited)

// Check 4: Verify history has timestamps
db.pricing_history.find({}, { "archived_at": 1 }).toArray()
// Expected: Each backup has archived_at timestamp

// Check 5: Verify no duplicate pricing IDs
db.pricing.aggregate([
  { $group: { _id: "$_id", count: { $sum: 1 } } },
  { $match: { count: { $gt: 1 } } }
])
// Expected: No results (no duplicates)
```

### Test 6: Admin Dashboard
```bash
# Get admin JWT token first
TOKEN=$(curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin_password"}' \
  | jq -r '.access_token')

# Test dashboard endpoint
curl -X GET http://localhost:8000/admin/dashboard \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# Verify response structure
# Expected JSON with:
# - job_status (status, last_run, success, error, sources_fetched, etc.)
# - current_pricing (last_updated, sources, total_currencies_configured)
# - historical_backups (total_count, max_allowed, backups[])
# - scheduling (next_scheduled_run, time_until_next_run_seconds)
# - manual_trigger_endpoint
# - timestamp
```

### Test 7: Performance Baseline
```bash
# Run 10 requests to establish baseline
echo "First request (cache miss):"
time curl -s http://localhost:8000/estimate > /dev/null

echo "Second request (cache hit):"
time curl -s http://localhost:8000/estimate > /dev/null

echo "Third request (cache hit):"
time curl -s http://localhost:8000/estimate > /dev/null

# Expected:
# First: 100-300ms
# Second: 20-50ms (10x faster)
# Third: 20-50ms (cached)
```

---

## 🔍 Validation Checklist

### Functional Validation
- [ ] **Validators work:** DAU > 1B rejected
- [ ] **Storage validation:** > 1TB rejected
- [ ] **Revenue validation:** Negative values rejected
- [ ] **Caching headers:** Present in responses
- [ ] **GZIP compression:** Enabled and working
- [ ] **MongoDB replace:** No duplicates created
- [ ] **History limit:** ≤ 2 backups
- [ ] **Admin dashboard:** All fields present

### Performance Validation
- [ ] **Cache hits:** 10x faster than misses
- [ ] **Compression:** 70% size reduction
- [ ] **Database queries:** Indexes being used
- [ ] **Response time:** <100ms on cache hit

### Compatibility Validation
- [ ] **Existing clients:** Still work
- [ ] **API contracts:** Unchanged
- [ ] **Database schema:** Unchanged
- [ ] **Error messages:** Clear and helpful

---

## 🚨 Troubleshooting

### Issue: Validators not working
**Solution:** Check that `field_validator` is imported correctly
```python
from pydantic import field_validator  # ✅ Correct
from pydantic.validators import validator  # ❌ Old way
```

### Issue: GZIP not compressing
**Solution:** Check middleware order and minimum size
```python
# Middleware must be added AFTER FastAPI creation
app = FastAPI()
app.add_middleware(GZIPMiddleware, minimum_size=1000)  # ✅ Correct
```

### Issue: Caching not working
**Solution:** Verify response headers are being set
```python
from fastapi.responses import JSONResponse
response = JSONResponse(content=data)
response.headers["Cache-Control"] = "public, max-age=300"  # ✅ Must use JSONResponse
return response
```

### Issue: MongoDB backups still unlimited
**Solution:** Check that `database.py` `create_indexes()` was called
```python
# In lifespan() startup:
await Database.create_indexes()  # ✅ Must be called
# This creates TTL index for auto-cleanup
```

### Issue: Parameter order error
**Solution:** Verify EstimationService.estimate() call order
```python
# ✅ CORRECT ORDER:
EstimationService.estimate(architecture, traffic, currency)

# ❌ WRONG ORDER:
EstimationService.estimate(traffic, architecture, currency)
```

---

## 📊 Expected Results

### Before Optimization
| Metric | Value |
|--------|-------|
| Estimate response | 300-500ms |
| Response size | ~150KB |
| MongoDB storage | ~500MB+ |
| Query speed | ~100ms |
| Caching | None |
| Compression | None |

### After Optimization
| Metric | Value |
|--------|-------|
| Estimate response (hit) | 20-50ms |
| Response size (compressed) | ~45KB |
| MongoDB storage | ~50MB |
| Query speed | ~2-5ms |
| Caching | 5-60min TTL |
| Compression | 70% reduction |

---

## ✅ Sign-Off Checklist

- [ ] Code reviewed by peer
- [ ] All tests passing
- [ ] No syntax errors
- [ ] No breaking changes
- [ ] Backward compatible
- [ ] MongoDB strategy correct
- [ ] History limit enforced
- [ ] Validators working
- [ ] Caching working
- [ ] Compression working
- [ ] Admin dashboard enhanced
- [ ] Performance verified
- [ ] Documentation complete
- [ ] Ready for production

---

**Once all tests pass, the deployment is ready! ✅**
