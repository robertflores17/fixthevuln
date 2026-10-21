"""Guards the multi-planner bundle prices: the worker (source of truth) and store.js must agree,
and each bundle must really save at least the 25% its badge claims."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _table(path, scale):
    src = (ROOT / path).read_text()
    block = re.search(r'const PRODUCT_BUNDLE_PRICING = \{(.*?)\n\};', src, re.S).group(1)
    return {pid: {'planners': int(n), 'single': round(float(s) * scale), 'bundle': round(float(b) * scale)}
            for pid, n, s, b in re.findall(
                r"'([\w-]+)': \{ planners: (\d+), single: ([\d.]+), bundle: ([\d.]+) \}", block)}


def _per_planner(path, scale):
    src = (ROOT / path).read_text()
    block = re.search(r'const PRICING = \{(.*?)\};', src, re.S).group(1)
    return {k: round(float(v) * scale) for k, v in re.findall(r'(\w+):\s+([\d.]+)', block)}


class StorePricingParity(unittest.TestCase):
    def test_worker_and_store_js_agree(self):
        worker = _table('store/cloudflare-worker.js', 1)
        frontend = _table('store/store.js', 100)
        self.assertTrue(worker)
        self.assertEqual(worker, frontend)

    def test_bundles_save_at_least_25_percent(self):
        per = _per_planner('store/cloudflare-worker.js', 1)
        for pid, b in _table('store/cloudflare-worker.js', 1).items():
            self.assertLessEqual(b['single'], b['planners'] * per['standard'] * 0.75, pid)
            self.assertLessEqual(b['bundle'], b['planners'] * per['bundle'] * 0.75, pid)

    def test_badge_matches_claim(self):
        js = (ROOT / 'store/store.js').read_text()
        self.assertIn("id: 'lifestyle-bundle'", js)
        self.assertRegex(js, r"id: 'lifestyle-bundle'.*meta: '3 planners · Save 25%'")


if __name__ == '__main__':
    unittest.main()
