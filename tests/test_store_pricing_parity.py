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

    def test_price_tables_agree(self):
        wp = {k: int(v) for k, v in re.findall(r'(\w+):\s+(\d+),', _block(WORKER, 'PRICING'))}
        sp = {k: round(float(v) * 100) for k, v in re.findall(r'(\w+):\s+([\d.]+),', _block(STORE, 'PRICING'))}
        self.assertEqual(wp, sp)
        wc = {int(n): (int(a), int(b)) for n, a, b in re.findall(
            r'(\d): \{ single: (\d+),\s+bundle: (\d+) \}', _block(WORKER, 'CP_PRICING'))}
        sc = {int(n): (round(float(a) * 100), round(float(b) * 100)) for n, a, b in re.findall(
            r'(\d): \{ single: ([\d.]+),\s+bundle: ([\d.]+),', _block(STORE, 'CAREER_PATH_PRICING'))}
        self.assertEqual(wc, sc)

    def test_career_path_strikethrough_totals_use_current_prices(self):
        std = float(re.search(r'standard:\s+([\d.]+),', _block(STORE, 'PRICING')).group(1))
        bun = float(re.search(r'bundle:\s+([\d.]+),', _block(STORE, 'PRICING')).group(1))
        rows = re.findall(r'(\d): \{ single: ([\d.]+),\s+bundle: ([\d.]+), indivSingle: ([\d.]+), indivBundle: ([\d.]+)',
                          _block(STORE, 'CAREER_PATH_PRICING'))
        self.assertEqual(len(rows), 3)
        for n, single, bundle, indiv_single, indiv_bundle in rows:
            self.assertAlmostEqual(float(indiv_single), int(n) * std, 2, n)
            self.assertAlmostEqual(float(indiv_bundle), int(n) * bun, 2, n)
            self.assertLess(float(single), float(indiv_single), n)
            self.assertLess(float(bundle), float(indiv_bundle), n)

    def test_vendor_packs_are_bundle_only_and_priced_as_anchor(self):
        names = _block(WORKER, 'CERT_NAMES')
        bundle = int(re.search(r'bundle:\s+(\d+)', _block(WORKER, 'PRICING')).group(1))
        formats = _formats(WORKER)
        packs = {pid: b for pid, b in _bundles(WORKER, 1).items() if pid.endswith('-complete')}
        self.assertEqual(set(packs), {'comptia-complete', 'microsoft-complete', 'aws-complete'})
        for pid, b in packs.items():
            self.assertEqual(formats[pid], ['bundle'], pid)
            self.assertIn(f"'{pid}':", names, pid)
            for item in b['items']:
                self.assertIn(f"'{item}':", names, (pid, item))
            self.assertLess(b['single'], len(b['items']) * bundle, pid)
            self.assertGreater(b['single'], bundle, pid)  # still the expensive anchor tier

    def test_badge_matches_claim(self):
        self.assertRegex((ROOT / STORE).read_text(),
                         r"id: 'lifestyle-bundle'.*meta: '3 planners · Save 25%'")


if __name__ == '__main__':
    unittest.main()
