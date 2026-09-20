"""Pins the CVSS v2 band cap on the live CVE-page pipeline.

CVSS v2 has no Critical band; its top rating is High (7.0-10.0). This
function used to apply v3.1 bands to every score regardless of spec, so a
v2-only CVE at >=9.0 would render CRITICAL on a published CVE page -- a
rating that does not exist in that scale. The same defect was found and
fixed on the AI IDE tracker side (aggregate_ai_ide_vulns.severity_label);
this is the KEV-publish-pipeline copy, found while carrying that fix through.

Currently latent, not live: no entry in data/kev-data.json is v2-only at the
time this was fixed (all 12 pre-2016 candidates also carry a v3.1 metric).
The version now travels fetch_kev.py -> pending_review.json (`cvss_version`)
-> generate_html.py's convert_to_kev_format (`cvssVersion`) ->
generate_cve_pages.severity_label, so the next v2-only NVD entry renders
correctly without anyone touching this file again.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

from generate_cve_pages import severity_label


class TestVersionAwareSeverityLabel(unittest.TestCase):
    def test_v2_caps_at_high(self):
        self.assertEqual(severity_label(9.5, 'v2.0'), 'HIGH')
        self.assertEqual(severity_label(10.0, 'v2.0'), 'HIGH')

    def test_v2_string_variants_all_recognised(self):
        for v in ('v2', 'v2.0', '2', '2.0', 'V2.0'):
            with self.subTest(version=v):
                self.assertEqual(severity_label(9.5, v), 'HIGH')

    def test_v3_and_v4_use_critical(self):
        for v in ('v3.1', 'v3.0', 'v4.0'):
            with self.subTest(version=v):
                self.assertEqual(severity_label(9.5, v), 'CRITICAL')

    def test_missing_version_keeps_old_behaviour(self):
        """Every entry published before this field existed, and every
        hand-typed one since, has no cvssVersion. That must still band as
        v3.1 -- the function's previous, unconditional behaviour -- not
        silently degrade to UNKNOWN or v2."""
        self.assertEqual(severity_label(9.5, ''), 'CRITICAL')
        self.assertEqual(severity_label(9.5), 'CRITICAL')

    def test_lower_bands_are_shared_across_versions(self):
        for v in ('v3.1', 'v2.0'):
            with self.subTest(version=v):
                self.assertEqual(severity_label(7.5, v), 'HIGH')
                self.assertEqual(severity_label(5.0, v), 'MEDIUM')
                self.assertEqual(severity_label(0.5, v), 'LOW')

    def test_none_cvss_is_unknown_regardless_of_version(self):
        self.assertEqual(severity_label(None, 'v2.0'), 'UNKNOWN')

    def test_no_currently_published_entry_changes_label(self):
        """The whole point of this fix is that it is latent, not live: it
        must not silently re-band any of the 227 already-published CVE
        pages."""
        import json
        kev_path = Path(__file__).resolve().parent.parent / 'data' / 'kev-data.json'
        data = json.loads(kev_path.read_text(encoding='utf-8'))
        vulns = data.get('vulnerabilities', data if isinstance(data, list) else [])
        for v in vulns:
            cvss = v.get('cvss')
            if cvss is None:
                continue
            with self.subTest(cve=v.get('id')):
                self.assertEqual(severity_label(cvss),
                                 severity_label(cvss, v.get('cvssVersion', '')))


if __name__ == '__main__':
    unittest.main()
