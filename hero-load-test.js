import http from 'k6/http';
import { check, sleep } from 'k6';

// Keep the load small: this is a learning test on a free GitHub Pages site.
export const options = {
  vus: 3,            // 3 virtual users at the same time
  duration: '15s',   // run for 15 seconds
  thresholds: {
    http_req_failed: ['rate<0.01'],      // less than 1% of requests may fail
    http_req_duration: ['p(95)<2000'],   // 95% of requests must finish under 2 seconds
  },
};

const BASE = 'https://dola333.github.io/Hero-travel-repo/';
const PAGES = ['', 'packages.html', 'testimonial.html', 'blog.html', 'contact.html'];

export default function () {
  for (const page of PAGES) {
    const res = http.get(BASE + page);

    check(res, {
      'status is 200': (r) => r.status === 200,
      'response time under 2s': (r) => r.timings.duration < 2000,
    });

    sleep(1); // pause 1 second, like a real visitor reading the page
  }
}