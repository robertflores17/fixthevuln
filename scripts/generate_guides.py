#!/usr/bin/env python3
"""Generated 11 guide pages for AI Security, GRC, and Blue Team content gaps.

PAGE_CONFIGS is now empty. All 11 entries (the original 9 plus mlsecops.html
and threat-hunting.html) drifted from their live pages, which were hand-edited
and post-processed by inject_navbar_rss.py, inject_blog_links.py,
inject_store_ctas.py and inject_error_reporter.py, none of which this script
knew about. A run on 2026-09-17 produced a net -634 lines by reverting all of
it (see tasks/lessons.md). Entries were retired rather than resynced since no
other script imports this module or PAGE_CONFIGS.

main() still chains generate_ai_vuln_pages.main() so the AI-VULN-GRID blocks
on owasp-llm-top10.html and agentic-skills-top-10.html stay repopulated from
data/ai-vuln-content.json — that path reads/writes those pages directly and
doesn't depend on PAGE_CONFIGS.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.templates import page_wrapper, esc, breadcrumb_schema, article_schema, faq_schema
from lib.constants import SITE_URL


def build_related(items):
    """Build related resources cards."""
    cards = []
    for url, emoji, title, desc in items:
        cards.append(f'''                <a href="{url}" style="background: var(--bg-tertiary, #f8f9fa); color: var(--text-primary, #333); padding: 1.25rem; border-radius: 8px; text-decoration: none; border: 2px solid var(--border-color, #e0e0e0);">
                    <strong style="display: block; margin-bottom: 0.5rem; color: var(--accent-primary, #667eea);">{emoji} {esc(title)}</strong>
                    <span style="font-size: 0.9rem; color: var(--text-muted, #666);">{esc(desc)}</span>
                </a>''')
    return '\n'.join(cards)


def build_quiz_links(quiz_links):
    """Build quiz link section."""
    links = ''
    for url, text in quiz_links:
        links += f'                <a href="{url}" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">{esc(text)}</a>\n'
    return f'''            <!-- Quiz Links -->
            <section style="margin-top: 1.5rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px;">
                <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Test Your Knowledge</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
{links}                </div>
            </section>'''


def generate_page(cfg):
    """Generate a complete HTML page from config dict."""
    filename = cfg['filename']
    title = cfg['title']
    desc = cfg['description']
    keywords = cfg['keywords']
    tagline = cfg['tagline']
    bc_name, bc_url = cfg['breadcrumb_parent']
    short_title = cfg.get('short_title', tagline)
    page_css = cfg.get('page_css', '')
    content_html = cfg['content_html']
    quiz_links = cfg.get('quiz_links', [])
    faq_items = cfg.get('faq_items', [])
    related = cfg.get('related', [])
    cta_heading = cfg.get('cta_heading', 'Explore More Security Guides')

    # Build schema blocks
    canonical = f'{SITE_URL}/{filename}'
    schemas = [
        breadcrumb_schema([
            ("Home", f"{SITE_URL}/"),
            (bc_name, f"{SITE_URL}/{bc_url}"),
            (short_title, None),
        ]),
        article_schema(title, desc, "2026-03-24"),
    ]
    if faq_items:
        schemas.append(faq_schema(faq_items))

    # Build quiz section
    quiz_section = ''
    if quiz_links:
        quiz_section = '\n' + build_quiz_links(quiz_links) + '\n'

    # Build related section
    related_cards = build_related(related) if related else ''
    related_section = ''
    if related_cards:
        related_section = f'''
        <!-- Related Content -->
        <section style="margin-top: 3rem; padding-top: 2rem; border-top: 2px solid var(--border-color, #e0e0e0);">
            <h2 style="margin-bottom: 1.5rem;">Related Resources</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
{related_cards}
            </div>
        </section>
'''

    # Page-specific inline CSS
    css_style = f'\n    <style>\n{page_css}\n    </style>' if page_css else ''

    # Assemble page content (everything between nav/share_bar and footer)
    content = f"""{css_style}
    <header>
        <div class="container">
            <a href="index.html" style="text-decoration: none; color: inherit;"><h1>FixTheVuln</h1></a>
            <p class="tagline">{esc(tagline)}</p>
        </div>
    </header>

    <main class="container">
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; justify-content: center; padding: 0.75rem; margin-bottom: 1rem; font-size: 0.8rem; color: var(--text-muted); border-bottom: 1px solid var(--border-color);">
            <span>By <strong>FixTheVuln Team</strong></span>
            <span aria-hidden="true">&middot;</span>
            <span>Sources: CISA, NVD, OWASP</span>
        </div>
{quiz_section}
        <a href="index.html" class="back-link">&larr; Back to Home</a>

{content_html}

        <section class="cta">
            <h2>{esc(cta_heading)}</h2>
            <p>For comprehensive tutorials and security guides:</p>
            <a href="https://fixthevuln.com" class="cta-button" target="_blank">Visit FixTheVuln.com &rarr;</a>
        </section>
{related_section}
    </main>"""

    return page_wrapper(
        title=title,
        description=desc,
        canonical=canonical,
        content=content,
        keywords=keywords,
        schema_blocks=schemas,
        extra_body_end='  <script src="/js/error-reporter.js?v=1"></script>',
    )


# ── Page Configs & Main ──────────────────────────────────────────────

PAGE_CONFIGS = [
]


def main():
    for cfg in PAGE_CONFIGS:
        html = generate_page(cfg)
        out = REPO / cfg['filename']
        out.write_text(html, encoding='utf-8')
        print(f"  OK  {cfg['filename']}")
    print(f"\nGenerated {len(PAGE_CONFIGS)} pages")

    # The owasp-llm-top10 config ships EMPTY AI-VULN-GRID markers: the ten cards
    # are owned by data/ai-vuln-content.json, not by this file. Without this call
    # the hub ships with an empty grid and all ten technique pages lose their only
    # inbound link — and nothing else catches it, because the markers are still
    # present and the HTML is still valid.
    import generate_ai_vuln_pages
    print("\nRepopulating technique grids...")
    generate_ai_vuln_pages.main()


if __name__ == '__main__':
    main()

