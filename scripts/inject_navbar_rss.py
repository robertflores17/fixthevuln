#!/usr/bin/env python3
"""Inject global navbar and RSS autodiscovery link into all HTML pages."""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_NAV = """<nav class="site-nav">
    <div class="container">
        <a href="index.html" class="site-nav-logo">FixTheVuln</a>
        <div class="site-nav-links">
            <a href="guides.html">Guides</a>
            <a href="tools.html">Tools</a>
            <a href="compliance.html">Compliance</a>
            <a href="resources.html">Resources</a>
            <a href="blog/">Blog</a>
        </div>
    </div>
</nav>"""

BLOG_NAV = """<nav class="site-nav">
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
</nav>"""

ROOT_RSS = '    <link rel="alternate" type="application/rss+xml" title="FixTheVuln Blog" href="blog/feed.xml">'
BLOG_RSS = '    <link rel="alternate" type="application/rss+xml" title="FixTheVuln Blog" href="feed.xml">'


def process_file(filepath):
    rel = os.path.relpath(filepath, BASE_DIR)
    is_blog = rel.startswith('blog/')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # --- Inject navbar ---
    if 'site-nav' not in content:
        # Find <body> or <body ...> tag
        body_match = re.search(r'<body[^>]*>', content)
        if body_match:
            insert_pos = body_match.end()
            nav = BLOG_NAV if is_blog else ROOT_NAV
            content = content[:insert_pos] + '\n' + nav + content[insert_pos:]
            modified = True
            print(f'  NAV added: {rel}')
        else:
            print(f'  ERROR: No <body> tag in {rel}')
    else:
        print(f'  NAV skip (exists): {rel}')

    # --- Inject RSS autodiscovery ---
    if 'application/rss+xml' not in content:
        # Insert before </head>
        head_end = content.find('</head>')
        if head_end > 0:
            rss_link = BLOG_RSS if is_blog else ROOT_RSS
            content = content[:head_end] + rss_link + '\n' + content[head_end:]
            modified = True
            print(f'  RSS added: {rel}')
        else:
            print(f'  ERROR: No </head> tag in {rel}')
    else:
        print(f'  RSS skip (exists): {rel}')

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    # Collect all HTML files
    html_files = sorted(glob.glob(os.path.join(BASE_DIR, '*.html')))
    html_files += sorted(glob.glob(os.path.join(BASE_DIR, 'blog', '*.html')))

    print(f'Processing {len(html_files)} HTML files...\n')

    for filepath in html_files:
        process_file(filepath)

    print(f'\nDone. Processed {len(html_files)} files.')


if __name__ == '__main__':
    main()
