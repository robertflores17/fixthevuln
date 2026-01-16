#!/usr/bin/env python3
"""
FixTheVuln - Automated Security News Fetcher
Fetches latest security vulnerabilities and news from multiple sources
"""

import os
import json
import requests
from datetime import datetime
import feedparser
from pathlib import Path

# Configuration
NEWS_SOURCES = {
    'cisa_kev': 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',
    'nvd_recent': 'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=10',
    'bleeping_computer': 'https://www.bleepingcomputer.com/feed/',
    'thehackernews': 'https://feeds.feedburner.com/TheHackersNews',
}

OUTPUT_DIR = Path('posts')
TEMPLATE_FILE = Path('post-template.html')

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

def generate_blog_post(post_data):
    """Generate HTML blog post from template"""
    
    # Read template
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
    else:
        # Fallback inline template
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
        # Create filename from title and date
        safe_title = ''.join(c if c.isalnum() else '-' for c in post['title'][:50]).lower()
        filename = f"{post['date']}-{safe_title}.html"
        filepath = OUTPUT_DIR / filename
        
        # Generate and save post
        html = generate_blog_post(post)
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
