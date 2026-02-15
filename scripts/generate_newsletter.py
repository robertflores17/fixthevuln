#!/usr/bin/env python3
"""
Newsletter Copy Generator for FixTheVuln.com
Generates ready-to-paste beehiiv newsletter content for each newly published
blog post.

Usage:
    python3 scripts/generate_newsletter.py              # Generate newsletters
    python3 scripts/generate_newsletter.py --dry-run    # Preview without writing
    python3 scripts/generate_newsletter.py --all        # Regenerate for all posts
"""

import json
import sys
import re
from pathlib import Path
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    """Extract visible text from HTML, stripping tags."""

    def __init__(self):
        super().__init__()
        self._text = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'nav', 'footer'):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'nav', 'footer'):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self._text.append(data)

    def get_text(self):
        return ' '.join(self._text)


def extract_sections(html_path):
    """Pull h2 headings and first paragraph from blog HTML."""
    if not html_path.exists():
        return []

    html = html_path.read_text(encoding='utf-8')

    # Find h2 headings
    headings = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
    # Strip any inner tags from headings
    clean = []
    for h in headings:
        text = re.sub(r'<[^>]+>', '', h).strip()
        if text and len(text) < 120:
            clean.append(text)
    return clean[:6]  # Cap at 6 section headings


def generate_newsletter(post, repo_root):
    """Generate beehiiv newsletter content for a single post."""
    title = post['title']
    excerpt = post.get('excerpt', '')
    url = f"https://fixthevuln.com{post['url']}"
    date = post.get('date', '')

    # Try to extract section headings from the actual HTML
    blog_path = repo_root / post['url'].lstrip('/')
    sections = extract_sections(blog_path)

    # Build the "In this issue" bullet list
    if sections:
        bullets = '\n'.join(f'  - {s}' for s in sections)
    else:
        bullets = (
            '  - Key takeaways for security professionals\n'
            '  - How this maps to Security+ SY0-701 exam domains\n'
            '  - Actionable steps you can take right now'
        )

    # Determine topic type for the sign-off CTA
    title_lower = title.lower()
    if any(w in title_lower for w in ['threat', 'roundup', 'cve', 'vulnerability', 'week']):
        post_type = 'roundup'
    elif any(w in title_lower for w in ['ai', 'agentic', 'machine learning']):
        post_type = 'editorial'
    else:
        post_type = 'general'

    cta_lines = {
        'roundup': (
            'Stay ahead of emerging threats. Bookmark FixTheVuln.com and check '
            'back every week for the latest vulnerability roundups.'
        ),
        'editorial': (
            'Understanding these trends is essential for passing Security+ and '
            'for real-world defense. Bookmark FixTheVuln.com for more deep dives.'
        ),
        'general': (
            'Keep learning, keep building your skills. '
            'Bookmark FixTheVuln.com for free guides, tools, and weekly threat intel.'
        ),
    }

    # ---- Subject Line ----
    subject = title
    if len(subject) > 70:
        # Shorten for email subject
        subject = subject[:67].rsplit(' ', 1)[0] + '...'

    # ---- Preview Text ----
    preview = excerpt[:140]
    if len(excerpt) > 140:
        preview = preview.rsplit(' ', 1)[0] + '...'

    # ---- Body ----
    body = f"""Subject: {subject}
Preview text: {preview}

---

Hi there,

We just published a new post on FixTheVuln.com:

**{title}**

{excerpt}

In this issue:
{bullets}

Read the full post here:
{url}

---

Studying for a certification? Our study planners give you a structured 8-week plan with domain trackers, practice exam schedules, and proven strategies.

Browse planners: https://SmartSheetByRobert.etsy.com

---

{cta_lines[post_type]}

Stay secure,
The FixTheVuln Team

---
You're receiving this because you subscribed at FixTheVuln.com.
"""

    return {
        'subject': subject,
        'preview': preview,
        'body': body,
    }


def main():
    repo_root = Path(__file__).resolve().parent.parent
    dry_run = '--dry-run' in sys.argv
    regen_all = '--all' in sys.argv

    metadata_path = repo_root / 'data' / 'blog_metadata.json'
    newsletter_dir = repo_root / 'data' / 'newsletters'
    newsletter_dir.mkdir(exist_ok=True)

    if not metadata_path.exists():
        print('  No blog_metadata.json found, skipping newsletter generation.')
        return

    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    posts = metadata.get('posts', [])

    if not posts:
        print('  No published posts found.')
        return

    generated = 0
    for post in posts:
        slug = post['slug']
        out_path = newsletter_dir / f"{slug}-newsletter.txt"

        if out_path.exists() and not regen_all:
            continue

        result = generate_newsletter(post, repo_root)

        if dry_run:
            print(f'  DRY-RUN would write data/newsletters/{slug}-newsletter.txt')
            print(f'    Subject: {result["subject"]}')
        else:
            out_path.write_text(result['body'], encoding='utf-8')
            print(f'  GENERATED data/newsletters/{slug}-newsletter.txt')

        generated += 1

    if generated == 0:
        print('  No new newsletters to generate.')
    else:
        print(f'\n  Generated newsletter copy for {generated} post(s).')


if __name__ == '__main__':
    main()
