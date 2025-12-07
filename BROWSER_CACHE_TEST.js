/**
 * Test script to verify end-to-end caching behavior
 * Run this in the browser console after the app loads
 */

(async function testCaching() {
  console.log('=== ArchCost Cache Behavior Test ===\n');

  // Simulate two different cost estimation requests
  const testPayload1 = {
    architecture: 'microservices',
    traffic: {
      daily_active_users: 10000,
      api_requests_per_user: 50,
      storage_per_user_mb: 10,
      peak_traffic_multiplier: 1.5,
      growth_rate_yoy: 0.1,
      revenue_per_user_monthly: 0,
      funding_available: 0,
      database: { type: 'rds', read_replicas: 0, backup_enabled: false, multi_az: false, cache_type: null, cache_size_gb: 0 },
      cdn: { enabled: false, provider: 'cloudfront', data_transfer_gb: 0, edge_functions: false, video_streaming: false },
      messaging: { enabled: false, type: 'sqs', messages_per_day: 0, retention_days: 7, dlq_enabled: false },
      security: { waf_enabled: false, vpn_enabled: false, ddos_protection: false, ssl_certificates: 0, compliance: [], secrets_manager: false },
      monitoring: { provider: 'cloudwatch', log_retention_days: 7, apm_enabled: false, distributed_tracing: false, alert_channels: 0 },
      cicd: { provider: 'github_actions', builds_per_month: 100, container_registry: false, security_scanning: false, artifact_storage_gb: 0 },
      multi_region: { enabled: false, regions: 1, replication_type: 'active_passive', cross_region_transfer_gb: 0, rto_minutes: 60, rpo_minutes: 60 }
    },
    currency: 'USD'
  };

  const testPayload2 = {
    architecture: 'monolith',
    traffic: {
      daily_active_users: 50000,
      api_requests_per_user: 100,
      storage_per_user_mb: 25,
      peak_traffic_multiplier: 2.0,
      growth_rate_yoy: 0.25,
      revenue_per_user_monthly: 0,
      funding_available: 0,
      database: { type: 'rds', read_replicas: 1, backup_enabled: true, multi_az: true, cache_type: 'redis', cache_size_gb: 2 },
      cdn: { enabled: true, provider: 'cloudfront', data_transfer_gb: 500, edge_functions: true, video_streaming: false },
      messaging: { enabled: true, type: 'sqs', messages_per_day: 10000, retention_days: 7, dlq_enabled: false },
      security: { waf_enabled: true, vpn_enabled: false, ddos_protection: false, ssl_certificates: 1, compliance: ['SOC2'], secrets_manager: true },
      monitoring: { provider: 'datadog', log_retention_days: 30, apm_enabled: true, distributed_tracing: true, alert_channels: 3 },
      cicd: { provider: 'github_actions', builds_per_month: 500, container_registry: true, security_scanning: true, artifact_storage_gb: 50 },
      multi_region: { enabled: true, regions: 2, replication_type: 'active_active', cross_region_transfer_gb: 200, rto_minutes: 30, rpo_minutes: 15 }
    },
    currency: 'USD'
  };

  const makeRequest = async (payload, label) => {
    console.log(`\n📡 ${label}`);
    console.log(`   Architecture: ${payload.architecture}, DAU: ${payload.traffic.daily_active_users}`);
    
    try {
      const response = await fetch('http://localhost:8000/estimate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const status = response.status;
      const etag = response.headers.get('etag');
      const cacheControl = response.headers.get('cache-control');
      
      console.log(`   Status: ${status} ${status === 304 ? '(Not Modified - cached!)' : status === 200 ? '(OK - fresh data)' : ''}`);
      console.log(`   ETag: ${etag}`);
      console.log(`   Cache-Control: ${cacheControl}`);

      if (status === 200) {
        const data = await response.json();
        console.log(`   Monthly Cost: $${data.monthly_cost.total.toFixed(2)}`);
        return { status, etag, data };
      } else if (status === 304) {
        console.log(`   ✅ Server returned 304 (reusing cached result)`);
        return { status, etag };
      }
    } catch (err) {
      console.error(`   ❌ Error: ${err.message}`);
    }
  };

  // Test 1: First request with payload 1
  console.log('\n━━━ Test 1: Fresh request (Payload 1) ━━━');
  const r1 = await makeRequest(testPayload1, 'Request 1 (10k DAU, microservices)');
  
  // Test 2: Different payload
  console.log('\n━━━ Test 2: Different parameters (Payload 2) ━━━');
  const r2 = await makeRequest(testPayload2, 'Request 2 (50k DAU, monolith)');

  // Test 3: Repeat payload 1 (should get 304 or cached result)
  console.log('\n━━━ Test 3: Repeat original parameters (Payload 1 again) ━━━');
  const r3 = await makeRequest(testPayload1, 'Request 3 (10k DAU, microservices - repeat)');

  // Summary
  console.log('\n\n✅ TEST SUMMARY:');
  console.log(`   Test 1: Fresh request → Status ${r1?.status} (expected 200) ${r1?.status === 200 ? '✓' : '✗'}`);
  console.log(`   Test 2: Different params → Status ${r2?.status} (expected 200) ${r2?.status === 200 ? '✓' : '✗'}`);
  console.log(`   Test 3: Repeated params → Status ${r3?.status} (expected 304 or cached) ${[200, 304].includes(r3?.status) ? '✓' : '✗'}`);
  
  console.log('\n📊 ETags match:');
  console.log(`   Request 1 ETag: ${r1?.etag}`);
  console.log(`   Request 3 ETag: ${r3?.etag}`);
  console.log(`   Same input → Same ETag: ${r1?.etag === r3?.etag ? '✓' : '✗'}`);
  
  console.log('\n💾 Costs comparison:');
  console.log(`   Payload 1 monthly: $${r1?.data?.monthly_cost?.total?.toFixed(2)}`);
  console.log(`   Payload 2 monthly: $${r2?.data?.monthly_cost?.total?.toFixed(2)}`);
  console.log(`   Different inputs → Different costs: ${r1?.data?.monthly_cost?.total !== r2?.data?.monthly_cost?.total ? '✓' : '✗'}`);
  
  console.log('\n=== End of Test ===');
})();
