"""Sprint kit sections 8-11 (ownership, exceptions, metrics, scan mapping) build into four pages with unique form fields.
Skipped where reportlab isn't installed (it is pinned in requirements-sprint-kit.txt for the kit workflow)."""
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

try:
    import generate_sprint_kit as kit
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate
except ImportError:  # pragma: no cover
    kit = None


@unittest.skipIf(kit is None, 'reportlab not installed')
class SprintKitWorkbook(unittest.TestCase):
    def build(self, entries):
        path = Path(tempfile.mkdtemp()) / 'workbook.pdf'
        doc = SimpleDocTemplate(str(path), pagesize=letter)
        doc.build(kit.build_workbook(entries, kit.get_styles()))
        return doc.page, path.read_bytes()

    def test_four_pages_with_unique_fields(self):
        pages, pdf = self.build([{'vendor': 'Microsoft'}, {'vendor': 'Adobe'}, {'vendor': 'Microsoft'}])
        self.assertEqual(pages, 4)
        fields = re.findall(rb'/T \(([^)]*)\)', pdf)
        self.assertGreater(len(fields), 100)
        self.assertEqual(len(fields), len(set(fields)), 'AcroForm field names must be unique')

    def test_vendor_names_are_escaped_and_empty_cycle_still_builds(self):
        pages, _ = self.build([{'vendor': 'A&B <Corp>'}])
        self.assertEqual(pages, 4)
        self.assertEqual(self.build([])[0], 4)

    def test_cover_lists_all_eleven_sections(self):
        src = (ROOT / 'scripts/generate_sprint_kit.py').read_text()
        for n in range(1, 12):
            self.assertRegex(src, rf'"{n}\. \S', n)


if __name__ == '__main__':
    unittest.main()
