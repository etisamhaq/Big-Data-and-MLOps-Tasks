import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Ramp up to 20 users
    { duration: '1m', target: 20 },  // Stay at 20 users
    { duration: '30s', target: 0 },  // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    errors: ['rate<0.1'],            // Error rate should be less than 10%
  },
};

const payload = JSON.stringify({
  features: [5.1, 3.5, 1.4, 0.2]
});

const params = {
  headers: {
    'Content-Type': 'application/json',
  },
};

export default function () {
  // Health check
  const healthCheck = http.get('http://localhost/health');
  check(healthCheck, {
    'health check status is 200': (r) => r.status === 200,
  });

  // Prediction request
  const predictionRes = http.post('http://localhost/predict', payload, params);
  
  check(predictionRes, {
    'status is 200': (r) => r.status === 200,
    'prediction exists': (r) => JSON.parse(r.body).hasOwnProperty('prediction'),
    'container_id exists': (r) => JSON.parse(r.body).hasOwnProperty('container_id'),
  });

  // Record errors
  errorRate.add(predictionRes.status !== 200);

  // Wait between requests
  sleep(1);
} 