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


HOSTILE = '<hostile-tag a="1">&bare & </para><b>'


def _paragraph_texts(flowables):
    """Every Paragraph's source markup, including those inside table cells."""
    from reportlab.platypus import Paragraph, Table
    for f in flowables:
        if isinstance(f, Paragraph):
            yield f.text
        elif isinstance(f, Table):
            for row in f._cellvalues:
                yield from _paragraph_texts([c for c in row if not isinstance(c, str)])
        elif isinstance(f, (list, tuple)):
            yield from _paragraph_texts(f)


@unittest.skipIf(kit is None, 'reportlab not installed')
class SprintKitMarkupSafety(unittest.TestCase):
    """KEV text is external data and ReportLab Paragraphs parse XML-like markup: it must be escaped on the way in."""

    def entries(self):
        base = {'cveID': 'CVE-2026-0001' + HOSTILE, 'vendor': HOSTILE, 'product': HOSTILE, 'name': HOSTILE,
                'description': HOSTILE, 'requiredAction': HOSTILE, 'dueDate': '2026-11-03',
                'dateAdded': '2026-10-13', 'ransomware': 'Known', 'cwes': ['CWE-79' + HOSTILE], 'cvss': 9.8,
                'epss': 0.5, 'epss_percentile': 0.9, 'pps': 90,
                'notes': 'https://example.com/advisory?a=1&b=2 ; https://vendor.example/' + HOSTILE}
        return [dict(base), dict(base, cveID='CVE-2026-0002' + HOSTILE, cvss=7.5)]

    def test_no_raw_hostile_markup_reaches_any_paragraph(self):
        styles, entries = kit.get_styles(), self.entries()
        from datetime import datetime
        start, end = datetime(2026, 9, 9), datetime(2026, 10, 13)
        builds = {
            'cover': lambda: kit.build_cover_page(entries, 'October 2026', start, end, styles),
            'triage': lambda: kit.build_triage_matrix(entries, styles),
            'trend': lambda: kit.build_trend_page(entries, 2026, 10, styles),
            'details': lambda: kit.build_cve_detail_pages(entries, styles),
            'calendar': lambda: kit.build_sprint_calendar(end, entries, styles),
            'checklist': lambda: kit.build_testing_checklist(entries, styles),
            'sla': lambda: kit.build_sla_tracker(entries, styles),
            'summary': lambda: kit.build_executive_summary(entries, 'October 2026', start, end, styles),
            'workbook': lambda: kit.build_workbook(entries, styles),
        }
        for name, build in builds.items():
            for text in _paragraph_texts(build()):
                self.assertNotIn('<hostile', text, f'{name}: unescaped external text in {text[:120]!r}')


if __name__ == '__main__':
    unittest.main()
