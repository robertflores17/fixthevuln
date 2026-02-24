#!/usr/bin/env python3
"""
Generate monthly Patch Tuesday Sprint Kit PDF.

Pulls CISA KEV CVEs for the current Patch Tuesday cycle, enriches with
EPSS scores, and generates a professional multi-page intelligence PDF containing:
  1. Cover page with severity breakdown, EPSS high-risk callout
  2. Triage Matrix (pre-filled with CVE data)
  3. Month-over-Month Trend (comparison with previous cycle)
  4. CVE Remediation Details (descriptions, CWE, EPSS, advisory links)
  5. 14-Day Sprint Calendar (data-driven tasks, due date callouts)
  6. Testing & Rollback Checklist (pre-filled vendors/products)
  7. SLA Compliance Tracker (pre-filled severity counts & deadlines)
  8. Executive Summary (CWE analysis, risk highlights, EPSS distribution)

Usage:
  python scripts/generate_sprint_kit.py                    # current month
  python scripts/generate_sprint_kit.py --month 2026-03    # specific month
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from calendar import monthrange

# ── ReportLab imports ────────────────────────────────
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable, Flowable
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import HorizontalBarChart

# ── AcroForm Flowable Subclasses ─────────────────────
# These allow interactive PDF form fields inside Platypus Table cells.

class AcroTextField(Flowable):
    """Interactive text field that drops into Table cells."""

    def __init__(self, name, width=60, height=14, multiline=False,
                 fontsize=8, maxlen=0):
        super().__init__()
        self.field_name = name
        self.width = width
        self.height = height
        self.multiline = multiline
        self.fontsize = fontsize
        self.maxlen = maxlen

    def wrap(self, availWidth, availHeight):
        return (self.width, self.height)

    def draw(self):
        self.canv.acroForm.textfield(
            name=self.field_name,
            x=0, y=0,
            width=self.width,
            height=self.height,
            fontSize=self.fontsize,
            fontName='Helvetica',
            borderWidth=0.5,
            borderColor=HexColor('#cbd5e1'),
            fillColor=HexColor('#f8fafc'),
            textColor=HexColor('#1e293b'),
            fieldFlags='multiline' if self.multiline else '',
            maxlen=self.maxlen,
            forceBorder=True,
            annotationFlags='print',
            relative=True,
        )


class AcroCheckbox(Flowable):
    """Interactive checkbox that drops into Table cells."""

    def __init__(self, name, size=12):
        super().__init__()
        self.field_name = name
        self.size = size

    def wrap(self, availWidth, availHeight):
        return (self.size, self.size)

    def draw(self):
        self.canv.acroForm.checkbox(
            name=self.field_name,
            x=0, y=0,
            size=self.size,
            borderWidth=0.5,
            borderColor=HexColor('#cbd5e1'),
            fillColor=HexColor('#f8fafc'),
            buttonStyle='check',
            fieldFlags='',
            forceBorder=True,
            annotationFlags='print',
            relative=True,
        )


class ChartFlowable(Flowable):
    """Wraps a ReportLab Drawing for use in Platypus layouts."""

    def __init__(self, drawing):
        super().__init__()
        self.drawing = drawing

    def wrap(self, availWidth, availHeight):
        return self.drawing.width, self.drawing.height

    def draw(self):
        self.drawing.drawOn(self.canv, 0, 0)


# ── Configuration ────────────────────────────────────
DATA_DIR = Path(__file__).parent.parent / "data"
KEV_FILE = DATA_DIR / "kev.json"
OUTPUT_DIR = DATA_DIR / "sprint-kits"
MANIFEST_FILE = DATA_DIR / "sprint-kit-manifest.json"

EPSS_API_URL = "https://api.first.org/data/v1/epss"
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = os.environ.get('NVD_API_KEY', '')
NVD_DELAY = 0.6 if NVD_API_KEY else 6.0

# ── Colors ───────────────────────────────────────────
BRAND_GREEN = HexColor('#10b981')
BRAND_TEAL = HexColor('#06b6d4')
DARK_BG = HexColor('#0f172a')
DARK_CARD = HexColor('#1e293b')
HEADER_BG = HexColor('#10b981')
ROW_ALT = HexColor('#f0fdf4')
ROW_WHITE = HexColor('#ffffff')
TEXT_DARK = HexColor('#1e293b')
TEXT_MED = HexColor('#475569')
TEXT_LIGHT = HexColor('#94a3b8')
CRITICAL_RED = HexColor('#dc2626')
HIGH_ORANGE = HexColor('#ea580c')
MEDIUM_YELLOW = HexColor('#ca8a04')
LOW_BLUE = HexColor('#2563eb')
BORDER_GRAY = HexColor('#e2e8f0')

# ── CWE Name Mapping (top ~30 common CWEs) ─────────
CWE_NAMES = {
    'CWE-20': 'Improper Input Validation',
    'CWE-22': 'Path Traversal',
    'CWE-77': 'Command Injection',
    'CWE-78': 'OS Command Injection',
    'CWE-79': 'Cross-site Scripting (XSS)',
    'CWE-89': 'SQL Injection',
    'CWE-94': 'Code Injection',
    'CWE-119': 'Buffer Overflow',
    'CWE-120': 'Classic Buffer Overflow',
    'CWE-122': 'Heap-based Buffer Overflow',
    'CWE-125': 'Out-of-bounds Read',
    'CWE-190': 'Integer Overflow',
    'CWE-200': 'Information Exposure',
    'CWE-269': 'Improper Privilege Management',
    'CWE-284': 'Improper Access Control',
    'CWE-287': 'Improper Authentication',
    'CWE-306': 'Missing Authentication',
    'CWE-352': 'Cross-Site Request Forgery (CSRF)',
    'CWE-416': 'Use After Free',
    'CWE-434': 'Unrestricted File Upload',
    'CWE-476': 'NULL Pointer Dereference',
    'CWE-502': 'Deserialization of Untrusted Data',
    'CWE-601': 'Open Redirect',
    'CWE-611': 'XML External Entity (XXE)',
    'CWE-668': 'Exposure of Resource to Wrong Sphere',
    'CWE-693': 'Protection Mechanism Failure',
    'CWE-787': 'Out-of-bounds Write',
    'CWE-798': 'Use of Hard-coded Credentials',
    'CWE-862': 'Missing Authorization',
    'CWE-863': 'Incorrect Authorization',
    'CWE-918': 'Server-Side Request Forgery (SSRF)',
}

# ── URL label patterns for advisory links ───────────
URL_LABELS = [
    ('nvd.nist.gov', 'NVD Detail'),
    ('microsoft.com', 'Microsoft Advisory'),
    ('dell.com', 'Dell Support'),
    ('gitlab.com', 'GitLab Advisory'),
    ('github.com', 'GitHub Advisory'),
    ('roundcube.net', 'Roundcube Advisory'),
    ('oracle.com', 'Oracle Advisory'),
    ('apache.org', 'Apache Advisory'),
    ('mozilla.org', 'Mozilla Advisory'),
    ('cisco.com', 'Cisco Advisory'),
    ('adobe.com', 'Adobe Advisory'),
    ('google.com', 'Google Advisory'),
    ('beyondtrust.com', 'BeyondTrust Advisory'),
    ('synacor.com', 'Synacor Advisory'),
    ('zimbra.com', 'Zimbra Advisory'),
]

# ── EPSS interpretation tiers ───────────────────────
EPSS_TIERS = [
    (0.95, 'Top 5%', CRITICAL_RED),
    (0.80, 'Top 20%', HIGH_ORANGE),
    (0.50, 'Above Median', MEDIUM_YELLOW),
    (0.0, 'Below Median', LOW_BLUE),
]


# ══════════════════════════════════════════════════════
# Helper functions
# ══════════════════════════════════════════════════════

def parse_notes(notes_str):
    """Parse semicolon-separated URL string into labeled advisory links."""
    if not notes_str:
        return []
    links = []
    for raw_url in notes_str.split(';'):
        url = raw_url.strip()
        if not url:
            continue
        label = 'Reference'
        for pattern, name in URL_LABELS:
            if pattern in url:
                label = name
                break
        links.append({'label': label, 'url': url})
    return links


def epss_interpretation(percentile):
    """Return (tier_label, color) for an EPSS percentile (0-1)."""
    for threshold, label, color in EPSS_TIERS:
        if percentile >= threshold:
            return label, color
    return 'Below Median', LOW_BLUE


def calculate_pps(entry):
    """Compute Patch Priority Score (0-100) from CVSS, EPSS percentile, and ransomware signal."""
    cvss = entry.get('cvss', 0) or 0
    epss_pctl = entry.get('epss_percentile', 0) or 0
    rw = 100 if entry.get('ransomware') == 'Known' else 0

    cvss_norm = (cvss / 10.0) * 100
    epss_scaled = epss_pctl * 100

    pps = (cvss_norm * 0.40) + (epss_scaled * 0.45) + (rw * 0.15)
    return int(round(min(pps, 100)))


def pps_label(score):
    """Return (label, color_hex) for a PPS score."""
    if score >= 80:
        return ('CRITICAL', '#dc2626')
    if score >= 60:
        return ('HIGH', '#ea580c')
    if score >= 40:
        return ('MODERATE', '#ca8a04')
    return ('LOW', '#2563eb')


def generate_executive_narrative(entries, sev, vendors, cwes):
    """Build a data-driven executive narrative string."""
    total = len(entries)
    vendor_count = len(vendors)
    critical = sev['critical']

    pps_scores = [e.get('pps', 0) for e in entries]
    avg_pps = sum(pps_scores) / len(pps_scores) if pps_scores else 0

    parts = []

    # Opening
    parts.append(
        f"This Patch Tuesday cycle includes {total} vulnerabilities across "
        f"{vendor_count} vendor{'s' if vendor_count != 1 else ''}, "
        f"with {critical} rated critical severity."
    )

    # EPSS paragraph
    top5_entries = [e for e in entries if e.get('epss_percentile', 0) >= 0.95]
    if top5_entries:
        top_entry = max(top5_entries, key=lambda e: e.get('pps', 0))
        parts.append(
            f"{len(top5_entries)} CVE{'s' if len(top5_entries) != 1 else ''} "
            f"rank in the EPSS Top 5% for exploitation likelihood, indicating active or "
            f"imminent exploitation. The highest-risk vulnerability is {top_entry['cveID']} "
            f"({top_entry['vendor']} {top_entry['product']}, CVSS {top_entry.get('cvss', 0):.1f}, "
            f"PPS {top_entry.get('pps', 0)}), which should be prioritized for immediate remediation."
        )

    # Ransomware paragraph
    rw_entries = [e for e in entries if e.get('ransomware') == 'Known']
    if rw_entries:
        rw_cves = ", ".join(e['cveID'] for e in rw_entries[:5])
        if len(rw_entries) > 5:
            rw_cves += f", +{len(rw_entries) - 5} more"
        parts.append(
            f"{len(rw_entries)} vulnerabilit{'ies' if len(rw_entries) != 1 else 'y'} "
            f"{'are' if len(rw_entries) != 1 else 'is'} linked to known ransomware campaigns: "
            f"{rw_cves}. These represent elevated organizational risk and should be escalated."
        )

    # CWE paragraph
    if cwes:
        top_cwe_id, top_cwe_name, top_cwe_count = cwes[0]
        parts.append(
            f"The most prevalent weakness type is {top_cwe_id} \u2014 {top_cwe_name} "
            f"({top_cwe_count} instance{'s' if top_cwe_count != 1 else ''}), suggesting a pattern "
            f"that may warrant focused vendor communication or compensating controls."
        )

    # Closing
    if avg_pps >= 60:
        risk_level = "HIGH"
    elif avg_pps >= 40:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"

    parts.append(
        f"Overall cycle risk is {risk_level} based on an average "
        f"Patch Priority Score of {avg_pps:.0f}/100."
    )

    return "\n\n".join(parts)


def get_previous_month_data(current_year, current_month):
    """Load previous month's data from manifest for trend comparison."""
    if not MANIFEST_FILE.exists():
        return None

    with open(MANIFEST_FILE) as f:
        manifest = json.load(f)

    # Calculate previous month
    if current_month == 1:
        prev_year, prev_month = current_year - 1, 12
    else:
        prev_year, prev_month = current_year, current_month - 1

    key = f"{prev_year}-{prev_month:02d}"
    return manifest.get(key)


def cwe_analysis(entries):
    """Return sorted list of (cwe_id, cwe_name, count) tuples."""
    counts = {}
    for e in entries:
        for cwe_id in e.get('cwes', []):
            counts[cwe_id] = counts.get(cwe_id, 0) + 1
    result = []
    for cwe_id, count in counts.items():
        name = CWE_NAMES.get(cwe_id, 'Other')
        result.append((cwe_id, name, count))
    result.sort(key=lambda x: x[2], reverse=True)
    return result


# ══════════════════════════════════════════════════════
# Patch Tuesday date calculations
# ══════════════════════════════════════════════════════

def get_patch_tuesday(year, month):
    """Return the 2nd Tuesday of the given month."""
    # Find first day of month
    first_day_weekday = datetime(year, month, 1).weekday()  # 0=Mon, 1=Tue
    # Days until first Tuesday
    days_to_tue = (1 - first_day_weekday) % 7
    first_tuesday = 1 + days_to_tue
    second_tuesday = first_tuesday + 7
    return datetime(year, month, second_tuesday)


def get_patch_cycle_range(year, month):
    """
    Return (start, end) date range for the Patch Tuesday cycle.
    Cycle runs from 2nd Tuesday of month N through day before 2nd Tuesday of month N+1.
    """
    start = get_patch_tuesday(year, month)

    # Next month's Patch Tuesday
    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1
    end = get_patch_tuesday(next_year, next_month) - timedelta(days=1)

    return start, end


# ══════════════════════════════════════════════════════
# Data fetching
# ══════════════════════════════════════════════════════

def load_kev_data():
    """Load the CISA KEV catalog from local file."""
    if not KEV_FILE.exists():
        print(f"Error: {KEV_FILE} not found. Run fetch_kev.py first.")
        sys.exit(1)
    with open(KEV_FILE) as f:
        return json.load(f)


def filter_kev_for_cycle(vulnerabilities, cycle_start, cycle_end):
    """Filter KEV entries to those added during the Patch Tuesday cycle."""
    filtered = []
    for vuln in vulnerabilities:
        date_added = vuln.get('dateAdded', '')
        try:
            added_dt = datetime.strptime(date_added, '%Y-%m-%d')
            if cycle_start <= added_dt <= cycle_end:
                filtered.append(vuln)
        except ValueError:
            continue
    return filtered


def fetch_epss_scores(cve_ids):
    """Batch-fetch EPSS scores from FIRST API."""
    if not cve_ids:
        return {}

    print(f"Fetching EPSS scores for {len(cve_ids)} CVEs...")
    results = {}

    # API supports batch queries via comma-separated CVE IDs
    # Process in chunks of 30 to avoid URL length limits
    chunk_size = 30
    for i in range(0, len(cve_ids), chunk_size):
        chunk = cve_ids[i:i + chunk_size]
        cve_param = ','.join(chunk)
        url = f"{EPSS_API_URL}?cve={cve_param}"

        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'FixTheVuln-SprintKit/1.0'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            for entry in data.get('data', []):
                cve_id = entry.get('cve', '')
                epss = entry.get('epss', 0)
                percentile = entry.get('percentile', 0)
                results[cve_id] = {
                    'score': float(epss),
                    'percentile': float(percentile)
                }
                print(f"  {cve_id}: EPSS {float(epss):.4f} (P{float(percentile)*100:.0f})")

        except Exception as e:
            print(f"  Warning: EPSS fetch failed for chunk: {e}")

        if i + chunk_size < len(cve_ids):
            time.sleep(1)

    # Fill missing with zeros
    for cve_id in cve_ids:
        if cve_id not in results:
            results[cve_id] = {'score': 0.0, 'percentile': 0.0}

    return results


def fetch_cvss_from_nvd(cve_id):
    """Fetch CVSS score from NVD for a single CVE (reuses fetch_kev.py logic)."""
    url = f"{NVD_API_URL}?cveId={cve_id}"
    headers = {'User-Agent': 'FixTheVuln-SprintKit/1.0'}
    if NVD_API_KEY:
        headers['apiKey'] = NVD_API_KEY

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

        vulns = data.get('vulnerabilities', [])
        if not vulns:
            return None

        cve_data = vulns[0].get('cve', {})
        metrics = cve_data.get('metrics', {})

        for key in ('cvssMetricV31', 'cvssMetricV30'):
            metric_list = metrics.get(key, [])
            if metric_list:
                score = metric_list[0].get('cvssData', {}).get('baseScore')
                if score is not None:
                    return float(score)

        v2_list = metrics.get('cvssMetricV2', [])
        if v2_list:
            score = v2_list[0].get('cvssData', {}).get('baseScore')
            if score is not None:
                return float(score)

        return None
    except Exception as e:
        print(f"    Warning: NVD lookup failed for {cve_id}: {e}")
        return None


def enrich_with_cvss(cve_entries, epss_data):
    """Fetch CVSS from NVD for any CVEs missing scores. Returns enriched list."""
    needs_cvss = [e for e in cve_entries if e.get('cvss') is None]
    if not needs_cvss:
        return cve_entries

    print(f"Fetching CVSS from NVD for {len(needs_cvss)} CVEs...")
    for i, entry in enumerate(needs_cvss):
        cve_id = entry['cveID']
        print(f"  [{i+1}/{len(needs_cvss)}] {cve_id}...", end=" ", flush=True)
        score = fetch_cvss_from_nvd(cve_id)
        if score is not None:
            entry['cvss'] = score
            print(f"CVSS {score}")
        else:
            entry['cvss'] = 0.0
            print("no score")

        if i < len(needs_cvss) - 1:
            time.sleep(NVD_DELAY)

    return cve_entries


def build_enriched_cve_list(kev_vulns, epss_data):
    """Build enriched CVE entries with CVSS + EPSS, sorted by risk."""
    entries = []
    for vuln in kev_vulns:
        cve_id = vuln.get('cveID', '')
        epss = epss_data.get(cve_id, {'score': 0.0, 'percentile': 0.0})

        entries.append({
            'cveID': cve_id,
            'vendor': vuln.get('vendorProject', 'Unknown'),
            'product': vuln.get('product', ''),
            'name': vuln.get('vulnerabilityName', ''),
            'description': vuln.get('shortDescription', ''),
            'dateAdded': vuln.get('dateAdded', ''),
            'dueDate': vuln.get('dueDate', ''),
            'ransomware': vuln.get('knownRansomwareCampaignUse', 'Unknown'),
            'cwes': vuln.get('cwes', []),
            'requiredAction': vuln.get('requiredAction', ''),
            'notes': vuln.get('notes', ''),
            'cvss': None,  # Will be filled by NVD
            'epss': epss['score'],
            'epss_percentile': epss['percentile'],
        })

    # Enrich with CVSS
    entries = enrich_with_cvss(entries, epss_data)

    # Compute Patch Priority Score for each entry
    for entry in entries:
        entry['pps'] = calculate_pps(entry)

    # Sort by PPS descending (single composite score drives priority)
    entries.sort(key=lambda e: e.get('pps', 0), reverse=True)

    return entries


# ══════════════════════════════════════════════════════
# PDF Generation
# ══════════════════════════════════════════════════════

def severity_label(cvss):
    """Return (label, color) for a CVSS score."""
    if cvss is None or cvss == 0:
        return ('N/A', TEXT_LIGHT)
    if cvss >= 9.0:
        return ('CRITICAL', CRITICAL_RED)
    if cvss >= 7.0:
        return ('HIGH', HIGH_ORANGE)
    if cvss >= 4.0:
        return ('MEDIUM', MEDIUM_YELLOW)
    return ('LOW', LOW_BLUE)


def severity_breakdown(entries):
    """Return dict with counts per severity tier."""
    counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'na': 0}
    for e in entries:
        cvss = e.get('cvss', 0) or 0
        if cvss >= 9.0:
            counts['critical'] += 1
        elif cvss >= 7.0:
            counts['high'] += 1
        elif cvss >= 4.0:
            counts['medium'] += 1
        elif cvss > 0:
            counts['low'] += 1
        else:
            counts['na'] += 1
    return counts


def vendor_summary(entries):
    """Return sorted list of (vendor, count) tuples."""
    counts = {}
    for e in entries:
        v = e.get('vendor', 'Unknown')
        counts[v] = counts.get(v, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)


def get_styles():
    """Build custom paragraph styles."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'KitTitle', parent=styles['Title'],
        fontSize=28, leading=34, textColor=TEXT_DARK,
        spaceAfter=6, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'KitSubtitle', parent=styles['Normal'],
        fontSize=14, leading=18, textColor=TEXT_MED,
        spaceAfter=20, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'SectionHeader', parent=styles['Heading1'],
        fontSize=18, leading=22, textColor=TEXT_DARK,
        spaceBefore=12, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'SubHeader', parent=styles['Heading2'],
        fontSize=13, leading=16, textColor=TEXT_MED,
        spaceBefore=6, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'KitBody', parent=styles['Normal'],
        fontSize=10, leading=14, textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'SmallText', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=TEXT_LIGHT
    ))
    styles.add(ParagraphStyle(
        'CellText', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        'CellTextSmall', parent=styles['Normal'],
        fontSize=7, leading=9, textColor=TEXT_MED
    ))
    styles.add(ParagraphStyle(
        'FooterText', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=TEXT_LIGHT,
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'DetailTitle', parent=styles['Normal'],
        fontSize=11, leading=14, textColor=TEXT_DARK,
        fontName='Helvetica-Bold', spaceBefore=2, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'DetailBody', parent=styles['Normal'],
        fontSize=9, leading=12, textColor=TEXT_DARK,
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'DetailSmall', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=TEXT_MED,
        spaceAfter=1
    ))
    styles.add(ParagraphStyle(
        'LinkText', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=BRAND_TEAL,
        leftIndent=12
    ))
    styles.add(ParagraphStyle(
        'RiskBullet', parent=styles['Normal'],
        fontSize=9, leading=13, textColor=TEXT_DARK,
        leftIndent=16, bulletIndent=6,
        spaceBefore=2, spaceAfter=2
    ))

    return styles


def add_footer(canvas, doc):
    """Draw footer on every page."""
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(TEXT_LIGHT)
    canvas.drawCentredString(
        letter[0] / 2, 0.4 * inch,
        f"FixTheVuln Patch Tuesday Sprint Kit  |  fixthevuln.com  |  Page {doc.page}"
    )
    canvas.restoreState()


def build_cover_page(entries, month_label, cycle_start, cycle_end, styles):
    """Build cover page flowables."""
    elements = []

    elements.append(Spacer(1, 1.2 * inch))

    # Brand badge
    badge_style = ParagraphStyle(
        'Badge', parent=styles['Normal'],
        fontSize=11, leading=14, textColor=BRAND_GREEN,
        alignment=TA_CENTER, fontName='Helvetica-Bold',
        spaceBefore=0, spaceAfter=8
    )
    elements.append(Paragraph("SECURITY OPERATIONS KIT", badge_style))

    # Title
    elements.append(Paragraph("Patch Tuesday Sprint Kit", styles['KitTitle']))
    elements.append(Paragraph(month_label, styles['KitSubtitle']))

    elements.append(Spacer(1, 0.3 * inch))

    # Stats row
    sev = severity_breakdown(entries)
    ransomware_count = sum(1 for e in entries if e.get('ransomware') == 'Known')
    pps_scores = [e.get('pps', 0) for e in entries]
    avg_pps = int(round(sum(pps_scores) / len(pps_scores))) if pps_scores else 0
    avg_pps_lbl, avg_pps_color = pps_label(avg_pps)

    stats_data = [[
        Paragraph(f'<font size="22"><b>{len(entries)}</b></font><br/><font size="9" color="#64748b">Total CVEs</font>', ParagraphStyle('s', alignment=TA_CENTER)),
        Paragraph(f'<font size="22" color="#dc2626"><b>{sev["critical"]}</b></font><br/><font size="9" color="#64748b">Critical</font>', ParagraphStyle('s', alignment=TA_CENTER)),
        Paragraph(f'<font size="22" color="#ea580c"><b>{sev["high"]}</b></font><br/><font size="9" color="#64748b">High</font>', ParagraphStyle('s', alignment=TA_CENTER)),
        Paragraph(f'<font size="22" color="#ca8a04"><b>{sev["medium"]}</b></font><br/><font size="9" color="#64748b">Medium</font>', ParagraphStyle('s', alignment=TA_CENTER)),
        Paragraph(f'<font size="22" color="#2563eb"><b>{sev["low"]}</b></font><br/><font size="9" color="#64748b">Low</font>', ParagraphStyle('s', alignment=TA_CENTER)),
        Paragraph(f'<font size="22" color="{avg_pps_color}"><b>{avg_pps}</b></font><br/><font size="9" color="#64748b">Avg PPS</font>', ParagraphStyle('s', alignment=TA_CENTER)),
    ]]

    stats_table = Table(stats_data, colWidths=[1.08 * inch] * 6)
    stats_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_GRAY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8fafc')),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        "PPS = Patch Priority Score (40% CVSS + 45% EPSS Percentile + 15% Ransomware Signal)",
        styles['SmallText']
    ))

    elements.append(Spacer(1, 0.3 * inch))

    # Cycle info
    cycle_text = f"Patch Tuesday Cycle: {cycle_start.strftime('%b %d')} \u2013 {cycle_end.strftime('%b %d, %Y')}"
    elements.append(Paragraph(cycle_text, ParagraphStyle(
        'cycle', parent=styles['KitBody'], alignment=TA_CENTER, textColor=TEXT_MED
    )))

    if ransomware_count > 0:
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(
            f'<font color="#dc2626"><b>{ransomware_count} CVE{"s" if ransomware_count != 1 else ""} linked to known ransomware campaigns</b></font>',
            ParagraphStyle('warn', alignment=TA_CENTER, fontSize=11)
        ))

    # EPSS high-risk callout
    epss_top5 = sum(1 for e in entries if e.get('epss_percentile', 0) >= 0.95)
    if epss_top5 > 0:
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(
            f'<font color="#ea580c"><b>{epss_top5} CVE{"s" if epss_top5 != 1 else ""} in EPSS Top 5% exploitation likelihood</b></font>',
            ParagraphStyle('epss_warn', alignment=TA_CENTER, fontSize=11)
        ))

    elements.append(Spacer(1, 0.5 * inch))

    # Vendor summary
    vendors = vendor_summary(entries)
    if vendors:
        elements.append(Paragraph("Vendor Summary", styles['SubHeader']))
        vendor_text = "  |  ".join(f"{v}: {c}" for v, c in vendors[:10])
        elements.append(Paragraph(vendor_text, ParagraphStyle(
            'vend', parent=styles['KitBody'], alignment=TA_CENTER, fontSize=9, textColor=TEXT_MED
        )))

    elements.append(Spacer(1, 0.8 * inch))

    # Contents
    elements.append(Paragraph("Kit Contents", styles['SubHeader']))
    contents = [
        "1. Triage Matrix \u2014 Pre-filled CVE data with CVSS & EPSS scores",
        "2. Month-over-Month Trend \u2014 Comparison with previous cycle",
        "3. CVE Remediation Details \u2014 Descriptions, CWE, EPSS context, advisory links",
        "4. 14-Day Sprint Calendar \u2014 Data-driven tasks from Patch Tuesday",
        "5. Testing & Rollback Checklist \u2014 Pre-filled vendors/products",
        "6. SLA Compliance Tracker \u2014 Pre-filled severity counts & deadlines",
        "7. Executive Summary \u2014 CWE analysis, risk highlights, EPSS distribution",
    ]
    for item in contents:
        elements.append(Paragraph(item, ParagraphStyle(
            'toc', parent=styles['KitBody'], fontSize=10, leftIndent=20, spaceBefore=3
        )))

    elements.append(PageBreak())
    return elements


def build_triage_matrix(entries, styles):
    """Page 2+: Pre-filled triage matrix table."""
    elements = []

    elements.append(Paragraph("1. Triage Matrix", styles['SectionHeader']))  # Section 1 stays as-is
    elements.append(Paragraph(
        "Pre-filled with CISA KEV vulnerabilities for this Patch Tuesday cycle. "
        "Sorted by Patch Priority Score (PPS) descending. Mark your triage decision in the Priority column.",
        styles['KitBody']
    ))
    elements.append(Spacer(1, 10))

    # Table header
    header = [
        Paragraph('<b>CVE ID</b>', styles['CellText']),
        Paragraph('<b>Vendor / Product</b>', styles['CellText']),
        Paragraph('<b>CVSS</b>', styles['CellText']),
        Paragraph('<b>EPSS</b>', styles['CellText']),
        Paragraph('<b>Due Date</b>', styles['CellText']),
        Paragraph('<b>KR</b>', styles['CellText']),
        Paragraph('<b>PPS</b>', styles['CellText']),
        Paragraph('<b>Priority</b>', styles['CellText']),
        Paragraph('<b>Owner</b>', styles['CellText']),
    ]

    col_widths = [1.05 * inch, 1.25 * inch, 0.45 * inch, 0.5 * inch, 0.7 * inch, 0.35 * inch, 0.45 * inch, 0.9 * inch, 1.05 * inch]

    rows = [header]
    for i, e in enumerate(entries):
        cvss = e.get('cvss', 0) or 0
        sev_label, sev_color = severity_label(cvss)
        epss = e.get('epss', 0) or 0
        rw = 'Yes' if e.get('ransomware') == 'Known' else ''
        pps = e.get('pps', 0)
        pps_lbl, pps_color = pps_label(pps)

        rows.append([
            Paragraph(f'<font size="7">{e["cveID"]}</font>', styles['CellText']),
            Paragraph(f'<font size="7">{e["vendor"]}<br/>{e["product"]}</font>', styles['CellTextSmall']),
            Paragraph(f'<font size="8" color="{sev_color.hexval()}">{cvss:.1f}</font>', styles['CellText']),
            Paragraph(f'<font size="7">{epss:.3f}</font>', styles['CellText']),
            Paragraph(f'<font size="7">{e.get("dueDate", "")}</font>', styles['CellText']),
            Paragraph(f'<font size="7" color="#dc2626">{rw}</font>', styles['CellText']),
            Paragraph(f'<font size="8" color="{pps_color}"><b>{pps}</b></font>', styles['CellText']),
            AcroTextField(name=f'triage_priority_{i}', width=56, height=14),
            AcroTextField(name=f'triage_owner_{i}', width=66, height=14),
        ])

    table = Table(rows, colWidths=col_widths, repeatRows=1)

    # Alternate row colors
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
        # Extra padding for form field rows
        ('BOTTOMPADDING', (7, 1), (8, -1), 8),
    ]

    for i in range(1, len(rows)):
        bg = ROW_ALT if i % 2 == 0 else ROW_WHITE
        table_style.append(('BACKGROUND', (0, i), (-1, i), bg))

    # Add legend as final row spanning all columns so it never splits to a separate page
    legend_text = "KR = Known Ransomware  |  EPSS = Exploit Prediction Scoring (0\u20131)  |  PPS = Patch Priority Score \u2014 40% CVSS + 45% EPSS + 15% Ransomware (0\u2013100)"
    legend_row = [Paragraph(f'<font size="7" color="#94a3b8">{legend_text}</font>', styles['CellText'])] + [''] * 8
    rows.append(legend_row)
    table_style.append(('SPAN', (0, len(rows) - 1), (-1, len(rows) - 1)))
    table_style.append(('BACKGROUND', (0, len(rows) - 1), (-1, len(rows) - 1), ROW_WHITE))
    table_style.append(('TOPPADDING', (0, len(rows) - 1), (-1, len(rows) - 1), 6))
    table_style.append(('BOTTOMPADDING', (0, len(rows) - 1), (-1, len(rows) - 1), 4))

    table.setStyle(TableStyle(table_style))
    elements.append(table)

    elements.append(PageBreak())
    return elements


def build_cve_detail_pages(entries, styles):
    """Pages: Detailed CVE remediation guidance (~3 per page)."""
    elements = []

    elements.append(Paragraph("3. CVE Remediation Details", styles['SectionHeader']))
    elements.append(Paragraph(
        "Detailed guidance for each vulnerability in this cycle. Includes weakness type, "
        "exploitation likelihood, vendor advisories, and required actions.",
        styles['KitBody']
    ))
    elements.append(Spacer(1, 8))

    for idx, e in enumerate(entries):
        cvss = e.get('cvss', 0) or 0
        sev_label_str, sev_color = severity_label(cvss)
        epss_pct = e.get('epss_percentile', 0)
        tier_label, tier_color = epss_interpretation(epss_pct)

        # ── Severity + CVE ID + CVSS header row ──
        header_text = (
            f'<font color="{sev_color.hexval()}">[{sev_label_str}]</font> '
            f'<b>{e["cveID"]}</b>'
            f'<font size="9" color="#475569">  &mdash;  CVSS {cvss:.1f}</font>'
        )
        elements.append(Paragraph(header_text, styles['DetailTitle']))

        # ── Vulnerability name ──
        name = e.get('name', '')
        if name:
            elements.append(Paragraph(
                f'<i>{name}</i>', styles['DetailSmall']
            ))

        # ── Description ──
        desc = e.get('description', '')
        if desc:
            # Truncate very long descriptions
            if len(desc) > 300:
                desc = desc[:297] + '...'
            elements.append(Paragraph(desc, styles['DetailBody']))

        # ── Metadata line: CWE + EPSS + Due Date ──
        meta_parts = []

        cwes = e.get('cwes', [])
        if cwes:
            cwe_strs = []
            for cwe_id in cwes:
                cwe_name = CWE_NAMES.get(cwe_id, '')
                cwe_strs.append(f'{cwe_id} ({cwe_name})' if cwe_name else cwe_id)
            meta_parts.append(f'<b>Weakness:</b> {", ".join(cwe_strs)}')

        epss_score = e.get('epss', 0) or 0
        if epss_score > 0:
            meta_parts.append(
                f'<b>EPSS:</b> {epss_score:.4f} &mdash; '
                f'<font color="{tier_color.hexval()}">{tier_label} most likely exploited</font>'
            )

        due = e.get('dueDate', '')
        rw = e.get('ransomware', 'Unknown')
        if due:
            meta_parts.append(f'<b>Due Date:</b> {due}  |  <b>Ransomware:</b> {rw}')

        for part in meta_parts:
            elements.append(Paragraph(part, styles['DetailSmall']))

        # ── Required action ──
        action = e.get('requiredAction', '')
        if action:
            elements.append(Paragraph(
                f'<b>Required Action:</b> {action}', styles['DetailSmall']
            ))

        # ── Vendor advisories from notes ──
        links = parse_notes(e.get('notes', ''))
        if links:
            elements.append(Paragraph('<b>Vendor Advisories:</b>', styles['DetailSmall']))
            for link in links:
                # Truncate long URLs for display
                display_url = link['url']
                if len(display_url) > 70:
                    display_url = display_url[:67] + '...'
                elements.append(Paragraph(
                    f'&bull; {link["label"]}: {display_url}',
                    styles['LinkText']
                ))

        # Separator between CVEs
        elements.append(Spacer(1, 4))
        elements.append(HRFlowable(
            width="100%", thickness=0.5, color=BORDER_GRAY,
            spaceBefore=2, spaceAfter=6
        ))

        # Page break every 3 CVEs (but not after the last one)
        if (idx + 1) % 3 == 0 and idx < len(entries) - 1:
            elements.append(PageBreak())

    elements.append(PageBreak())
    return elements


def build_trend_page(entries, year, month, styles):
    """Page: Month-over-month trend comparison."""
    elements = []

    elements.append(Paragraph("2. Month-over-Month Trend", styles['SectionHeader']))

    prev_data = get_previous_month_data(year, month)

    if not prev_data:
        elements.append(Paragraph(
            "First report &mdash; trend data will be available starting next month "
            "when a comparison baseline exists.",
            styles['KitBody']
        ))
        elements.append(Spacer(1, 20))

        # Still show current month stats as a baseline table
        elements.append(Paragraph("Current Month Baseline", styles['SubHeader']))
        sev = severity_breakdown(entries)
        vendors = vendor_summary(entries)
        ransomware_count = sum(1 for e in entries if e.get('ransomware') == 'Known')

        baseline_rows = [
            [Paragraph('<b>Metric</b>', styles['CellText']),
             Paragraph('<b>Value</b>', styles['CellText'])],
            [Paragraph('Total CVEs', styles['CellText']),
             Paragraph(str(len(entries)), styles['CellText'])],
            [Paragraph('Critical', styles['CellText']),
             Paragraph(str(sev['critical']), styles['CellText'])],
            [Paragraph('High', styles['CellText']),
             Paragraph(str(sev['high']), styles['CellText'])],
            [Paragraph('Medium', styles['CellText']),
             Paragraph(str(sev['medium']), styles['CellText'])],
            [Paragraph('Low', styles['CellText']),
             Paragraph(str(sev['low']), styles['CellText'])],
            [Paragraph('Ransomware-Linked', styles['CellText']),
             Paragraph(str(ransomware_count), styles['CellText'])],
            [Paragraph('Unique Vendors', styles['CellText']),
             Paragraph(str(len(vendors)), styles['CellText'])],
        ]

        baseline_table = Table(baseline_rows, colWidths=[3.0 * inch, 3.5 * inch])
        baseline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
            ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(baseline_table)

    else:
        elements.append(Paragraph(
            "Comparison with previous Patch Tuesday cycle. Delta shows change from last month.",
            styles['KitBody']
        ))
        elements.append(Spacer(1, 10))

        sev = severity_breakdown(entries)
        vendors = vendor_summary(entries)
        ransomware_count = sum(1 for e in entries if e.get('ransomware') == 'Known')
        prev_sev = prev_data.get('severity', {})

        def delta_str(current, previous):
            diff = current - previous
            if diff > 0:
                return f'+{diff}'
            elif diff < 0:
                return str(diff)
            return '0'

        def delta_pct(current, previous):
            if previous == 0:
                return 'NEW' if current > 0 else '—'
            pct = ((current - previous) / previous) * 100
            if pct > 0:
                return f'+{pct:.0f}%'
            elif pct < 0:
                return f'{pct:.0f}%'
            return '0%'

        metrics = [
            ('Total CVEs', len(entries), prev_data.get('total_cves', 0)),
            ('Critical', sev['critical'], prev_sev.get('critical', 0)),
            ('High', sev['high'], prev_sev.get('high', 0)),
            ('Medium', sev['medium'], prev_sev.get('medium', 0)),
            ('Low', sev['low'], prev_sev.get('low', 0)),
            ('Ransomware-Linked', ransomware_count, prev_data.get('ransomware_linked', 0)),
            ('Unique Vendors', len(vendors), len(prev_data.get('top_vendors', []))),
        ]

        header = [
            Paragraph('<b>Metric</b>', styles['CellText']),
            Paragraph('<b>This Month</b>', styles['CellText']),
            Paragraph('<b>Last Month</b>', styles['CellText']),
            Paragraph('<b>Delta</b>', styles['CellText']),
            Paragraph('<b>% Change</b>', styles['CellText']),
        ]

        trend_rows = [header]
        for label, current, previous in metrics:
            d = delta_str(current, previous)
            d_color = '#dc2626' if current > previous else '#10b981' if current < previous else '#475569'
            trend_rows.append([
                Paragraph(f'<font size="9"><b>{label}</b></font>', styles['CellText']),
                Paragraph(f'<font size="9">{current}</font>', styles['CellText']),
                Paragraph(f'<font size="9">{previous}</font>', styles['CellText']),
                Paragraph(f'<font size="9" color="{d_color}">{d}</font>', styles['CellText']),
                Paragraph(f'<font size="9" color="{d_color}">{delta_pct(current, previous)}</font>', styles['CellText']),
            ])

        trend_table = Table(trend_rows, colWidths=[1.6 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch])
        trend_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
            ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(trend_table)

        # New/recurring vendor analysis
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Vendor Analysis", styles['SubHeader']))

        prev_vendor_names = {v['vendor'] for v in prev_data.get('top_vendors', [])}
        current_vendor_names = {v for v, _ in vendors}
        new_vendors = current_vendor_names - prev_vendor_names
        recurring = current_vendor_names & prev_vendor_names

        if new_vendors:
            elements.append(Paragraph(
                f'<b>New vendors this cycle:</b> {", ".join(sorted(new_vendors))}',
                styles['KitBody']
            ))
        if recurring:
            elements.append(Paragraph(
                f'<b>Recurring vendors:</b> {", ".join(sorted(recurring))}',
                styles['KitBody']
            ))

    elements.append(PageBreak())
    return elements


def build_sprint_calendar(cycle_start, entries, styles):
    """Page: 14-Day Sprint Calendar dated from Patch Tuesday with data-driven tasks."""
    elements = []

    sev = severity_breakdown(entries)
    vendors = vendor_summary(entries)
    total = len(entries)

    # Build vendor deployment string
    vendor_str = ", ".join(f"{v} ({c} CVEs)" for v, c in vendors[:4])
    if len(vendors) > 4:
        vendor_str += f", +{len(vendors) - 4} more"

    # Critical CVE IDs for Wave 1
    critical_cves = [e['cveID'] for e in entries if (e.get('cvss', 0) or 0) >= 9.0]
    critical_str = ", ".join(critical_cves[:4])
    if len(critical_cves) > 4:
        critical_str += f", +{len(critical_cves) - 4} more"

    # Build due date map: which CVEs are due on which day within the 14-day sprint
    due_date_flags = {}
    for e in entries:
        try:
            due_dt = datetime.strptime(e.get('dueDate', ''), '%Y-%m-%d')
            day_offset = (due_dt - cycle_start).days + 1  # 1-indexed
            if 1 <= day_offset <= 14:
                due_date_flags.setdefault(day_offset, []).append(e['cveID'])
        except (ValueError, TypeError):
            pass

    elements.append(Paragraph("4. 14-Day Sprint Calendar", styles['SectionHeader']))
    elements.append(Paragraph(
        f"Starting from Patch Tuesday ({cycle_start.strftime('%B %d, %Y')}). "
        "Tasks are auto-populated from this cycle's CVE data.",
        styles['KitBody']
    ))
    elements.append(Spacer(1, 10))

    header = [
        Paragraph('<b>Day</b>', styles['CellText']),
        Paragraph('<b>Date</b>', styles['CellText']),
        Paragraph('<b>Phase</b>', styles['CellText']),
        Paragraph('<b>Tasks</b>', styles['CellText']),
        Paragraph('<b>Done</b>', styles['CellText']),
    ]

    col_widths = [0.45 * inch, 0.75 * inch, 0.9 * inch, 3.5 * inch, 0.9 * inch]

    phases = [
        (1, "ASSESS", f"Review {total} CVEs ({sev['critical']} Critical, {sev['high']} High) from CISA KEV"),
        (2, "ASSESS", "Complete triage matrix; assign severity priorities and owners"),
        (3, "PLAN", f"Plan deployment for {vendor_str}"),
        (4, "PLAN", "Build test cases; prepare rollback procedures per vendor"),
        (5, "TEST", "Deploy patches to test/staging environment"),
        (6, "TEST", "Validate functionality; run regression tests"),
        (7, "TEST", "Sign off on test results; document exceptions"),
        (8, "DEPLOY", f"Deploy critical patches (Wave 1): {critical_str}" if critical_cves else "Deploy critical/high patches to production (Wave 1)"),
        (9, "DEPLOY", "Monitor Wave 1; deploy high-severity patches (Wave 2)"),
        (10, "DEPLOY", "Deploy medium/low patches (Wave 3)"),
        (11, "VERIFY", "Run post-deployment vulnerability scans"),
        (12, "VERIFY", "Validate patch compliance; update CMDB"),
        (13, "REPORT", "Compile SLA metrics; draft executive summary"),
        (14, "REPORT", "Final review; distribute report to stakeholders"),
    ]

    rows = [header]
    for day_num, phase, tasks in phases:
        day_date = cycle_start + timedelta(days=day_num - 1)
        # Append due date callout if any CVEs are due on this day
        task_text = tasks
        if day_num in due_date_flags:
            due_cves = due_date_flags[day_num]
            task_text += f' <font color="#dc2626"><b>[DEADLINE: {len(due_cves)} CVE{"s" if len(due_cves) != 1 else ""} due]</b></font>'
        rows.append([
            Paragraph(f'<font size="9"><b>{day_num}</b></font>', styles['CellText']),
            Paragraph(f'<font size="8">{day_date.strftime("%b %d")}</font>', styles['CellText']),
            Paragraph(f'<font size="8"><b>{phase}</b></font>', styles['CellText']),
            Paragraph(f'<font size="8">{task_text}</font>', styles['CellText']),
            AcroCheckbox(name=f'sprint_done_{day_num}', size=12),
        ])

    table = Table(rows, colWidths=col_widths, repeatRows=1)

    phase_colors = {
        'ASSESS': HexColor('#dbeafe'),
        'PLAN': HexColor('#fef3c7'),
        'TEST': HexColor('#ede9fe'),
        'DEPLOY': HexColor('#dcfce7'),
        'VERIFY': HexColor('#fce7f3'),
        'REPORT': HexColor('#f1f5f9'),
    }

    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        # Extra padding for checkbox column
        ('BOTTOMPADDING', (4, 1), (4, -1), 7),
    ]

    for i, (day_num, phase, tasks) in enumerate(phases, 1):
        bg = phase_colors.get(phase, ROW_WHITE)
        table_style.append(('BACKGROUND', (0, i), (-1, i), bg))

    table.setStyle(TableStyle(table_style))
    elements.append(table)

    elements.append(PageBreak())
    return elements


def build_testing_checklist(entries, styles):
    """Page: Testing & Rollback Checklist pre-filled with vendor/product."""
    elements = []

    elements.append(Paragraph("5. Testing &amp; Rollback Checklist", styles['SectionHeader']))
    elements.append(Paragraph(
        "Pre-filled with vendors and products from this cycle's triage data. "
        "Check off each step as testing progresses.",
        styles['KitBody']
    ))
    elements.append(Spacer(1, 10))

    header = [
        Paragraph('<b>Vendor / Product</b>', styles['CellText']),
        Paragraph('<b>Patch ID</b>', styles['CellText']),
        Paragraph('<b>Snapshot<br/>Created</b>', styles['CellText']),
        Paragraph('<b>Test<br/>Deployed</b>', styles['CellText']),
        Paragraph('<b>Functional<br/>Test</b>', styles['CellText']),
        Paragraph('<b>Regression<br/>Test</b>', styles['CellText']),
        Paragraph('<b>Prod<br/>Deployed</b>', styles['CellText']),
        Paragraph('<b>Rollback<br/>Verified</b>', styles['CellText']),
    ]

    col_widths = [1.7 * inch, 0.9 * inch, 0.65 * inch, 0.65 * inch, 0.65 * inch, 0.65 * inch, 0.65 * inch, 0.65 * inch]

    # Deduplicate by vendor+product
    seen = set()
    check_phases = ['snapshot', 'testdeploy', 'functional', 'regression', 'proddeploy', 'rollback']
    rows = [header]
    row_idx = 0
    for e in entries:
        key = f"{e['vendor']}|{e['product']}"
        if key in seen:
            continue
        seen.add(key)

        cbs = [AcroCheckbox(name=f'test_{phase}_{row_idx}', size=11) for phase in check_phases]
        rows.append([
            Paragraph(f'<font size="8">{e["vendor"]}<br/>{e["product"]}</font>', styles['CellText']),
            Paragraph(f'<font size="7">{e["cveID"]}</font>', styles['CellTextSmall']),
            *cbs,
        ])
        row_idx += 1

    # Add a few blank rows for manual additions
    for extra_i in range(3):
        cbs = [AcroCheckbox(name=f'test_{phase}_extra_{extra_i}', size=11) for phase in check_phases]
        rows.append([
            AcroTextField(name=f'test_vendor_extra_{extra_i}', width=130, height=14),
            AcroTextField(name=f'test_patch_extra_{extra_i}', width=70, height=14),
            *cbs,
        ])

    table = Table(rows, colWidths=col_widths, repeatRows=1)

    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
        # Extra padding for form field rows
        ('BOTTOMPADDING', (2, 1), (-1, -1), 7),
    ]

    for i in range(1, len(rows)):
        bg = ROW_ALT if i % 2 == 0 else ROW_WHITE
        table_style.append(('BACKGROUND', (0, i), (-1, i), bg))

    table.setStyle(TableStyle(table_style))
    elements.append(table)

    elements.append(PageBreak())
    return elements


def build_sla_tracker(entries, styles):
    """Page: SLA Compliance Tracker with pre-filled CVE counts."""
    elements = []

    sev = severity_breakdown(entries)

    # Build earliest deadline per severity
    def earliest_deadline(min_cvss, max_cvss):
        dates = []
        for e in entries:
            cvss = e.get('cvss', 0) or 0
            if min_cvss <= cvss <= max_cvss:
                try:
                    dates.append(datetime.strptime(e.get('dueDate', ''), '%Y-%m-%d'))
                except (ValueError, TypeError):
                    pass
        return min(dates).strftime('%b %d, %Y') if dates else '—'

    elements.append(Paragraph("6. SLA Compliance Tracker", styles['SectionHeader']))
    elements.append(Paragraph(
        "Track patching SLA compliance by severity tier. Total CVEs and earliest deadlines "
        "are pre-filled from this cycle's data.",
        styles['KitBody']
    ))
    elements.append(Spacer(1, 10))

    # SLA targets reference
    elements.append(Paragraph("Standard SLA Targets (adjust to your organization)", styles['SubHeader']))

    sla_header = [
        Paragraph('<b>Severity</b>', styles['CellText']),
        Paragraph('<b>CVSS Range</b>', styles['CellText']),
        Paragraph('<b>Industry Standard</b>', styles['CellText']),
        Paragraph('<b>Your SLA Target</b>', styles['CellText']),
    ]
    sla_rows = [sla_header]
    sla_defaults = [
        ('Critical', '9.0 \u2013 10.0', '72 hours (3 days)', ''),
        ('High', '7.0 \u2013 8.9', '7 days', ''),
        ('Medium', '4.0 \u2013 6.9', '30 days', ''),
        ('Low', '0.1 \u2013 3.9', '90 days', ''),
    ]

    sla_colors = [
        CRITICAL_RED, HIGH_ORANGE, MEDIUM_YELLOW, LOW_BLUE
    ]

    sla_sev_keys = ['critical', 'high', 'medium', 'low']
    for i, (sev_name, rng, standard, target) in enumerate(sla_defaults):
        sla_rows.append([
            Paragraph(f'<font size="9" color="{sla_colors[i].hexval()}"><b>{sev_name}</b></font>', styles['CellText']),
            Paragraph(f'<font size="9">{rng}</font>', styles['CellText']),
            Paragraph(f'<font size="9">{standard}</font>', styles['CellText']),
            AcroTextField(name=f'sla_target_{sla_sev_keys[i]}', width=148, height=14),
        ])

    sla_table = Table(sla_rows, colWidths=[1.2 * inch, 1.2 * inch, 1.8 * inch, 2.3 * inch])
    sla_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Extra padding for form field column
        ('BOTTOMPADDING', (3, 1), (3, -1), 8),
    ]))
    elements.append(sla_table)

    elements.append(Spacer(1, 20))

    # Compliance tracking table — pre-filled with counts and deadlines
    elements.append(Paragraph("Compliance Tracking", styles['SubHeader']))

    track_header = [
        Paragraph('<b>Severity</b>', styles['CellText']),
        Paragraph('<b>Total<br/>CVEs</b>', styles['CellText']),
        Paragraph('<b>Earliest<br/>Deadline</b>', styles['CellText']),
        Paragraph('<b>Patched<br/>On Time</b>', styles['CellText']),
        Paragraph('<b>Patched<br/>Late</b>', styles['CellText']),
        Paragraph('<b>Not Yet<br/>Patched</b>', styles['CellText']),
        Paragraph('<b>Compliance<br/>%</b>', styles['CellText']),
    ]

    sev_data = [
        ('Critical', sev['critical'], earliest_deadline(9.0, 10.0)),
        ('High', sev['high'], earliest_deadline(7.0, 8.9)),
        ('Medium', sev['medium'], earliest_deadline(4.0, 6.9)),
        ('Low', sev['low'], earliest_deadline(0.1, 3.9)),
    ]

    track_metrics = ['ontime', 'late', 'unpatched', 'compliance']
    track_rows = [track_header]
    for sev_name, count, deadline in sev_data:
        sev_key = sev_name.lower()
        track_rows.append([
            Paragraph(f'<font size="9"><b>{sev_name}</b></font>', styles['CellText']),
            Paragraph(f'<font size="9">{count}</font>', styles['CellText']),
            Paragraph(f'<font size="8">{deadline}</font>', styles['CellText']),
            AcroTextField(name=f'sla_ontime_{sev_key}', width=55, height=14),
            AcroTextField(name=f'sla_late_{sev_key}', width=48, height=14),
            AcroTextField(name=f'sla_unpatched_{sev_key}', width=55, height=14),
            AcroTextField(name=f'sla_compliance_{sev_key}', width=62, height=14),
        ])

    # Totals row
    track_rows.append([
        Paragraph('<font size="9"><b>TOTAL</b></font>', styles['CellText']),
        Paragraph(f'<font size="9"><b>{len(entries)}</b></font>', styles['CellText']),
        Paragraph('', styles['CellText']),
        AcroTextField(name='sla_ontime_total', width=55, height=14),
        AcroTextField(name='sla_late_total', width=48, height=14),
        AcroTextField(name='sla_unpatched_total', width=55, height=14),
        AcroTextField(name='sla_compliance_total', width=62, height=14),
    ])

    track_table = Table(track_rows, colWidths=[0.9 * inch, 0.65 * inch, 0.9 * inch, 0.8 * inch, 0.7 * inch, 0.8 * inch, 0.9 * inch])
    track_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, -1), (-1, -1), HexColor('#f1f5f9')),
        ('LINEABOVE', (0, -1), (-1, -1), 1.5, TEXT_MED),
        # Extra padding for form field columns
        ('BOTTOMPADDING', (3, 1), (-1, -1), 10),
    ]))
    elements.append(track_table)

    elements.append(PageBreak())
    return elements


def build_severity_donut(sev):
    """Build a severity distribution donut chart Drawing."""
    d = Drawing(200, 200)

    # Title — positioned above label zone
    d.add(String(100, 188, 'Severity Distribution', fontSize=10,
                 fontName='Helvetica-Bold', textAnchor='middle',
                 fillColor=HexColor('#1e293b')))

    segments = []
    colors = []
    labels = []
    tier_data = [
        ('Critical', sev.get('critical', 0), HexColor('#dc2626')),
        ('High', sev.get('high', 0), HexColor('#ea580c')),
        ('Medium', sev.get('medium', 0), HexColor('#ca8a04')),
        ('Low', sev.get('low', 0), HexColor('#2563eb')),
    ]

    for label, count, color in tier_data:
        if count > 0:
            segments.append(count)
            colors.append(color)
            labels.append(f'{label}: {count}')

    if not segments:
        return d

    pie = Pie()
    pie.x = 30
    pie.y = 10
    pie.width = 130
    pie.height = 130
    pie.data = segments
    pie.labels = labels
    pie.simpleLabels = 0
    pie.innerRadiusFraction = 0.5
    pie.slices.strokeWidth = 1
    pie.slices.strokeColor = white

    for i, color in enumerate(colors):
        pie.slices[i].fillColor = color
        pie.slices[i].labelRadius = 1.35
        pie.slices[i].fontName = 'Helvetica'
        pie.slices[i].fontSize = 8

    d.add(pie)
    return d


def build_epss_bar_chart(top5, top20, above, below):
    """Build an EPSS risk distribution horizontal bar chart Drawing."""
    d = Drawing(280, 200)

    # Title
    d.add(String(140, 188, 'EPSS Risk Distribution', fontSize=10,
                 fontName='Helvetica-Bold', textAnchor='middle',
                 fillColor=HexColor('#1e293b')))

    bc = HorizontalBarChart()
    bc.x = 90
    bc.y = 15
    bc.width = 170
    bc.height = 130
    bc.data = [[top5, top20, above, below]]
    bc.categoryAxis.categoryNames = ['Top 5%', 'Top 20%', 'Above Med', 'Below Med']
    bc.categoryAxis.labels.fontName = 'Helvetica'
    bc.categoryAxis.labels.fontSize = 8
    bc.categoryAxis.labels.dx = -5
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max(top5, top20, above, below, 1) + 1
    bc.valueAxis.valueStep = max(1, (max(top5, top20, above, below, 1) + 1) // 5) or 1
    bc.valueAxis.labels.fontName = 'Helvetica'
    bc.valueAxis.labels.fontSize = 7
    bc.bars.strokeWidth = 0

    bar_colors = [HexColor('#dc2626'), HexColor('#ea580c'), HexColor('#ca8a04'), HexColor('#2563eb')]
    for i, color in enumerate(bar_colors):
        bc.bars[0, i].fillColor = color

    d.add(bc)
    return d


def build_executive_summary(entries, month_label, cycle_start, cycle_end, styles):
    """Page: Executive Summary with pre-filled metrics, CWE analysis, risk highlights, and EPSS distribution."""
    elements = []

    elements.append(Paragraph("7. Executive Summary", styles['SectionHeader']))
    elements.append(Paragraph(
        f"Patch Management Report \u2014 {month_label}",
        ParagraphStyle('esub', parent=styles['SubHeader'], alignment=TA_CENTER)
    ))
    elements.append(Spacer(1, 10))

    # Pre-filled metrics section
    sev = severity_breakdown(entries)
    vendors = vendor_summary(entries)
    ransomware_count = sum(1 for e in entries if e.get('ransomware') == 'Known')

    metrics_data = [
        ['Reporting Period', f'{cycle_start.strftime("%B %d")} \u2013 {cycle_end.strftime("%B %d, %Y")}'],
        ['Total CVEs in Scope', str(len(entries))],
        ['Critical Severity', str(sev['critical'])],
        ['High Severity', str(sev['high'])],
        ['Medium Severity', str(sev['medium'])],
        ['Low Severity', str(sev['low'])],
        ['Ransomware-Linked', str(ransomware_count)],
        ['Vendors Affected', str(len(vendors))],
        ['Top Vendor', f'{vendors[0][0]} ({vendors[0][1]} CVEs)' if vendors else 'N/A'],
    ]

    metrics_rows = []
    for label, value in metrics_data:
        metrics_rows.append([
            Paragraph(f'<font size="9"><b>{label}</b></font>', styles['CellText']),
            Paragraph(f'<font size="9">{value}</font>', styles['CellText']),
        ])

    metrics_table = Table(metrics_rows, colWidths=[2.5 * inch, 4.0 * inch])
    metrics_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f0fdf4')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(metrics_table)

    elements.append(Spacer(1, 14))

    # ── Visual Charts (side by side) ──
    epss_top5 = sum(1 for e in entries if e.get('epss_percentile', 0) >= 0.95)
    epss_top20 = sum(1 for e in entries if 0.80 <= e.get('epss_percentile', 0) < 0.95)
    epss_above_median = sum(1 for e in entries if 0.50 <= e.get('epss_percentile', 0) < 0.80)
    epss_below_median = sum(1 for e in entries if e.get('epss_percentile', 0) < 0.50)

    donut_drawing = build_severity_donut(sev)
    bar_drawing = build_epss_bar_chart(epss_top5, epss_top20, epss_above_median, epss_below_median)

    chart_row = [[ChartFlowable(donut_drawing), ChartFlowable(bar_drawing)]]
    chart_table = Table(chart_row, colWidths=[3.2 * inch, 3.8 * inch])
    chart_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(chart_table)

    elements.append(Spacer(1, 14))

    # ── CWE Analysis table ──
    cwes = cwe_analysis(entries)
    if cwes:
        elements.append(Paragraph("<b>Weakness Type Analysis (CWE)</b>", styles['KitBody']))
        elements.append(Spacer(1, 4))

        cwe_header = [
            Paragraph('<b>CWE ID</b>', styles['CellText']),
            Paragraph('<b>Weakness Type</b>', styles['CellText']),
            Paragraph('<b>Count</b>', styles['CellText']),
        ]
        cwe_rows = [cwe_header]
        for cwe_id, cwe_name, count in cwes[:5]:
            cwe_rows.append([
                Paragraph(f'<font size="8">{cwe_id}</font>', styles['CellText']),
                Paragraph(f'<font size="8">{cwe_name}</font>', styles['CellText']),
                Paragraph(f'<font size="8">{count}</font>', styles['CellText']),
            ])

        cwe_table = Table(cwe_rows, colWidths=[1.0 * inch, 3.8 * inch, 0.7 * inch])
        cwe_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
            ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(cwe_table)
        elements.append(Spacer(1, 14))

    # ── Risk Highlights (auto-generated bullets) ──
    elements.append(Paragraph("<b>Risk Highlights</b>", styles['KitBody']))
    elements.append(Spacer(1, 4))

    risk_bullets = []
    if epss_top5 > 0:
        risk_bullets.append(f'{epss_top5} CVE{"s" if epss_top5 != 1 else ""} in EPSS Top 5% (highest exploitation likelihood)')
    if epss_top20 > 0:
        risk_bullets.append(f'{epss_top20} CVE{"s" if epss_top20 != 1 else ""} in EPSS Top 20%')
    if ransomware_count > 0:
        risk_bullets.append(f'{ransomware_count} CVE{"s" if ransomware_count != 1 else ""} linked to known ransomware campaigns')
    if vendors:
        risk_bullets.append(f'Most affected vendor: {vendors[0][0]} with {vendors[0][1]} CVEs')
    if sev['critical'] > 0:
        risk_bullets.append(f'{sev["critical"]} critical-severity vulnerabilities requiring immediate attention')

    for bullet in risk_bullets:
        elements.append(Paragraph(f'\u2022 {bullet}', styles['RiskBullet']))

    elements.append(Spacer(1, 14))

    # ── EPSS Risk Distribution ──
    elements.append(Paragraph("<b>EPSS Exploitation Likelihood Distribution</b>", styles['KitBody']))
    elements.append(Spacer(1, 4))

    epss_dist_header = [
        Paragraph('<b>EPSS Tier</b>', styles['CellText']),
        Paragraph('<b>Percentile Range</b>', styles['CellText']),
        Paragraph('<b>CVEs</b>', styles['CellText']),
    ]
    epss_dist_rows = [epss_dist_header]
    epss_tiers_data = [
        ('Top 5%', '\u2265 95th', epss_top5, CRITICAL_RED),
        ('Top 20%', '80th \u2013 94th', epss_top20, HIGH_ORANGE),
        ('Above Median', '50th \u2013 79th', epss_above_median, MEDIUM_YELLOW),
        ('Below Median', '< 50th', epss_below_median, LOW_BLUE),
    ]

    for tier_name, pct_range, count, color in epss_tiers_data:
        epss_dist_rows.append([
            Paragraph(f'<font size="8" color="{color.hexval()}"><b>{tier_name}</b></font>', styles['CellText']),
            Paragraph(f'<font size="8">{pct_range}</font>', styles['CellText']),
            Paragraph(f'<font size="8">{count}</font>', styles['CellText']),
        ])

    epss_dist_table = Table(epss_dist_rows, colWidths=[1.5 * inch, 1.5 * inch, 0.7 * inch])
    epss_dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(epss_dist_table)

    elements.append(Spacer(1, 14))

    # ── Auto-Generated Executive Narrative ──
    narrative_text = generate_executive_narrative(entries, sev, vendors, cwes)

    elements.append(Paragraph('<b>Key Risks &amp; Analysis</b>', styles['KitBody']))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        '<font size="8" color="#64748b"><i>(Auto-generated from cycle data)</i></font>',
        styles['SmallText']
    ))
    elements.append(Spacer(1, 3))

    # Render each paragraph of the narrative
    narrative_style = ParagraphStyle(
        'Narrative', parent=styles['DetailBody'],
        fontSize=9, leading=13, textColor=TEXT_DARK,
        spaceBefore=2, spaceAfter=6
    )
    for para in narrative_text.split('\n\n'):
        if para.strip():
            elements.append(Paragraph(para.strip(), narrative_style))

    elements.append(Spacer(1, 8))

    # Additional Notes (fillable)
    elements.append(Paragraph('<b>Additional Notes</b>', styles['KitBody']))
    elements.append(Spacer(1, 4))
    elements.append(AcroTextField(
        name='exec_notes', width=468, height=60,
        multiline=True, fontsize=9, maxlen=0,
    ))
    elements.append(Spacer(1, 8))

    # Recommendations for Next Cycle (fillable)
    elements.append(Paragraph('<b>Recommendations for Next Cycle</b>', styles['KitBody']))
    elements.append(Spacer(1, 4))
    elements.append(AcroTextField(
        name='exec_recommendations', width=468, height=60,
        multiline=True, fontsize=9, maxlen=0,
    ))
    elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 12))

    # Signature block
    elements.append(HRFlowable(width="100%", thickness=1, color=TEXT_MED, spaceBefore=0, spaceAfter=6))

    sig_data = [[
        Paragraph('<font size="9"><b>Prepared By</b></font>', styles['CellText']),
        Paragraph('<font size="9"><b>Title</b></font>', styles['CellText']),
        Paragraph('<font size="9"><b>Date</b></font>', styles['CellText']),
        Paragraph('<font size="9"><b>Signature</b></font>', styles['CellText']),
    ], [
        AcroTextField(name='sig_prepared_by', width=105, height=18),
        AcroTextField(name='sig_title', width=105, height=18),
        AcroTextField(name='sig_date', width=85, height=18),
        AcroTextField(name='sig_signature', width=135, height=18),
    ]]

    sig_table = Table(sig_data, colWidths=[1.6 * inch, 1.6 * inch, 1.3 * inch, 2.0 * inch])
    sig_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # Extra padding for form field row
        ('BOTTOMPADDING', (0, 1), (-1, 1), 22),
    ]))
    elements.append(sig_table)

    return elements


def generate_pdf(entries, year, month, cycle_start, cycle_end):
    """Generate the complete Sprint Kit PDF."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    month_label = f"{cycle_start.strftime('%B %Y')}"
    filename = f"patch-sprint-kit-{year}-{month:02d}.pdf"
    filepath = OUTPUT_DIR / filename

    print(f"\nGenerating PDF: {filename}")

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=letter,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        title=f"Patch Tuesday Sprint Kit - {month_label}",
        author="FixTheVuln",
    )

    styles = get_styles()
    elements = []

    # Build all pages
    elements.extend(build_cover_page(entries, month_label, cycle_start, cycle_end, styles))
    elements.extend(build_triage_matrix(entries, styles))
    elements.extend(build_trend_page(entries, year, month, styles))
    elements.extend(build_cve_detail_pages(entries, styles))
    elements.extend(build_sprint_calendar(cycle_start, entries, styles))
    elements.extend(build_testing_checklist(entries, styles))
    elements.extend(build_sla_tracker(entries, styles))
    elements.extend(build_executive_summary(entries, month_label, cycle_start, cycle_end, styles))

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)

    page_count = doc.page
    print(f"PDF generated: {filepath}")
    print(f"  Pages: {page_count}")
    print(f"  CVEs: {len(entries)}")

    return filepath, filename


# ══════════════════════════════════════════════════════
# Manifest
# ══════════════════════════════════════════════════════

def update_manifest(filename, year, month, entries, cycle_start, cycle_end):
    """Update the sprint-kit-manifest.json with metadata."""
    manifest = {}
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE) as f:
            manifest = json.load(f)

    sev = severity_breakdown(entries)
    vendors = vendor_summary(entries)

    # EPSS stats
    epss_scores = [e.get('epss', 0) for e in entries if e.get('epss', 0) > 0]
    avg_epss = sum(epss_scores) / len(epss_scores) if epss_scores else 0
    epss_top5_count = sum(1 for e in entries if e.get('epss_percentile', 0) >= 0.95)

    # Top CWEs
    cwes = cwe_analysis(entries)
    top_cwes = [{'id': cid, 'name': name, 'count': cnt} for cid, name, cnt in cwes[:5]]

    key = f"{year}-{month:02d}"
    manifest[key] = {
        'filename': filename,
        'generated_at': datetime.now().isoformat(),
        'cycle_start': cycle_start.strftime('%Y-%m-%d'),
        'cycle_end': cycle_end.strftime('%Y-%m-%d'),
        'total_cves': len(entries),
        'severity': sev,
        'top_vendors': [{'vendor': v, 'count': c} for v, c in vendors[:5]],
        'unique_vendors': len(vendors),
        'ransomware_linked': sum(1 for e in entries if e.get('ransomware') == 'Known'),
        'avg_epss': round(avg_epss, 4),
        'epss_top5_count': epss_top5_count,
        'top_cwes': top_cwes,
    }

    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest updated: {MANIFEST_FILE}")


# ══════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Generate Patch Tuesday Sprint Kit PDF"
    )
    parser.add_argument(
        '--month', type=str, default=None,
        help='Target month in YYYY-MM format (default: current month)'
    )
    args = parser.parse_args()

    # Parse target month
    if args.month:
        try:
            dt = datetime.strptime(args.month, '%Y-%m')
            year, month = dt.year, dt.month
        except ValueError:
            print(f"Error: Invalid month format '{args.month}'. Use YYYY-MM.")
            sys.exit(1)
    else:
        now = datetime.now()
        year, month = now.year, now.month

    print("=" * 60)
    print(f"PATCH TUESDAY SPRINT KIT GENERATOR")
    print(f"Target: {year}-{month:02d}")
    print("=" * 60)

    # Calculate cycle dates
    cycle_start, cycle_end = get_patch_cycle_range(year, month)
    print(f"Patch Tuesday cycle: {cycle_start.strftime('%Y-%m-%d')} to {cycle_end.strftime('%Y-%m-%d')}")

    # Load KEV data
    kev_data = load_kev_data()
    all_vulns = kev_data.get('vulnerabilities', [])
    print(f"Total KEV catalog: {len(all_vulns)} CVEs")

    # Filter to cycle
    cycle_vulns = filter_kev_for_cycle(all_vulns, cycle_start, cycle_end)
    print(f"CVEs in this cycle: {len(cycle_vulns)}")

    if not cycle_vulns:
        print("\nNo CVEs found for this Patch Tuesday cycle.")
        print("This may mean:")
        print("  - The KEV data hasn't been updated yet (run fetch_kev.py)")
        print("  - No CVEs were added during this cycle period")
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write("has_cves=false\n")
        sys.exit(0)

    # Fetch EPSS scores
    cve_ids = [v['cveID'] for v in cycle_vulns]
    epss_data = fetch_epss_scores(cve_ids)

    # Build enriched, sorted CVE list
    entries = build_enriched_cve_list(cycle_vulns, epss_data)

    # Generate PDF
    filepath, filename = generate_pdf(entries, year, month, cycle_start, cycle_end)

    # Update manifest
    update_manifest(filename, year, month, entries, cycle_start, cycle_end)

    # GitHub Actions output
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"filename={filename}\n")
            f.write(f"filepath={filepath}\n")
            f.write(f"cve_count={len(entries)}\n")

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
