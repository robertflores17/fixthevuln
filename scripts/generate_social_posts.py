#!/usr/bin/env python3
"""
Social Media Copy Generator for FixTheVuln.com
Generates ready-to-paste Instagram, Facebook, and Twitter/X posts
for each newly published blog post.

Usage:
    python3 scripts/generate_social_posts.py              # Generate social copy
    python3 scripts/generate_social_posts.py --dry-run    # Preview without writing
    python3 scripts/generate_social_posts.py --all        # Regenerate for all posts
"""

import json
import sys
import random
from pathlib import Path


# Hashtag pools by topic
HASHTAG_POOLS = {
    'security': [
        '#cybersecurity', '#infosec', '#securityplus', '#comptia',
        '#hacking', '#ethicalhacking', '#pentest', '#cyberthreats',
        '#itsecurity', '#informationsecurity', '#cyberdefense',
        '#securityawareness', '#threatintelligence', '#blueteam',
        '#securityoperations', '#vulnerabilitymanagement',
    ],
    'certification': [
        '#securityplus', '#comptia', '#sy0701', '#itcertification',
        '#cybersecuritycertification', '#studyplanner', '#examprep',
        '#itcareers', '#cybersecuritycareer', '#techcareers',
        '#certificationgoals', '#studytips', '#passthefirsttime',
    ],
    'threats': [
        '#cyberthreats', '#cve', '#vulnerability', '#zerodayattack',
        '#malware', '#ransomware', '#phishing', '#datasecurity',
        '#cisakev', '#threatintel', '#incidentresponse',
        '#patchmanagement', '#riskmanagement',
    ],
    'ai': [
        '#aiinsecurity', '#artificialintelligence', '#agenticai',
        '#aisecurity', '#machinelearning', '#aithreats',
        '#cybersecurityai', '#securityautomation',
    ],
    'general': [
        '#fixthevuln', '#cybersecuritytips', '#techsecurity',
        '#learninfosec', '#securityguide', '#cybered',
        '#digitalsecurity', '#onlinesafety',
    ],
}

# Hook templates (randomized for variety)
INSTAGRAM_HOOKS = [
    "Most people don't realize this about {topic}...",
    "If you're studying for Security+, you NEED to know this.",
    "This changes everything about {topic}.",
    "Here's what no one tells you about {topic}.",
    "Security professionals are talking about this.",
    "Your Security+ exam will test you on this.",
    "This is the #1 thing to know about {topic} right now.",
    "Stop scrolling. This is important for your career.",
]

FACEBOOK_HOOKS = [
    "Just published a deep dive on {topic}.",
    "If you're in cybersecurity, this matters to you.",
    "New on the FixTheVuln blog: {title}",
    "This is what every IT professional needs to understand about {topic}.",
    "We just broke down {topic} and mapped it to Security+ exam domains.",
]

TWITTER_TEMPLATES = [
    "{title}\n\n{key_point}\n\nRead more: {url}",
    "New post: {title}\n\n{key_point}\n\n{url}",
    "{key_point}\n\nFull breakdown: {url}",
]


def generate_hashtags(post, count=25):
    """Generate relevant hashtags based on post content."""
    title_lower = post.get('title', '').lower()
    desc_lower = post.get('excerpt', '').lower()
    combined = title_lower + ' ' + desc_lower

    tags = set()

    # Always include general tags
    tags.update(random.sample(HASHTAG_POOLS['general'], min(4, len(HASHTAG_POOLS['general']))))

    # Add topic-specific tags
    if any(w in combined for w in ['security+', 'comptia', 'certification', 'exam', 'sy0-701']):
        tags.update(random.sample(HASHTAG_POOLS['certification'], min(6, len(HASHTAG_POOLS['certification']))))

    if any(w in combined for w in ['ai', 'agentic', 'artificial intelligence', 'machine learning']):
        tags.update(random.sample(HASHTAG_POOLS['ai'], min(5, len(HASHTAG_POOLS['ai']))))

    if any(w in combined for w in ['cve', 'vulnerability', 'threat', 'exploit', 'kev', 'cisa']):
        tags.update(random.sample(HASHTAG_POOLS['threats'], min(6, len(HASHTAG_POOLS['threats']))))

    # Fill remaining with security tags
    remaining = count - len(tags)
    if remaining > 0:
        available = [t for t in HASHTAG_POOLS['security'] if t not in tags]
        tags.update(random.sample(available, min(remaining, len(available))))

    return ' '.join(sorted(tags)[:count])


def extract_key_point(post):
    """Extract a compelling key point from the post description."""
    desc = post.get('excerpt', '')
    if len(desc) > 200:
        # Truncate at sentence boundary
        sentences = desc.split('. ')
        result = sentences[0] + '.'
        if len(result) < 100 and len(sentences) > 1:
            result += ' ' + sentences[1] + '.'
        return result
    return desc


def extract_topic(post):
    """Extract the main topic from the title."""
    title = post.get('title', '')
    # Remove common prefixes/suffixes
    topic = title.split('.')[0].split(':')[0].split('—')[0].strip()
    # Shorten if too long
    if len(topic) > 50:
        words = topic.split()
        topic = ' '.join(words[:6])
    return topic.lower()


def generate_instagram(post):
    """Generate Instagram caption with hashtags."""
    title = post['title']
    topic = extract_topic(post)
    key_point = extract_key_point(post)
    url = f"https://fixthevuln.com{post['url']}"
    hashtags = generate_hashtags(post)

    hook = random.choice(INSTAGRAM_HOOKS).format(topic=topic)

    caption = f"""{hook}

{key_point}

We broke this down on the blog with actionable takeaways — link in bio.

Key points:
- What it means for security professionals
- How it maps to Security+ exam domains
- What you can do about it right now

Save this post for your study sessions.

{hashtags}"""

    return {
        'caption': caption,
        'hashtags': hashtags,
        'url': url,
    }


def generate_facebook(post):
    """Generate Facebook post with link."""
    title = post['title']
    topic = extract_topic(post)
    key_point = extract_key_point(post)
    url = f"https://fixthevuln.com{post['url']}"

    hook = random.choice(FACEBOOK_HOOKS).format(topic=topic, title=title)

    fb_post = f"""{hook}

{key_point}

If you're studying for Security+ or working in IT security, this breakdown maps directly to the SY0-701 exam objectives — so you're learning real-world skills AND exam material at the same time.

Read the full analysis: {url}

Studying for a certification? Check out our study planners at SmartSheetByRobert.etsy.com — structured plans with domain trackers and exam strategies."""

    return {
        'post': fb_post,
        'url': url,
    }


def generate_twitter(post):
    """Generate Twitter/X post (280 char max)."""
    title = post['title']
    key_point = extract_key_point(post)
    url = f"https://fixthevuln.com{post['url']}"

    # Shorten key point to fit
    max_point_len = 280 - len(url) - 20  # leave room for URL and newlines
    if len(key_point) > max_point_len:
        key_point = key_point[:max_point_len - 3] + '...'

    template = random.choice(TWITTER_TEMPLATES)
    tweet = template.format(title=title, key_point=key_point, url=url)

    # Ensure under 280 chars
    if len(tweet) > 280:
        tweet = f"{key_point[:200]}...\n\n{url}"

    return {
        'tweet': tweet,
        'url': url,
    }


def main():
    repo_root = Path(__file__).resolve().parent.parent
    dry_run = '--dry-run' in sys.argv
    regen_all = '--all' in sys.argv

    metadata_path = repo_root / 'data' / 'blog_metadata.json'
    social_dir = repo_root / 'data' / 'social'
    social_dir.mkdir(exist_ok=True)

    if not metadata_path.exists():
        print('  No blog_metadata.json found, skipping social generation.')
        return

    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    posts = metadata.get('posts', [])

    if not posts:
        print('  No published posts found.')
        return

    generated = 0
    for post in posts:
        slug = post['slug']
        out_path = social_dir / f"{slug}-social.json"

        if out_path.exists() and not regen_all:
            continue

        social_data = {
            'slug': slug,
            'title': post['title'],
            'generated': post.get('date', ''),
            'instagram': generate_instagram(post),
            'facebook': generate_facebook(post),
            'twitter': generate_twitter(post),
        }

        if dry_run:
            print(f'  DRY-RUN would write data/social/{slug}-social.json')
        else:
            out_path.write_text(
                json.dumps(social_data, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8'
            )
            print(f'  GENERATED data/social/{slug}-social.json')

        generated += 1

    if generated == 0:
        print('  No new social posts to generate.')
    else:
        print(f'\n  Generated social copy for {generated} post(s).')


if __name__ == '__main__':
    main()
