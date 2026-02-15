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
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
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
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


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
    meta_desc = f'{cve_id} — CVSS {cvss_display} ({sev}). {desc[:150]}'
    zero_day_badge = '<span style="display:inline-block;background:#dc3545;color:white;padding:0.2rem 0.6rem;border-radius:4px;font-size:0.8rem;font-weight:600;margin-left:0.5rem;">ZERO-DAY</span>' if is_zero_day else ''
    archived_badge = '<span style="display:inline-block;background:#6c757d;color:white;padding:0.2rem 0.6rem;border-radius:4px;font-size:0.8rem;font-weight:600;margin-left:0.5rem;">ARCHIVED</span>' if archived else '<span style="display:inline-block;background:#28a745;color:white;padding:0.2rem 0.6rem;border-radius:4px;font-size:0.8rem;font-weight:600;margin-left:0.5rem;">ACTIVE</span>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <link rel="preconnect" href="https://static.cloudflareinsights.com" crossorigin>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{escape_html(meta_desc)}">
    <meta name="keywords" content="{cve_id}, CVE, vulnerability, CISA KEV, {escape_html(title)}, cybersecurity">
    <title>{escape_html(page_title)}</title>
    <link rel="canonical" href="https://fixthevuln.com/cve/{cve_id}.html">
    <meta property="og:title" content="{escape_html(page_title)}">
    <meta property="og:description" content="{escape_html(meta_desc)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://fixthevuln.com/cve/{cve_id}.html">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape_html(page_title)}">
    <meta name="twitter:description" content="{escape_html(meta_desc)}">
    <meta name="twitter:image" content="https://fixthevuln.com/og-image.png">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23667eea'/%3E%3Ctext x='50' y='68' font-family='Arial,sans-serif' font-size='60' font-weight='bold' fill='white' text-anchor='middle'%3EF%3C/text%3E%3C/svg%3E">
    <link rel="stylesheet" href="../style.min.css">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": "{escape_html(cve_id)}: {escape_html(title)}",
        "description": "{escape_html(meta_desc)}",
        "datePublished": "{date_added}",
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
            {{ "@type": "ListItem", "position": 2, "name": "CVE Database", "item": "https://fixthevuln.com/cve/" }},
            {{ "@type": "ListItem", "position": 3, "name": "{cve_id}" }}
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
            <h3 style="color: white; margin-bottom: 0.5rem;">Stay Ahead of Vulnerabilities</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">Structured study planners for 34+ security certifications. Master vulnerability management with domain trackers and exam strategies.</p>
            <a href="https://www.etsy.com/shop/SmartSheetByRobert?section_id=57227085" target="_blank" rel="noopener" style="display: inline-block; background: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: 600;">Shop Security+ Planner</a>
        </section>

        <a href="../index.html" class="back-link">&larr; Back to Home</a>
        <a href="index.html" class="back-link" style="margin-left: 1rem;">&larr; All CVEs</a>
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
        return f'''                <tr>
                    <td><a href="{cve_id}.html" style="color:#667eea;font-weight:600;">{cve_id}</a></td>
                    <td>{title}{zero_day}</td>
                    <td><span style="display:inline-block;background:{sev_color};color:white;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;font-weight:600;">{cvss_display} {sev}</span></td>
                    <td>{date_added}</td>
                </tr>'''

    active_rows = '\n'.join(make_row(v) for v in sorted(active, key=lambda x: x.get('cvss') or 0, reverse=True))
    archived_rows = '\n'.join(make_row(v) for v in sorted(archived, key=lambda x: x.get('dateAdded', ''), reverse=True))

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <link rel="preconnect" href="https://static.cloudflareinsights.com" crossorigin>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Browse {len(vulns)} tracked CVEs from the CISA Known Exploited Vulnerabilities catalog. CVSS scores, fix instructions, and NVD links.">
    <meta name="keywords" content="CVE database, CISA KEV, vulnerability database, CVE lookup, cybersecurity vulnerabilities">
    <title>CVE Database &mdash; CISA KEV Tracker - FixTheVuln</title>
    <link rel="canonical" href="https://fixthevuln.com/cve/">
    <meta property="og:title" content="CVE Database &mdash; CISA KEV Tracker - FixTheVuln">
    <meta property="og:description" content="Browse {len(vulns)} tracked CVEs from the CISA Known Exploited Vulnerabilities catalog.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://fixthevuln.com/cve/">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="CVE Database &mdash; CISA KEV Tracker - FixTheVuln">
    <meta name="twitter:description" content="Browse {len(vulns)} tracked CVEs from the CISA Known Exploited Vulnerabilities catalog.">
    <meta name="twitter:image" content="https://fixthevuln.com/og-image.png">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23667eea'/%3E%3Ctext x='50' y='68' font-family='Arial,sans-serif' font-size='60' font-weight='bold' fill='white' text-anchor='middle'%3EF%3C/text%3E%3C/svg%3E">
    <link rel="stylesheet" href="../style.min.css">
    <style>
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
            .cve-table th:nth-child(4), .cve-table td:nth-child(4) {{ display: none; }}
        }}
    </style>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://fixthevuln.com/" }},
            {{ "@type": "ListItem", "position": 2, "name": "CVE Database" }}
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
                    <tr><th>CVE ID</th><th>Title</th><th>CVSS</th><th>Date Added</th></tr>
                </thead>
                <tbody>
{active_rows}
                </tbody>
            </table>
        </div>

        <div id="tab-archived" class="tab-content">
            <table class="cve-table" id="archived-table">
                <thead>
                    <tr><th>CVE ID</th><th>Title</th><th>CVSS</th><th>Date Added</th></tr>
                </thead>
                <tbody>
{archived_rows}
                </tbody>
            </table>
        </div>

        <!-- Etsy CTA -->
        <section style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">SmartSheetByRobert</p>
            <h3 style="color: white; margin-bottom: 0.5rem;">Master Vulnerability Management</h3>
            <p style="opacity: 0.9; margin-bottom: 1rem;">Structured study planners for Security+, CySA+, and 30+ certifications. Domain trackers, time blocking, and exam strategies.</p>
            <a href="https://www.etsy.com/shop/SmartSheetByRobert?section_id=57227085" target="_blank" rel="noopener" style="display: inline-block; background: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: 600;">Shop Study Planners</a>
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
<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "8304415b01684a00adedcbf6975458d7"}}'></script><!-- End Cloudflare Web Analytics -->
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

    # Generate individual CVE pages
    for v in vulns:
        html = generate_cve_page(v)
        out_path = CVE_DIR / f"{v['id']}.html"
        out_path.write_text(html, encoding='utf-8')

    print(f'  GENERATED {len(vulns)} individual CVE pages.')

    # Generate index page
    index_html = generate_index_page(vulns)
    (CVE_DIR / 'index.html').write_text(index_html, encoding='utf-8')
    print('  GENERATED cve/index.html')

    # Update sitemap
    update_sitemap(vulns)

    print(f'\n  Done. {len(vulns) + 1} files in cve/.')


if __name__ == '__main__':
    main()
