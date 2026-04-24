#!/usr/bin/env python3
"""
Certification Comparison Page Generator for FixTheVuln.com
Reads data/cert-comparisons.json and generates comparison HTML pages + index.
Also updates sitemap.xml with comparison entries.

Usage:
    python3 scripts/generate_comparisons.py
"""

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.templates import (html_head, nav, share_bar, footer, cf_analytics,
                           article_schema, breadcrumb_schema, esc)
from lib.constants import SITE_URL, COMPARISON_CSS_VERSION

DATA_PATH = REPO_ROOT / 'data' / 'cert-comparisons.json'
COMP_DIR = REPO_ROOT / 'comparisons'
TODAY = date.today().isoformat()
TODAY_DISPLAY = date.today().strftime('%B %-d, %Y')


def escape_html(text):
    """Escape HTML special characters (alias for esc)."""
    return esc(str(text))


def truncate_sentence(text, max_len):
    """Truncate text at a word boundary, ending at a sentence if possible."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    # Try to end at last sentence boundary
    for sep in ['. ', '! ', '? ']:
        idx = truncated.rfind(sep)
        if idx > max_len // 2:
            return truncated[:idx + 1]
    # Fall back to last word boundary
    idx = truncated.rfind(' ')
    if idx > 0:
        return truncated[:idx]
    return truncated


def build_faq_schema(c1, c2, comp):
    """Build FAQPage JSON-LD schema for a comparison page."""
    name1 = c1['name']
    name2 = c2['name']

    faqs = [
        {
            "question": f"What is the difference between {name1} and {name2}?",
            "answer": comp['description']
        },
        {
            "question": f"Should I get {name1} or {name2} first?",
            "answer": comp['recommended_order']
        },
        {
            "question": f"Who should get {name1}?",
            "answer": comp['who_should_get']['cert1']
        },
        {
            "question": f"Who should get {name2}?",
            "answer": comp['who_should_get']['cert2']
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


def generate_comparison_page(comp, certs):
    """Generate a single comparison page."""
    c1 = certs[comp['cert1']]
    c2 = certs[comp['cert2']]
    title = comp['title']
    slug = comp['slug']
    desc = comp['description']
    who1 = comp['who_should_get']['cert1']
    who2 = comp['who_should_get']['cert2']
    order = comp['recommended_order']
    tips = comp['study_tips']
    page_title = f'{title}: Which Certification Should You Get? - FixTheVuln'
    meta_desc = truncate_sentence(f'{title} comparison. {desc}', 160)

    # Vendor → store category page mapping
    VENDOR_STORE = {
        'CompTIA': '/store/comptia.html', 'ISC2': '/store/security-governance.html',
        '(ISC)2': '/store/security-governance.html', 'AWS': '/store/aws.html',
        'Cisco': '/store/cisco.html', 'Microsoft': '/store/microsoft.html',
        'Google Cloud': '/store/google-cloud.html', 'EC-Council': '/store/offensive-devops.html',
        'OffSec': '/store/offensive-devops.html', 'HashiCorp': '/store/offensive-devops.html',
        'CNCF': '/store/offensive-devops.html', 'ISACA': '/store/security-governance.html',
        'GIAC': '/store/security-governance.html',
    }
    store_url = VENDOR_STORE.get(c1.get('vendor', ''), '/store/store.html')

    # Comparison cert-key → cert page filename mapping
    CERT_PAGE_MAP = {
        'security-plus': 'comptia-security-plus', 'cysa-plus': 'comptia-cysa-plus',
        'pentest-plus': 'comptia-pentest-plus', 'network-plus': 'comptia-network-plus',
        'a-plus': 'comptia-a-plus-1201', 'sscp': 'isc2-sscp', 'cissp': 'isc2-cissp',
        'ccsp': 'isc2-ccsp', 'cc': 'isc2-cc', 'cism': 'isaca-cism',
        'cisa': 'isaca-cisa', 'crisc': 'isaca-crisc',
        'aws-saa': 'aws-solutions-architect', 'aws-sap': 'aws-solutions-architect',
        'aws-security-specialty': 'aws-security-specialty', 'aws-ccp': 'aws-cloud-practitioner',
        'azure-az-104': 'ms-az-104', 'azure-az-500': 'ms-az-500',
        'azure-az-900': 'ms-az-900', 'ccna': 'cisco-ccna',
        'ccnp-encor': 'cisco-ccnp-encor', 'ccnp-security': 'cisco-ccnp-security',
        'cyberops': 'cisco-cyberops', 'ceh': 'ec-ceh', 'oscp': 'offsec-oscp',
        'gsec': 'giac-gsec', 'gcih': 'giac-gcih', 'gpen': 'giac-gpen',
        'casp-plus': 'comptia-casp-plus', 'cloud-plus': 'comptia-cloud-plus',
        'linux-plus': 'comptia-linux-plus', 'server-plus': 'comptia-server-plus',
        'data-plus': 'comptia-data-plus',
    }
    cert1_page = CERT_PAGE_MAP.get(comp['cert1'], '')
    cert2_page = CERT_PAGE_MAP.get(comp['cert2'], '')

    # Build "Deep Dive" internal links (deduplicate if both certs map to same page)
    deep_dive_links = []
    seen_pages = set()
    for cert_key, cert_data, cert_page in [(comp['cert1'], c1, cert1_page), (comp['cert2'], c2, cert2_page)]:
        if cert_page and cert_page not in seen_pages:
            seen_pages.add(cert_page)
            deep_dive_links.append(
                f'<a href="../certs/{cert_page}.html" style="padding:0.75rem;background:var(--bg-tertiary);border-radius:6px;text-decoration:none;color:var(--text-primary);border:1px solid var(--border-color);transition:border-color 0.2s;">{escape_html(cert_data["name"])} Study Guide</a>'
            )
    # Always add practice tests link
    deep_dive_links.append(
        '<a href="../practice-tests.html" style="padding:0.75rem;background:var(--bg-tertiary);border-radius:6px;text-decoration:none;color:var(--text-primary);border:1px solid var(--border-color);transition:border-color 0.2s;">All Practice Tests</a>'
    )
    deep_dive_html = '\n                '.join(deep_dive_links)

    # Build FAQ schema and visible content
    faqs, faq_schema_json = build_faq_schema(c1, c2, comp)

    faq_details = '\n'.join(
        f'''            <details class="faq-item">
                <summary>{escape_html(f["question"])}</summary>
                <p>{escape_html(f["answer"])}</p>
            </details>'''
        for f in faqs
    )

    def spec_row(label, key):
        v1 = escape_html(c1.get(key, 'N/A'))
        v2 = escape_html(c2.get(key, 'N/A'))
        return f'<tr><td style="font-weight:600;color:var(--text-muted);">{label}</td><td>{v1}</td><td>{v2}</td></tr>'

    table_rows = '\n'.join([
        spec_row('Vendor', 'vendor'),
        spec_row('Exam Code', 'code'),
        spec_row('Level', 'level'),
        spec_row('Cost', 'cost'),
        spec_row('Duration', 'duration'),
        spec_row('Questions', 'questions'),
        spec_row('Passing Score', 'passing'),
        spec_row('Renewal', 'renewal'),
        spec_row('Prerequisites', 'prerequisites'),
        spec_row('Avg Salary Range', 'salary_range'),
    ])

    canonical = f'{SITE_URL}/comparisons/{slug}.html'
    keywords = f"{escape_html(c1['name'])}, {escape_html(c2['name'])}, certification comparison, {escape_html(c1['vendor'])}, {escape_html(c2['vendor'])}, IT certification"
    schema_blocks = [
        article_schema(f'{title}: Which Certification Should You Get?', meta_desc, TODAY),
        breadcrumb_schema([("Home", f"{SITE_URL}/"), ("Certification Comparisons", f"{SITE_URL}/comparisons/"), (title, None)]),
        faq_schema_json,
    ]
    head = html_head(f'{title}: Which Certification Should You Get?', meta_desc, canonical,
                     keywords=keywords,
                     extra_css=[f'comparison.css?v={COMPARISON_CSS_VERSION}'],
                     schema_blocks=schema_blocks, depth=1)

    return f'''<!DOCTYPE html>
<html lang="en">
{head}
<body>
{nav(depth=1)}
{share_bar()}

    <header class="content-header">
        <div class="container">
            <h1>{escape_html(title)}</h1>
            <p>Which certification should you get?</p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.25rem;">Last updated: {TODAY_DISPLAY}</p>
        </div>
    </header>

    <main class="container">
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; justify-content: center; padding: 0.75rem; margin-bottom: 1rem; font-size: 0.8rem; color: var(--text-muted); border-bottom: 1px solid var(--border-color);">
            <span>By <strong>FixTheVuln Team</strong></span>
            <span aria-hidden="true">&middot;</span>
            <span>Independent certification guidance</span>
        </div>
        <div class="content-wrapper">

            <p>{escape_html(desc)}</p>

            <h2>Side-by-Side Comparison</h2>
            <div style="overflow-x: auto;">
            <table class="compare-table">
                <thead>
                    <tr>
                        <th></th>
                        <th>{escape_html(c1['name'])}</th>
                        <th>{escape_html(c2['name'])}</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            </div>

            <h2>Focus Areas</h2>
            <div class="who-grid">
                <div class="who-card">
                    <h4>{escape_html(c1['name'])}</h4>
                    <p>{escape_html(c1.get('focus', ''))}</p>
                </div>
                <div class="who-card">
                    <h4>{escape_html(c2['name'])}</h4>
                    <p>{escape_html(c2.get('focus', ''))}</p>
                </div>
            </div>

            <h2>Who Should Get Which?</h2>
            <div class="who-grid">
                <div class="who-card">
                    <h4>Get {escape_html(c1['name'])} if...</h4>
                    <p>{escape_html(who1)}</p>
                </div>
                <div class="who-card">
                    <h4>Get {escape_html(c2['name'])} if...</h4>
                    <p>{escape_html(who2)}</p>
                </div>
            </div>

            <h2>Recommended Order</h2>
            <p>{escape_html(order)}</p>

            <h2>Study Tips</h2>
            <p>{escape_html(tips)}</p>

            <h2>Frequently Asked Questions</h2>
{faq_details}

            <h2>Test Your Knowledge</h2>
            <p>Already studying? Try our free tools:</p>
            <ul>
                <li><a href="../security-quiz.html">Security+ Practice Quiz</a> &mdash; 300 questions mapped to SY0-701 domains</li>
                <li><a href="../cvss-calculator.html">CVSS Calculator</a> &mdash; Practice scoring vulnerabilities</li>
            </ul>

        </div>

        <!-- Deep Dive Guides -->
        <section style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px;">
            <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Deep Dive Guides</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
                {deep_dive_html}
            </div>
        </section>

        <!-- Store CTA -->
        <section style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">FixTheVuln Store</p>
            <h3 style="color: white; margin-bottom: 0.5rem;">Get the Study Planner for {escape_html(c1['name'])}</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">Structured study planners with domain trackers, time blocking, and exam strategies. Standard + ADHD-friendly editions.</p>
            <a href="{store_url}" style="display: inline-block; background: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: 600;">Shop {escape_html(c1['vendor'])} Planners</a>
            <p style="font-size: 0.8rem; opacity: 0.85; margin-top: 0.75rem;">Also available: CompTIA, (ISC)2, AWS, Cisco, and 60+ more</p>
        </section>

        <a href="../index.html" class="back-link">&larr; Back to Home</a>
        <a href="index.html" class="back-link" style="margin-left: 1rem;">&larr; All Comparisons</a>
    </main>

{footer(affiliate_disclosure=True)}
{cf_analytics()}
</body>
</html>'''


def generate_index_page(comparisons, certs):
    """Generate the comparisons directory index page."""
    cards = []
    for comp in comparisons:
        c1 = certs[comp['cert1']]
        c2 = certs[comp['cert2']]
        cards.append(f'''            <a href="{comp['slug']}.html" style="display:block;padding:1.25rem;background:var(--bg-secondary);border-radius:10px;text-decoration:none;color:var(--text-primary);border:1px solid var(--border-color);transition:border-color 0.2s,transform 0.2s;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                    <span style="font-weight:700;font-size:1.05rem;">{escape_html(comp['title'])}</span>
                    <span style="color:#667eea;font-size:0.9rem;">&rarr;</span>
                </div>
                <p style="font-size:0.85rem;color:var(--text-muted);margin:0;">{escape_html(c1['vendor'])} {escape_html(c1['level'])} vs {escape_html(c2['vendor'])} {escape_html(c2['level'])}</p>
            </a>''')

    cards_html = '\n'.join(cards)

    idx_desc = f'Compare IT security certifications side by side. {len(comparisons)} detailed comparisons including Security+, CISSP, AWS, CySA+, and more.'
    idx_keywords = 'certification comparison, Security+ vs CySA+, CISSP vs CISM, IT certification guide, cybersecurity certifications'
    idx_canonical = f'{SITE_URL}/comparisons/'
    idx_schema = [breadcrumb_schema([("Home", f"{SITE_URL}/"), ("Certification Comparisons", None)])]
    idx_head = html_head('Certification Comparisons &mdash; Which Cert Should You Get?', idx_desc, idx_canonical,
                         keywords=idx_keywords, schema_blocks=idx_schema, depth=1)

    return f'''<!DOCTYPE html>
<html lang="en">
{idx_head}
<body>
{nav(depth=1)}
{share_bar()}

    <header class="content-header">
        <div class="container">
            <h1>Certification Comparisons</h1>
            <p>Side-by-side guides to help you choose the right certification</p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.25rem;">{len(comparisons)} comparisons &mdash; Updated {TODAY_DISPLAY}</p>
        </div>
    </header>

    <main class="container">
        <section class="intro">
            <h2>Which Certification Should You Get?</h2>
            <p>Choosing between IT security certifications can be overwhelming. These side-by-side comparisons break down cost, difficulty, career impact, and recommended order so you can make an informed decision.</p>
        </section>

        <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(320px, 1fr));gap:1rem;margin:2rem 0;">
{cards_html}
        </div>

        <!-- Store CTA -->
        <section style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">FixTheVuln Store</p>
            <h3 style="color: white; margin-bottom: 0.5rem;">Ready to Start Studying?</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">Structured study planners for 60+ certifications. Standard + ADHD-friendly editions with domain trackers and exam strategies.</p>
            <div style="display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap;">
                <a href="/store/comptia.html" style="background: rgba(255,255,255,0.12); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.25);">CompTIA</a>
                <a href="/store/security-governance.html" style="background: rgba(255,255,255,0.12); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.25);">(ISC)2</a>
                <a href="/store/aws.html" style="background: rgba(255,255,255,0.12); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.25);">AWS</a>
                <a href="/store/cisco.html" style="background: rgba(255,255,255,0.12); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.25);">Cisco</a>
            </div>
        </section>

        <a href="../index.html" class="back-link">&larr; Back to Home</a>
    </main>

{footer(affiliate_disclosure=True)}
{cf_analytics()}
</body>
</html>'''


def main():
    if not DATA_PATH.exists():
        print('  ERROR: data/cert-comparisons.json not found.')
        return

    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    certs = data.get('certifications', {})
    comparisons = data.get('comparisons', [])

    if not comparisons:
        print('  No comparisons found.')
        return

    COMP_DIR.mkdir(exist_ok=True)

    _SLUG_CHARS = set('abcdefghijklmnopqrstuvwxyz0123456789-')

    # Generate individual comparison pages
    for comp in comparisons:
        slug = comp['slug']
        if not slug or set(slug) - _SLUG_CHARS:
            raise ValueError(f'Invalid comparison slug {slug!r}: must be [a-z0-9-]+')
        html = generate_comparison_page(comp, certs)
        out_path = COMP_DIR / f"{slug}.html"
        out_path.write_text(html, encoding='utf-8')

    print(f'  GENERATED {len(comparisons)} comparison pages.')

    # Generate index page
    index_html = generate_index_page(comparisons, certs)
    (COMP_DIR / 'index.html').write_text(index_html, encoding='utf-8')
    print('  GENERATED comparisons/index.html')

    # Sitemap is managed by scripts/generate_sitemap.py — run it after adding new comparisons.
    print('  NOTE: run `python3 scripts/generate_sitemap.py` to refresh sitemap.xml.')

    print(f'\n  Done. {len(comparisons) + 1} files in comparisons/.')


if __name__ == '__main__':
    main()
