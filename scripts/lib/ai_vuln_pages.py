"""Renders one ai-vulnerabilities/<id>.html page from a data/ai-vuln-content.json
entry. The only place technique-page HTML is assembled — generate_ai_vuln_pages.py
(Task 4) is the sole caller. Depth is always 1 (ai-vulnerabilities/ is one
directory below site root), matching cve/ and blog/.
"""
from .templates import page_wrapper, esc, breadcrumb_schema, article_schema
from .constants import SITE_URL, SITE_NAME


def _mitigations_html(mitigations):
    items = "\n".join(
        f'                    <li><input type="checkbox"> {esc(m)}</li>'
        for m in mitigations
    )
    return f'''            <h3>Mitigations</h3>
            <div class="remediation">
                <ul>
{items}
                </ul>
            </div>'''


def _sections_html(sections):
    parts = []
    for s in sections:
        # s["html"] originates from the one-time verbatim migration (Task 2) or
        # from fixthevuln-lead editing data/ai-vuln-content.json under the
        # Marlowe/Sable/Griggs review loop — never raw user input — so it is
        # trusted markup, same trust level as every other *_html field the
        # existing generators (generate_cve_pages.py) already render as-is.
        parts.append(f'            <h3>{esc(s["heading"])}</h3>\n{s["html"]}')
    return "\n".join(parts)


def _related_links_html(related_links):
    if not related_links:
        return ""
    links = "\n".join(
        f'<a href="{esc(l["href"])}">{esc(l["text"])} &rarr;</a>'
        for l in related_links
    )
    return f'\n            <p>{links}</p>'


def render_technique_page(entry, hub_url, hub_name, last_updated):
    # Unescaped — passed to page_wrapper/html_head, which escapes it once for
    # <title>/meta (and json.dumps below, for which raw text is correct).
    # Do NOT esc() here or it double-escapes (e.g. "&amp;" -> "&amp;amp;").
    title = f'{entry["code"]}: {entry["name"]}'
    # Escaped — used directly in the body below, which doesn't route through
    # html_head's own escaping.
    heading = f'{esc(entry["code"])}: {esc(entry["name"])}'
    canonical = f'{SITE_URL}/ai-vulnerabilities/{entry["id"]}.html'
    description = f'{title} — risk level {entry["risk_level"]}. Part of the {hub_name} technique library on {SITE_NAME}.'

    content = f'''    <header>
        <div class="container">
            <a href="../index.html" style="text-decoration: none; color: inherit;"><h1>{SITE_NAME}</h1></a>
            <p class="tagline">{heading}</p>
        </div>
    </header>

    <main class="container">
        <a href="../{hub_url.lstrip('/')}" class="back-link">&larr; Back to {esc(hub_name)}</a>

        <section class="vulnerability-card">
            <h2>{heading}</h2>
            <p><strong>Risk Level:</strong> <span style="color: {esc(entry["risk_color"])}; font-weight: 700;">{esc(entry["risk_level"])}</span></p>
            {entry.get("summary_html", "")}
{_sections_html(entry["sections"])}
{_mitigations_html(entry["mitigations"])}
{_related_links_html(entry.get("related_links", []))}
        </section>
    </main>'''

    schema_blocks = [
        breadcrumb_schema([
            ("Home", f"{SITE_URL}/"),
            (hub_name, f"{SITE_URL}/{hub_url.lstrip('/')}"),
            (title, None),
        ]),
        article_schema(title, description, last_updated),
    ]

    return page_wrapper(
        title=title,
        description=description,
        canonical=canonical,
        content=content,
        depth=1,
        schema_blocks=schema_blocks,
    )
