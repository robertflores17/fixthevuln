"""
FixTheVuln — Shared HTML Templates

All generators import from here instead of defining their own boilerplate.
One nav. One footer. One share bar. One source of truth.
"""

import json
from .constants import (
    STYLE_CSS_VERSION, QUIZ_CSS_VERSION, COMPARISON_CSS_VERSION,
    SITE_NAME, SITE_URL, OG_IMAGE, CYBERFOLIO_URL,
    CF_ANALYTICS_TOKEN, FAVICON_SVG,
)


# ---------------------------------------------------------------------------
# Escape Helpers
# ---------------------------------------------------------------------------

def esc(text):
    """Escape for HTML content and attributes."""
    if not text:
        return ''
    return (text
            .replace('&', '&amp;')
            .replace('"', '&quot;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace("'", '&#039;'))


def json_esc(text):
    """Escape for JSON string values inside <script> blocks."""
    if not text:
        return ''
    return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')


# ---------------------------------------------------------------------------
# Navigation (standardized .site-nav — used by ALL generators)
# ---------------------------------------------------------------------------

def nav(depth=0):
    """Return the site navigation HTML.

    Args:
        depth: directory depth from site root (0 = root, 1 = /comparisons/, etc.)
               Used to prefix relative hrefs.
    """
    prefix = '../' * depth
    return f"""<nav class="site-nav">
    <div class="container">
        <a href="{'/' if depth == 0 else prefix}" class="site-nav-logo">{SITE_NAME}</a>
        <button class="nav-toggle" aria-label="Menu" onclick="this.classList.toggle('active');this.parentElement.querySelector('.site-nav-links').classList.toggle('open')"><span></span><span></span><span></span></button>
        <div class="site-nav-links">
            <a href="{prefix}guides.html">Guides</a>
            <a href="{prefix}tools.html">Tools</a>
            <a href="{prefix}compliance.html">Compliance</a>
            <a href="{prefix}resources.html">Resources</a>
            <a href="{prefix}practice-tests.html">Quizzes</a>
            <a href="{prefix}career-paths.html">Career Paths</a>
            <a href="{prefix}blog/">Blog</a>
            <a href="/store/store.html" style="background: linear-gradient(135deg, #2563eb, #7c3aed); color: white; padding: .35rem .75rem; border-radius: 6px; font-size: .85rem; font-weight: 600; text-decoration: none;">Store</a>
        </div>
    </div>
</nav>"""


# ---------------------------------------------------------------------------
# Social Share Bar
# ---------------------------------------------------------------------------

def share_bar():
    """Return the social share bar (LinkedIn, Twitter/X, Reddit, Copy Link)."""
    return """<!-- Social Share Bar -->
<div class="share-bar">
    <a class="share-linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=" onclick="this.href+=encodeURIComponent(window.location.href)" target="_blank" rel="noopener" title="Share on LinkedIn">
        <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
    </a>
    <a class="share-twitter" href="https://twitter.com/intent/tweet?url=" onclick="this.href='https://twitter.com/intent/tweet?url='+encodeURIComponent(window.location.href)+'&text='+encodeURIComponent(document.title)" target="_blank" rel="noopener" title="Share on X/Twitter">
        <svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    </a>
    <a class="share-reddit" href="https://reddit.com/submit?url=" onclick="this.href='https://reddit.com/submit?url='+encodeURIComponent(window.location.href)+'&title='+encodeURIComponent(document.title)" target="_blank" rel="noopener" title="Share on Reddit">
        <svg viewBox="0 0 24 24"><path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 0-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"/></svg>
    </a>
    <a class="share-copy" href="javascript:void(0)" onclick="navigator.clipboard.writeText(window.location.href).then(()=>{this.title='Copied!';setTimeout(()=>this.title='Copy link',2000)})" title="Copy link">
        <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </a>
</div>"""


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

def footer(affiliate_disclosure=False, quiz_disclaimer=None):
    """Return the site footer.

    Args:
        affiliate_disclosure: Include affiliate links disclosure paragraph.
        quiz_disclaimer: Vendor name for quiz disclaimer (e.g., "CompTIA").
                         If None, no disclaimer is shown.
    """
    extras = ''
    if affiliate_disclosure:
        extras += """
        <p style="font-size: 0.85rem; color: #999; margin-top: 1rem;">
            <strong>Affiliate Disclosure:</strong> Some links on this site are affiliate links. We may earn a commission when you purchase through these links at no additional cost to you. We only recommend tools and services we trust.
        </p>"""
    if quiz_disclaimer:
        extras += f"""
        <p style="font-size: 0.8rem; color: #888; margin-top: 0.75rem;"><strong>Disclaimer:</strong> These practice questions are independently created for educational purposes only and are not official exam questions. {esc(quiz_disclaimer)}\u00ae trademarks belong to their respective owners. FixTheVuln is not affiliated with or endorsed by {esc(quiz_disclaimer)}. Use this quiz as a supplemental study aid.</p>"""

    return f"""<footer>
    <div class="container">
        <p>&copy; 2026 {SITE_NAME}. Practical Vulnerability Remediation.</p>
        <p>Study Planners: <a href="/store/store.html">{SITE_NAME} Store</a> | Career Tools: <a href="{CYBERFOLIO_URL}" target="_blank" rel="noopener">CyberFolio</a></p>{extras}
    </div>
</footer>"""


# ---------------------------------------------------------------------------
# Cloudflare Analytics
# ---------------------------------------------------------------------------

def cf_analytics():
    """Return the Cloudflare Web Analytics script tag."""
    return (
        f'<!-- Cloudflare Web Analytics -->'
        f'<script defer src=\'https://static.cloudflareinsights.com/beacon.min.js\' '
        f'data-cf-beacon=\'{{"token": "{CF_ANALYTICS_TOKEN}"}}\'></script>'
        f'<!-- End Cloudflare Web Analytics -->'
    )


# ---------------------------------------------------------------------------
# <head> Builder
# ---------------------------------------------------------------------------

def html_head(title, description, canonical, *,
              keywords=None, extra_css=None, schema_blocks=None, depth=0,
              rss=True):
    """Build the <head> section with meta, OG, Twitter, favicon, CSS, schema.

    Args:
        title: Page title (appears in <title> and OG/Twitter).
        description: Meta description.
        canonical: Full canonical URL (e.g., https://fixthevuln.com/path.html).
        keywords: Optional meta keywords string.
        extra_css: List of additional CSS hrefs (e.g., ['quiz.css?v=3']).
        schema_blocks: List of JSON-LD schema strings to embed.
        depth: Directory depth from root (for CSS path prefix).
        rss: Include RSS link (default True).
    """
    prefix = '../' * depth
    full_title = f"{title} - {SITE_NAME}"
    desc_esc = esc(description)
    title_esc = esc(full_title)

    keywords_tag = f'\n    <meta name="keywords" content="{esc(keywords)}">' if keywords else ''

    extra_css_tags = ''
    if extra_css:
        for css in extra_css:
            extra_css_tags += f'\n    <link rel="stylesheet" href="{prefix}{css}">'

    schema_tags = ''
    if schema_blocks:
        for schema in schema_blocks:
            safe_schema = schema.replace('</', '<\\/')
            schema_tags += f'\n    <script type="application/ld+json">\n{safe_schema}\n    </script>'

    rss_tag = f'\n    <link rel="alternate" type="application/rss+xml" title="{SITE_NAME} Blog" href="{prefix}blog/feed.xml">' if rss else ''

    return f"""<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <link rel="preconnect" href="https://static.cloudflareinsights.com" crossorigin>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc_esc}">{keywords_tag}
    <title>{title_esc}</title>
    <link rel="canonical" href="{esc(canonical)}">
    <meta property="og:title" content="{title_esc}">
    <meta property="og:description" content="{desc_esc}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{esc(canonical)}">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title_esc}">
    <meta name="twitter:description" content="{desc_esc}">
    <meta name="twitter:image" content="{OG_IMAGE}">
    <link rel="icon" type="image/svg+xml" href="{FAVICON_SVG}">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="stylesheet" href="{prefix}style.min.css?v={STYLE_CSS_VERSION}">{extra_css_tags}{schema_tags}{rss_tag}
</head>"""


# ---------------------------------------------------------------------------
# Schema.org JSON-LD Helpers
# ---------------------------------------------------------------------------

def breadcrumb_schema(items):
    """Build BreadcrumbList JSON-LD.

    Args:
        items: List of (name, url) tuples. Last item has no URL (current page).
               Example: [("Home", "https://fixthevuln.com/"), ("Guides", "https://fixthevuln.com/guides.html"), ("NIST Framework", None)]
    """
    list_items = []
    for i, (name, url) in enumerate(items, 1):
        item = {"@type": "ListItem", "position": i, "name": name}
        if url:
            item["item"] = url
        list_items.append(item)

    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": list_items,
    }, indent=8)


def faq_schema(questions):
    """Build FAQPage JSON-LD.

    Args:
        questions: List of (question, answer) tuples.
    """
    entities = []
    for q, a in questions:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a,
            }
        })

    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }, indent=8)


def article_schema(headline, description, date_published, date_modified=None):
    """Build TechArticle JSON-LD.

    Args:
        headline: Article title.
        description: Article description.
        date_published: ISO date string (YYYY-MM-DD).
        date_modified: ISO date string. Defaults to date_published.
    """
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": headline,
        "description": description,
        "datePublished": date_published,
        "dateModified": date_modified or date_published,
        "author": {"@type": "Organization", "name": f"{SITE_NAME} Team", "url": SITE_URL},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
    }, indent=8)


# ---------------------------------------------------------------------------
# Full Page Wrapper
# ---------------------------------------------------------------------------

def page_wrapper(title, description, canonical, content, *,
                 keywords=None, extra_css=None, schema_blocks=None,
                 depth=0, include_share_bar=True,
                 affiliate_disclosure=False, quiz_disclaimer=None,
                 rss=True, extra_body_end=''):
    """Assemble a complete HTML page.

    Args:
        title: Page title.
        description: Meta description.
        canonical: Full canonical URL.
        content: Main page content HTML (everything between nav and footer).
        keywords: Optional meta keywords.
        extra_css: Additional CSS files list.
        schema_blocks: JSON-LD schema strings list.
        depth: Directory depth from root.
        include_share_bar: Show social share bar (default True).
        affiliate_disclosure: Show affiliate disclosure in footer.
        quiz_disclaimer: Vendor name for quiz disclaimer.
        rss: Include RSS link.
        extra_body_end: Extra HTML before </body> (e.g., <script> tags).
    """
    head = html_head(title, description, canonical,
                     keywords=keywords, extra_css=extra_css,
                     schema_blocks=schema_blocks, depth=depth, rss=rss)
    nav_html = nav(depth=depth)
    share = share_bar() if include_share_bar else ''
    foot = footer(affiliate_disclosure=affiliate_disclosure,
                  quiz_disclaimer=quiz_disclaimer)
    analytics = cf_analytics()

    return f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
{nav_html}
{share}
{content}
{foot}
{analytics}
{extra_body_end}
</body>
</html>"""
