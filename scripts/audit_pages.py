#!/usr/bin/env python3
"""
FixTheVuln Educational Page Audit

Weekly automated audit that checks:
  1. Broken external links (HTTP HEAD → GET fallback)
  2. Stale pages not updated recently
  3. Outdated version references

Usage:
  python scripts/audit_pages.py              # Full audit
  python scripts/audit_pages.py --skip-links # Skip link checking (fast mode)
  python scripts/audit_pages.py --json       # JSON output only
"""

import os
import re
import sys
import json
import time
import hashlib
import argparse
import urllib.request
import urllib.error
import ssl
from html.parser import HTMLParser
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from urllib.parse import urlparse

# ── Configuration ──────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files/dirs to exclude from audit
EXCLUDE_FILES = {
    '404.html', 'privacy.html', 'terms.html', 'success.html',
    'smartsheetbyrobert-privacy.html', 'sitemap.xml',
}
EXCLUDE_DIRS = {'store', 'data', 'assets', 'scripts', '.github', 'node_modules', 'planner'}

# Hub/index pages (not educational content, just navigation)
HUB_PAGES = {
    'index.html', 'start-here.html', 'resources.html', 'tools.html',
    'guides.html', 'compliance.html', 'practice-tests.html',
    'career-paths.html', 'contact.html', 'about.html',
}

# Domains to skip when link-checking
SKIP_LINK_DOMAINS = {
    'static.cloudflareinsights.com', 'fonts.googleapis.com',
    'fonts.gstatic.com', 'js.stripe.com', 'fixthevuln.com',
    'www.fixthevuln.com', 'localhost', '127.0.0.1',
}

# URL patterns to skip (social share templates, affiliate tracking, anchors)
SKIP_LINK_PATTERNS = [
    re.compile(r'linkedin\.com/sharing/'),
    re.compile(r'twitter\.com/intent/'),
    re.compile(r'x\.com/intent/'),
    re.compile(r'reddit\.com/submit'),
    re.compile(r'jdoqocy\.com'),
    re.compile(r'buy\.stripe\.com'),
    re.compile(r'^mailto:'),
    re.compile(r'^javascript:'),
    re.compile(r'^#'),
    re.compile(r'^tel:'),
]

# ── Staleness thresholds (days) ────────────────────────────

HIGH_VOLATILITY_DAYS = 90
MED_VOLATILITY_DAYS = 180
LOW_VOLATILITY_DAYS = 365

HIGH_VOLATILITY_PAGES = {
    'owasp-top10.html', 'quick-fixes.html', 'cve-lookup.html',
    'kev-archive.html', 'vuln-tracking.html', 'security-headers.html',
    'version-alerting.html',
}

LOW_VOLATILITY_PAGES = {
    'nist-framework.html', 'gdpr-guide.html', 'hipaa-guide.html',
    'pci-dss.html', 'soc2-basics.html', 'cis-controls.html',
    'incident-response.html', 'security-analyst-roadmap.html',
}

TOOL_PAGES = {
    'xss-playground.html', 'sql-injection-simulator.html', 'jwt-decoder.html',
    'certificate-decoder.html', 'cvss-calculator.html', 'base64-tool.html',
    'hash-generator.html', 'regex-tester.html', 'password-generator.html',
    'subnet-calculator.html', 'password-strength.html',
}

# ── Version patterns that may become outdated ──────────────

VERSION_PATTERNS = [
    (re.compile(r'\bTLS\s+1\.[01]\b'), 'Deprecated TLS version (1.0/1.1)'),
    (re.compile(r'\bOpenSSL\s+[\d]+\.[\d]+\.\d+\w?\b'), 'OpenSSL version'),
    (re.compile(r'\bPCI[\s-]DSS[ \t]+v[\d.]+\b'), 'PCI-DSS version'),
    (re.compile(r'\bNIST\s+SP\s+800-\d+(?:\s+(?:Rev\.?\s*)?\d+)?\b'), 'NIST SP reference'),
    (re.compile(r'\bOWASP\s+Top\s+10\s+20\d{2}\b'), 'OWASP Top 10 year'),
    (re.compile(r'\bCVSS\s+v?[234](?:\.\d)?\b'), 'CVSS version'),
    (re.compile(r'\b(?:SY0|N10|CAS|CS0|PT0|CV0|XK0)-\d{3}\b'), 'CompTIA exam code'),
    (re.compile(r'\b(?:AZ|SC|AI|DP|MS|PL)-\d{3}\b'), 'Microsoft exam code'),
    (re.compile(r'\b(?:SAA|DVA|SOA|CLF|SCS|DBS|MLS|DEA)-C\d{2}\b'), 'AWS exam code'),
    (re.compile(r'\b200-30[12]\b|\b350-[47]01\b'), 'Cisco exam code'),
]

# ── HTTP settings ──────────────────────────────────────────

HTTP_TIMEOUT = 15
HTTP_CONCURRENCY = 8
USER_AGENT = 'Mozilla/5.0 (compatible; FixTheVuln-AuditBot/1.0; +https://fixthevuln.com)'


# ══════════════════════════════════════════════════════════
# HTML Parser — extracts links, dates, and text content
# ══════════════════════════════════════════════════════════

class PageParser(HTMLParser):
    """Extracts external links, last-updated dates, and page text."""

    def __init__(self):
        super().__init__()
        self.links = []
        self.last_updated = None
        self.text_chunks = []
        self._in_script = False
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self._in_script = True
        elif tag == 'style':
            self._in_style = True
        elif tag == 'a':
            href = dict(attrs).get('href', '')
            if href and href.startswith('http'):
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag == 'script':
            self._in_script = False
        elif tag == 'style':
            self._in_style = False

    def handle_data(self, data):
        if self._in_script or self._in_style:
            return
        self.text_chunks.append(data)
        # Check for "Last updated: Month Day, Year"
        match = re.search(
            r'Last\s+updated:\s+(\w+\s+\d{1,2},?\s+\d{4})', data, re.IGNORECASE
        )
        if match:
            try:
                date_str = match.group(1).replace(',', '')
                self.last_updated = datetime.strptime(date_str, '%B %d %Y')
            except ValueError:
                pass

    @property
    def full_text(self):
        return ' '.join(self.text_chunks)


# ══════════════════════════════════════════════════════════
# Page Discovery
# ══════════════════════════════════════════════════════════

def discover_pages():
    """Find all educational HTML pages to audit."""
    pages = []

    for html_file in sorted(REPO_ROOT.glob('*.html')):
        name = html_file.name
        if name in EXCLUDE_FILES:
            continue
        pages.append(html_file)

    # Include blog posts
    blog_dir = REPO_ROOT / 'blog'
    if blog_dir.is_dir():
        for html_file in sorted(blog_dir.glob('*.html')):
            if html_file.name != 'index.html':
                pages.append(html_file)

    return pages


def get_staleness_threshold(filename):
    """Return the stale threshold in days for a page."""
    if filename in HIGH_VOLATILITY_PAGES:
        return HIGH_VOLATILITY_DAYS
    if filename in LOW_VOLATILITY_PAGES or filename in TOOL_PAGES:
        return LOW_VOLATILITY_DAYS
    if filename in HUB_PAGES:
        return LOW_VOLATILITY_DAYS
    if filename.endswith('-quiz.html'):
        return LOW_VOLATILITY_DAYS
    # Default: medium volatility (hardening guides, etc.)
    return MED_VOLATILITY_DAYS


# ══════════════════════════════════════════════════════════
# Link Checking
# ══════════════════════════════════════════════════════════

def should_skip_link(url):
    """Check if a URL should be skipped."""
    for pattern in SKIP_LINK_PATTERNS:
        if pattern.search(url):
            return True
    try:
        parsed = urlparse(url)
        if parsed.hostname and parsed.hostname in SKIP_LINK_DOMAINS:
            return True
    except Exception:
        return True
    return False


def check_link(url):
    """
    Check if a URL is reachable. Returns (url, status_code, status_text).
    Uses HEAD first, falls back to GET on 405/error.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for method in ['HEAD', 'GET']:
        try:
            req = urllib.request.Request(
                url, method=method,
                headers={'User-Agent': USER_AGENT}
            )
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT, context=ctx) as resp:
                code = resp.getcode()
                if code < 400:
                    return (url, code, 'ok')
                if method == 'HEAD' and code in (405, 403):
                    continue  # retry with GET
                return (url, code, 'error')
        except urllib.error.HTTPError as e:
            if method == 'HEAD' and e.code in (405, 403, 429):
                continue  # retry with GET
            return (url, e.code, 'error' if e.code >= 400 else 'warning')
        except urllib.error.URLError as e:
            if method == 'HEAD':
                continue
            return (url, 0, f'connection_error: {e.reason}')
        except Exception as e:
            if method == 'HEAD':
                continue
            return (url, 0, f'error: {type(e).__name__}')

    return (url, 0, 'unreachable')


def check_links_parallel(urls):
    """Check multiple URLs in parallel. Returns list of (url, code, status)."""
    results = []
    # Deduplicate
    unique_urls = list(set(urls))
    total = len(unique_urls)

    if total == 0:
        return results

    print(f'  Checking {total} unique external links...', file=sys.stderr)
    done = 0

    with ThreadPoolExecutor(max_workers=HTTP_CONCURRENCY) as pool:
        futures = {pool.submit(check_link, url): url for url in unique_urls}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            done += 1
            if done % 20 == 0:
                print(f'    {done}/{total} checked...', file=sys.stderr)

    return results


# ══════════════════════════════════════════════════════════
# Version Reference Scanning
# ══════════════════════════════════════════════════════════

def scan_version_references(text, filename):
    """Find potentially outdated version references in page text."""
    findings = []
    for pattern, description in VERSION_PATTERNS:
        for match in pattern.finditer(text):
            findings.append({
                'match': match.group(),
                'type': description,
            })
    # Deduplicate
    seen = set()
    unique = []
    for f in findings:
        key = (f['match'], f['type'])
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


# ══════════════════════════════════════════════════════════
# Main Audit
# ══════════════════════════════════════════════════════════

def audit_page(filepath):
    """Audit a single page. Returns dict of findings."""
    filename = filepath.name
    rel_path = str(filepath.relative_to(REPO_ROOT))

    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        return {'file': rel_path, 'error': str(e)}

    parser = PageParser()
    try:
        parser.feed(content)
    except Exception:
        pass

    # Collect external links (filtered)
    ext_links = [url for url in parser.links if not should_skip_link(url)]

    # Staleness check
    threshold = get_staleness_threshold(filename)
    stale_info = None
    if parser.last_updated:
        age_days = (datetime.now() - parser.last_updated).days
        if age_days > threshold:
            stale_info = {
                'last_updated': parser.last_updated.strftime('%Y-%m-%d'),
                'age_days': age_days,
                'threshold_days': threshold,
            }
    elif filename not in HUB_PAGES:
        stale_info = {
            'last_updated': None,
            'age_days': None,
            'threshold_days': threshold,
            'note': 'No "Last updated" date found on page',
        }

    # Version references
    versions = scan_version_references(parser.full_text, filename)

    return {
        'file': rel_path,
        'external_links': ext_links,
        'stale': stale_info,
        'version_refs': versions,
        'last_updated': parser.last_updated.strftime('%Y-%m-%d') if parser.last_updated else None,
    }


def run_audit(skip_links=False):
    """Run the full audit. Returns structured report."""
    print('FixTheVuln Educational Page Audit', file=sys.stderr)
    print('=' * 40, file=sys.stderr)

    pages = discover_pages()
    print(f'Found {len(pages)} pages to audit\n', file=sys.stderr)

    # Phase 1: Parse all pages
    print('Phase 1: Parsing pages...', file=sys.stderr)
    page_results = []
    all_links = []  # (url, source_file)

    for filepath in pages:
        result = audit_page(filepath)
        page_results.append(result)
        for link in result.get('external_links', []):
            all_links.append((link, result['file']))

    # Phase 2: Check links
    broken_links = []
    warning_links = []

    if not skip_links:
        print(f'\nPhase 2: Link checking...', file=sys.stderr)
        unique_urls = list(set(url for url, _ in all_links))
        link_results = check_links_parallel(unique_urls)

        # Build lookup: url → (code, status)
        link_status = {url: (code, status) for url, code, status in link_results}

        # Map broken links back to source pages
        url_to_pages = defaultdict(list)
        for url, source in all_links:
            url_to_pages[url].append(source)

        for url, (code, status) in link_status.items():
            entry = {
                'url': url,
                'status_code': code,
                'status': status,
                'pages': url_to_pages[url],
            }
            if status != 'ok':
                if code in (403, 429) or 'connection_error' in str(status):
                    warning_links.append(entry)
                else:
                    broken_links.append(entry)
    else:
        print('\nPhase 2: Skipping link checks (--skip-links)\n', file=sys.stderr)

    # Phase 3: Compile report
    print('\nPhase 3: Compiling report...', file=sys.stderr)

    stale_pages = [r for r in page_results if r.get('stale')]
    pages_with_versions = [r for r in page_results if r.get('version_refs')]
    pages_with_errors = [r for r in page_results if r.get('error')]

    report = {
        'audit_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'pages_audited': len(pages),
        'total_external_links': len(set(url for url, _ in all_links)),
        'summary': {
            'broken_links': len(broken_links),
            'warning_links': len(warning_links),
            'stale_pages': len(stale_pages),
            'version_references': sum(len(r['version_refs']) for r in pages_with_versions),
            'parse_errors': len(pages_with_errors),
        },
        'broken_links': sorted(broken_links, key=lambda x: x['status_code']),
        'warning_links': sorted(warning_links, key=lambda x: x['url']),
        'stale_pages': sorted(
            [{'file': r['file'], **r['stale']} for r in stale_pages],
            key=lambda x: x.get('age_days') or 9999,
            reverse=True,
        ),
        'version_references': [
            {'file': r['file'], 'refs': r['version_refs']}
            for r in pages_with_versions
        ],
        'errors': [{'file': r['file'], 'error': r['error']} for r in pages_with_errors],
    }

    return report


# ══════════════════════════════════════════════════════════
# Report Formatting
# ══════════════════════════════════════════════════════════

def format_markdown(report):
    """Format the audit report as markdown."""
    lines = []
    s = report['summary']

    lines.append(f"## Educational Page Audit — {report['audit_date']}")
    lines.append('')
    lines.append(f"**Pages audited:** {report['pages_audited']} | "
                 f"**External links checked:** {report['total_external_links']}")
    lines.append('')

    # Quick summary
    has_issues = (s['broken_links'] + s['stale_pages'] + s['parse_errors']) > 0

    if not has_issues and s['warning_links'] == 0:
        lines.append('All pages passed audit checks.')
        return '\n'.join(lines)

    # Broken links
    if report['broken_links']:
        lines.append(f"### Broken Links ({s['broken_links']})")
        lines.append('')
        for entry in report['broken_links']:
            pages_str = ', '.join(f'`{p}`' for p in entry['pages'])
            lines.append(f"- **{entry['status_code']}** `{entry['url']}`")
            lines.append(f"  Found in: {pages_str}")
        lines.append('')

    # Warning links (403, 429, connection errors)
    if report['warning_links']:
        lines.append(f"### Link Warnings ({s['warning_links']})")
        lines.append('')
        lines.append('> These may be false positives (bot-blocking, rate limiting).')
        lines.append('')
        for entry in report['warning_links'][:20]:  # Cap at 20
            pages_str = ', '.join(f'`{p}`' for p in entry['pages'])
            lines.append(f"- **{entry['status_code']}** `{entry['url']}` — {entry['status']}")
            lines.append(f"  Found in: {pages_str}")
        if len(report['warning_links']) > 20:
            lines.append(f"- *...and {len(report['warning_links']) - 20} more warnings*")
        lines.append('')

    # Stale pages
    if report['stale_pages']:
        lines.append(f"### Stale Pages ({s['stale_pages']})")
        lines.append('')
        lines.append('| Page | Last Updated | Age | Threshold |')
        lines.append('|------|-------------|-----|-----------|')
        for entry in report['stale_pages']:
            updated = entry.get('last_updated') or 'Not set'
            age = f"{entry['age_days']}d" if entry.get('age_days') else 'N/A'
            threshold = f"{entry['threshold_days']}d"
            note = f" ⚠️ {entry['note']}" if entry.get('note') else ''
            lines.append(f"| `{entry['file']}` | {updated} | {age} | {threshold} |{note}")
        lines.append('')

    # Version references
    if report['version_references']:
        lines.append(f"### Version References to Review ({s['version_references']})")
        lines.append('')
        lines.append('> These are not necessarily wrong — review to confirm they are current.')
        lines.append('')
        for entry in report['version_references']:
            lines.append(f"**`{entry['file']}`**")
            for ref in entry['refs']:
                lines.append(f"  - `{ref['match']}` — {ref['type']}")
        lines.append('')

    # Errors
    if report['errors']:
        lines.append(f"### Parse Errors ({s['parse_errors']})")
        lines.append('')
        for entry in report['errors']:
            lines.append(f"- `{entry['file']}`: {entry['error']}")
        lines.append('')

    # Checklist
    lines.append('### Action Items')
    lines.append('')
    if report['broken_links']:
        lines.append('- [ ] Fix or remove broken links')
    if report['stale_pages']:
        lines.append('- [ ] Review and update stale pages')
    if report['version_references']:
        lines.append('- [ ] Verify version references are current')
    if report['errors']:
        lines.append('- [ ] Investigate page parse errors')
    lines.append('')
    lines.append('---')
    lines.append('*Generated by `scripts/audit_pages.py` — [FixTheVuln](https://fixthevuln.com)*')

    return '\n'.join(lines)


# ══════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='FixTheVuln Educational Page Audit')
    parser.add_argument('--skip-links', action='store_true', help='Skip external link checking')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of markdown')
    parser.add_argument('--output', type=str, help='Write report to file')
    args = parser.parse_args()

    report = run_audit(skip_links=args.skip_links)

    if args.json:
        output = json.dumps(report, indent=2)
    else:
        output = format_markdown(report)

    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f'\nReport written to {args.output}', file=sys.stderr)
    else:
        print(output)

    # Exit with non-zero if there are actionable issues
    s = report['summary']
    if s['broken_links'] > 0 or s['stale_pages'] > 0 or s['parse_errors'] > 0:
        print(f"\nAudit found issues: {s['broken_links']} broken links, "
              f"{s['stale_pages']} stale pages, {s['parse_errors']} errors",
              file=sys.stderr)
        sys.exit(1)
    else:
        print('\nAudit passed with no critical issues.', file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
