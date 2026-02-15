#!/usr/bin/env python3
"""
SEO Cross-Linker for FixTheVuln.com
Injects "Latest from the Blog" links into existing guide/tool pages.
Matches blog posts to pages by keyword relevance.

Usage:
    python3 scripts/inject_blog_links.py              # Inject links
    python3 scripts/inject_blog_links.py --dry-run    # Preview changes
"""

import json
import re
import sys
from pathlib import Path


# Keyword mappings: page filename → keywords to match in blog post titles/descriptions
PAGE_KEYWORDS = {
    'security-quiz.html': ['security+', 'sy0-701', 'comptia', 'exam', 'certification', 'study'],
    'cvss-calculator.html': ['cvss', 'vulnerability', 'cve', 'threat', 'kev', 'critical'],
    'owasp-top10.html': ['owasp', 'web security', 'injection', 'xss', 'application security'],
    'api-security.html': ['api', 'web security', 'authentication', 'authorization'],
    'cloud-security.html': ['cloud', 'aws', 'azure', 'serverless', 'container'],
    'container-security.html': ['docker', 'container', 'kubernetes', 'cloud'],
    'incident-response.html': ['incident', 'response', 'forensics', 'breach', 'siem'],
    'linux-hardening.html': ['linux', 'hardening', 'server', 'command injection', 'os'],
    'windows-hardening.html': ['windows', 'hardening', 'active directory', 'powershell'],
    'ssl-tls.html': ['ssl', 'tls', 'encryption', 'certificate', 'https'],
    'encryption-cheatsheet.html': ['encryption', 'cryptography', 'hash', 'cipher'],
    'port-security.html': ['port', 'network', 'firewall', 'scanning'],
    'log-management.html': ['log', 'siem', 'monitoring', 'detection', 'alert'],
    'secrets-management.html': ['secret', 'credential', 'password', 'key management'],
    'security-headers.html': ['header', 'web security', 'csp', 'hsts'],
    'password-strength.html': ['password', 'credential', 'authentication', 'brute force'],
    'password-generator.html': ['password', 'credential', 'security'],
    'cve-lookup.html': ['cve', 'vulnerability', 'nvd', 'kev', 'exploit'],
    'quick-fixes.html': ['patch', 'fix', 'vulnerability', 'remediation', 'hardening'],
    'nist-framework.html': ['nist', 'framework', 'compliance', 'governance', 'risk'],
    'cis-controls.html': ['cis', 'controls', 'benchmark', 'hardening', 'compliance'],
    'start-here.html': ['security+', 'beginner', 'learning', 'career', 'certification'],
    'resources.html': ['study', 'resource', 'certification', 'learning', 'tool'],
}

# Blog link HTML marker
BLOG_LINK_MARKER = '<!-- Blog Cross-Links -->'
BLOG_LINK_END = '<!-- End Blog Cross-Links -->'


def score_relevance(post, keywords):
    """Score how relevant a blog post is to a set of keywords."""
    title_lower = post.get('title', '').lower()
    excerpt_lower = post.get('excerpt', '').lower()
    combined = title_lower + ' ' + excerpt_lower

    score = 0
    for kw in keywords:
        if kw.lower() in combined:
            # Title matches are worth more
            if kw.lower() in title_lower:
                score += 3
            else:
                score += 1
    return score


def build_blog_links_html(matching_posts):
    """Build the HTML section for blog cross-links."""
    links = []
    for post in matching_posts[:3]:  # max 3 blog links per page
        url = f"blog/{post['slug']}.html"
        title = post['title']
        if len(title) > 70:
            title = title[:67] + '...'
        links.append(
            f'                    <a href="{url}" style="padding: 0.75rem; background: var(--bg-tertiary); '
            f'border-radius: 6px; text-decoration: none; color: var(--text-primary); '
            f'border: 1px solid var(--border-color); transition: border-color 0.2s;">'
            f'{title}</a>'
        )

    return f'''
            {BLOG_LINK_MARKER}
            <section style="margin-top: 1.5rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px;">
                <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Latest from the Blog</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
{chr(10).join(links)}
                </div>
            </section>
            {BLOG_LINK_END}'''


def main():
    repo_root = Path(__file__).resolve().parent.parent
    dry_run = '--dry-run' in sys.argv

    metadata_path = repo_root / 'data' / 'blog_metadata.json'
    if not metadata_path.exists():
        print('  No blog_metadata.json found, skipping cross-linking.')
        return

    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    posts = metadata.get('posts', [])

    if not posts:
        print('  No published posts for cross-linking.')
        return

    updated = 0
    for page_name, keywords in PAGE_KEYWORDS.items():
        page_path = repo_root / page_name
        if not page_path.exists():
            continue

        # Score all posts against this page's keywords
        scored = []
        for post in posts:
            score = score_relevance(post, keywords)
            if score > 0:
                scored.append((score, post))

        if not scored:
            continue

        # Sort by relevance score
        scored.sort(key=lambda x: x[0], reverse=True)
        matching = [post for _, post in scored]

        content = page_path.read_text(encoding='utf-8')

        # Remove existing blog links if present
        if BLOG_LINK_MARKER in content:
            content = re.sub(
                rf'\n\s*{re.escape(BLOG_LINK_MARKER)}.*?{re.escape(BLOG_LINK_END)}',
                '',
                content,
                flags=re.DOTALL
            )

        # Find insertion point — before the back-link or before </main>
        blog_html = build_blog_links_html(matching)

        if '<a href="index.html" class="back-link">' in content:
            content = content.replace(
                '<a href="index.html" class="back-link">',
                blog_html + '\n\n            <a href="index.html" class="back-link">'
            )
        elif '</main>' in content:
            content = content.replace(
                '</main>',
                blog_html + '\n    </main>'
            )
        else:
            continue

        if dry_run:
            print(f'  DRY-RUN would update {page_name} ({len(matching)} blog links)')
        else:
            page_path.write_text(content, encoding='utf-8')
            print(f'  UPDATED {page_name} ({min(3, len(matching))} blog links)')

        updated += 1

    if updated == 0:
        print('  No pages updated with blog links.')
    else:
        print(f'\n  Cross-linked blog posts into {updated} page(s).')


if __name__ == '__main__':
    main()
