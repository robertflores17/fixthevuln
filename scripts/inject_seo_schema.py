#!/usr/bin/env python3
"""Inject SEO schema (Quiz, FAQPage) into existing pages.

- Quiz pages (66): adds Quiz schema after BreadcrumbList
- Roadmap pages (66): adds FAQPage schema after BreadcrumbList
- Blog study guide pages (~63): adds FAQPage schema after BreadcrumbList

Idempotent — safe to re-run. Skips pages that already have the target schema.

Usage:
    python3 scripts/inject_seo_schema.py              # Inject all
    python3 scripts/inject_seo_schema.py --dry-run     # Preview only
    python3 scripts/inject_seo_schema.py --quiz-only   # Quiz pages only
    python3 scripts/inject_seo_schema.py --roadmap-only
    python3 scripts/inject_seo_schema.py --blog-only
"""

import argparse
import json
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ── Helpers ──────────────────────────────────────────────────────────────

def esc_json(s):
    """Escape a string for safe embedding inside a JSON string value."""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def build_ld_json(obj):
    """Return a pretty-printed <script type="application/ld+json"> block."""
    blob = json.dumps(obj, indent=4, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{blob}\n</script>'


def find_breadcrumb_end(html):
    """Find insertion point right after the last BreadcrumbList ld+json block.
    Returns the character index right after the closing </script> tag."""
    # Find all ld+json blocks
    pattern = r'<script\s+type="application/ld\+json">\s*\{[^<]*"@type"\s*:\s*"BreadcrumbList"[^<]*</script>'
    matches = list(re.finditer(pattern, html, re.DOTALL))
    if matches:
        return matches[-1].end()
    return -1


def find_tech_article_breadcrumb_end(html):
    """Find insertion point after both TechArticle + BreadcrumbList blocks.
    Returns the character index right after the last of the two."""
    # Find all ld+json blocks
    blocks = list(re.finditer(
        r'<script\s+type="application/ld\+json">\s*\{.*?</script>',
        html, re.DOTALL
    ))
    if not blocks:
        return -1
    # Return end of the last schema block in <head>
    head_end = html.find('</head>')
    last_block = None
    for b in blocks:
        if b.end() < head_end:
            last_block = b
    return last_block.end() if last_block else -1


# ── Quiz Schema ──────────────────────────────────────────────────────────

def extract_quiz_info(html, filepath):
    """Extract quiz metadata from HTML for Quiz schema."""
    # Title: "Free CompTIA Security+ Practice Quiz — SY0-701 Questions - FixTheVuln"
    title_m = re.search(r'<title>(.+?)</title>', html)
    if not title_m:
        return None
    title = title_m.group(1).replace('&mdash;', '—').replace('&#8212;', '—').strip()
    # Remove " - FixTheVuln" suffix
    title = re.sub(r'\s*-\s*FixTheVuln$', '', title)
    # Remove "Free " prefix for schema name
    quiz_name = re.sub(r'^Free\s+', '', title)
    # Strip trailing "— ..." (exam code or question count)
    quiz_name = re.sub(r'\s*—.*$', '', quiz_name)

    # Total questions — prefer tagline which always has the real count
    # Tagline: "... Practice Quiz — 30 Questions" or "... Quiz — 250 Questions Across 8 Domains"
    total_q = None
    tag_m = re.search(r'class="tagline"[^>]*>[^<]*?(\d+)\s+Questions', html)
    if tag_m:
        total_q = int(tag_m.group(1))

    # Domains from QuizEngine.init config — find all name:'...' entries
    # after the 'domains:' key in the script block
    domains = []
    domains_section = re.search(r'domains:\s*\{(.+?)\}\s*,\s*\n\s*fallback', html, re.DOTALL)
    if not domains_section:
        # Try without fallback anchor (hand-crafted pages)
        domains_section = re.search(r'domains:\s*\{(.+?)\}\s*,', html, re.DOTALL)
    if domains_section:
        domain_block = domains_section.group(1)
        for dm in re.finditer(r"name:\s*'([^']+)'", domain_block):
            domains.append(dm.group(1))

    # "About" — the cert/exam name
    about_name = quiz_name.replace(' Practice Quiz', '').strip()

    return {
        'name': quiz_name,
        'about': about_name,
        'total_questions': total_q,
        'domains': domains,
    }


def build_quiz_schema(info):
    """Build Quiz schema.org object."""
    obj = {
        "@context": "https://schema.org",
        "@type": "Quiz",
        "name": info['name'],
        "about": {
            "@type": "Thing",
            "name": info['about']
        },
        "educationalLevel": "Professional",
    }
    if info['total_questions']:
        obj["numberOfQuestions"] = info['total_questions']
    if info['domains']:
        obj["assesses"] = info['domains']
    return obj


def process_quiz_pages(dry_run=False):
    """Inject Quiz schema into quiz pages."""
    quiz_files = sorted(REPO.glob('*-quiz.html'))
    stats = {'processed': 0, 'skipped': 0, 'modified': 0, 'errors': 0}

    for fp in quiz_files:
        fname = fp.name
        html = fp.read_text(encoding='utf-8')

        # Idempotent check
        if '"@type": "Quiz"' in html or '"@type":"Quiz"' in html:
            stats['skipped'] += 1
            continue

        stats['processed'] += 1
        info = extract_quiz_info(html, fp)
        if not info:
            print(f'  SKIP {fname}: could not extract quiz info')
            stats['errors'] += 1
            continue

        insert_pos = find_breadcrumb_end(html)
        if insert_pos == -1:
            print(f'  SKIP {fname}: no BreadcrumbList found')
            stats['errors'] += 1
            continue

        schema_block = build_ld_json(build_quiz_schema(info))
        new_html = html[:insert_pos] + '\n    ' + schema_block + html[insert_pos:]

        if dry_run:
            q = info['total_questions'] or '?'
            d = len(info['domains'])
            print(f'  [DRY RUN] {fname}: Quiz schema ({q} questions, {d} domains)')
        else:
            fp.write_text(new_html, encoding='utf-8')
            print(f'  INJECTED {fname}: Quiz schema')
        stats['modified'] += 1

    return stats


# ── Roadmap FAQPage Schema ───────────────────────────────────────────────

def extract_roadmap_info(html, filepath):
    """Extract roadmap metadata from HTML for FAQPage schema."""
    # Title: "CompTIA Security+ Study Roadmap — Free Week-by-Week Plan | FixTheVuln"
    title_m = re.search(r'<title>(.+?)</title>', html)
    if not title_m:
        return None
    raw_title = title_m.group(1).replace('&mdash;', '—').strip()
    # Extract cert name: everything before " Study Roadmap"
    cert_m = re.search(r'^(.+?)\s+Study Roadmap', raw_title)
    cert_name = cert_m.group(1) if cert_m else raw_title.split('|')[0].strip()

    # Number of weeks from NUM_WEEKS constant in script
    weeks_m = re.search(r'const\s+NUM_WEEKS\s*=\s*(\d+)', html)
    num_weeks = int(weeks_m.group(1)) if weeks_m else None

    # Domain names + weights from heatmap bars
    # Supports: "12%", "20-25%", "~23%"
    domains = []
    for dm in re.finditer(
        r'<span[^>]*>D\d+:\s*(.+?)</span>.*?>(~?[\d]+(?:-[\d]+)?(?:\.[\d]+)?)%</div>',
        html, re.DOTALL
    ):
        domains.append({'name': dm.group(1).strip(), 'weight': dm.group(2)})

    return {
        'cert_name': cert_name,
        'num_weeks': num_weeks,
        'domains': domains,
    }


def build_roadmap_faq(info):
    """Build FAQPage schema for a roadmap page."""
    cert = info['cert_name']
    weeks = info['num_weeks']

    # Q1: Study duration
    if weeks:
        a1 = (f"A structured study plan for {cert} spans {weeks} weeks. "
              f"Each week focuses on specific exam domains with targeted objectives, "
              f"building knowledge progressively from foundational concepts to advanced topics.")
    else:
        a1 = (f"Study duration for {cert} varies by experience level. "
              f"Follow a structured week-by-week roadmap that covers all exam domains progressively.")

    # Q2: Domain coverage
    if info['domains']:
        domain_list = ', '.join(
            f"{d['name']} ({d['weight']}%)" for d in info['domains']
        )
        a2 = f"The {cert} exam covers these domains: {domain_list}. Focus more study time on higher-weighted domains."
    else:
        a2 = f"The {cert} exam covers multiple domains. Check the official exam objectives for the complete domain breakdown and weight distribution."

    # Q3: Study approach
    a3 = (f"The best study approach for {cert} is to follow a structured roadmap: "
          f"start with the domain heatmap to understand weight distribution, "
          f"then work through each week's objectives sequentially. "
          f"Use practice quizzes to test retention and track your progress with the built-in checklist.")

    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"How long should I study for {cert}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a1
                }
            },
            {
                "@type": "Question",
                "name": f"What domains does the {cert} exam cover?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a2
                }
            },
            {
                "@type": "Question",
                "name": f"What's the best study approach for {cert}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a3
                }
            }
        ]
    }
    return faq


def process_roadmap_pages(dry_run=False):
    """Inject FAQPage schema into roadmap pages."""
    roadmaps_dir = REPO / 'roadmaps'
    if not roadmaps_dir.exists():
        print('  WARNING: roadmaps/ directory not found')
        return {'processed': 0, 'skipped': 0, 'modified': 0, 'errors': 0}

    stats = {'processed': 0, 'skipped': 0, 'modified': 0, 'errors': 0}

    for fp in sorted(roadmaps_dir.glob('*.html')):
        fname = fp.name
        if fname == 'index.html':
            continue

        html = fp.read_text(encoding='utf-8')

        # Idempotent check
        if '"@type": "FAQPage"' in html or '"@type":"FAQPage"' in html:
            stats['skipped'] += 1
            continue

        stats['processed'] += 1
        info = extract_roadmap_info(html, fp)
        if not info:
            print(f'  SKIP roadmaps/{fname}: could not extract roadmap info')
            stats['errors'] += 1
            continue

        insert_pos = find_breadcrumb_end(html)
        if insert_pos == -1:
            print(f'  SKIP roadmaps/{fname}: no BreadcrumbList found')
            stats['errors'] += 1
            continue

        schema_block = build_ld_json(build_roadmap_faq(info))
        new_html = html[:insert_pos] + '\n    ' + schema_block + html[insert_pos:]

        if dry_run:
            w = info['num_weeks'] or '?'
            d = len(info['domains'])
            print(f'  [DRY RUN] roadmaps/{fname}: FAQPage ({w} weeks, {d} domains)')
        else:
            fp.write_text(new_html, encoding='utf-8')
            print(f'  INJECTED roadmaps/{fname}: FAQPage schema')
        stats['modified'] += 1

    return stats


# ── Blog FAQPage Schema ─────────────────────────────────────────────────

def extract_blog_info(html, filepath):
    """Extract blog study guide metadata for FAQPage schema."""
    title_m = re.search(r'<title>(.+?)</title>', html)
    if not title_m:
        return None
    raw_title = title_m.group(1).strip()
    # Remove " - FixTheVuln"
    title = re.sub(r'\s*-\s*FixTheVuln$', '', raw_title)

    # Extract cert name from title like "CompTIA Security+ Study Guide: Everything..."
    cert_m = re.search(r'^(.+?)\s+Study Guide', title)
    cert_name = cert_m.group(1).strip() if cert_m else title.split(':')[0].strip()

    # Meta description
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    description = desc_m.group(1) if desc_m else ''

    return {
        'cert_name': cert_name,
        'title': title,
        'description': description,
    }


def build_blog_faq(info):
    """Build FAQPage schema for a blog study guide."""
    cert = info['cert_name']
    desc = info['description']

    # Q1: What does the exam cover?
    if desc:
        a1 = f"{desc} Review the complete domain breakdown and exam objectives to build a targeted study plan."
    else:
        a1 = f"The {cert} exam covers multiple domains testing both theoretical knowledge and practical skills. Review the official exam objectives for the complete breakdown."

    # Q2: How to prepare?
    a2 = (f"To prepare for {cert}, follow a structured study plan: "
          f"start with the exam objectives and domain weights, "
          f"use official study materials and practice tests, "
          f"and track your progress across all domains. "
          f"Focus extra time on heavily-weighted domains and weak areas identified through practice quizzes.")

    # Q3: Is it worth it?
    a3 = (f"The {cert} certification validates in-demand skills and is recognized by employers worldwide. "
          f"It demonstrates professional competency, can lead to higher salaries, "
          f"and opens doors to specialized roles in IT and cybersecurity. "
          f"Many job postings list it as a preferred or required qualification.")

    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"What does the {cert} exam cover?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a1
                }
            },
            {
                "@type": "Question",
                "name": f"How should I prepare for {cert}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a2
                }
            },
            {
                "@type": "Question",
                "name": f"Is the {cert} certification worth it?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a3
                }
            }
        ]
    }
    return faq


def process_blog_pages(dry_run=False):
    """Inject FAQPage schema into blog study guide pages."""
    blog_dir = REPO / 'blog'
    if not blog_dir.exists():
        print('  WARNING: blog/ directory not found')
        return {'processed': 0, 'skipped': 0, 'modified': 0, 'errors': 0}

    stats = {'processed': 0, 'skipped': 0, 'modified': 0, 'errors': 0}

    for fp in sorted(blog_dir.glob('*-study-guide.html')):
        fname = fp.name
        html = fp.read_text(encoding='utf-8')

        # Idempotent check
        if '"@type": "FAQPage"' in html or '"@type":"FAQPage"' in html:
            stats['skipped'] += 1
            continue

        stats['processed'] += 1
        info = extract_blog_info(html, fp)
        if not info:
            print(f'  SKIP blog/{fname}: could not extract blog info')
            stats['errors'] += 1
            continue

        insert_pos = find_tech_article_breadcrumb_end(html)
        if insert_pos == -1:
            print(f'  SKIP blog/{fname}: no schema blocks found')
            stats['errors'] += 1
            continue

        schema_block = build_ld_json(build_blog_faq(info))
        new_html = html[:insert_pos] + '\n    ' + schema_block + html[insert_pos:]

        if dry_run:
            print(f'  [DRY RUN] blog/{fname}: FAQPage ({info["cert_name"]})')
        else:
            fp.write_text(new_html, encoding='utf-8')
            print(f'  INJECTED blog/{fname}: FAQPage schema')
        stats['modified'] += 1

    return stats


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Inject SEO schema into FixTheVuln pages')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without writing')
    parser.add_argument('--quiz-only', action='store_true', help='Only process quiz pages')
    parser.add_argument('--roadmap-only', action='store_true', help='Only process roadmap pages')
    parser.add_argument('--blog-only', action='store_true', help='Only process blog pages')
    args = parser.parse_args()

    # If no filter specified, process all
    do_all = not (args.quiz_only or args.roadmap_only or args.blog_only)

    mode = '[DRY RUN] ' if args.dry_run else ''
    print(f'\n{mode}SEO Schema Injection')
    print('=' * 50)

    total = {'processed': 0, 'skipped': 0, 'modified': 0, 'errors': 0}

    if do_all or args.quiz_only:
        print(f'\n{mode}Quiz Pages (Quiz schema)')
        print('-' * 40)
        stats = process_quiz_pages(dry_run=args.dry_run)
        for k in total:
            total[k] += stats[k]
        print(f'  → {stats["modified"]} modified, {stats["skipped"]} skipped, {stats["errors"]} errors')

    if do_all or args.roadmap_only:
        print(f'\n{mode}Roadmap Pages (FAQPage schema)')
        print('-' * 40)
        stats = process_roadmap_pages(dry_run=args.dry_run)
        for k in total:
            total[k] += stats[k]
        print(f'  → {stats["modified"]} modified, {stats["skipped"]} skipped, {stats["errors"]} errors')

    if do_all or args.blog_only:
        print(f'\n{mode}Blog Study Guide Pages (FAQPage schema)')
        print('-' * 40)
        stats = process_blog_pages(dry_run=args.dry_run)
        for k in total:
            total[k] += stats[k]
        print(f'  → {stats["modified"]} modified, {stats["skipped"]} skipped, {stats["errors"]} errors')

    print(f'\n{"=" * 50}')
    print(f'TOTAL: {total["modified"]} modified, {total["skipped"]} skipped, {total["errors"]} errors')
    print()


if __name__ == '__main__':
    main()
