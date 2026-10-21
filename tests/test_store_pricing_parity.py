"""Guards the multi-planner bundle and per-product format tables: the worker (source of truth)
and store.js must agree, and each bundle must really save at least the 25% its badge claims."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKER = 'store/cloudflare-worker.js'
STORE = 'store/store.js'


def _block(path, name):
    src = (ROOT / path).read_text()
    return re.search(r'const ' + name + r' = \{(.*?)\n\};', src, re.S).group(1)


def _bundles(path, scale):
    out = {}
    for pid, items, single in re.findall(
            r"'([\w-]+)': \{ items: \[([^\]]*)\], single: ([\d.]+) \}", _block(path, 'PRODUCT_BUNDLE_PRICING')):
        out[pid] = {'items': re.findall(r"'([\w-]+)'", items), 'single': round(float(single) * scale)}
    return out


def _formats(path):
    return {pid: re.findall(r"'(\w+)'", fmts)
            for pid, fmts in re.findall(r"'([\w-]+)':\s+\[([^\]]*)\]", _block(path, 'PRODUCT_FORMATS'))}


class StorePricingParity(unittest.TestCase):
    def test_bundle_tables_agree(self):
        worker = _bundles(WORKER, 1)
        self.assertTrue(worker)
        self.assertEqual(worker, _bundles(STORE, 100))

    def test_format_tables_agree(self):
        worker = _formats(WORKER)
        self.assertTrue(worker)
        self.assertEqual(worker, _formats(STORE))

    def test_bundles_save_at_least_25_percent(self):
        standard = int(re.search(r'standard:\s+(\d+)', _block(WORKER, 'PRICING')).group(1))
        for pid, b in _bundles(WORKER, 1).items():
            self.assertLessEqual(b['single'], len(b['items']) * standard * 0.75, pid)

    def test_bundle_formats_exist_for_every_component(self):
        formats = _formats(WORKER)
        for pid, b in _bundles(WORKER, 1).items():
            for item in b['items']:
                self.assertTrue(set(formats[pid]) <= set(formats.get(item, formats[pid])), (pid, item))

    def test_badge_matches_claim(self):
        self.assertRegex((ROOT / STORE).read_text(),
                         r"id: 'lifestyle-bundle'.*meta: '3 planners · Save 25%'")


if __name__ == '__main__':
    unittest.main()
