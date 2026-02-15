#!/usr/bin/env python3
"""
Editorial Blog Publishing System for FixTheVuln.com
Converts markdown drafts to fully-templated HTML blog posts.

Usage:
    python3 scripts/publish_editorial.py              # Publish all new drafts
    python3 scripts/publish_editorial.py --dry-run    # Preview without writing files
    python3 scripts/publish_editorial.py --draft FILE  # Publish a specific draft
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Markdown → HTML converter (pure Python, no dependencies)
# ---------------------------------------------------------------------------

class MarkdownConverter:
    """Converts a subset of markdown to HTML suitable for blog posts."""

    def convert(self, text):
        lines = text.split('\n')
        html_parts = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Fenced code blocks
            if line.strip().startswith('```'):
                lang = line.strip()[3:].strip()
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(self._escape(lines[i]))
                    i += 1
                i += 1  # skip closing ```
                cls = f' class="language-{lang}"' if lang else ''
                html_parts.append(f'<pre><code{cls}>{chr(10).join(code_lines)}</code></pre>')
                continue

            # Headings
            m = re.match(r'^(#{1,6})\s+(.+)$', line)
            if m:
                level = len(m.group(1))
                text_content = m.group(2)
                slug = re.sub(r'[^a-z0-9]+', '-', text_content.lower()).strip('-')
                html_parts.append(f'<h{level} id="{slug}">{self._inline(text_content)}</h{level}>')
                i += 1
                continue

            # Horizontal rule
            if line.strip() in ('---', '***', '___') and i > 0:
                html_parts.append('<hr>')
                i += 1
                continue

            # Blockquote
            if line.strip().startswith('> '):
                quote_lines = []
                while i < len(lines) and lines[i].strip().startswith('> '):
                    quote_lines.append(self._inline(lines[i].strip()[2:]))
                    i += 1
                html_parts.append(f'<blockquote><p>{"<br>".join(quote_lines)}</p></blockquote>')
                continue

            # Unordered list
            if re.match(r'^[\s]*[-*]\s+', line):
                items = []
                while i < len(lines) and re.match(r'^[\s]*[-*]\s+', lines[i]):
                    text_content = re.sub(r'^[\s]*[-*]\s+', '', lines[i])
                    items.append(f'    <li>{self._inline(text_content)}</li>')
                    i += 1
                html_parts.append('<ul>\n' + '\n'.join(items) + '\n</ul>')
                continue

            # Ordered list
            if re.match(r'^[\s]*\d+\.\s+', line):
                items = []
                while i < len(lines) and re.match(r'^[\s]*\d+\.\s+', lines[i]):
                    text_content = re.sub(r'^[\s]*\d+\.\s+', '', lines[i])
                    items.append(f'    <li>{self._inline(text_content)}</li>')
                    i += 1
                html_parts.append('<ol>\n' + '\n'.join(items) + '\n</ol>')
                continue

            # Blank line
            if not line.strip():
                i += 1
                continue

            # Paragraph (collect consecutive non-blank lines)
            para_lines = []
            while i < len(lines) and lines[i].strip() and not re.match(r'^#{1,6}\s', lines[i]) and not lines[i].strip().startswith('```') and not lines[i].strip().startswith('> ') and not re.match(r'^[\s]*[-*]\s+', lines[i]) and not re.match(r'^[\s]*\d+\.\s+', lines[i]) and lines[i].strip() not in ('---', '***', '___'):
                para_lines.append(lines[i].strip())
                i += 1
            if para_lines:
                html_parts.append(f'<p>{self._inline(" ".join(para_lines))}</p>')
            continue

        return '\n\n'.join(html_parts)

    def _inline(self, text):
        # Links [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        # Bold **text**
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic *text*
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Inline code `text`
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        return text

    def _escape(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ---------------------------------------------------------------------------
# Blog publisher
# ---------------------------------------------------------------------------

class BlogPublisher:
    def __init__(self, repo_root, dry_run=False):
        self.repo_root = Path(repo_root)
        self.drafts_dir = self.repo_root / 'drafts'
        self.blog_dir = self.repo_root / 'blog'
        self.data_dir = self.repo_root / 'data'
        self.dry_run = dry_run
        self.converter = MarkdownConverter()

        self.blog_dir.mkdir(exist_ok=True)
        self.metadata_path = self.data_dir / 'blog_metadata.json'
        self.cta_path = self.data_dir / 'cta_templates.json'

        self.metadata = self._load_json(self.metadata_path, {"posts": [], "last_updated": ""})
        self.cta_templates = self._load_json(self.cta_path, {})
        self.published_slugs = {p['slug'] for p in self.metadata['posts']}

    # -- entry points -------------------------------------------------------

    def publish_all(self):
        """Process all unpublished .md files in drafts/."""
        new_posts = []
        for md_file in sorted(self.drafts_dir.glob('*.md')):
            if md_file.name.startswith('_'):
                continue
            fm, body = self._parse_frontmatter(md_file.read_text(encoding='utf-8'))
            if not fm:
                print(f'  SKIP {md_file.name} (no frontmatter)')
                continue
            if fm['slug'] in self.published_slugs:
                print(f'  SKIP {md_file.name} (already published)')
                continue
            html = self._build_post_html(fm, body)
            out_path = self.blog_dir / f"{fm['slug']}.html"
            if self.dry_run:
                print(f'  DRY-RUN would write {out_path.relative_to(self.repo_root)}')
            else:
                out_path.write_text(html, encoding='utf-8')
                print(f'  PUBLISHED {out_path.relative_to(self.repo_root)}')
                # rename draft so it isn't re-processed
                md_file.rename(md_file.with_suffix('.md.published'))
            new_posts.append(fm)

        if new_posts:
            self._update_metadata(new_posts)
            self._generate_blog_index()
            self._generate_rss_feed()
            self._update_sitemap(new_posts)
        else:
            print('  No new drafts to publish.')

        return new_posts

    def publish_single(self, filename):
        """Process a single draft file."""
        md_file = self.drafts_dir / filename
        if not md_file.exists():
            print(f'  ERROR: {md_file} not found')
            return []
        fm, body = self._parse_frontmatter(md_file.read_text(encoding='utf-8'))
        if not fm:
            print(f'  ERROR: no frontmatter in {filename}')
            return []
        html = self._build_post_html(fm, body)
        out_path = self.blog_dir / f"{fm['slug']}.html"
        if self.dry_run:
            print(f'  DRY-RUN would write {out_path.relative_to(self.repo_root)}')
        else:
            out_path.write_text(html, encoding='utf-8')
            print(f'  PUBLISHED {out_path.relative_to(self.repo_root)}')
            md_file.rename(md_file.with_suffix('.md.published'))

        self._update_metadata([fm])
        self._generate_blog_index()
        self._generate_rss_feed()
        self._update_sitemap([fm])
        return [fm]

    # -- frontmatter --------------------------------------------------------

    def _parse_frontmatter(self, text):
        """Extract YAML-like frontmatter and markdown body."""
        m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', text, re.DOTALL)
        if not m:
            return None, text

        fm_text = m.group(1)
        body = m.group(2).strip()
        fm = {}

        for line in fm_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                key, val = line.split(':', 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                fm[key] = val

        # defaults
        fm.setdefault('author', 'FixTheVuln Team')
        fm.setdefault('sources', 'Industry frameworks and standards')
        fm.setdefault('cta_section', 'comptia')
        fm.setdefault('date', datetime.now().strftime('%Y-%m-%d'))
        fm.setdefault('updated', fm['date'])

        required = ['title', 'description', 'slug']
        for field in required:
            if field not in fm:
                print(f'  WARNING: missing required field "{field}" in frontmatter')
                return None, body

        return fm, body

    # -- HTML generation ----------------------------------------------------

    def _build_post_html(self, fm, markdown_body):
        """Build a complete HTML page from frontmatter + markdown."""
        html_body = self.converter.convert(markdown_body)
        title = fm['title']
        description = fm['description']
        keywords = fm.get('keywords', '')
        slug = fm['slug']
        date_pub = fm['date']
        date_upd = fm.get('updated', date_pub)
        author = fm['author']
        sources = fm['sources']
        canonical = f'https://fixthevuln.com/blog/{slug}.html'

        try:
            date_display = datetime.strptime(date_pub, '%Y-%m-%d').strftime('%B %Y')
        except ValueError:
            date_display = date_pub

        etsy_cta = self._build_etsy_cta(fm.get('cta_section', 'comptia'))
        related_tools = self._build_related_tools()

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <link rel="preconnect" href="https://static.cloudflareinsights.com" crossorigin>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{self._esc_attr(description)}">
    <meta name="keywords" content="{self._esc_attr(keywords)}">
    <title>{self._esc(title)} - FixTheVuln</title>
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{self._esc_attr(title)} - FixTheVuln">
    <meta property="og:description" content="{self._esc_attr(description)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{self._esc_attr(title)} - FixTheVuln">
    <meta name="twitter:description" content="{self._esc_attr(description)}">
    <meta name="twitter:image" content="https://fixthevuln.com/og-image.png">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23667eea'/%3E%3Ctext x='50' y='68' font-family='Arial,sans-serif' font-size='60' font-weight='bold' fill='white' text-anchor='middle'%3EF%3C/text%3E%3C/svg%3E">
    <link rel="stylesheet" href="../style.min.css">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": "{self._esc_json(title)}",
        "description": "{self._esc_json(description)}",
        "datePublished": "{date_pub}",
        "dateModified": "{date_upd}",
        "author": {{ "@type": "Organization", "name": "{self._esc_json(author)}", "url": "https://fixthevuln.com" }},
        "publisher": {{ "@type": "Organization", "name": "FixTheVuln", "url": "https://fixthevuln.com" }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://fixthevuln.com/" }},
            {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://fixthevuln.com/blog/" }},
            {{ "@type": "ListItem", "position": 3, "name": "{self._esc_json(title)}" }}
        ]
    }}
    </script>
</head>
<body>
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
            <h1>{self._esc(title)}</h1>
            <p>Expert cybersecurity insights for IT professionals</p>
            <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">Last updated: {date_display}</p>
        </div>
    </header>

    <main class="container">
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; justify-content: center; padding: 0.75rem; margin-bottom: 1rem; font-size: 0.8rem; color: var(--text-muted); border-bottom: 1px solid var(--border-color);">
            <span>By <strong>{self._esc(author)}</strong></span>
            <span aria-hidden="true">&middot;</span>
            <span>Peer-reviewed security content</span>
            <span aria-hidden="true">&middot;</span>
            <span>Sources: {self._esc(sources)}</span>
        </div>
        <div class="content-wrapper">
{html_body}
        </div>

{related_tools}

{etsy_cta}

            <a href="../index.html" class="back-link">&larr; Back to Home</a>
            <a href="index.html" class="back-link" style="margin-left: 1rem;">&larr; All Blog Posts</a>
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

    # -- CTA sections -------------------------------------------------------

    def _build_etsy_cta(self, section_key):
        """Build the Etsy CTA section from cta_templates.json."""
        sections = self.cta_templates.get('etsy_sections', {})
        section = sections.get(section_key, sections.get('comptia', {}))

        if not section:
            return ''

        title = section.get('title', 'Get the Study Planner')
        desc = section.get('description', '')
        cta_text = section.get('cta_text', 'Shop Now')
        url = section.get('url', 'https://www.etsy.com/shop/SmartSheetByRobert')
        also = section.get('also_available', '')

        also_html = f'''
                <p style="font-size: 0.8rem; opacity: 0.85; margin-top: 0.75rem;">Also available: {self._esc(also)}</p>''' if also else ''

        return f'''
            <!-- Etsy CTA -->
            <section style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 2rem; text-align: center;">
                <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.6; margin-bottom: 0.3rem;">SmartSheetByRobert</p>
                <h3 style="color: white; margin-bottom: 0.5rem;">{self._esc(title)}</h3>
                <p style="opacity: 0.9; margin-bottom: 1rem;">{self._esc(desc)}</p>
                <a href="{url}" target="_blank" rel="noopener" style="display: inline-block; background: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: 600;">{self._esc(cta_text)}</a>{also_html}
            </section>'''

    def _build_related_tools(self):
        """Build the related resources / tools section."""
        tools = self.cta_templates.get('tool_links', {})
        if not tools:
            return ''

        links_html = []
        for key, info in tools.items():
            url = info.get('url', f'/{key}.html')
            # Adjust path for blog subdirectory
            if url.startswith('/'):
                url = '..' + url
            name = info.get('title', key.replace('-', ' ').title())
            links_html.append(
                f'                    <a href="{url}" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">{self._esc(name)}</a>'
            )

        return f'''
            <!-- Related Tools -->
            <section style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px;">
                <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Free Security Tools</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
{chr(10).join(links_html)}
                </div>
            </section>'''

    # -- blog index ---------------------------------------------------------

    def _generate_blog_index(self):
        """Generate blog/index.html listing all published posts."""
        posts = sorted(self.metadata['posts'], key=lambda p: p['date'], reverse=True)

        cards = []
        for p in posts:
            try:
                date_fmt = datetime.strptime(p['date'], '%Y-%m-%d').strftime('%B %d, %Y')
            except ValueError:
                date_fmt = p['date']
            cards.append(f'''
            <article style="padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px; margin-bottom: 1.5rem; border: 1px solid var(--border-color);">
                <h2 style="margin-bottom: 0.5rem;"><a href="{p['slug']}.html" style="color: var(--text-primary); text-decoration: none;">{self._esc(p['title'])}</a></h2>
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.75rem;">{date_fmt} &middot; {self._esc(p.get('author', 'FixTheVuln Team'))}</p>
                <p style="color: var(--text-secondary); margin-bottom: 0.75rem;">{self._esc(p.get('excerpt', ''))}</p>
                <a href="{p['slug']}.html" style="color: var(--accent-primary); text-decoration: none; font-weight: 600;">Read more &rarr;</a>
            </article>''')

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <link rel="preconnect" href="https://static.cloudflareinsights.com" crossorigin>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="FixTheVuln Blog - Expert cybersecurity insights, threat analysis, and IT certification study guides.">
    <meta name="keywords" content="cybersecurity blog, threat intelligence, Security+ exam, vulnerability analysis">
    <title>Blog - FixTheVuln</title>
    <link rel="canonical" href="https://fixthevuln.com/blog/">
    <meta property="og:title" content="Blog - FixTheVuln">
    <meta property="og:description" content="Expert cybersecurity insights, threat analysis, and IT certification study guides.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://fixthevuln.com/blog/">
    <meta property="og:image" content="https://fixthevuln.com/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Blog - FixTheVuln">
    <meta name="twitter:description" content="Expert cybersecurity insights, threat analysis, and IT certification study guides.">
    <meta name="twitter:image" content="https://fixthevuln.com/og-image.png">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23667eea'/%3E%3Ctext x='50' y='68' font-family='Arial,sans-serif' font-size='60' font-weight='bold' fill='white' text-anchor='middle'%3EF%3C/text%3E%3C/svg%3E">
    <link rel="stylesheet" href="../style.min.css">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Blog",
        "headline": "FixTheVuln Blog",
        "description": "Expert cybersecurity insights for IT professionals",
        "author": {{ "@type": "Organization", "name": "FixTheVuln", "url": "https://fixthevuln.com" }},
        "publisher": {{ "@type": "Organization", "name": "FixTheVuln", "url": "https://fixthevuln.com" }}
    }}
    </script>
</head>
<body>
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
            <h1>FixTheVuln Blog</h1>
            <p>Expert cybersecurity insights for IT professionals</p>
            <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">Threat analysis &middot; Certification prep &middot; Vulnerability research</p>
        </div>
    </header>

    <main class="container">
        <div class="content-wrapper">
{''.join(cards) if cards else '<p>No posts yet. Check back soon!</p>'}

            <!-- Related Tools -->
            <section style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px;">
                <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Free Security Tools</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
                    <a href="../cvss-calculator.html" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">CVSS Calculator</a>
                    <a href="../security-quiz.html" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">Security+ Quiz</a>
                    <a href="../password-strength.html" style="padding: 0.75rem; background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; color: var(--text-primary); border: 1px solid var(--border-color); transition: border-color 0.2s;">Password Strength Checker</a>
                </div>
            </section>

            <a href="../index.html" class="back-link">&larr; Back to Home</a>
        </div>
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

        if self.dry_run:
            print(f'  DRY-RUN would write blog/index.html')
        else:
            (self.blog_dir / 'index.html').write_text(html, encoding='utf-8')
            print(f'  GENERATED blog/index.html')

    # -- RSS feed -----------------------------------------------------------

    def _generate_rss_feed(self):
        """Generate blog/feed.xml RSS 2.0 feed."""
        posts = sorted(self.metadata['posts'], key=lambda p: p['date'], reverse=True)[:20]

        items = []
        for p in posts:
            try:
                dt = datetime.strptime(p['date'], '%Y-%m-%d')
                pub_date = dt.strftime('%a, %d %b %Y 00:00:00 GMT')
            except ValueError:
                pub_date = p['date']

            title_esc = self._esc(p['title'])
            excerpt_esc = self._esc(p.get('excerpt', ''))
            link = f"https://fixthevuln.com{p['url']}"

            items.append(f'''    <item>
      <title>{title_esc}</title>
      <link>{link}</link>
      <description>{excerpt_esc}</description>
      <pubDate>{pub_date}</pubDate>
      <guid>{link}</guid>
    </item>''')

        rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>FixTheVuln Blog</title>
    <link>https://fixthevuln.com/blog/</link>
    <description>Expert cybersecurity insights, threat analysis, and IT certification study guides.</description>
    <language>en-us</language>
    <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
    <atom:link href="https://fixthevuln.com/blog/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
'''

        if self.dry_run:
            print('  DRY-RUN would write blog/feed.xml')
        else:
            (self.blog_dir / 'feed.xml').write_text(rss, encoding='utf-8')
            print('  GENERATED blog/feed.xml')

    # -- sitemap ------------------------------------------------------------

    def _update_sitemap(self, new_posts):
        """Add new blog post URLs to sitemap.xml."""
        sitemap_path = self.repo_root / 'sitemap.xml'
        if not sitemap_path.exists():
            print('  WARNING: sitemap.xml not found, skipping update')
            return

        content = sitemap_path.read_text(encoding='utf-8')
        today = datetime.now().strftime('%Y-%m-%d')

        # Check if blog index entry exists
        if 'fixthevuln.com/blog/' not in content:
            blog_index_entry = f'''
  <!-- Blog -->
  <url>
    <loc>https://fixthevuln.com/blog/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>'''
            content = content.replace('</urlset>', blog_index_entry + '\n</urlset>')
        else:
            # Update blog index lastmod
            content = re.sub(
                r'(<loc>https://fixthevuln\.com/blog/</loc>\s*<lastmod>)\d{4}-\d{2}-\d{2}(</lastmod>)',
                rf'\g<1>{today}\g<2>',
                content
            )

        # Add individual post entries
        for post in new_posts:
            post_url = f"https://fixthevuln.com/blog/{post['slug']}.html"
            if post_url not in content:
                entry = f'''  <url>
    <loc>{post_url}</loc>
    <lastmod>{post['date']}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>'''
                content = content.replace('</urlset>', entry + '\n</urlset>')

        if self.dry_run:
            print(f'  DRY-RUN would update sitemap.xml')
        else:
            sitemap_path.write_text(content, encoding='utf-8')
            print(f'  UPDATED sitemap.xml')

    # -- metadata -----------------------------------------------------------

    def _update_metadata(self, new_posts):
        """Update data/blog_metadata.json with new posts."""
        for fm in new_posts:
            entry = {
                'slug': fm['slug'],
                'title': fm['title'],
                'date': fm['date'],
                'author': fm.get('author', 'FixTheVuln Team'),
                'excerpt': fm['description'][:200],
                'url': f"/blog/{fm['slug']}.html"
            }
            # Remove existing entry with same slug (for re-publishes)
            self.metadata['posts'] = [p for p in self.metadata['posts'] if p['slug'] != fm['slug']]
            self.metadata['posts'].append(entry)
            self.published_slugs.add(fm['slug'])

        self.metadata['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        if self.dry_run:
            print(f'  DRY-RUN would update data/blog_metadata.json')
        else:
            self._save_json(self.metadata_path, self.metadata)
            print(f'  UPDATED data/blog_metadata.json')

    # -- helpers ------------------------------------------------------------

    def _load_json(self, path, default):
        if path.exists():
            return json.loads(path.read_text(encoding='utf-8'))
        return default

    def _save_json(self, path, data):
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    def _esc(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def _esc_attr(self, text):
        return self._esc(text).replace('"', '&quot;')

    def _esc_json(self, text):
        return text.replace('\\', '\\\\').replace('"', '\\"')


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    repo_root = Path(__file__).resolve().parent.parent
    dry_run = '--dry-run' in sys.argv

    print(f'FixTheVuln Editorial Publisher')
    print(f'  Repo: {repo_root}')
    print(f'  Mode: {"DRY RUN" if dry_run else "LIVE"}')
    print()

    publisher = BlogPublisher(repo_root, dry_run=dry_run)

    # Check for --draft flag
    if '--draft' in sys.argv:
        idx = sys.argv.index('--draft')
        if idx + 1 < len(sys.argv):
            filename = sys.argv[idx + 1]
            posts = publisher.publish_single(filename)
        else:
            print('  ERROR: --draft requires a filename')
            sys.exit(1)
    else:
        posts = publisher.publish_all()

    if posts:
        print(f'\nPublished {len(posts)} post(s):')
        for p in posts:
            print(f'  - {p["title"]}')
            print(f'    URL: https://fixthevuln.com/blog/{p["slug"]}.html')
    else:
        print('\nNo new posts published.')


if __name__ == '__main__':
    main()
