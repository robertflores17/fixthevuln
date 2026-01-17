#!/usr/bin/env python3
"""
FixTheVuln - Automated Security News Fetcher with Unsplash Images
Fetches latest security vulnerabilities and news from multiple sources
"""

import os
import json
import requests
from datetime import datetime
import feedparser
from pathlib import Path
import hashlib
import time

# Configuration
NEWS_SOURCES = {
    'cisa_kev': 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',
    'nvd_recent': 'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=10',
    'bleeping_computer': 'https://www.bleepingcomputer.com/feed/',
    'thehackernews': 'https://feeds.feedburner.com/TheHackersNews',
}

OUTPUT_DIR = Path('posts')
IMAGES_DIR = Path('images')
TEMPLATE_FILE = Path('post-template.html')

# Unsplash API
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY', '')
UNSPLASH_API_URL = 'https://api.unsplash.com/photos/random'

# Security-related search terms for images
IMAGE_KEYWORDS = [
    'cybersecurity',
    'hacking',
    'computer security',
    'network security',
    'data security',
    'code security',
    'digital security',
    'cyber attack',
]

def fetch_unsplash_image(query='cybersecurity', post_title=''):
    """Fetch a random security-related image from Unsplash"""
    if not UNSPLASH_ACCESS_KEY:
        print("⚠️  No Unsplash API key found. Skipping image fetch.")
        return None
    
    try:
        # Try to match image to post topic
        if 'docker' in post_title.lower() or 'container' in post_title.lower():
            query = 'containers technology'
        elif 'sql' in post_title.lower() or 'database' in post_title.lower():
            query = 'database security'
        elif 'jenkins' in post_title.lower() or 'ci/cd' in post_title.lower():
            query = 'devops security'
        elif 'cloud' in post_title.lower():
            query = 'cloud computing'
        else:
            # Use random security keyword
            import random
            query = random.choice(IMAGE_KEYWORDS)
        
        params = {
            'query': query,
            'orientation': 'landscape',
            'client_id': UNSPLASH_ACCESS_KEY,
        }
        
        response = requests.get(UNSPLASH_API_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            image_url = data['urls']['regular']  # High quality but not too large
            image_id = data['id']
            photographer = data['user']['name']
            photographer_url = data['user']['links']['html']
            
            return {
                'url': image_url,
                'id': image_id,
                'photographer': photographer,
                'photographer_url': photographer_url,
                'download_link': f"{photographer_url}?utm_source=fixthevuln&utm_medium=referral"
            }
        else:
            print(f"⚠️  Unsplash API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"⚠️  Error fetching Unsplash image: {e}")
        return None

def download_image(image_data, post_id):
    """Download and save image locally"""
    if not image_data:
        return None
    
    try:
        # Create images directory if it doesn't exist
        IMAGES_DIR.mkdir(exist_ok=True)
        
        # Generate filename from post_id
        filename = f"post-{post_id}.jpg"
        filepath = IMAGES_DIR / filename
        
        # Download image
        response = requests.get(image_data['url'], timeout=15)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"📷 Downloaded image: {filename}")
            return f"../images/{filename}"
        else:
            return None
            
    except Exception as e:
        print(f"⚠️  Error downloading image: {e}")
        return None

def fetch_cisa_kev():
    """Fetch CISA Known Exploited Vulnerabilities"""
    try:
        response = requests.get(NEWS_SOURCES['cisa_kev'], timeout=10)
        data = response.json()
        
        vulnerabilities = data.get('vulnerabilities', [])[:5]  # Get latest 5
        posts = []
        
        for vuln in vulnerabilities:
            posts.append({
                'title': f"CISA Alert: {vuln.get('cveID')} - {vuln.get('vulnerabilityName')}",
                'description': f"{vuln.get('shortDescription')} (Vendor: {vuln.get('vendorProject')})",
                'source': 'CISA KEV',
                'date': vuln.get('dateAdded', datetime.now().strftime('%Y-%m-%d')),
                'link': f"https://nvd.nist.gov/vuln/detail/{vuln.get('cveID')}",
                'severity': 'Critical' if 'ransomware' in vuln.get('knownRansomwareCampaignUse', '').lower() else 'High',
                'cve_id': vuln.get('cveID'),
                'remediation_hint': vuln.get('requiredAction', 'Apply vendor patches immediately')
            })
        
        return posts
    except Exception as e:
        print(f"Error fetching CISA KEV: {e}")
        return []

def fetch_rss_feed(feed_url, source_name, max_items=3):
    """Fetch and parse RSS feeds"""
    try:
        feed = feedparser.parse(feed_url)
        posts = []
        
        for entry in feed.entries[:max_items]:
            # Extract date
            published = entry.get('published_parsed') or entry.get('updated_parsed')
            date_str = datetime(*published[:6]).strftime('%Y-%m-%d') if published else datetime.now().strftime('%Y-%m-%d')
            
            posts.append({
                'title': entry.get('title', 'Untitled'),
                'description': entry.get('summary', '')[:300] + '...',
                'source': source_name,
                'date': date_str,
                'link': entry.get('link', '#'),
                'severity': 'Medium',  # Default for news items
            })
        
        return posts
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
        return []

def generate_blog_post(post_data, image_path=None, image_credit=None):
    """Generate HTML blog post from template"""
    
    # Read template
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
    else:
        # Fallback inline template with image support
        template = """<!DOCTYPE HTML>
<html>
<head>
    <title>{{TITLE}} - FixTheVuln</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="../assets/css/main.css" />
</head>
<body class="is-preload">
    <div id="content">
        <div class="inner">
            <article class="box post">
                <header>
                    <h2>{{TITLE}}</h2>
                    <p>{{SOURCE}} - {{DATE}}</p>
                </header>
                <div class="info">
                    <span class="date"><span class="month">{{MONTH}}</span> <span class="day">{{DAY}}</span><span class="year">, {{YEAR}}</span></span>
                    <ul class="stats">
                        <li><a href="#" class="icon fa-exclamation-triangle">{{SEVERITY}}</a></li>
                        <li><a href="{{LINK}}" class="icon fa-external-link-alt">Source</a></li>
                    </ul>
                </div>
                {{IMAGE_SECTION}}
                <div class="content">
                    <p><strong>Summary:</strong> {{DESCRIPTION}}</p>
                    {{CVE_SECTION}}
                    {{REMEDIATION_SECTION}}
                    <p><strong>Source:</strong> <a href="{{LINK}}" target="_blank">Read full article</a></p>
                    <p style="margin-top: 2em; padding: 1em; background: #f5f5f5; border-left: 4px solid #333;">
                        <strong>Need help with this vulnerability?</strong> I provide hands-on remediation services. 
                        <a href="../contact.html">Get in touch</a> for a free consultation.
                    </p>
                </div>
            </article>
        </div>
    </div>
    <div id="sidebar">
        <h1 id="logo"><a href="../index.html">FIXTHEVULN</a></h1>
        <nav id="nav">
            <ul>
                <li><a href="../index.html">Latest Posts</a></li>
                <li><a href="../about.html">About</a></li>
                <li><a href="../services.html">Services</a></li>
                <li><a href="../contact.html">Contact</a></li>
            </ul>
        </nav>
    </div>
</body>
</html>"""
    
    # Parse date
    date_obj = datetime.strptime(post_data['date'], '%Y-%m-%d')
    
    # Build image section
    image_section = ""
    if image_path:
        image_section = f'<a href="#" class="image featured"><img src="{image_path}" alt="{post_data["title"]}" /></a>'
        if image_credit:
            image_section += f'\n<p style="font-size: 0.8em; color: #888;">Photo by <a href="{image_credit["photographer_url"]}" target="_blank">{image_credit["photographer"]}</a> on <a href="{image_credit["download_link"]}" target="_blank">Unsplash</a></p>'
    
    # Build CVE section if available
    cve_section = ""
    if post_data.get('cve_id'):
        cve_section = f"""
                    <p><strong>CVE ID:</strong> <code>{post_data['cve_id']}</code></p>
                    <p><strong>NVD Link:</strong> <a href="https://nvd.nist.gov/vuln/detail/{post_data['cve_id']}" target="_blank">{post_data['cve_id']}</a></p>
        """
    
    # Build remediation section
    remediation_section = ""
    if post_data.get('remediation_hint'):
        remediation_section = f"""
                    <p><strong>Recommended Action:</strong> {post_data['remediation_hint']}</p>
        """
    
    # Replace placeholders
    html = template.replace('{{TITLE}}', post_data['title'])
    html = html.replace('{{SOURCE}}', post_data['source'])
    html = html.replace('{{DATE}}', post_data['date'])
    html = html.replace('{{MONTH}}', date_obj.strftime('%B'))
    html = html.replace('{{DAY}}', str(date_obj.day))
    html = html.replace('{{YEAR}}', str(date_obj.year))
    html = html.replace('{{SEVERITY}}', post_data.get('severity', 'Medium'))
    html = html.replace('{{DESCRIPTION}}', post_data['description'])
    html = html.replace('{{LINK}}', post_data['link'])
    html = html.replace('{{CVE_SECTION}}', cve_section)
    html = html.replace('{{REMEDIATION_SECTION}}', remediation_section)
    html = html.replace('{{IMAGE_SECTION}}', image_section)
    
    return html

def update_index_with_posts(all_posts):
    """Update index.html with latest posts"""
    # This would insert the latest posts into your index.html
    # For now, we'll create a posts archive
    pass

def main():
    """Main execution"""
    print("🔍 Fetching security news...")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    all_posts = []
    
    # Fetch from all sources
    print("📡 Fetching CISA KEV...")
    all_posts.extend(fetch_cisa_kev())
    
    print("📡 Fetching Bleeping Computer...")
    all_posts.extend(fetch_rss_feed(NEWS_SOURCES['bleeping_computer'], 'Bleeping Computer'))
    
    print("📡 Fetching The Hacker News...")
    all_posts.extend(fetch_rss_feed(NEWS_SOURCES['thehackernews'], 'The Hacker News'))
    
    # Sort by date (newest first)
    all_posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate blog posts
    print(f"\n✍️  Generating {len(all_posts)} blog posts...")
    
    for i, post in enumerate(all_posts[:10]):  # Limit to 10 most recent
        # Generate unique post ID
        post_id = hashlib.md5(f"{post['title']}{post['date']}".encode()).hexdigest()[:8]
        
        # Fetch and download image from Unsplash
        print(f"🖼️  Fetching image for: {post['title'][:50]}...")
        image_data = fetch_unsplash_image(post_title=post['title'])
        image_path = download_image(image_data, post_id) if image_data else None
        
        # Small delay to respect Unsplash API rate limits
        time.sleep(0.5)
        
        # Create filename from title and date
        safe_title = ''.join(c if c.isalnum() else '-' for c in post['title'][:50]).lower()
        filename = f"{post['date']}-{safe_title}.html"
        filepath = OUTPUT_DIR / filename
        
        # Generate and save post
        html = generate_blog_post(post, image_path, image_data)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Created: {filename}")
    
    # Create index of all posts
    posts_index = {
        'generated_at': datetime.now().isoformat(),
        'posts': all_posts
    }
    
    with open(OUTPUT_DIR / 'index.json', 'w') as f:
        json.dump(posts_index, f, indent=2)
    
    print(f"\n🎉 Done! Generated {len(all_posts)} posts in {OUTPUT_DIR}/")
    print(f"📋 Posts index saved to {OUTPUT_DIR}/index.json")

if __name__ == '__main__':
    main()
