#!/usr/bin/env python3
"""
One-time helper: builds the practice-tests.html hub page from quiz JSON data.
Outputs the final HTML to stdout (redirect to file).

Usage:
    python3 scripts/build_practice_tests_hub.py > practice-tests.html
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_practice_test_pages import (
    QUIZ_REGISTRY, VENDOR_META, VENDOR_ORDER, load_quiz_data,
)
from lib.constants import (
    PRACTICE_TESTS_CSS_VERSION, STYLE_CSS_VERSION,
    SITE_URL, SITE_NAME, OG_IMAGE, CF_ANALYTICS_TOKEN, FAVICON_SVG,
)
from lib.templates import (
    nav, share_bar, footer, cf_analytics, breadcrumb_schema, faq_schema, esc,
)

# Load all quiz data
all_quizzes = []
for q in QUIZ_REGISTRY:
    data = load_quiz_data(q['json'])
    if data:
        all_quizzes.append((q, data))

# Compute totals
total_q = sum(d['total_questions'] for _, d in all_quizzes)
total_domains = sum(d['domain_count'] for _, d in all_quizzes)
total_tests = len(all_quizzes)

# Vendor stats
vendor_stats = {}
for q, d in all_quizzes:
    v = q['vendor']
    if v not in vendor_stats:
        vendor_stats[v] = {'count': 0, 'questions': 0}
    vendor_stats[v]['count'] += 1
    vendor_stats[v]['questions'] += d['total_questions']

# --- Build vendor showcase cards ---
vendor_cards = []
for v in VENDOR_ORDER:
    m = VENDOR_META[v]
    s = vendor_stats.get(v, {'count': 0, 'questions': 0})
    vendor_cards.append(f"""            <a href="practice-tests/{v}.html" class="pt-hub-card">
                <div class="pt-hub-icon">{m['icon']}</div>
                <div class="pt-hub-name">{esc(m['name'])}</div>
                <div class="pt-hub-desc">{esc(m['desc'])}</div>
                <div class="pt-hub-meta"><span><strong>{s['count']}</strong> tests</span><span><strong>{s['questions']:,}</strong> questions</span></div>
                <div class="pt-hub-link">Browse {esc(m['name'])} Tests &rarr;</div>
            </a>""")

# --- Build quiz cards (all 68) ---
quiz_cards = []
for q, d in all_quizzes:
    domains_str = ' &bull; '.join(
        esc(dd['name']) for dd in d['domains'].values()
    )
    quiz_cards.append(f"""            <div class="pt-quiz-card" data-vendor="{q['vendor']}">
                <div class="pt-quiz-vendor">{esc(VENDOR_META[q['vendor']]['name'])}</div>
                <h3>{esc(q['name'])} {esc(q['exam'])}</h3>
                <div class="pt-quiz-tagline">{esc(q['tagline'])}</div>
                <div class="pt-quiz-stats">
                    <span class="pt-quiz-stat"><strong>{d['total_questions']}</strong> questions</span>
                    <span class="pt-quiz-stat"><strong>{d['domain_count']}</strong> domains</span>
                </div>
                <div class="pt-quiz-domains">{domains_str}</div>
                <a href="{q['quiz']}" class="pt-quiz-cta">Start {esc(q['short'])} Quiz &rarr;</a>
            </div>""")

# --- Build ItemList schema ---
item_list = json.dumps({
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    'name': 'Free Cybersecurity Practice Tests',
    'numberOfItems': total_tests,
    'itemListElement': [
        {
            '@type': 'ListItem',
            'position': i + 1,
            'name': f'{q["name"]} {q["exam"]} Practice Test',
            'url': f'{SITE_URL}/{q["quiz"]}',
        }
        for i, (q, _) in enumerate(all_quizzes)
    ],
}, indent=8)

breadcrumb = breadcrumb_schema([
    ('Home', f'{SITE_URL}/'),
    ('Practice Tests', None),
])

faq_items = [
    ('Are these practice tests really free?', 'Yes. All 68 practice tests are completely free with no login required, no paywall, and no ads. Take as many quizzes as you want, as many times as you want.'),
    ('How are the questions weighted?', 'Questions are weighted to match official exam domain percentages. If an exam domain is worth 25% of the real test, roughly 25% of our practice questions come from that domain.'),
    ('Do you cover all exam domains?', 'Yes. Every practice test covers all domains from the current exam objectives. Domain filters let you focus on specific areas where you need more practice.'),
    ('Can I use these to pass my certification exam?', 'Our practice tests are a supplemental study tool — not a replacement for official study materials, courses, or hands-on experience. They help you identify knowledge gaps and build test-taking confidence.'),
    ('How often are questions updated?', 'Questions are reviewed and updated when certification exam objectives change. We align to the latest exam versions including Security+ SY0-701, AWS SAA-C03, AZ-900, CCNA 200-301, and more.'),
    ('Do you track my scores?', 'Score history is saved locally in your browser using localStorage. No data is sent to any server. You can view your progress on the Knowledge Gap Dashboard.'),
]

faq_schema_json = faq_schema(faq_items)

# --- Build filter tabs ---
filter_tabs = ['        <button class="pt-filter-tab active" data-vendor="all">All</button>']
for v in VENDOR_ORDER:
    m = VENDOR_META[v]
    filter_tabs.append(f'        <button class="pt-filter-tab" data-vendor="{v}">{esc(m["name"])}</button>')

# --- Build FAQ HTML ---
faq_html = []
for q, a in faq_items:
    faq_html.append(f"""        <details class="pt-faq-item">
            <summary>{esc(q)}</summary>
            <p>{esc(a)}</p>
        </details>""")

# --- Assemble full page ---
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="dns-prefetch" href="https://static.cloudflareinsights.com">
    <link rel="preconnect" href="https://static.cloudflareinsights.com" crossorigin>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&family=IBM+Plex+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Free cybersecurity practice tests for 68 certifications. {total_q:,}+ questions across CompTIA, AWS, Microsoft, Cisco, ISC2, and more. Domain-weighted, timed, with progress tracking.">
    <meta name="keywords" content="cybersecurity practice test, free certification quiz, Security+ practice test, CISSP mock exam, AWS practice questions, Azure certification quiz, CCNA practice test, CompTIA quiz, ISC2 practice exam, OSCP practice questions">
    <title>Free Cybersecurity Practice Tests &mdash; {total_q:,}+ Questions, 68 Certifications - {SITE_NAME}</title>
    <link rel="canonical" href="{SITE_URL}/practice-tests.html">
    <meta property="og:title" content="Free Cybersecurity Practice Tests &mdash; {total_q:,}+ Questions - {SITE_NAME}">
    <meta property="og:description" content="Free practice tests for 68 cybersecurity certifications. {total_q:,}+ domain-weighted questions with explanations. No login required.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{SITE_URL}/practice-tests.html">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Free Cybersecurity Practice Tests &mdash; {total_q:,}+ Questions - {SITE_NAME}">
    <meta name="twitter:description" content="Free practice tests for 68 cybersecurity certifications. Domain-weighted questions with explanations.">
    <meta name="twitter:image" content="{OG_IMAGE}">
    <link rel="icon" type="image/svg+xml" href="{FAVICON_SVG}">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="stylesheet" href="style.min.css?v={STYLE_CSS_VERSION}">
    <link rel="stylesheet" href="practice-tests.css?v={PRACTICE_TESTS_CSS_VERSION}">
    <link rel="alternate" type="application/rss+xml" title="{SITE_NAME} Blog" href="blog/feed.xml">
    <script type="application/ld+json">
{breadcrumb}
    </script>
    <script type="application/ld+json">
{item_list}
    </script>
    <script type="application/ld+json">
{faq_schema_json}
    </script>
</head>
<body>
{nav(depth=0)}
{share_bar()}

    <div class="pt-page">

    <section class="pt-hero pt-animate">
        <div class="pt-hero-badge">🛡️ Free Practice Tests</div>
        <h1>Certification Practice Tests</h1>
        <p class="pt-hero-sub">{total_q:,}+ free questions across {total_tests} practice tests for 13 vendor ecosystems. Domain-weighted, timed, with instant results and progress tracking.</p>
        <div class="pt-hero-chips">
            <span class="pt-hero-chip">📝 {total_q:,}+ Questions</span>
            <span class="pt-hero-chip">🏆 {total_tests} Practice Tests</span>
            <span class="pt-hero-chip">🎯 Domain-Weighted</span>
            <span class="pt-hero-chip">📊 Progress Tracking</span>
        </div>
    </section>

    <div class="pt-stats-banner pt-animate pt-delay-1">
        <div class="pt-stat"><div class="pt-stat-value">{total_tests}</div><div class="pt-stat-label">Practice Tests</div></div>
        <div class="pt-stat"><div class="pt-stat-value">{total_q:,}+</div><div class="pt-stat-label">Questions</div></div>
        <div class="pt-stat"><div class="pt-stat-value">13</div><div class="pt-stat-label">Vendors</div></div>
        <div class="pt-stat"><div class="pt-stat-value">{total_domains}</div><div class="pt-stat-label">Exam Domains</div></div>
    </div>

    <!-- Vendor Showcase -->
    <section class="pt-section pt-animate pt-delay-2">
        <h2 class="pt-section-title">Browse by Vendor</h2>
        <p class="pt-section-subtitle">Select a vendor to see all available practice tests</p>
        <div class="pt-hub-grid">
{chr(10).join(vendor_cards)}
        </div>
    </section>

    <!-- Filter Tabs + Full Quiz Grid -->
    <section class="pt-section">
        <h2 class="pt-section-title">All Practice Tests</h2>
        <p class="pt-section-subtitle">Filter by vendor or browse the full catalog</p>
    </section>

    <div class="pt-filter-bar">
{chr(10).join(filter_tabs)}
    </div>

    <section class="pt-section">
        <div class="pt-quiz-grid" id="quizGrid">
{chr(10).join(quiz_cards)}
        </div>
        <p id="noResults" style="display:none; text-align:center; color:var(--text-muted); padding:40px 0; font-size:15px;">No practice tests found for this vendor.</p>
    </section>

    <!-- Store CTA -->
    <section class="pt-section">
        <div class="pt-store-cta">
            <h3>Turn Quiz Practice Into Cert Success</h3>
            <p>Pair your practice tests with structured study planners. Domain-by-domain schedules, progress trackers, and exam-day checklists. Available for 60+ certifications.</p>
            <a href="/store/store.html" class="pt-store-cta-btn">Browse Study Planners &rarr;</a>
        </div>
    </section>

    <!-- FAQ -->
    <section class="pt-faq-section">
        <h2>Frequently Asked Questions</h2>
{chr(10).join(faq_html)}
    </section>

    <!-- Trust -->
    <section class="pt-trust-section">
        <div class="pt-trust-grid">
            <div class="pt-trust-item"><div class="pt-trust-icon">🆓</div><div class="pt-trust-label">100% Free</div><div class="pt-trust-desc">No login, no paywall, no ads</div></div>
            <div class="pt-trust-item"><div class="pt-trust-icon">🎯</div><div class="pt-trust-label">Domain-Weighted</div><div class="pt-trust-desc">Questions match official exam weights</div></div>
            <div class="pt-trust-item"><div class="pt-trust-icon">⏱️</div><div class="pt-trust-label">Timed Mode</div><div class="pt-trust-desc">Simulate real exam conditions</div></div>
            <div class="pt-trust-item"><div class="pt-trust-icon">📊</div><div class="pt-trust-label">Progress Tracking</div><div class="pt-trust-desc">Track scores across sessions</div></div>
        </div>
    </section>

    </div>

{footer(affiliate_disclosure=True)}

    <!-- Dark Mode Toggle -->
    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode" title="Toggle dark/light mode">
        <span id="theme-icon">🌙</span>
    </button>

    <script>
    // Dark mode toggle
    function toggleTheme() {{
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('fixthevuln-theme', newTheme);
        document.getElementById('theme-icon').textContent = newTheme === 'dark' ? '☀️' : '🌙';
    }}
    (function() {{
        const saved = localStorage.getItem('fixthevuln-theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = saved || (prefersDark ? 'dark' : 'light');
        if (theme === 'dark') {{
            document.documentElement.setAttribute('data-theme', 'dark');
            document.getElementById('theme-icon').textContent = '☀️';
        }}
    }})();

    // Vendor filter tabs
    document.querySelectorAll('.pt-filter-tab').forEach(function(tab) {{
        tab.addEventListener('click', function() {{
            document.querySelectorAll('.pt-filter-tab').forEach(function(t) {{ t.classList.remove('active'); }});
            this.classList.add('active');
            var vendor = this.getAttribute('data-vendor');
            var cards = document.querySelectorAll('.pt-quiz-card');
            var visible = 0;
            cards.forEach(function(card) {{
                if (vendor === 'all' || card.getAttribute('data-vendor') === vendor) {{
                    card.style.display = '';
                    visible++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            document.getElementById('noResults').style.display = visible === 0 ? 'block' : 'none';
        }});
    }});
    </script>
{cf_analytics()}
    <script src="/js/error-reporter.js"></script>
</body>
</html>"""

print(page)
