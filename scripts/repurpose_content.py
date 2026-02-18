#!/usr/bin/env python3
"""
Content Repurposer for FixTheVuln.com
Takes a single blog post and generates 5+ social media posts from it.
One blog post = one full week of social content.

Usage:
    python3 scripts/repurpose_content.py              # Repurpose new posts
    python3 scripts/repurpose_content.py --dry-run    # Preview without writing
    python3 scripts/repurpose_content.py --all        # Regenerate all
"""

import json
import re
import sys
import random
from pathlib import Path


# CTA variations for Etsy
ETSY_CTAS = [
    "Studying for Security+? Grab the study planner at SmartSheetByRobert.etsy.com",
    "Need a study system? SmartSheetByRobert.etsy.com has planners for every major IT cert.",
    "Get organized for your exam: SmartSheetByRobert.etsy.com",
    "The ADHD-friendly cert study planner: SmartSheetByRobert.etsy.com",
]

# Quiz answer pools
QUIZ_WRONG_ANSWERS = [
    "Network segmentation",
    "Encryption at rest",
    "Multi-factor authentication",
    "Firewall rules",
    "Access control lists",
    "SIEM correlation",
    "Incident response plan",
    "Patch management",
    "Data loss prevention",
    "Endpoint detection",
    "Privileged access management",
    "Security awareness training",
]

HASHTAG_BASE = "#cybersecurity #infosec #securityplus #comptia #fixthevuln #itsecurity #cybersecuritytips #learninfosec"


def extract_sections(html_content):
    """Extract H2 and H3 sections with their content from HTML."""
    sections = []

    # Find all H2 sections
    h2_pattern = re.compile(r'<h2[^>]*>(.*?)</h2>(.*?)(?=<h2|$)', re.DOTALL)

    for match in h2_pattern.finditer(html_content):
        title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        body = match.group(2)

        # Extract text content (strip HTML)
        text = re.sub(r'<[^>]+>', ' ', body)
        text = re.sub(r'\s+', ' ', text).strip()

        # Extract list items
        items = re.findall(r'<li>(.*?)</li>', body, re.DOTALL)
        items = [re.sub(r'<[^>]+>', '', item).strip() for item in items]

        # Extract H3 subsections
        h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', body)
        h3s = [re.sub(r'<[^>]+>', '', h).strip() for h in h3s]

        sections.append({
            'title': title,
            'text': text[:500],  # first 500 chars
            'items': items[:6],  # first 6 list items
            'subsections': h3s,
        })

    return sections


def generate_tip_posts(sections, post_title, post_url):
    """Generate tip posts — one per major section."""
    tips = []
    for section in sections:
        if not section['text'] or len(section['text']) < 50:
            continue

        # Build tip content
        title = section['title']
        content = section['text'][:300]

        # Add bullet points if available
        bullets = ''
        if section['items']:
            bullet_items = section['items'][:4]
            bullets = '\n'.join(f"- {item[:80]}" for item in bullet_items)

        ig_caption = f"""Security tip: {title}

{content[:200]}...

{bullets}

Full breakdown on the blog — link in bio.

{HASHTAG_BASE} #{title.lower().replace(' ', '').replace('-', '')[:20]}"""

        fb_post = f"""Security Tip: {title}

{content}

{bullets}

Read the full article: {post_url}

{random.choice(ETSY_CTAS)}"""

        tips.append({
            'type': 'tip',
            'section': title,
            'instagram': {'caption': ig_caption},
            'facebook': {'post': fb_post},
        })

    return tips[:5]  # max 5 tip posts


def generate_did_you_know(sections, post_title, post_url):
    """Generate a 'did you know' hook post from the most interesting content."""
    # Find the section with the most compelling content
    best = None
    for section in sections:
        if any(w in section['text'].lower() for w in ['zero-day', 'critical', '9.8', '9.0', 'unprecedented', 'first time', 'million', 'billion']):
            best = section
            break
    if not best and sections:
        best = sections[0]
    if not best:
        return None

    text = best['text'][:250]

    ig_caption = f"""Did you know?

{text}

This is why staying current on threats matters — whether you're in the field or studying for your cert.

Save this. Share it with someone studying for Security+.

{HASHTAG_BASE} #didyouknow #cyberfacts"""

    fb_post = f"""Did you know?

{text}

We break down what this means for security professionals and how it maps to Security+ exam objectives.

Full article: {post_url}"""

    return {
        'type': 'did_you_know',
        'instagram': {'caption': ig_caption},
        'facebook': {'post': fb_post},
    }


def generate_quiz_post(sections, post_title, post_url):
    """Generate a quiz-style engagement post."""
    # Find a section with clear topic
    quiz_section = None
    for section in sections:
        if section['subsections'] or section['items']:
            quiz_section = section
            break
    if not quiz_section and sections:
        quiz_section = sections[0]
    if not quiz_section:
        return None

    topic = quiz_section['title']
    correct = topic

    # Pick wrong answers
    wrongs = random.sample(QUIZ_WRONG_ANSWERS, 3)

    # Shuffle options
    options = [correct] + wrongs
    random.shuffle(options)
    correct_letter = chr(65 + options.index(correct))  # A, B, C, or D

    ig_caption = f"""Pop quiz time!

Which Security+ concept is MOST relevant to: "{topic}"?

A) {options[0]}
B) {options[1]}
C) {options[2]}
D) {options[3]}

Drop your answer in the comments!

Answer: {correct_letter} — {correct}

Full explanation on the blog — link in bio.

{HASHTAG_BASE} #securityquiz #examprep #sy0701"""

    fb_post = f"""Quick Security+ Quiz!

Which concept is most relevant to: "{topic}"?

A) {options[0]}
B) {options[1]}
C) {options[2]}
D) {options[3]}

Comment your answer! Full explanation here: {post_url}"""

    return {
        'type': 'quiz',
        'question': topic,
        'correct_answer': f"{correct_letter}) {correct}",
        'instagram': {'caption': ig_caption},
        'facebook': {'post': fb_post},
    }


def generate_list_post(sections, post_title, post_url):
    """Generate a numbered list post from subsections or items."""
    # Collect all actionable items
    items = []
    for section in sections:
        if section['subsections']:
            items.extend(section['subsections'])
        elif section['items']:
            items.extend(section['items'][:3])

    if len(items) < 3:
        return None

    items = items[:6]  # max 6 items
    numbered = '\n'.join(f"{i+1}. {item[:80]}" for i, item in enumerate(items))

    ig_caption = f"""{len(items)} key takeaways from: {post_title[:60]}

{numbered}

Which one surprised you the most? Comment below!

Full breakdown on the blog — link in bio.

{HASHTAG_BASE} #cybersecuritytips #securitytips"""

    fb_post = f"""{len(items)} Key Takeaways: {post_title}

{numbered}

These map directly to Security+ SY0-701 exam objectives. Whether you're studying or working in the field, these are worth knowing.

Read the full analysis: {post_url}

{random.choice(ETSY_CTAS)}"""

    return {
        'type': 'list',
        'item_count': len(items),
        'instagram': {'caption': ig_caption},
        'facebook': {'post': fb_post},
    }


def generate_cta_post(post_title, post_url):
    """Generate a direct CTA post for the Etsy shop."""
    ig_caption = f"""Are you studying for Security+, CISSP, or another IT cert?

We just published a breakdown of the latest cybersecurity threats — and mapped them to actual exam objectives.

But knowing the threats is just step one. You need a SYSTEM to study effectively.

That's why we built structured study planners:
- study schedules
- Domain-by-domain trackers
- Practice exam schedules
- Time blocking templates
- Progress tracking

Available for Security+, CISSP, AWS, CCNA, and more.

Link in bio or visit SmartSheetByRobert.etsy.com

{HASHTAG_BASE} #studyplanner #certprep #itcertification #examprep"""

    fb_post = f"""New on the blog: {post_title}

Read it here: {post_url}

If you're preparing for Security+ or any IT certification, pair this knowledge with a structured study system.

Our planners at SmartSheetByRobert.etsy.com include:
- study schedules for every major IT cert
- Domain trackers and progress monitoring
- ADHD-friendly layouts with time blocking

Available for CompTIA, (ISC)2, AWS, and Cisco certifications.

Shop now: https://www.etsy.com/shop/SmartSheetByRobert"""

    return {
        'type': 'cta',
        'instagram': {'caption': ig_caption},
        'facebook': {'post': fb_post},
    }


def main():
    repo_root = Path(__file__).resolve().parent.parent
    dry_run = '--dry-run' in sys.argv
    regen_all = '--all' in sys.argv

    metadata_path = repo_root / 'data' / 'blog_metadata.json'
    blog_dir = repo_root / 'blog'
    social_dir = repo_root / 'data' / 'social'
    social_dir.mkdir(exist_ok=True)

    if not metadata_path.exists():
        print('  No blog_metadata.json found, skipping.')
        return

    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    posts = metadata.get('posts', [])

    if not posts:
        print('  No published posts found.')
        return

    generated = 0
    for post in posts:
        slug = post['slug']
        out_path = social_dir / f"{slug}-repurposed.json"

        if out_path.exists() and not regen_all:
            continue

        # Read the published HTML
        html_path = blog_dir / f"{slug}.html"
        if not html_path.exists():
            print(f'  SKIP {slug} (HTML not found)')
            continue

        html_content = html_path.read_text(encoding='utf-8')
        post_url = f"https://fixthevuln.com{post['url']}"

        # Extract sections
        sections = extract_sections(html_content)
        if not sections:
            print(f'  SKIP {slug} (no sections found)')
            continue

        # Generate all post types
        repurposed = {
            'slug': slug,
            'title': post['title'],
            'post_url': post_url,
            'posts': [],
        }

        # 1. Tip posts (1 per section, max 5)
        tips = generate_tip_posts(sections, post['title'], post_url)
        repurposed['posts'].extend(tips)

        # 2. Did you know
        dyk = generate_did_you_know(sections, post['title'], post_url)
        if dyk:
            repurposed['posts'].append(dyk)

        # 3. Quiz post
        quiz = generate_quiz_post(sections, post['title'], post_url)
        if quiz:
            repurposed['posts'].append(quiz)

        # 4. List post
        list_post = generate_list_post(sections, post['title'], post_url)
        if list_post:
            repurposed['posts'].append(list_post)

        # 5. CTA post
        cta = generate_cta_post(post['title'], post_url)
        repurposed['posts'].append(cta)

        repurposed['total_posts'] = len(repurposed['posts'])

        if dry_run:
            print(f'  DRY-RUN {slug}: {repurposed["total_posts"]} social posts')
        else:
            out_path.write_text(
                json.dumps(repurposed, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8'
            )
            print(f'  GENERATED {slug}: {repurposed["total_posts"]} social posts')

        generated += 1

    if generated == 0:
        print('  No new posts to repurpose.')
    else:
        print(f'\n  Repurposed {generated} post(s) into social content.')


if __name__ == '__main__':
    main()
