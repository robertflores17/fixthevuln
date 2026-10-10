import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
from lib.templates import existing_date_published  # noqa: E402


class ExistingDatePublishedTest(unittest.TestCase):
    def test_keeps_date_from_existing_page(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'page.html'
            p.write_text('{"datePublished": "2026-02-14", "dateModified": "2026-10-10"}')
            self.assertEqual(existing_date_published(p, '2026-10-11'), '2026-02-14')

    def test_defaults_for_new_page(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(existing_date_published(Path(d) / 'missing.html', '2026-10-11'), '2026-10-11')


if __name__ == '__main__':
    unittest.main()
