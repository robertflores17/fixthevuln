#!/usr/bin/env python3
"""
OWASP WSTG Page Generator for FixTheVuln.com
Reads data/wstg-data.json and generates hub page + 12 category pages.
Also updates sitemap.xml with WSTG entries.

Usage:
    python3 scripts/generate_wstg_pages.py
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.templates import (html_head, nav, share_bar, footer, cf_analytics,
                           article_schema, breadcrumb_schema, esc)
from lib.constants import SITE_URL
from entity_extractor import OWASP_LABELS, OWASP_COLORS

DATA_PATH = REPO_ROOT / 'data' / 'wstg-data.json'
WSTG_DIR = REPO_ROOT / 'wstg'
SITEMAP_PATH = REPO_ROOT / 'sitemap.xml'
TODAY = date.today().isoformat()


def escape_html(text):
    """Escape HTML special characters (alias for esc)."""
    return esc(str(text))


def build_owasp_badges(owasp_refs):
    """Render OWASP Top 10 badge pills linking to owasp-top10.html."""
    if not owasp_refs:
        return ''
    badges = []
    for ref in owasp_refs:
        label = OWASP_LABELS.get(ref, ref)
        color = OWASP_COLORS.get(ref, '#6c757d')
        badges.append(
            f'<a href="../owasp-top10.html" style="display:inline-block;background:{color};color:white;'
            f'padding:0.25rem 0.75rem;border-radius:4px;font-size:0.8rem;font-weight:600;'
            f'text-decoration:none;margin:0.15rem;" title="{escape_html(label)}">{escape_html(ref)}</a>'
        )
    return '<div style="display:flex;flex-wrap:wrap;gap:0.25rem;margin:1rem 0;">' + ''.join(badges) + '</div>'


def build_cwe_badges(cwes):
    """Render CWE badge pills."""
    if not cwes:
        return ''
    badges = []
    for cwe in cwes:
        badges.append(
            f'<span style="display:inline-block;background:var(--bg-tertiary);color:var(--text-secondary);'
            f'padding:0.2rem 0.6rem;border-radius:4px;font-size:0.75rem;font-weight:600;'
            f'border:1px solid var(--border-color);margin:0.1rem;">{escape_html(cwe)}</span>'
        )
    return ' '.join(badges)


def build_cert_badges(certs):
    """Render certification relevance badges."""
    if not certs:
        return ''
    # Map cert names to cert page slugs
    CERT_SLUGS = {
        'Security+': 'comptia-security-plus', 'CEH': 'ec-ceh', 'OSCP': 'offsec-oscp',
        'GPEN': 'giac-gpen', 'CISSP': 'isc2-cissp', 'GWAPT': None,
        'CySA+': 'comptia-cysa-plus', 'PenTest+': 'comptia-pentest-plus',
        'CASP+': 'comptia-casp-plus', 'CCSP': 'isc2-ccsp',
    }
    badges = []
    for cert in certs:
        slug = CERT_SLUGS.get(cert)
        if slug:
            badges.append(
                f'<a href="../certs/{slug}.html" style="display:inline-block;background:var(--bg-secondary);'
                f'color:var(--text-primary);padding:0.3rem 0.8rem;border-radius:6px;font-size:0.8rem;'
                f'font-weight:600;text-decoration:none;border:1px solid var(--border-color);">{escape_html(cert)}</a>'
            )
        else:
            badges.append(
                f'<span style="display:inline-block;background:var(--bg-secondary);color:var(--text-primary);'
                f'padding:0.3rem 0.8rem;border-radius:6px;font-size:0.8rem;font-weight:600;'
                f'border:1px solid var(--border-color);">{escape_html(cert)}</span>'
            )
    return '<div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin:0.75rem 0;">' + ''.join(badges) + '</div>'


def build_difficulty_badge(difficulty):
    """Render difficulty level badge."""
    colors = {
        'Beginner': '#28a745',
        'Intermediate': '#ffc107',
        'Advanced': '#dc3545',
    }
    color = colors.get(difficulty, '#6c757d')
    text_color = '#000' if difficulty == 'Intermediate' else '#fff'
    return (f'<span style="display:inline-block;background:{color};color:{text_color};'
            f'padding:0.2rem 0.6rem;border-radius:4px;font-size:0.75rem;font-weight:600;">'
            f'{escape_html(difficulty)}</span>')


def build_test_section(test):
    """Generate HTML for a single test case section."""
    test_id = test['id']
    anchor = test_id.lower()
    name = test.get('short_name', test['name'])
    desc = test.get('description', '')
    why = test.get('why_it_matters', '')
    checks = test.get('what_to_check', [])
    tools = test.get('common_tools', [])
    cwes = test.get('related_cwes', [])
    difficulty = test.get('difficulty', '')

    checks_html = '\n'.join(
        f'                    <li>{escape_html(c)}</li>' for c in checks
    )

    tools_html = ' '.join(
        f'<span style="display:inline-block;background:var(--bg-tertiary);padding:0.2rem 0.5rem;'
        f'border-radius:4px;font-size:0.75rem;border:1px solid var(--border-color);">{escape_html(t)}</span>'
        for t in tools
    )

    cwe_html = build_cwe_badges(cwes)
    diff_badge = build_difficulty_badge(difficulty) if difficulty else ''

    return f'''
            <div id="{anchor}" style="background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:1.5rem;margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;margin-bottom:0.75rem;">
                    <h3 style="margin:0;font-size:1.05rem;color:var(--text-primary);">{escape_html(test_id)}: {escape_html(name)}</h3>
                    {diff_badge}
                </div>
                <p style="color:var(--text-secondary);line-height:1.6;margin-bottom:0.75rem;">{escape_html(desc)}</p>
                <div style="background:var(--bg-tertiary);border-left:4px solid #667eea;padding:0.75rem 1rem;border-radius:0 6px 6px 0;margin-bottom:0.75rem;">
                    <strong>Why it matters:</strong> {escape_html(why)}
                </div>
                <h4 style="font-size:0.9rem;margin-bottom:0.5rem;">What to Check</h4>
                <ul style="color:var(--text-secondary);line-height:1.8;padding-left:1.25rem;margin-bottom:0.75rem;">
{checks_html}
                </ul>
                <div style="display:flex;flex-wrap:wrap;gap:0.75rem;align-items:center;">
                    <div><strong style="font-size:0.8rem;">Tools:</strong> {tools_html}</div>
                </div>
                {f'<div style="margin-top:0.5rem;">{cwe_html}</div>' if cwe_html else ''}
            </div>'''


def build_quick_ref_table(tests):
    """Generate quick-reference table for a category page."""
    rows = []
    for t in tests:
        anchor = t['id'].lower()
        name = t.get('short_name', t['name'])
        cwes = ', '.join(t.get('related_cwes', []))
        diff = t.get('difficulty', '')
        rows.append(
            f'                    <tr>'
            f'<td style="font-weight:600;white-space:nowrap;">{escape_html(t["id"])}</td>'
            f'<td><a href="#{anchor}" style="color:var(--accent-color);text-decoration:none;">{escape_html(name)}</a></td>'
            f'<td style="font-size:0.8rem;color:var(--text-muted);">{escape_html(cwes)}</td>'
            f'<td>{build_difficulty_badge(diff)}</td>'
            f'</tr>'
        )
    return '\n'.join(rows)


def generate_category_page(cat, all_categories):
    """Generate a complete WSTG category page."""
    code = cat['code']
    slug = cat['slug']
    name = cat['name']
    icon = cat.get('icon', '')
    summary = cat.get('summary', '')
    intro = cat.get('intro', summary)
    tests = cat.get('tests', [])
    owasp_refs = cat.get('owasp_top10_refs', [])
    cwes = cat.get('related_cwes', [])
    certs = cat.get('relevant_certs', [])
    difficulty = cat.get('difficulty', '')
    faq_items = cat.get('faq_items', [])

    page_title = f'{code}: {name} — OWASP Testing Guide | FixTheVuln'
    meta_desc = f'OWASP WSTG {name}: {len(tests)} security test cases. {summary}'
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + '...'

    # Build sections
    owasp_badges = build_owasp_badges(owasp_refs)
    cert_badges = build_cert_badges(certs)
    test_sections = '\n'.join(build_test_section(t) for t in tests)
    quick_ref_rows = build_quick_ref_table(tests)

    # FAQ schema
    faq_schema = ''
    faq_visible = ''
    if faq_items:
        schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": f["a"]}
                }
                for f in faq_items
            ]
        }
        faq_schema = f'''    <script type="application/ld+json">
{json.dumps(schema, indent=8, ensure_ascii=False)}
    </script>'''
        faq_visible = '\n'.join(
            f'            <details class="faq-item">\n'
            f'                <summary>{escape_html(f["q"])}</summary>\n'
            f'                <p>{escape_html(f["a"])}</p>\n'
            f'            </details>'
            for f in faq_items
        )

    # Related categories (pick 3-4 others)
    related = [c for c in all_categories if c['code'] != code][:4]
    related_cards = '\n'.join(
        f'                <a href="{c["slug"]}.html" style="display:block;padding:1rem;background:var(--bg-secondary);'
        f'border-radius:8px;text-decoration:none;color:var(--text-primary);border:1px solid var(--border-color);">'
        f'<strong>{escape_html(c["code"])}</strong><br>'
        f'<span style="font-size:0.85rem;color:var(--text-muted);">{escape_html(c["name"])}</span></a>'
        for c in related
    )

    cat_canonical = f'{SITE_URL}/wstg/{slug}.html'
    cat_keywords = f'{escape_html(code)}, OWASP WSTG, {escape_html(name)}, web security testing, penetration testing, {", ".join(certs)}'
    cat_schemas = [
        article_schema(f'{code}: {name} — OWASP Web Security Testing Guide', meta_desc, TODAY),
        breadcrumb_schema([("Home", f"{SITE_URL}/"), ("Guides", f"{SITE_URL}/guides.html"), ("OWASP WSTG", f"{SITE_URL}/wstg/"), (name, None)]),
    ]
    if faq_schema:
        # Extract JSON from the script tag wrapper
        faq_json_raw = faq_schema.replace('    <script type="application/ld+json">\n', '').replace('\n    </script>', '')
        cat_schemas.append(faq_json_raw)
    cat_head = html_head(page_title, meta_desc, cat_canonical,
                         keywords=cat_keywords, schema_blocks=cat_schemas, depth=1)

    return f'''<!DOCTYPE html>
<html lang="en">
{cat_head}
<body>
{nav(depth=1)}
{share_bar()}

    <header class="content-header">
        <div class="container">
            <h1>{icon} {escape_html(code)}: {escape_html(name)}</h1>
            <p>OWASP Web Security Testing Guide v4.2</p>
        </div>
    </header>

    <main class="container">
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; justify-content: center; padding: 0.75rem; margin-bottom: 1rem; font-size: 0.8rem; color: var(--text-muted); border-bottom: 1px solid var(--border-color);">
            <span>By <strong>FixTheVuln Team</strong></span>
            <span aria-hidden="true">&middot;</span>
            <span>Sources: OWASP WSTG v4.2</span>
        </div>
        <div class="content-wrapper">

            <a href="index.html" class="back-link">&larr; OWASP WSTG Guide</a>

            <p>{escape_html(intro)}</p>

            <div style="display:flex;flex-wrap:wrap;gap:0.75rem;align-items:center;margin:1rem 0;">
                <span style="font-weight:600;color:var(--text-muted);font-size:0.85rem;">Difficulty:</span> {build_difficulty_badge(difficulty)}
                <span style="font-weight:600;color:var(--text-muted);font-size:0.85rem;margin-left:0.5rem;">{len(tests)} test cases</span>
            </div>

            <h2>OWASP Top 10 Mapping</h2>
            <p>This testing category relates to the following OWASP Top 10 2021 categories:</p>
            {owasp_badges}

            <h2>Quick Reference</h2>
            <div style="overflow-x: auto;">
            <table class="compare-table">
                <thead>
                    <tr>
                        <th>Test ID</th>
                        <th>Name</th>
                        <th>CWEs</th>
                        <th>Difficulty</th>
                    </tr>
                </thead>
                <tbody>
{quick_ref_rows}
                </tbody>
            </table>
            </div>

            <h2>Detailed Test Cases</h2>
{test_sections}

            <h2>Relevant Certifications</h2>
            <p>The following certifications cover {escape_html(name).lower()} concepts:</p>
            {cert_badges}

            <h2>Frequently Asked Questions</h2>
{faq_visible}

        </div>

        <!-- CyberFolio CTA -->
        <div style="border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 12px; text-align: center; margin-top: 1.5rem;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.5; margin-bottom: 0.3rem;">CyberFolio</p>
            <p style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Mastering web security testing? Showcase your skills.</p>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">Build a shareable cybersecurity portfolio that highlights your certifications, projects, and skills &mdash; free.</p>
            <a href="https://cyberfolio.io" style="display:inline-block;background:#06b6d4;color:white;padding:0.6rem 1.5rem;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.95rem;" target="_blank" rel="noopener">Build Your Portfolio &rarr;</a>
        </div>

        <!-- Related Categories -->
        <section style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px;">
            <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Related WSTG Categories</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
{related_cards}
            </div>
        </section>

        <a href="../index.html" class="back-link">&larr; Back to Home</a>
        <a href="index.html" class="back-link" style="margin-left: 1rem;">&larr; All WSTG Categories</a>
    </main>

{footer(affiliate_disclosure=True)}
{cf_analytics()}
</body>
</html>'''


def generate_index_page(categories, meta):
    """Generate the WSTG hub/index page."""
    total_tests = meta.get('total_tests', 112)
    total_cats = meta.get('total_categories', 12)
    version = meta.get('version', '4.2')

    cards = []
    for cat in categories:
        test_count = len(cat.get('tests', []))
        cards.append(
            f'            <a href="{cat["slug"]}.html" style="display:block;padding:1.25rem;background:var(--bg-secondary);'
            f'border-radius:10px;text-decoration:none;color:var(--text-primary);border:1px solid var(--border-color);'
            f'transition:border-color 0.2s,transform 0.2s;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">'
            f'<span style="font-weight:700;font-size:1.05rem;">{cat.get("icon", "")} {escape_html(cat["code"])}</span>'
            f'<span style="color:#667eea;font-size:0.85rem;">{test_count} tests &rarr;</span>'
            f'</div>'
            f'<p style="font-size:0.95rem;font-weight:600;margin:0 0 0.25rem;">{escape_html(cat["name"])}</p>'
            f'<p style="font-size:0.8rem;color:var(--text-muted);margin:0;">{escape_html(cat.get("summary", ""))}</p>'
            f'</a>'
        )
    cards_html = '\n'.join(cards)

    idx_desc = f'OWASP Web Security Testing Guide (WSTG) v{version} -- {total_tests} security test cases across {total_cats} categories. Free educational guides for Security+, CEH, OSCP, and GPEN certification prep.'
    idx_keywords = 'OWASP WSTG, web security testing guide, penetration testing methodology, OWASP testing, web application security, Security+, CEH, OSCP'
    idx_schemas = [breadcrumb_schema([("Home", f"{SITE_URL}/"), ("Guides", f"{SITE_URL}/guides.html"), ("OWASP WSTG", None)])]
    idx_head = html_head(f'OWASP Web Security Testing Guide (WSTG) &mdash; {total_tests} Test Cases', idx_desc,
                         f'{SITE_URL}/wstg/', keywords=idx_keywords, schema_blocks=idx_schemas, depth=1)

    return f'''<!DOCTYPE html>
<html lang="en">
{idx_head}
<body>
{nav(depth=1)}
{share_bar()}

    <header class="content-header">
        <div class="container">
            <h1>OWASP Web Security Testing Guide</h1>
            <p>{total_tests} security test cases across {total_cats} categories</p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.25rem;">WSTG v{version}</p>
        </div>
    </header>

    <main class="container">
        <section class="intro">
            <h2>What is the OWASP WSTG?</h2>
            <p>The OWASP Web Security Testing Guide (WSTG) is the premier open-source resource for web application security testing methodology. It provides a complete framework of {total_tests} test cases organized into {total_cats} categories, covering everything from information gathering and authentication testing to business logic flaws and API security.</p>
            <p>Whether you're studying for Security+, CEH, OSCP, or GPEN — or conducting professional penetration tests — the WSTG provides the systematic approach you need.</p>
        </section>

        <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(320px, 1fr));gap:1rem;margin:2rem 0;">
{cards_html}
        </div>

        <!-- Related OWASP Content -->
        <section style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px;">
            <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Related OWASP Content</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
                <a href="../owasp-top10.html" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">OWASP Top 10 2021</a>
                <a href="../owasp-llm-top10.html" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">OWASP LLM Top 10</a>
                <a href="../api-security.html" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">API Security Best Practices</a>
            </div>
        </section>

        <!-- CyberFolio CTA -->
        <div style="border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 12px; text-align: center; margin-top: 1.5rem;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.5; margin-bottom: 0.3rem;">CyberFolio</p>
            <p style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Building security testing skills? Track your progress.</p>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">Build a shareable cybersecurity portfolio that highlights your certifications, projects, and skills &mdash; free.</p>
            <a href="https://cyberfolio.io" style="display:inline-block;background:#06b6d4;color:white;padding:0.6rem 1.5rem;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.95rem;" target="_blank" rel="noopener">Build Your Portfolio &rarr;</a>
        </div>

        <a href="../index.html" class="back-link">&larr; Back to Home</a>
    </main>

{footer(affiliate_disclosure=True)}
{cf_analytics()}
</body>
</html>'''


def update_sitemap(categories):
    """Update sitemap.xml with WSTG entries."""
    sitemap_text = SITEMAP_PATH.read_text(encoding='utf-8')

    # Remove any existing WSTG entries
    sitemap_text = re.sub(
        r'\n  <!-- WSTG Pages -->.*?(?=\n  <!--|\n</urlset>)',
        '',
        sitemap_text,
        flags=re.DOTALL,
    )

    # Build WSTG entries
    entries = f'\n  <!-- WSTG Pages -->\n  <url>\n    <loc>https://fixthevuln.com/wstg/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>'

    for cat in categories:
        entries += f'''
  <url>
    <loc>https://fixthevuln.com/wstg/{cat["slug"]}.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>'''

    # Insert before </urlset>
    sitemap_text = sitemap_text.replace('</urlset>', entries + '\n</urlset>')
    SITEMAP_PATH.write_text(sitemap_text, encoding='utf-8')
    print(f'  SITEMAP updated with {len(categories) + 1} WSTG entries.')


def main():
    if not DATA_PATH.exists():
        print('  ERROR: data/wstg-data.json not found.')
        return

    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    meta = data.get('meta', {})
    categories = data.get('categories', [])

    if not categories:
        print('  No categories found.')
        return

    WSTG_DIR.mkdir(exist_ok=True)

    # Generate individual category pages
    for cat in categories:
        html = generate_category_page(cat, categories)
        out_path = WSTG_DIR / f"{cat['slug']}.html"
        out_path.write_text(html, encoding='utf-8')

    print(f'  GENERATED {len(categories)} WSTG category pages.')

    # Generate index page
    index_html = generate_index_page(categories, meta)
    (WSTG_DIR / 'index.html').write_text(index_html, encoding='utf-8')
    print('  GENERATED wstg/index.html')

    # Update sitemap
    update_sitemap(categories)

    total_tests = sum(len(c.get('tests', [])) for c in categories)
    print(f'\n  Done. {len(categories) + 1} files in wstg/. ({total_tests} test cases total)')


if __name__ == '__main__':
    main()
