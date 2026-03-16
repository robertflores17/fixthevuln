#!/usr/bin/env python3
"""Generate a comprehensive sitemap.xml from the filesystem.

Scans all .html files, categorizes by directory/type, assigns priorities,
and writes sitemap.xml with lastmod dates from git history.

Usage:
    python3 scripts/generate_sitemap.py              # generate sitemap.xml
    python3 scripts/generate_sitemap.py --dry-run     # preview without writing
    python3 scripts/generate_sitemap.py --count       # just print URL count
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"
BASE_URL = "https://fixthevuln.com"

# Directories to scan for .html files (relative to repo root)
CONTENT_DIRS = ["blog", "certs", "comparisons", "roadmaps", "cve", "store"]

# Files to exclude from sitemap
EXCLUDE_FILES = {
    "404.html",
    "analytics.html",       # internal dashboard
    "knowledge-gaps.html",  # internal dashboard
    "vuln-classifier.html", # internal tool
}

# Pages that are tools (priority 0.8)
TOOL_PAGES = {
    "base64-tool.html", "certificate-decoder.html", "cvss-calculator.html",
    "hash-generator.html", "jwt-decoder.html", "password-generator.html",
    "password-strength.html", "regex-tester.html", "sql-injection-simulator.html",
    "subnet-calculator.html", "xss-playground.html",
}

# Pages that are compliance guides (priority 0.8)
COMPLIANCE_PAGES = {
    "cis-controls.html", "gdpr-guide.html", "hipaa-guide.html",
    "nist-framework.html", "pci-dss.html", "soc2-basics.html",
    "risk-register-guide.html", "third-party-risk.html",
}

# Hub/navigation pages (priority 0.9)
HUB_PAGES = {
    "guides.html", "tools.html", "compliance.html", "resources.html",
    "career-paths.html", "practice-tests.html", "about.html", "contact.html",
    "planner.html", "kev-archive.html", "cve-lookup.html",
    "cert-cost-calculator.html", "study-tracker.html", "exploit-tracker.html",
    "start-here.html", "security-analyst-roadmap.html",
}

# Guide pages (priority 0.8)
GUIDE_PAGES = {
    "api-security.html", "cloud-security.html", "container-security.html",
    "database-security.html", "encryption-cheatsheet.html", "incident-response.html",
    "linux-hardening.html", "log-management.html", "osi-layer-attacks.html",
    "owasp-top10.html", "password-policy.html", "port-security.html",
    "quick-fixes.html", "secrets-management.html", "security-headers.html",
    "ssl-tls.html", "version-alerting.html", "vuln-tracking.html",
    "windows-hardening.html", "wordpress-security.html",
    "what-is-cybersecurity.html", "how-to-get-into-cybersecurity.html",
    "red-teaming-guide.html", "cybersecurity-salary-guide.html",
    "best-cybersecurity-certifications.html", "cybersecurity-job-trends.html",
    "owasp-llm-top10.html", "prompt-injection.html", "model-poisoning.html",
    "mlsecops.html", "ai-security-careers.html", "grc-career-path.html",
    "siem-rule-writing.html", "threat-hunting.html", "log-analysis-cheatsheet.html",
}


def get_last_commit_date(filepath):
    """Get the last git commit date for a file in YYYY-MM-DD format."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", filepath],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        if result.stdout.strip():
            return result.stdout.strip()[:10]
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def classify_root_page(filename):
    """Classify a root-level HTML file and return (priority, changefreq, category)."""
    if filename == "index.html":
        return 1.0, "weekly", "Homepage"
    if filename in HUB_PAGES:
        return 0.9, "monthly", "Hub Pages"
    if filename in TOOL_PAGES:
        return 0.8, "monthly", "Interactive Tools"
    if filename in COMPLIANCE_PAGES:
        return 0.8, "monthly", "Compliance Guides"
    if filename in GUIDE_PAGES:
        return 0.8, "monthly", "Security Guides"
    if filename.endswith("-quiz.html"):
        return 0.6, "monthly", "Practice Quizzes"
    # Remaining root pages default to guides
    return 0.7, "monthly", "Other Pages"


def classify_subdir_page(subdir):
    """Classify a page in a subdirectory and return (priority, changefreq, category)."""
    mapping = {
        "blog":        (0.7, "weekly",  "Blog Posts"),
        "certs":       (0.6, "monthly", "Certification Pages"),
        "comparisons": (0.7, "monthly", "Certification Comparisons"),
        "roadmaps":    (0.6, "monthly", "Study Roadmaps"),
        "cve":         (0.6, "weekly",  "CVE Pages"),
        "store":       (0.8, "monthly", "Store Pages"),
    }
    return mapping.get(subdir, (0.5, "monthly", "Other"))


def discover_pages():
    """Discover all .html pages and return list of (url, filepath, priority, changefreq, category)."""
    pages = []

    # Root-level .html files
    for f in sorted(REPO_ROOT.glob("*.html")):
        filename = f.name
        if filename in EXCLUDE_FILES:
            continue
        priority, changefreq, category = classify_root_page(filename)
        if filename == "index.html":
            url = BASE_URL + "/"
        else:
            url = f"{BASE_URL}/{filename}"
        pages.append((url, str(f.relative_to(REPO_ROOT)), priority, changefreq, category))

    # Subdirectory .html files
    for subdir in CONTENT_DIRS:
        dirpath = REPO_ROOT / subdir
        if not dirpath.is_dir():
            continue
        priority, changefreq, category = classify_subdir_page(subdir)
        for f in sorted(dirpath.glob("*.html")):
            filename = f.name
            if filename in EXCLUDE_FILES:
                continue
            rel_path = str(f.relative_to(REPO_ROOT))
            url = f"{BASE_URL}/{rel_path}"
            pages.append((url, rel_path, priority, changefreq, category))

    return pages


def generate_sitemap_xml(pages, use_git_dates=True):
    """Generate sitemap.xml content string."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    # Group by category for readability
    categories = {}
    for url, filepath, priority, changefreq, category in pages:
        if category not in categories:
            categories[category] = []
        categories[category].append((url, filepath, priority, changefreq))

    # Desired category order
    category_order = [
        "Homepage", "Hub Pages", "Store Pages",
        "Interactive Tools", "Compliance Guides", "Security Guides",
        "Blog Posts", "Certification Comparisons", "Other Pages",
        "Practice Quizzes", "Certification Pages", "Study Roadmaps",
        "CVE Pages",
    ]
    # Add any categories not in our predefined order
    for cat in categories:
        if cat not in category_order:
            category_order.append(cat)

    for category in category_order:
        if category not in categories:
            continue
        entries = categories[category]
        lines.append(f"\n  <!-- {category} ({len(entries)} pages) -->")
        for url, filepath, priority, changefreq in entries:
            lastmod = get_last_commit_date(filepath) if use_git_dates else datetime.now().strftime("%Y-%m-%d")
            lines.append("  <url>")
            lines.append(f"    <loc>{url}</loc>")
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
            lines.append(f"    <changefreq>{changefreq}</changefreq>")
            lines.append(f"    <priority>{priority}</priority>")
            lines.append("  </url>")

    lines.append("</urlset>")
    lines.append("")  # trailing newline
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive sitemap.xml")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--count", action="store_true", help="Just print URL count")
    parser.add_argument("--no-git-dates", action="store_true", help="Skip git log (faster, uses today's date)")
    args = parser.parse_args()

    pages = discover_pages()

    if args.count:
        print(f"Total pages discovered: {len(pages)}")
        categories = {}
        for _, _, _, _, cat in pages:
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")
        return

    print(f"Discovered {len(pages)} pages across {len(set(c for _, _, _, _, c in pages))} categories")

    if args.dry_run:
        for url, filepath, priority, _, category in pages:
            print(f"  [{priority}] {category}: {url}")
        print(f"\nTotal: {len(pages)} URLs (dry run — not written)")
        return

    use_git_dates = not args.no_git_dates
    if use_git_dates:
        print("Fetching git lastmod dates (this may take a moment)...")

    xml = generate_sitemap_xml(pages, use_git_dates=use_git_dates)
    SITEMAP_PATH.write_text(xml)
    print(f"Wrote {len(pages)} URLs to {SITEMAP_PATH}")


if __name__ == "__main__":
    main()
