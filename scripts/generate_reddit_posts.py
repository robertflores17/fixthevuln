#!/usr/bin/env python3
"""
Reddit Post Generator for FixTheVuln.com
Reads data/blog_metadata.json and generates Reddit post templates
for each blog article — 3 post types targeting different subreddits.

Usage:
    python3 scripts/generate_reddit_posts.py              # Generate reddit posts
    python3 scripts/generate_reddit_posts.py --dry-run    # Preview without writing
    python3 scripts/generate_reddit_posts.py --all        # Regenerate for all posts
"""

import json
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
METADATA_PATH = REPO_ROOT / 'data' / 'blog_metadata.json'
SOCIAL_DIR = REPO_ROOT / 'data' / 'social'

# Free tools on the site that can be shared
SITE_TOOLS = [
    {'name': 'Security+ Practice Quiz', 'path': 'security-quiz.html',
     'desc': '300 questions mapped to SY0-701 domains with explanations'},
    {'name': 'CVSS Calculator', 'path': 'cvss-calculator.html',
     'desc': 'Interactive CVSS v3.1 score calculator with severity breakdown'},
    {'name': 'Security Headers Checker', 'path': 'security-headers.html',
     'desc': 'Check if your site has the right HTTP security headers'},
    {'name': 'Password Strength Checker', 'path': 'password-strength.html',
     'desc': 'Test password strength with entropy analysis'},
    {'name': 'CVE Database', 'path': 'cve/',
     'desc': 'Browse CISA KEV vulnerabilities with fix guidance and CVSS scores'},
    {'name': 'Certification Comparisons', 'path': 'comparisons/',
     'desc': 'Side-by-side cert comparisons (Security+ vs CySA+, CISSP vs CISM, etc.)'},
]

# Subreddit-specific guidance
SUBREDDIT_NOTES = {
    'r/cybersecurity': {
        'rules': 'No self-promotion spam. Value-first posts welcome. Flair as Discussion or News.',
        'tone': 'Professional, analytical. Lead with insight, not link.',
        'schedule': 'Monday',
    },
    'r/CompTIA': {
        'rules': 'Study resources welcome if helpful. No spam. Flair as Resource or Study Material.',
        'tone': 'Helpful, encouraging. Speak to students prepping for exams.',
        'schedule': 'Wednesday',
    },
    'r/ITCareerQuestions': {
        'rules': 'Questions and advice threads. No direct self-promotion. Link only if relevant.',
        'tone': 'Conversational, career-focused. Frame as discussion, not promotion.',
        'schedule': 'Friday',
    },
}


def extract_topic(post):
    """Extract the main topic from the title."""
    title = post.get('title', '')
    topic = title.split('.')[0].split(':')[0].split('—')[0].strip()
    if len(topic) > 60:
        words = topic.split()
        topic = ' '.join(words[:8])
    return topic


def extract_key_insight(post):
    """Extract a key insight from the excerpt."""
    excerpt = post.get('excerpt', '')
    sentences = excerpt.split('. ')
    if len(sentences) >= 2:
        return sentences[0] + '. ' + sentences[1] + '.'
    return sentences[0] + '.' if sentences else excerpt


def generate_value_post(post):
    """Generate a value-first post for r/cybersecurity."""
    title = post['title']
    topic = extract_topic(post)
    insight = extract_key_insight(post)
    url = f"https://fixthevuln.com{post['url']}"

    post_titles = [
        f"{topic} — what security teams should know",
        f"Breaking down {topic.lower()} for defenders",
        f"{topic}: practical implications for your security program",
    ]

    body = f"""I've been researching {topic.lower()} and wanted to share some key takeaways:

{insight}

The part that stood out most to me is how this maps to real-world security operations — it's not just theoretical. If you're running a SOC or managing vulnerability programs, this directly affects your threat model.

Key points:
- How this changes the threat landscape for defenders
- Practical mitigations you can implement now
- Which frameworks/controls address this (mapped to Security+ domains for those studying)

I wrote up a detailed analysis here if you want the full breakdown: {url}

What's your team doing to address this? Curious to hear how others are handling it."""

    return {
        'subreddit': 'r/cybersecurity',
        'title_options': post_titles,
        'body': body,
        'notes': SUBREDDIT_NOTES['r/cybersecurity'],
    }


def generate_tool_share(post):
    """Generate a tool-share post for r/CompTIA."""
    title = post['title']
    topic = extract_topic(post)
    url = f"https://fixthevuln.com{post['url']}"

    # Pick a random tool to highlight
    tool = random.choice(SITE_TOOLS)
    tool_url = f"https://fixthevuln.com/{tool['path']}"

    post_titles = [
        f"Free resource: {tool['name']} for Security+ prep",
        f"Built a free {tool['name'].lower()} — might help with your studies",
        f"Free {tool['name'].lower()} mapped to SY0-701 objectives",
    ]

    body = f"""Hey everyone! Wanted to share a free tool that might help with your studies:

**{tool['name']}**: {tool['desc']}

Link: {tool_url}

It's completely free, no sign-up required. I built it as part of FixTheVuln.com, which has free security guides and tools.

Related: I also wrote up a breakdown of {topic.lower()} that maps to Security+ exam domains — useful if you're studying for SY0-701: {url}

Some other free tools on the site:
{chr(10).join(f'- **{t["name"]}**: {t["desc"]}' for t in SITE_TOOLS[:3] if t != tool)}

Hope this helps someone! Let me know if you have feedback or suggestions."""

    return {
        'subreddit': 'r/CompTIA',
        'title_options': post_titles,
        'body': body,
        'notes': SUBREDDIT_NOTES['r/CompTIA'],
    }


def generate_discussion_starter(post):
    """Generate a discussion-starter post for r/ITCareerQuestions."""
    title = post['title']
    topic = extract_topic(post)
    insight = extract_key_insight(post)
    url = f"https://fixthevuln.com{post['url']}"

    discussion_angles = [
        {
            'title': f"How is {topic.lower()} changing the job market for security roles?",
            'body': f"""I've been reading about {topic.lower()} and it got me thinking about career implications.

{insight}

For those of you working in security or transitioning into the field:

1. Are you seeing this come up in job interviews or requirements?
2. How are employers expecting candidates to address this?
3. Which certifications best prepare you for these kinds of challenges?

I found a good breakdown here that maps it to Security+ domains: {url}

But I'm more curious about the career angle — is this something hiring managers actually care about, or is it more of a "nice to know"?""",
        },
        {
            'title': f"Career advice: should I focus on {topic.lower()} as a specialization?",
            'body': f"""Trying to figure out my next career move and {topic.lower()} keeps coming up.

{insight}

I'm currently studying for Security+ and wondering if this is an area worth specializing in. For those already in the field:

- Is there demand for people who understand this?
- What certs/skills pair well with this knowledge?
- Is this a growing area or just a temporary trend?

Related reading that helped me understand the landscape: {url}

Would love to hear from anyone who's navigated a similar decision.""",
        },
    ]

    angle = random.choice(discussion_angles)

    return {
        'subreddit': 'r/ITCareerQuestions',
        'title_options': [angle['title']],
        'body': angle['body'],
        'notes': SUBREDDIT_NOTES['r/ITCareerQuestions'],
    }


def main():
    dry_run = '--dry-run' in sys.argv
    regen_all = '--all' in sys.argv

    if not METADATA_PATH.exists():
        print('  No blog_metadata.json found, skipping Reddit generation.')
        return

    SOCIAL_DIR.mkdir(exist_ok=True)

    metadata = json.loads(METADATA_PATH.read_text(encoding='utf-8'))
    posts = metadata.get('posts', [])

    if not posts:
        print('  No published posts found.')
        return

    generated = 0
    for post in posts:
        slug = post['slug']
        out_path = SOCIAL_DIR / f"{slug}-reddit.json"

        if out_path.exists() and not regen_all:
            continue

        reddit_data = {
            'slug': slug,
            'title': post['title'],
            'generated': post.get('date', ''),
            'posting_schedule': {
                'monday': 'r/cybersecurity — value post',
                'wednesday': 'r/CompTIA — tool share',
                'friday': 'r/ITCareerQuestions — discussion starter',
            },
            'posts': {
                'value_post': generate_value_post(post),
                'tool_share': generate_tool_share(post),
                'discussion_starter': generate_discussion_starter(post),
            },
        }

        if dry_run:
            print(f'  DRY-RUN would write data/social/{slug}-reddit.json')
        else:
            out_path.write_text(
                json.dumps(reddit_data, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8',
            )
            print(f'  GENERATED data/social/{slug}-reddit.json')

        generated += 1

    if generated == 0:
        print('  No new Reddit posts to generate.')
    else:
        print(f'\n  Generated Reddit templates for {generated} post(s).')


if __name__ == '__main__':
    main()
