"""The zip manifest script must cover every file a purchase can ask the worker to zip."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import build_zip_manifest as bzm  # noqa: E402


class ZipManifestCoverage(unittest.TestCase):
    def test_every_pack_component_bundle_zip_is_listed(self):
        worker = (ROOT / 'store/cloudflare-worker.js').read_text()
        packs = re.findall(r"'([\w-]+-complete)': \{ items: \[([^\]]*)\]", bzm.block(worker, 'PRODUCT_BUNDLE_PRICING'))
        self.assertEqual(len(packs), 3)
        listed = set(bzm.expected_files())
        for pack, items in packs:
            for cert in re.findall(r"'([\w-]+)'", items):
                self.assertIn(f'{cert}_bundle.zip', listed, (pack, cert))

    def test_composite_products_have_no_file_of_their_own(self):
        listed = bzm.expected_files()
        self.assertFalse([n for n in listed if n.startswith(('lifestyle-bundle', 'comptia-complete'))])
        self.assertEqual(len(listed), len(set(listed)))


if __name__ == '__main__':
    unittest.main()
