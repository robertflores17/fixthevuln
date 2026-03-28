#!/usr/bin/env python3
"""
CVE Page Generator for FixTheVuln.com
Reads data/kev-data.json and generates individual CVE pages + index page.
Also updates sitemap.xml with CVE entries.

Usage:
    python3 scripts/generate_cve_pages.py
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from lib.templates import (html_head, nav, share_bar, footer, cf_analytics,
                           article_schema, breadcrumb_schema, esc)
from lib.constants import SITE_URL
from entity_extractor import enrich_cve, OWASP_COLORS, OWASP_LABELS

KEV_PATH = REPO_ROOT / 'data' / 'kev-data.json'
CVE_DIR = REPO_ROOT / 'cve'
SITEMAP_PATH = REPO_ROOT / 'sitemap.xml'
TODAY = date.today().isoformat()


def severity_label(cvss):
    """Return severity label for a CVSS score."""
    if cvss is None:
        return 'UNKNOWN'
    if cvss >= 9.0:
        return 'CRITICAL'
    if cvss >= 7.0:
        return 'HIGH'
    if cvss >= 4.0:
        return 'MEDIUM'
    if cvss >= 0.1:
        return 'LOW'
    return 'NONE'


def severity_color(label):
    """Return badge color for severity."""
    return {
        'CRITICAL': '#dc3545',
        'HIGH': '#fd7e14',
        'MEDIUM': '#ffc107',
        'LOW': '#28a745',
        'NONE': '#6c757d',
        'UNKNOWN': '#6c757d',
    }.get(label, '#6c757d')


def severity_bg(label):
    """Return light background color for severity."""
    return {
        'CRITICAL': '#f8d7da',
        'HIGH': '#ffe5d0',
        'MEDIUM': '#fff3cd',
        'LOW': '#d4edda',
        'NONE': '#e2e3e5',
        'UNKNOWN': '#e2e3e5',
    }.get(label, '#e2e3e5')


def escape_html(text):
    """Escape HTML special characters (alias for esc)."""
    return esc(text)


def truncate_sentence(text, max_len):
    """Truncate text at a word boundary, ending at a sentence if possible."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    for sep in ['. ', '! ', '? ']:
        idx = truncated.rfind(sep)
        if idx > max_len // 2:
            return truncated[:idx + 1]
    idx = truncated.rfind(' ')
    if idx > 0:
        return truncated[:idx]
    return truncated


def build_cve_faq_schema(vuln):
    """Build FAQPage JSON-LD schema for a CVE page."""
    cve_id = vuln['id']
    title = vuln['title'].strip()
    desc = vuln.get('description', '')
    fix = vuln.get('fix', '')
    cvss = vuln.get('cvss')
    sev = severity_label(cvss)
    cvss_display = str(cvss) if cvss is not None else 'N/A'
    is_zero_day = vuln.get('isZeroDay', False)

    faqs = [
        {
            "question": f"What is {cve_id}?",
            "answer": f"{cve_id} ({title}) is a vulnerability with a CVSS score of {cvss_display} ({sev}).{' This is an actively exploited zero-day vulnerability.' if is_zero_day else ''} {desc}"
        },
        {
            "question": f"How do I fix {cve_id}?",
            "answer": fix if fix else f"Refer to the vendor advisory for {cve_id} for specific remediation steps."
        },
        {
            "question": f"How severe is {cve_id}?",
            "answer": f"{cve_id} has a CVSS score of {cvss_display}, classified as {sev}. {'This vulnerability is in the CISA Known Exploited Vulnerabilities (KEV) catalog, meaning it has been actively exploited in the wild.' if not vuln.get('archived', False) else 'This vulnerability was previously in the CISA KEV catalog.'}"
        }
    ]

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f["answer"]
                }
            }
            for f in faqs
        ]
    }

    return faqs, json.dumps(schema, indent=8, ensure_ascii=False)


def generate_owasp_badges(vuln):
    """Generate OWASP Top 10 badge HTML from enriched vuln data."""
    owasp = vuln.get('owasp', [])
    if not owasp:
        return ''
    badges = []
    for entry in owasp:
        oid = entry['id']
        label = entry['label']
        color = OWASP_COLORS.get(oid, '#6c757d')
        badges.append(
            f'<a href="../owasp-top10.html" style="display:inline-block;background:{color};color:white;'
            f'padding:0.2rem 0.6rem;border-radius:4px;font-size:0.8rem;font-weight:600;'
            f'text-decoration:none;" title="{escape_html(label)}">{escape_html(oid)}</a>'
        )
    return ' '.join(badges)


def generate_cve_page(vuln):
    """Generate an individual CVE page."""
    cve_id = vuln['id']
    title = vuln['title'].strip()
    cvss = vuln.get('cvss')
    cvss_display = str(cvss) if cvss is not None else 'N/A'
    sev = severity_label(cvss)
    sev_color = severity_color(sev)
    sev_bg = severity_bg(sev)
    desc = escape_html(vuln.get('description', ''))
    fix = escape_html(vuln.get('fix', ''))
    date_added = vuln.get('dateAdded', '')
    is_zero_day = vuln.get('isZeroDay', False)
    archived = vuln.get('archived', False)
    nvd_url = f'https://nvd.nist.gov/vuln/detail/{cve_id}'
    page_title = f'{cve_id}: {title} - FixTheVuln'
    meta_desc = truncate_sentence(f'{cve_id} — CVSS {cvss_display} ({sev}). {vuln.get("description", "")}', 160)
    zero_day_badge = '<span style="display:inline-block;background:#dc3545;color:white;padding:0.2rem 0.6rem;border-radius:4px;font-size:0.8rem;font-weight:600;margin-left:0.5rem;">ZERO-DAY</span>' if is_zero_day else ''
    archived_badge = '<span style="display:inline-block;background:#6c757d;color:white;padding:0.2rem 0.6rem;border-radius:4px;font-size:0.8rem;font-weight:600;margin-left:0.5rem;">ARCHIVED</span>' if archived else '<span style="display:inline-block;background:#28a745;color:white;padding:0.2rem 0.6rem;border-radius:4px;font-size:0.8rem;font-weight:600;margin-left:0.5rem;">ACTIVE</span>'
    owasp_badges = generate_owasp_badges(vuln)
    cwes = vuln.get('cwes', [])
    cwe_text = ', '.join(cwes) if cwes else ''

    # Build FAQ schema and visible content
    faqs, faq_schema_json = build_cve_faq_schema(vuln)
    faq_details = '\n'.join(
        f'            <details class="faq-item">\n'
        f'                <summary>{escape_html(f["question"])}</summary>\n'
        f'                <p>{escape_html(f["answer"])}</p>\n'
        f'            </details>'
        for f in faqs
    )

    canonical = f'{SITE_URL}/cve/{cve_id}.html'
    keywords = f"{cve_id}, CVE, vulnerability, CISA KEV, {escape_html(title)}, cybersecurity"
    schema_blocks = [
        article_schema(f'{cve_id}: {title}', meta_desc, date_added, date_modified=TODAY),
        breadcrumb_schema([("Home", f"{SITE_URL}/"), ("CVE Database", f"{SITE_URL}/cve/"), (cve_id, None)]),
        faq_schema_json,
    ]
    head = html_head(f'{cve_id}: {title}', meta_desc, canonical,
                     keywords=keywords, schema_blocks=schema_blocks, depth=1)

    return f'''<!DOCTYPE html>
<html lang="en">
{head}
<body>
{nav(depth=1)}
{share_bar()}

    <header class="content-header">
        <div class="container">
            <h1>{cve_id}</h1>
            <p>{escape_html(title)}</p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.25rem;">Added to CISA KEV: {date_added}</p>
        </div>
    </header>

    <main class="container">
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; justify-content: center; padding: 0.75rem; margin-bottom: 1rem; font-size: 0.8rem; color: var(--text-muted); border-bottom: 1px solid var(--border-color);">
            <span>By <strong>FixTheVuln Team</strong></span>
            <span aria-hidden="true">&middot;</span>
            <span>Sources: CISA KEV Catalog, NVD</span>
        </div>
        <div class="content-wrapper">

            <!-- Severity Badge -->
            <div style="display:flex;flex-wrap:wrap;gap:0.75rem;align-items:center;margin-bottom:1.5rem;">
                <span style="display:inline-block;background:{sev_color};color:white;padding:0.4rem 1rem;border-radius:6px;font-size:1rem;font-weight:700;">CVSS {cvss_display} &mdash; {sev}</span>
                {zero_day_badge}
                {archived_badge}
            </div>

            <!-- OWASP & CWE Classification -->
            <div style="display:flex;flex-wrap:wrap;gap:0.5rem;align-items:center;margin-bottom:1.5rem;">
                {f'<span style="font-size:0.8rem;color:var(--text-muted);font-weight:600;">OWASP:</span> {owasp_badges}' if owasp_badges else ''}
                {f'<span style="font-size:0.8rem;color:var(--text-muted);margin-left:0.5rem;">{escape_html(cwe_text)}</span>' if cwe_text else ''}
            </div>

            <h2>Description</h2>
            <p>{desc}</p>

            <h2>Required Action</h2>
            <div style="background:{sev_bg};border-left:4px solid {sev_color};padding:1rem;border-radius:0 8px 8px 0;margin:1rem 0;">
                <p style="margin:0;"><strong>Fix:</strong> {fix}</p>
            </div>

            <h2>References</h2>
            <ul>
                <li><a href="{nvd_url}" target="_blank" rel="noopener">NVD Entry for {cve_id}</a></li>
                <li><a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog" target="_blank" rel="noopener">CISA Known Exploited Vulnerabilities Catalog</a></li>
            </ul>

            <h2>Assess Your Risk</h2>
            <p>Use the <a href="../cvss-calculator.html">CVSS Calculator</a> to evaluate how this vulnerability affects your specific environment. Consider your network exposure, existing mitigations, and asset criticality.</p>

            <h2>Frequently Asked Questions</h2>
{faq_details}

        </div>

        <!-- Related Tools -->
        <section style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px;">
            <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Free Security Tools</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
                <a href="../cvss-calculator.html" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">CVSS Calculator</a>
                <a href="../security-quiz.html" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">Security+ Practice Quiz</a>
                <a href="../password-strength.html" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">Password Strength Checker</a>
            </div>
        </section>

        <!-- Store CTA -->
        <section style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">FixTheVuln Store</p>
            <h3 style="color: white; margin-bottom: 0.5rem;">Stay Ahead of Vulnerabilities</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">Structured study planners for 60+ security certifications. Master vulnerability management with domain trackers and exam strategies.</p>
            <a href="/store/comptia.html" style="display: inline-block; background: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: 600;">Shop Security+ Planner</a>
        </section>

        <!-- CyberFolio CTA -->
        <div style="border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 12px; text-align: center; margin-top: 1.5rem;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.5; margin-bottom: 0.3rem;">CyberFolio</p>
            <p style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Vulnerability management on your resume? Prove it.</p>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">Build a shareable cybersecurity portfolio that highlights your certifications, projects, and skills &mdash; free.</p>
            <a href="https://cyberfolio.io" style="display:inline-block;background:#06b6d4;color:white;padding:0.6rem 1.5rem;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.95rem;" target="_blank" rel="noopener">Build Your Portfolio &rarr;</a>
        </div>

        <a href="../index.html" class="back-link">&larr; Back to Home</a>
        <a href="index.html" class="back-link" style="margin-left: 1rem;">&larr; All CVEs</a>
    </main>

{footer(affiliate_disclosure=True)}
{cf_analytics()}
</body>
</html>'''


def generate_index_page(vulns):
    """Generate the CVE directory index page."""
    active = [v for v in vulns if not v.get('archived', False)]
    archived = [v for v in vulns if v.get('archived', False)]

    def make_row(v):
        cve_id = v['id']
        cvss = v.get('cvss')
        cvss_display = str(cvss) if cvss is not None else 'N/A'
        sev = severity_label(cvss)
        sev_color = severity_color(sev)
        title = escape_html(v['title'].strip())
        date_added = v.get('dateAdded', '')
        zero_day = ' <span style="background:#dc3545;color:white;padding:0.1rem 0.4rem;border-radius:3px;font-size:0.7rem;font-weight:600;">0-DAY</span>' if v.get('isZeroDay') else ''
        owasp = v.get('owasp', [])
        owasp_cell = ''
        if owasp:
            owasp_parts = []
            for entry in owasp:
                oid = entry['id']
                color = OWASP_COLORS.get(oid, '#6c757d')
                owasp_parts.append(
                    f'<span style="display:inline-block;background:{color};color:white;'
                    f'padding:0.1rem 0.4rem;border-radius:3px;font-size:0.7rem;font-weight:600;"'
                    f' title="{escape_html(entry["label"])}">{oid}</span>'
                )
            owasp_cell = ' '.join(owasp_parts)
        return f'''                <tr>
                    <td><a href="{cve_id}.html" style="color:#667eea;font-weight:600;">{cve_id}</a></td>
                    <td>{title}{zero_day}</td>
                    <td><span style="display:inline-block;background:{sev_color};color:white;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600;">{cvss_display} {sev}</span></td>
                    <td class="owasp-col">{owasp_cell}</td>
                    <td>{date_added}</td>
                </tr>'''

    active_rows = '\n'.join(make_row(v) for v in sorted(active, key=lambda x: x.get('cvss') or 0, reverse=True))
    archived_rows = '\n'.join(make_row(v) for v in sorted(archived, key=lambda x: x.get('dateAdded', ''), reverse=True))

    idx_desc = f'Browse {len(vulns)} tracked CVEs from the CISA Known Exploited Vulnerabilities catalog. CVSS scores, fix instructions, and NVD links.'
    idx_schema = [breadcrumb_schema([("Home", f"{SITE_URL}/"), ("CVE Database", None)])]
    idx_head = html_head('CVE Database &mdash; CISA KEV Tracker', idx_desc, f'{SITE_URL}/cve/',
                         keywords='CVE database, CISA KEV, vulnerability database, CVE lookup, cybersecurity vulnerabilities',
                         schema_blocks=idx_schema, depth=1)

    # Inject custom <style> into head (before closing </head>)
    idx_style = """    <style>
        .tab-buttons {{ display: flex; gap: 0.5rem; margin-bottom: 1.5rem; }}
        .tab-btn {{ padding: 0.5rem 1.25rem; border: 2px solid #667eea; background: white; color: #667eea; border-radius: 20px; cursor: pointer; font-weight: 600; transition: all 0.2s; }}
        .tab-btn:hover, .tab-btn.active {{ background: #667eea; color: white; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .cve-table {{ width: 100%; border-collapse: collapse; }}
        .cve-table th {{ text-align: left; padding: 0.75rem; border-bottom: 2px solid var(--border-color); font-size: 0.85rem; color: var(--text-muted); }}
        .cve-table td {{ padding: 0.75rem; border-bottom: 1px solid var(--border-color); }}
        .cve-table tr:hover {{ background: var(--bg-secondary); }}
        .search-box {{ width: 100%; padding: 0.75rem 1rem; border: 2px solid var(--border-color); border-radius: 8px; font-size: 1rem; margin-bottom: 1.5rem; background: var(--bg-primary); color: var(--text-primary); }}
        .search-box:focus {{ border-color: #667eea; outline: none; }}
        @media (max-width: 768px) {{
            .cve-table .owasp-col, .cve-table th:nth-child(4) {{ display: none; }}
            .cve-table th:nth-child(5), .cve-table td:nth-child(5) {{ display: none; }}
        }}
    </style>"""
    idx_head = idx_head.replace('</head>', idx_style + '\n</head>')

    return f'''<!DOCTYPE html>
<html lang="en">
{idx_head}
<body>
{nav(depth=1)}
{share_bar()}

    <header class="content-header">
        <div class="container">
            <h1>CVE Database</h1>
            <p>CISA Known Exploited Vulnerabilities Tracker</p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.25rem;">{len(vulns)} CVEs tracked &mdash; Updated {TODAY}</p>
        </div>
    </header>

    <main class="container">
        <input type="text" class="search-box" id="cve-search" placeholder="Search by CVE ID, vendor, or keyword..." oninput="filterTable()">

        <div class="tab-buttons">
            <button class="tab-btn active" onclick="switchTab('active')">Active ({len(active)})</button>
            <button class="tab-btn" onclick="switchTab('archived')">Archived ({len(archived)})</button>
        </div>

        <div id="tab-active" class="tab-content active">
            <table class="cve-table" id="active-table">
                <thead>
                    <tr><th>CVE ID</th><th>Title</th><th>CVSS</th><th class="owasp-col">OWASP</th><th>Date Added</th></tr>
                </thead>
                <tbody>
{active_rows}
                </tbody>
            </table>
        </div>

        <div id="tab-archived" class="tab-content">
            <table class="cve-table" id="archived-table">
                <thead>
                    <tr><th>CVE ID</th><th>Title</th><th>CVSS</th><th class="owasp-col">OWASP</th><th>Date Added</th></tr>
                </thead>
                <tbody>
{archived_rows}
                </tbody>
            </table>
        </div>

        <!-- Store CTA -->
        <section style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">FixTheVuln Store</p>
            <h3 style="color: white; margin-bottom: 0.5rem;">Master Vulnerability Management</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">Structured study planners for Security+, CySA+, and 60+ certifications. Domain trackers, time blocking, and exam strategies.</p>
            <a href="/store/store.html" style="display: inline-block; background: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: 600;">Shop Study Planners</a>
        </section>

        <a href="../index.html" class="back-link">&larr; Back to Home</a>
    </main>

{footer(affiliate_disclosure=True)}

    <script>
        function switchTab(tab) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tab).classList.add('active');
            event.target.classList.add('active');
        }}
        function filterTable() {{
            const query = document.getElementById('cve-search').value.toLowerCase();
            document.querySelectorAll('.cve-table tbody tr').forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            }});
        }}
    </script>
{cf_analytics()}
</body>
</html>'''


def update_sitemap(vulns):
    """Update sitemap.xml with CVE entries."""
    sitemap_text = SITEMAP_PATH.read_text(encoding='utf-8')

    # Remove any existing CVE entries
    sitemap_text = re.sub(
        r'\n  <!-- CVE Pages -->.*?(?=\n  <!--|\n</urlset>)',
        '',
        sitemap_text,
        flags=re.DOTALL,
    )

    # Build CVE entries
    cve_entries = f'\n  <!-- CVE Pages -->\n  <url>\n    <loc>https://fixthevuln.com/cve/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>'

    for v in vulns:
        cve_entries += f'''
  <url>
    <loc>https://fixthevuln.com/cve/{v["id"]}.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>'''

    # Insert before </urlset>
    sitemap_text = sitemap_text.replace('</urlset>', cve_entries + '\n</urlset>')
    SITEMAP_PATH.write_text(sitemap_text, encoding='utf-8')
    print(f'  SITEMAP updated with {len(vulns) + 1} CVE entries.')


def main():
    if not KEV_PATH.exists():
        print('  ERROR: data/kev-data.json not found.')
        return

    data = json.loads(KEV_PATH.read_text(encoding='utf-8'))
    vulns = data.get('vulnerabilities', [])

    if not vulns:
        print('  No vulnerabilities found.')
        return

    CVE_DIR.mkdir(exist_ok=True)

    # Enrich CVEs with CWE + OWASP classification
    enriched_vulns = [enrich_cve(v) for v in vulns]
    owasp_count = sum(1 for v in enriched_vulns if v.get('owasp'))
    cwe_count = sum(1 for v in enriched_vulns if v.get('cwes'))
    print(f'  ENRICHED {len(enriched_vulns)} CVEs ({cwe_count} with CWEs, {owasp_count} with OWASP)')

    # Generate individual CVE pages
    for v in enriched_vulns:
        html = generate_cve_page(v)
        out_path = CVE_DIR / f"{v['id']}.html"
        out_path.write_text(html, encoding='utf-8')

    print(f'  GENERATED {len(enriched_vulns)} individual CVE pages.')

    # Generate index page
    index_html = generate_index_page(enriched_vulns)
    (CVE_DIR / 'index.html').write_text(index_html, encoding='utf-8')
    print('  GENERATED cve/index.html')

    # Update sitemap
    update_sitemap(enriched_vulns)

    print(f'\n  Done. {len(vulns) + 1} files in cve/.')


if __name__ == '__main__':
    main()
