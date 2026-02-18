#!/usr/bin/env python3
"""
Certification Comparison Page Generator for FixTheVuln.com
Reads data/cert-comparisons.json and generates comparison HTML pages + index.
Also updates sitemap.xml with comparison entries.

Usage:
    python3 scripts/generate_comparisons.py
"""

import json
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / 'data' / 'cert-comparisons.json'
COMP_DIR = REPO_ROOT / 'comparisons'
SITEMAP_PATH = REPO_ROOT / 'sitemap.xml'
TODAY = date.today().isoformat()


def escape_html(text):
    """Escape HTML special characters."""
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


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
    meta_desc = f'{title} comparison. {desc[:150]}'

    # Use first cert's Etsy section for CTA
    etsy_section = c1.get('etsy_section', '57227085')

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

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <link rel="preconnect" href="https://static.cloudflareinsights.com" crossorigin>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{escape_html(meta_desc)}">
    <meta name="keywords" content="{escape_html(c1['name'])}, {escape_html(c2['name'])}, certification comparison, {escape_html(c1['vendor'])}, {escape_html(c2['vendor'])}, IT certification">
    <title>{escape_html(page_title)}</title>
    <link rel="canonical" href="https://fixthevuln.com/comparisons/{slug}.html">
    <meta property="og:title" content="{escape_html(page_title)}">
    <meta property="og:description" content="{escape_html(meta_desc)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://fixthevuln.com/comparisons/{slug}.html">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape_html(page_title)}">
    <meta name="twitter:description" content="{escape_html(meta_desc)}">
    <meta name="twitter:image" content="https://fixthevuln.com/og-image.png">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23667eea'/%3E%3Ctext x='50' y='68' font-family='Arial,sans-serif' font-size='60' font-weight='bold' fill='white' text-anchor='middle'%3EF%3C/text%3E%3C/svg%3E">
    <link rel="stylesheet" href="../style.min.css">
    <style>
        .compare-table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; }}
        .compare-table th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.75rem; text-align: center; }}
        .compare-table th:first-child {{ text-align: left; background: #f8f9fa; color: var(--text-primary); }}
        .compare-table td {{ padding: 0.75rem; border-bottom: 1px solid var(--border-color); text-align: center; }}
        .compare-table td:first-child {{ text-align: left; }}
        .compare-table tr:hover {{ background: var(--bg-secondary); }}
        .who-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin: 1.5rem 0; }}
        .who-card {{ background: var(--bg-secondary); padding: 1.5rem; border-radius: 10px; border-top: 4px solid #667eea; }}
        .who-card h4 {{ color: #667eea; margin-bottom: 0.5rem; }}
        @media (max-width: 768px) {{
            .who-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": "{escape_html(title)}: Which Certification Should You Get?",
        "description": "{escape_html(meta_desc)}",
        "datePublished": "{TODAY}",
        "dateModified": "{TODAY}",
        "author": {{ "@type": "Organization", "name": "FixTheVuln Team", "url": "https://fixthevuln.com" }},
        "publisher": {{ "@type": "Organization", "name": "FixTheVuln", "url": "https://fixthevuln.com" }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://fixthevuln.com/" }},
            {{ "@type": "ListItem", "position": 2, "name": "Certification Comparisons", "item": "https://fixthevuln.com/comparisons/" }},
            {{ "@type": "ListItem", "position": 3, "name": "{escape_html(title)}" }}
        ]
    }}
    </script>
    <link rel="alternate" type="application/rss+xml" title="FixTheVuln Blog" href="../blog/feed.xml">
</head>
<body>
<nav class="site-nav">
    <div class="container">
        <a href="../index.html" class="site-nav-logo">FixTheVuln</a>
        <div class="site-nav-links">
            <a href="../guides.html">Guides</a>
            <a href="../tools.html">Tools</a>
            <a href="../compliance.html">Compliance</a>
            <a href="../resources.html">Resources</a>
            <a href="../blog/">Blog</a>
        </div>
    </div>
</nav>
<!-- Social Share Bar -->
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
    <a class="share-copy" href="javascript:void(0)" onclick="navigator.clipboard.writeText(window.location.href).then(()=>{{this.title='Copied!';setTimeout(()=>this.title='Copy link',2000)}})" title="Copy link">
        <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </a>
</div>

    <header class="content-header">
        <div class="container">
            <h1>{escape_html(title)}</h1>
            <p>Which certification should you get?</p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.25rem;">Last updated: {TODAY}</p>
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

            <h2>Test Your Knowledge</h2>
            <p>Already studying? Try our free tools:</p>
            <ul>
                <li><a href="../security-quiz.html">Security+ Practice Quiz</a> &mdash; 300 questions mapped to SY0-701 domains</li>
                <li><a href="../cvss-calculator.html">CVSS Calculator</a> &mdash; Practice scoring vulnerabilities</li>
            </ul>

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

        <!-- Etsy CTA -->
        <section style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">SmartSheetByRobert</p>
            <h3 style="color: white; margin-bottom: 0.5rem;">Get the Study Planner for {escape_html(c1['name'])}</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">Structured study planners with domain trackers, time blocking, and exam strategies. Standard + ADHD-friendly editions.</p>
            <a href="https://www.etsy.com/shop/SmartSheetByRobert?section_id={etsy_section}" target="_blank" rel="noopener" style="display: inline-block; background: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: 600;">Shop {escape_html(c1['vendor'])} Planners</a>
            <p style="font-size: 0.8rem; opacity: 0.85; margin-top: 0.75rem;">Also available: CompTIA, (ISC)2, AWS, Cisco, and 30+ more</p>
        </section>

        <a href="../index.html" class="back-link">&larr; Back to Home</a>
        <a href="index.html" class="back-link" style="margin-left: 1rem;">&larr; All Comparisons</a>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 FixTheVuln. Practical Vulnerability Remediation.</p>
            <p>For detailed guides: <a href="https://fixthevuln.com" target="_blank">FixTheVuln.com</a> | Support us: <a href="https://www.etsy.com/shop/SmartSheetByRobert?ref=seller-platform-mcnav" target="_blank" rel="noopener">SmartSheetByRobert</a></p>
            <p style="font-size: 0.85rem; color: #999; margin-top: 1rem;">
                <strong>Affiliate Disclosure:</strong> Some links on this site are affiliate links. We may earn a commission when you purchase through these links at no additional cost to you. We only recommend tools and services we trust.
            </p>
        </div>
    </footer>
<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "8304415b01684a00adedcbf6975458d7"}}'></script><!-- End Cloudflare Web Analytics -->
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

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <link rel="preconnect" href="https://static.cloudflareinsights.com" crossorigin>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Compare IT security certifications side by side. {len(comparisons)} detailed comparisons including Security+, CISSP, AWS, CySA+, and more.">
    <meta name="keywords" content="certification comparison, Security+ vs CySA+, CISSP vs CISM, IT certification guide, cybersecurity certifications">
    <title>Certification Comparisons &mdash; Which Cert Should You Get? - FixTheVuln</title>
    <link rel="canonical" href="https://fixthevuln.com/comparisons/">
    <meta property="og:title" content="Certification Comparisons &mdash; Which Cert Should You Get? - FixTheVuln">
    <meta property="og:description" content="Compare IT security certifications side by side. {len(comparisons)} detailed comparisons.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://fixthevuln.com/comparisons/">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Certification Comparisons &mdash; Which Cert Should You Get? - FixTheVuln">
    <meta name="twitter:description" content="Compare IT security certifications side by side. {len(comparisons)} detailed comparisons.">
    <meta name="twitter:image" content="https://fixthevuln.com/og-image.png">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23667eea'/%3E%3Ctext x='50' y='68' font-family='Arial,sans-serif' font-size='60' font-weight='bold' fill='white' text-anchor='middle'%3EF%3C/text%3E%3C/svg%3E">
    <link rel="stylesheet" href="../style.min.css">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://fixthevuln.com/" }},
            {{ "@type": "ListItem", "position": 2, "name": "Certification Comparisons" }}
        ]
    }}
    </script>
    <link rel="alternate" type="application/rss+xml" title="FixTheVuln Blog" href="../blog/feed.xml">
</head>
<body>
<nav class="site-nav">
    <div class="container">
        <a href="../index.html" class="site-nav-logo">FixTheVuln</a>
        <div class="site-nav-links">
            <a href="../guides.html">Guides</a>
            <a href="../tools.html">Tools</a>
            <a href="../compliance.html">Compliance</a>
            <a href="../resources.html">Resources</a>
            <a href="../blog/">Blog</a>
        </div>
    </div>
</nav>
<!-- Social Share Bar -->
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
    <a class="share-copy" href="javascript:void(0)" onclick="navigator.clipboard.writeText(window.location.href).then(()=>{{this.title='Copied!';setTimeout(()=>this.title='Copy link',2000)}})" title="Copy link">
        <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
    </a>
</div>

    <header class="content-header">
        <div class="container">
            <h1>Certification Comparisons</h1>
            <p>Side-by-side guides to help you choose the right certification</p>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.25rem;">{len(comparisons)} comparisons &mdash; Updated {TODAY}</p>
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

        <!-- Etsy CTA -->
        <section style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">SmartSheetByRobert</p>
            <h3 style="color: white; margin-bottom: 0.5rem;">Ready to Start Studying?</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">Structured study planners for 30+ certifications. Standard + ADHD-friendly editions with domain trackers and exam strategies.</p>
            <div style="display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap;">
                <a href="https://www.etsy.com/shop/SmartSheetByRobert?section_id=57227085" target="_blank" rel="noopener" style="background: rgba(255,255,255,0.12); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.25);">CompTIA</a>
                <a href="https://www.etsy.com/shop/SmartSheetByRobert?section_id=57213094" target="_blank" rel="noopener" style="background: rgba(255,255,255,0.12); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.25);">(ISC)2</a>
                <a href="https://www.etsy.com/shop/SmartSheetByRobert?section_id=57187684" target="_blank" rel="noopener" style="background: rgba(255,255,255,0.12); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.25);">AWS</a>
                <a href="https://www.etsy.com/shop/SmartSheetByRobert?section_id=57187730" target="_blank" rel="noopener" style="background: rgba(255,255,255,0.12); color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.25);">Cisco</a>
            </div>
        </section>

        <a href="../index.html" class="back-link">&larr; Back to Home</a>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 FixTheVuln. Practical Vulnerability Remediation.</p>
            <p>For detailed guides: <a href="https://fixthevuln.com" target="_blank">FixTheVuln.com</a> | Support us: <a href="https://www.etsy.com/shop/SmartSheetByRobert?ref=seller-platform-mcnav" target="_blank" rel="noopener">SmartSheetByRobert</a></p>
            <p style="font-size: 0.85rem; color: #999; margin-top: 1rem;">
                <strong>Affiliate Disclosure:</strong> Some links on this site are affiliate links. We may earn a commission when you purchase through these links at no additional cost to you. We only recommend tools and services we trust.
            </p>
        </div>
    </footer>
<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "8304415b01684a00adedcbf6975458d7"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>'''


def update_sitemap(comparisons):
    """Update sitemap.xml with comparison entries."""
    sitemap_text = SITEMAP_PATH.read_text(encoding='utf-8')

    # Remove any existing comparison entries
    sitemap_text = re.sub(
        r'\n  <!-- Comparison Pages -->.*?(?=\n  <!--|\n</urlset>)',
        '',
        sitemap_text,
        flags=re.DOTALL,
    )

    # Build comparison entries
    entries = f'\n  <!-- Comparison Pages -->\n  <url>\n    <loc>https://fixthevuln.com/comparisons/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>'

    for comp in comparisons:
        entries += f'''
  <url>
    <loc>https://fixthevuln.com/comparisons/{comp["slug"]}.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>'''

    # Insert before </urlset>
    sitemap_text = sitemap_text.replace('</urlset>', entries + '\n</urlset>')
    SITEMAP_PATH.write_text(sitemap_text, encoding='utf-8')
    print(f'  SITEMAP updated with {len(comparisons) + 1} comparison entries.')


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

    # Generate individual comparison pages
    for comp in comparisons:
        html = generate_comparison_page(comp, certs)
        out_path = COMP_DIR / f"{comp['slug']}.html"
        out_path.write_text(html, encoding='utf-8')

    print(f'  GENERATED {len(comparisons)} comparison pages.')

    # Generate index page
    index_html = generate_index_page(comparisons, certs)
    (COMP_DIR / 'index.html').write_text(index_html, encoding='utf-8')
    print('  GENERATED comparisons/index.html')

    # Update sitemap
    update_sitemap(comparisons)

    print(f'\n  Done. {len(comparisons) + 1} files in comparisons/.')


if __name__ == '__main__':
    main()
