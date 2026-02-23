#!/usr/bin/env python3
"""
Generate monthly Patch Tuesday Sprint Kit PDF.

Pulls CISA KEV CVEs for the current Patch Tuesday cycle, enriches with
EPSS scores, and generates a professional multi-page PDF containing:
  1. Cover page with severity breakdown
  2. Triage Matrix (pre-filled with CVE data)
  3. 14-Day Sprint Calendar (dated from Patch Tuesday)
  4. Testing & Rollback Checklist (pre-filled vendors/products)
  5. SLA Compliance Tracker (blank)
  6. Executive Summary (pre-filled metrics, blank narrative)

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
from reportlab.platypus.flowables import HRFlowable

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
            'cvss': None,  # Will be filled by NVD
            'epss': epss['score'],
            'epss_percentile': epss['percentile'],
        })

    # Enrich with CVSS
    entries = enrich_with_cvss(entries, epss_data)

    # Sort: CVSS desc, then EPSS desc
    entries.sort(key=lambda e: (e.get('cvss', 0) or 0, e.get('epss', 0) or 0), reverse=True)

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

    stats_data = [[
        Paragraph(f'<font size="22"><b>{len(entries)}</b></font><br/><font size="9" color="#64748b">Total CVEs</font>', ParagraphStyle('s', alignment=TA_CENTER)),
        Paragraph(f'<font size="22" color="#dc2626"><b>{sev["critical"]}</b></font><br/><font size="9" color="#64748b">Critical</font>', ParagraphStyle('s', alignment=TA_CENTER)),
        Paragraph(f'<font size="22" color="#ea580c"><b>{sev["high"]}</b></font><br/><font size="9" color="#64748b">High</font>', ParagraphStyle('s', alignment=TA_CENTER)),
        Paragraph(f'<font size="22" color="#ca8a04"><b>{sev["medium"]}</b></font><br/><font size="9" color="#64748b">Medium</font>', ParagraphStyle('s', alignment=TA_CENTER)),
        Paragraph(f'<font size="22" color="#2563eb"><b>{sev["low"]}</b></font><br/><font size="9" color="#64748b">Low</font>', ParagraphStyle('s', alignment=TA_CENTER)),
    ]]

    stats_table = Table(stats_data, colWidths=[1.3 * inch] * 5)
    stats_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_GRAY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8fafc')),
    ]))
    elements.append(stats_table)

    elements.append(Spacer(1, 0.4 * inch))

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
        "1. Triage Matrix \u2014 Pre-filled with CISA KEV CVEs, CVSS & EPSS scores",
        "2. 14-Day Sprint Calendar \u2014 Dated from Patch Tuesday, daily checklists",
        "3. Testing & Rollback Checklist \u2014 Pre-filled vendors/products from triage data",
        "4. SLA Compliance Tracker \u2014 Severity tiers with target/actual tracking",
        "5. Executive Summary \u2014 Pre-filled metrics, blank narrative & signature sections",
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

    elements.append(Paragraph("1. Triage Matrix", styles['SectionHeader']))
    elements.append(Paragraph(
        "Pre-filled with CISA KEV vulnerabilities for this Patch Tuesday cycle. "
        "Sorted by risk (CVSS descending, then EPSS). Mark your triage decision in the Priority column.",
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
        Paragraph('<b>RW</b>', styles['CellText']),
        Paragraph('<b>Priority</b>', styles['CellText']),
        Paragraph('<b>Owner</b>', styles['CellText']),
    ]

    col_widths = [1.1 * inch, 1.8 * inch, 0.5 * inch, 0.55 * inch, 0.7 * inch, 0.35 * inch, 0.65 * inch, 0.85 * inch]

    rows = [header]
    for e in entries:
        cvss = e.get('cvss', 0) or 0
        sev_label, sev_color = severity_label(cvss)
        epss = e.get('epss', 0) or 0
        rw = 'Yes' if e.get('ransomware') == 'Known' else ''

        rows.append([
            Paragraph(f'<font size="7">{e["cveID"]}</font>', styles['CellText']),
            Paragraph(f'<font size="7">{e["vendor"]}<br/>{e["product"]}</font>', styles['CellTextSmall']),
            Paragraph(f'<font size="8" color="{sev_color.hexval()}">{cvss:.1f}</font>', styles['CellText']),
            Paragraph(f'<font size="7">{epss:.3f}</font>', styles['CellText']),
            Paragraph(f'<font size="7">{e.get("dueDate", "")}</font>', styles['CellText']),
            Paragraph(f'<font size="7" color="#dc2626">{rw}</font>', styles['CellText']),
            Paragraph('', styles['CellText']),  # blank for user
            Paragraph('', styles['CellText']),  # blank for user
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
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, TEXT_MED),
    ]

    for i in range(1, len(rows)):
        bg = ROW_ALT if i % 2 == 0 else ROW_WHITE
        table_style.append(('BACKGROUND', (0, i), (-1, i), bg))

    table.setStyle(TableStyle(table_style))
    elements.append(table)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "RW = Known Ransomware Campaign  |  EPSS = Exploit Prediction Scoring System (0\u20131, higher = more likely exploited)",
        styles['SmallText']
    ))

    elements.append(PageBreak())
    return elements


def build_sprint_calendar(cycle_start, styles):
    """Page: 14-Day Sprint Calendar dated from Patch Tuesday."""
    elements = []

    elements.append(Paragraph("2. 14-Day Sprint Calendar", styles['SectionHeader']))
    elements.append(Paragraph(
        f"Starting from Patch Tuesday ({cycle_start.strftime('%B %d, %Y')}). "
        "Check off tasks as your team completes each phase.",
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
        (1, "ASSESS", "Download & review CISA KEV updates; run vulnerability scans"),
        (2, "ASSESS", "Complete triage matrix; assign severity priorities"),
        (3, "PLAN", "Create deployment groups; schedule maintenance windows"),
        (4, "PLAN", "Build test cases; prepare rollback procedures"),
        (5, "TEST", "Deploy patches to test/staging environment"),
        (6, "TEST", "Validate functionality; run regression tests"),
        (7, "TEST", "Sign off on test results; document exceptions"),
        (8, "DEPLOY", "Deploy critical/high patches to production (Wave 1)"),
        (9, "DEPLOY", "Monitor Wave 1; deploy medium patches (Wave 2)"),
        (10, "DEPLOY", "Deploy remaining patches (Wave 3)"),
        (11, "VERIFY", "Run post-deployment vulnerability scans"),
        (12, "VERIFY", "Validate patch compliance; update CMDB"),
        (13, "REPORT", "Compile SLA metrics; draft executive summary"),
        (14, "REPORT", "Final review; distribute report to stakeholders"),
    ]

    rows = [header]
    for day_num, phase, tasks in phases:
        day_date = cycle_start + timedelta(days=day_num - 1)
        # Use checkbox unicode
        rows.append([
            Paragraph(f'<font size="9"><b>{day_num}</b></font>', styles['CellText']),
            Paragraph(f'<font size="8">{day_date.strftime("%b %d")}</font>', styles['CellText']),
            Paragraph(f'<font size="8"><b>{phase}</b></font>', styles['CellText']),
            Paragraph(f'<font size="8">{tasks}</font>', styles['CellText']),
            Paragraph('<font size="10">\u2610</font>', ParagraphStyle('cb', alignment=TA_CENTER, fontSize=10)),
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

    elements.append(Paragraph("3. Testing & Rollback Checklist", styles['SectionHeader']))
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
    rows = [header]
    for e in entries:
        key = f"{e['vendor']}|{e['product']}"
        if key in seen:
            continue
        seen.add(key)

        cb = Paragraph('<font size="10">\u2610</font>', ParagraphStyle('cb', alignment=TA_CENTER, fontSize=10))
        rows.append([
            Paragraph(f'<font size="8">{e["vendor"]}<br/>{e["product"]}</font>', styles['CellText']),
            Paragraph(f'<font size="7">{e["cveID"]}</font>', styles['CellTextSmall']),
            cb, cb, cb, cb, cb, cb,
        ])

    # Add a few blank rows for manual additions
    for _ in range(3):
        cb = Paragraph('<font size="10">\u2610</font>', ParagraphStyle('cb', alignment=TA_CENTER, fontSize=10))
        rows.append([
            Paragraph('', styles['CellText']),
            Paragraph('', styles['CellText']),
            cb, cb, cb, cb, cb, cb,
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
    ]

    for i in range(1, len(rows)):
        bg = ROW_ALT if i % 2 == 0 else ROW_WHITE
        table_style.append(('BACKGROUND', (0, i), (-1, i), bg))

    table.setStyle(TableStyle(table_style))
    elements.append(table)

    elements.append(PageBreak())
    return elements


def build_sla_tracker(styles):
    """Page: SLA Compliance Tracker with blank tracking rows."""
    elements = []

    elements.append(Paragraph("4. SLA Compliance Tracker", styles['SectionHeader']))
    elements.append(Paragraph(
        "Track patching SLA compliance by severity tier. Fill in your organization's "
        "SLA targets and track actual completion dates.",
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

    for i, (sev, rng, standard, target) in enumerate(sla_defaults):
        sla_rows.append([
            Paragraph(f'<font size="9" color="{sla_colors[i].hexval()}"><b>{sev}</b></font>', styles['CellText']),
            Paragraph(f'<font size="9">{rng}</font>', styles['CellText']),
            Paragraph(f'<font size="9">{standard}</font>', styles['CellText']),
            Paragraph(f'<font size="9">{target}</font>', styles['CellText']),
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
    ]))
    elements.append(sla_table)

    elements.append(Spacer(1, 20))

    # Compliance tracking table
    elements.append(Paragraph("Compliance Tracking", styles['SubHeader']))

    track_header = [
        Paragraph('<b>Severity</b>', styles['CellText']),
        Paragraph('<b>Total<br/>CVEs</b>', styles['CellText']),
        Paragraph('<b>Patched<br/>On Time</b>', styles['CellText']),
        Paragraph('<b>Patched<br/>Late</b>', styles['CellText']),
        Paragraph('<b>Not Yet<br/>Patched</b>', styles['CellText']),
        Paragraph('<b>Exception<br/>Granted</b>', styles['CellText']),
        Paragraph('<b>Compliance<br/>%</b>', styles['CellText']),
    ]

    track_rows = [track_header]
    for sev in ['Critical', 'High', 'Medium', 'Low']:
        track_rows.append([
            Paragraph(f'<font size="9"><b>{sev}</b></font>', styles['CellText']),
        ] + [Paragraph('', styles['CellText'])] * 6)

    # Totals row
    track_rows.append([
        Paragraph('<font size="9"><b>TOTAL</b></font>', styles['CellText']),
    ] + [Paragraph('', styles['CellText'])] * 6)

    track_table = Table(track_rows, colWidths=[1.0 * inch, 0.75 * inch, 0.85 * inch, 0.75 * inch, 0.85 * inch, 0.85 * inch, 1.0 * inch])
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
    ]))
    elements.append(track_table)

    elements.append(PageBreak())
    return elements


def build_executive_summary(entries, month_label, cycle_start, cycle_end, styles):
    """Page: Executive Summary with pre-filled metrics and blank narrative."""
    elements = []

    elements.append(Paragraph("5. Executive Summary", styles['SectionHeader']))
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

    elements.append(Spacer(1, 20))

    # Narrative sections (blank for user)
    narrative_sections = [
        "Summary of Actions Taken",
        "Key Risks & Exceptions",
        "Recommendations for Next Cycle",
    ]

    for section_title in narrative_sections:
        elements.append(Paragraph(f'<b>{section_title}</b>', styles['KitBody']))
        elements.append(Spacer(1, 4))

        # Blank lined area (3 lines)
        for _ in range(3):
            elements.append(HRFlowable(
                width="100%", thickness=0.5, color=BORDER_GRAY,
                spaceBefore=14, spaceAfter=0
            ))
        elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 20))

    # Signature block
    elements.append(HRFlowable(width="100%", thickness=1, color=TEXT_MED, spaceBefore=0, spaceAfter=6))

    sig_data = [[
        Paragraph('<font size="9"><b>Prepared By</b></font>', styles['CellText']),
        Paragraph('<font size="9"><b>Title</b></font>', styles['CellText']),
        Paragraph('<font size="9"><b>Date</b></font>', styles['CellText']),
        Paragraph('<font size="9"><b>Signature</b></font>', styles['CellText']),
    ], [
        Paragraph('', styles['CellText']),
        Paragraph('', styles['CellText']),
        Paragraph('', styles['CellText']),
        Paragraph('', styles['CellText']),
    ]]

    sig_table = Table(sig_data, colWidths=[1.6 * inch, 1.6 * inch, 1.3 * inch, 2.0 * inch])
    sig_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
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
    elements.extend(build_sprint_calendar(cycle_start, styles))
    elements.extend(build_testing_checklist(entries, styles))
    elements.extend(build_sla_tracker(styles))
    elements.extend(build_executive_summary(entries, month_label, cycle_start, cycle_end, styles))

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)

    print(f"PDF generated: {filepath}")
    print(f"  Pages: ~6-7 (cover + 5 templates)")
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

    key = f"{year}-{month:02d}"
    manifest[key] = {
        'filename': filename,
        'generated_at': datetime.now().isoformat(),
        'cycle_start': cycle_start.strftime('%Y-%m-%d'),
        'cycle_end': cycle_end.strftime('%Y-%m-%d'),
        'total_cves': len(entries),
        'severity': sev,
        'top_vendors': [{'vendor': v, 'count': c} for v, c in vendors[:5]],
        'ransomware_linked': sum(1 for e in entries if e.get('ransomware') == 'Known'),
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
