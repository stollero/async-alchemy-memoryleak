import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  // Key configurations for spike in this section
  stages: [
    { duration: '1m', target: 2000 }, // fast ramp-up to a high point
    { duration: '10s', target: 0 }, // quick ramp-down to 0 users
  ],
};

export default function() {
  const res = http.get('http://localhost:8000/status');
  check(res, {
    'status is 200': r => r.status === 200,
  });
  sleep(1);
}
