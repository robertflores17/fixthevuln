#!/usr/bin/env python3
"""Inject global navbar and RSS autodiscovery link into all HTML pages."""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_NAV = """<nav class="site-nav">
    <div class="container">
        <a href="/" class="site-nav-logo">FixTheVuln</a>
        <button class="nav-toggle" aria-label="Menu" onclick="this.classList.toggle('active');this.parentElement.querySelector('.site-nav-links').classList.toggle('open')"><span></span><span></span><span></span></button>
        <div class="site-nav-links">
            <a href="guides.html">Guides</a>
            <a href="tools.html">Tools</a>
            <a href="compliance.html">Compliance</a>
            <a href="resources.html">Resources</a>
            <a href="practice-tests.html">Quizzes</a>
            <a href="career-paths.html">Career Paths</a>
            <a href="blog/">Blog</a>
            <a href="/store/store.html" style="background: linear-gradient(135deg, #2563eb, #7c3aed); color: white; padding: .35rem .75rem; border-radius: 6px; font-size: .85rem; font-weight: 600; text-decoration: none;">Store</a>
        </div>
    </div>
</nav>"""

SUBDIR_NAV = """<nav class="site-nav">
    <div class="container">
        <a href="../" class="site-nav-logo">FixTheVuln</a>
        <button class="nav-toggle" aria-label="Menu" onclick="this.classList.toggle('active');this.parentElement.querySelector('.site-nav-links').classList.toggle('open')"><span></span><span></span><span></span></button>
        <div class="site-nav-links">
            <a href="../guides.html">Guides</a>
            <a href="../tools.html">Tools</a>
            <a href="../compliance.html">Compliance</a>
            <a href="../resources.html">Resources</a>
            <a href="../practice-tests.html">Quizzes</a>
            <a href="../career-paths.html">Career Paths</a>
            <a href="../blog/">Blog</a>
            <a href="/store/store.html" style="background: linear-gradient(135deg, #2563eb, #7c3aed); color: white; padding: .35rem .75rem; border-radius: 6px; font-size: .85rem; font-weight: 600; text-decoration: none;">Store</a>
        </div>
    </div>
</nav>"""

ROOT_RSS = '    <link rel="alternate" type="application/rss+xml" title="FixTheVuln Blog" href="blog/feed.xml">'
SUBDIR_RSS = '    <link rel="alternate" type="application/rss+xml" title="FixTheVuln Blog" href="../blog/feed.xml">'
BLOG_RSS = '    <link rel="alternate" type="application/rss+xml" title="FixTheVuln Blog" href="feed.xml">'

SUBDIRS = ['blog', 'cve', 'comparisons', 'roadmaps', 'certs', 'practice-tests', 'wstg', 'ai-vulnerabilities']


def get_subdir(rel_path):
    """Return the subdirectory name if file is in one, else None."""
    for sd in SUBDIRS:
        if rel_path.startswith(sd + '/'):
            return sd
    return None


def process_file(filepath):
    rel = os.path.relpath(filepath, BASE_DIR)
    subdir = get_subdir(rel)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # --- Inject navbar ---
    if 'site-nav' not in content:
        body_match = re.search(r'<body[^>]*>', content)
        if body_match:
            insert_pos = body_match.end()
            nav = SUBDIR_NAV if subdir else ROOT_NAV
            content = content[:insert_pos] + '\n' + nav + content[insert_pos:]
            modified = True
            print(f'  NAV added: {rel}')
        else:
            print(f'  ERROR: No <body> tag in {rel}')
    else:
        print(f'  NAV skip (exists): {rel}')

    # --- Inject RSS autodiscovery ---
    if 'application/rss+xml' not in content:
        head_end = content.find('</head>')
        if head_end > 0:
            if subdir == 'blog':
                rss_link = BLOG_RSS
            elif subdir:
                rss_link = SUBDIR_RSS
            else:
                rss_link = ROOT_RSS
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
    for sd in SUBDIRS:
        html_files += sorted(glob.glob(os.path.join(BASE_DIR, sd, '*.html')))

    print(f'Processing {len(html_files)} HTML files...\n')

    for filepath in html_files:
        process_file(filepath)

    print(f'\nDone. Processed {len(html_files)} files.')


if __name__ == '__main__':
    main()
