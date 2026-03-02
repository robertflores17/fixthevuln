#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt for AI discovery (llmstxt.org standard).

Parses sitemap.xml, categorizes all URLs by path pattern, and produces:
  - llms.txt       — concise summary with hub page links
  - llms-full.txt  — comprehensive listing of every URL grouped by category

Usage:
    python3 scripts/generate_llms_txt.py              # generate both files
    python3 scripts/generate_llms_txt.py --dry-run     # preview without writing
"""

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP_PATH = os.path.join(SITE_ROOT, "sitemap.xml")
LLMS_TXT_PATH = os.path.join(SITE_ROOT, "llms.txt")
LLMS_FULL_PATH = os.path.join(SITE_ROOT, "llms-full.txt")
BASE_URL = "https://fixthevuln.com"

# Abbreviation map for slug-to-title conversion
ABBREVIATIONS = {
    "aws": "AWS",
    "gcp": "GCP",
    "az": "Azure",
    "ms": "Microsoft",
    "sc": "SC",
    "dp": "DP",
    "ai": "AI",
    "isc2": "ISC2",
    "isaca": "ISACA",
    "giac": "GIAC",
    "ec": "EC-Council",
    "k8s": "Kubernetes",
    "offsec": "OffSec",
    "cissp": "CISSP",
    "ccsp": "CCSP",
    "sscp": "SSCP",
    "cc": "CC",
    "cisa": "CISA",
    "cism": "CISM",
    "crisc": "CRISC",
    "gsec": "GSEC",
    "gcih": "GCIH",
    "gcia": "GCIA",
    "gpen": "GPEN",
    "ceh": "CEH",
    "chfi": "CHFI",
    "cnd": "CND",
    "oscp": "OSCP",
    "oswa": "OSWA",
    "oswe": "OSWE",
    "cka": "CKA",
    "ckad": "CKAD",
    "cks": "CKS",
    "ccna": "CCNA",
    "ccnp": "CCNP",
    "cyberops": "CyberOps",
    "devnet": "DevNet",
    "comptia": "CompTIA",
    "cisco": "Cisco",
    "google": "Google",
    "hashicorp": "HashiCorp",
    "terraform": "Terraform",
    "vault": "Vault",
    "owasp": "OWASP",
    "nist": "NIST",
    "hipaa": "HIPAA",
    "gdpr": "GDPR",
    "pci": "PCI",
    "dss": "DSS",
    "soc2": "SOC 2",
    "cve": "CVE",
    "cvss": "CVSS",
    "kev": "KEV",
    "ssl": "SSL",
    "tls": "TLS",
    "xss": "XSS",
    "sql": "SQL",
    "jwt": "JWT",
    "api": "API",
    "osi": "OSI",
    "cis": "CIS",
    "clf": "CLF",
    "saa": "SAA",
    "soa": "SOA",
    "dva": "DVA",
    "dbs": "DBS",
    "dea": "DEA",
    "mls": "MLS",
    "ace": "ACE",
    "pca": "PCA",
    "pde": "PDE",
    "pse": "PSE",
    "cdl": "CDL",
    "cpts": "CPTS",
    "casp": "CASP",
    "cysa": "CySA",
    "itf": "ITF",
    "aplus": "A+",
    "aplus2": "A+ Core 2",
    "encor": "ENCOR",
}

# Category definitions: (category_name, matcher_fn, hub_url, hub_title)
# Order matters — first match wins for root-level pages
CATEGORIES = [
    ("Certification Study Planners", lambda p: p.startswith("certs/"), "/certs/", None),
    ("Certification Roadmaps", lambda p: p.startswith("roadmaps/"), "/roadmaps/", None),
    ("Practice Quizzes", lambda p: p.endswith("-quiz.html"), "/practice-tests.html", None),
    ("Blog & Study Guides", lambda p: p.startswith("blog/"), "/blog/", None),
    ("Certification Comparisons", lambda p: p.startswith("comparisons/"), "/comparisons/", None),
    ("CVE & Vulnerability Pages", lambda p: p.startswith("cve/"), "/cve-lookup.html", None),
    ("Store", lambda p: p.startswith("store/"), "/store/store.html", None),
    ("Interactive Security Tools", lambda p: _is_tool(p), "/tools.html", None),
    ("Compliance & Framework Guides", lambda p: _is_compliance(p), "/compliance.html", None),
    ("Security Guides", lambda p: _is_guide(p), "/guides.html", None),
]

TOOL_PAGES = {
    "base64-tool.html", "certificate-decoder.html", "cvss-calculator.html",
    "hash-generator.html", "jwt-decoder.html", "password-generator.html",
    "password-strength.html", "regex-tester.html", "sql-injection-simulator.html",
    "subnet-calculator.html", "xss-playground.html",
}

COMPLIANCE_PAGES = {
    "cis-controls.html", "gdpr-guide.html", "hipaa-guide.html",
    "nist-framework.html", "pci-dss.html", "soc2-basics.html",
}

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
    "best-cybersecurity-certifications.html",
    "cybersecurity-job-trends.html",
}

HUB_PAGES = {
    "", "guides.html", "tools.html", "compliance.html", "resources.html",
    "career-paths.html", "practice-tests.html", "about.html", "contact.html",
    "privacy.html", "start-here.html", "planner.html", "kev-archive.html",
    "cve-lookup.html", "cert-cost-calculator.html", "study-tracker.html",
    "exploit-tracker.html", "security-analyst-roadmap.html",
}


def _is_tool(path):
    return path in TOOL_PAGES


def _is_compliance(path):
    return path in COMPLIANCE_PAGES


def _is_guide(path):
    return path in GUIDE_PAGES


def parse_sitemap(sitemap_path):
    """Parse sitemap.xml and return list of URLs."""
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for url_elem in root.findall("sm:url", ns):
        loc = url_elem.find("sm:loc", ns)
        if loc is not None and loc.text:
            urls.append(loc.text.strip())
    return urls


def url_to_path(url):
    """Convert full URL to relative path (e.g., 'blog/foo.html')."""
    return url.replace(BASE_URL + "/", "").replace(BASE_URL, "")


def slug_to_title(filename):
    """Convert a slug filename to a human-readable title.

    Examples:
        'aws-solutions-architect.html' → 'AWS Solutions Architect'
        'comptia-security-plus-study-guide.html' → 'CompTIA Security+ Study Guide'
        'CVE-2025-40551.html' → 'CVE-2025-40551'
    """
    name = filename.replace(".html", "")

    # Preserve CVE IDs as-is (already uppercase with dashes)
    if re.match(r"^CVE-\d{4}-\d+$", name):
        return name
    # Remove common suffixes before processing
    name = re.sub(r"-study-guide$", " Study Guide", name)
    name = re.sub(r"-quiz$", " Quiz", name)

    # Split remaining slug
    suffix = ""
    if name.endswith(" Study Guide"):
        suffix = " Study Guide"
        name = name[: -len(" Study Guide")]
    elif name.endswith(" Quiz"):
        suffix = " Quiz"
        name = name[: -len(" Quiz")]

    parts = name.split("-")
    result = []
    i = 0
    while i < len(parts):
        part = parts[i]
        # Check for multi-word abbreviation matches (e.g., 'pci-dss')
        if i + 1 < len(parts):
            combo = f"{part}-{parts[i+1]}"
            if combo in ABBREVIATIONS:
                result.append(ABBREVIATIONS[combo])
                i += 2
                continue
        # Single-word abbreviation
        if part in ABBREVIATIONS:
            result.append(ABBREVIATIONS[part])
        elif part == "plus":
            # Append + to previous word
            if result:
                result[-1] = result[-1] + "+"
            else:
                result.append("Plus")
        elif part == "vs":
            result.append("vs.")
        else:
            result.append(part.capitalize())
        i += 1

    return " ".join(result) + suffix


def categorize_urls(urls):
    """Categorize URLs into groups. Returns dict of category → list of (url, title)."""
    categories = {}
    hub_urls = []

    for url in urls:
        path = url_to_path(url)

        # Hub/navigation pages go to a separate bucket
        if path in HUB_PAGES:
            hub_urls.append((url, slug_to_title(path) if path else "Homepage"))
            continue

        matched = False
        for cat_name, matcher, _, _ in CATEGORIES:
            if matcher(path):
                if cat_name not in categories:
                    categories[cat_name] = []
                # Extract filename for title
                filename = path.split("/")[-1] if "/" in path else path
                if not filename:
                    # Directory index page — use directory name
                    dirname = path.rstrip("/").split("/")[-1]
                    title = slug_to_title(dirname + ".html").replace(".html", "") + " Index"
                else:
                    title = slug_to_title(filename)
                categories[cat_name].append((url, title))
                matched = True
                break

        if not matched:
            # Uncategorized root pages
            if "Uncategorized" not in categories:
                categories["Uncategorized"] = []
            categories["Uncategorized"].append((url, slug_to_title(path)))

    return categories, hub_urls


def generate_llms_txt(categories, hub_urls):
    """Generate concise llms.txt content."""
    lines = []
    lines.append("# FixTheVuln")
    lines.append("")
    lines.append("> Free cybersecurity education platform with interactive tools, certification study planners, practice quizzes, vulnerability tracking, and compliance guides.")
    lines.append("")
    lines.append("FixTheVuln (fixthevuln.com) helps security professionals and students learn cybersecurity through hands-on tools and structured study resources. The site covers 60+ certification paths across CompTIA, AWS, Microsoft, Cisco, ISC2, ISACA, GIAC, EC-Council, OffSec, Google Cloud, HashiCorp, and Kubernetes. All content is free.")
    lines.append("")

    # Hub pages section
    lines.append("## Main Sections")
    lines.append("")
    hub_links = [
        (f"{BASE_URL}/", "Homepage"),
        (f"{BASE_URL}/start-here.html", "Start Here"),
        (f"{BASE_URL}/guides.html", "Security Guides"),
        (f"{BASE_URL}/tools.html", "Interactive Tools"),
        (f"{BASE_URL}/compliance.html", "Compliance Guides"),
        (f"{BASE_URL}/practice-tests.html", "Practice Quizzes"),
        (f"{BASE_URL}/career-paths.html", "Career Paths"),
        (f"{BASE_URL}/cve-lookup.html", "CVE Lookup"),
        (f"{BASE_URL}/kev-archive.html", "KEV Archive"),
        (f"{BASE_URL}/resources.html", "Resources"),
        (f"{BASE_URL}/store/store.html", "Study Planner Store"),
    ]
    for url, title in hub_links:
        lines.append(f"- [{title}]({url})")
    lines.append("")

    # Category summary sections with counts
    category_order = [
        "Interactive Security Tools",
        "Security Guides",
        "Compliance & Framework Guides",
        "Practice Quizzes",
        "Certification Study Planners",
        "Certification Roadmaps",
        "Certification Comparisons",
        "Blog & Study Guides",
        "CVE & Vulnerability Pages",
        "Store",
    ]

    for cat_name in category_order:
        if cat_name in categories:
            count = len(categories[cat_name])
            lines.append(f"## {cat_name} ({count} pages)")
            lines.append("")
            # Find the hub URL for this category
            for cname, _, hub_path, _ in CATEGORIES:
                if cname == cat_name and hub_path:
                    lines.append(f"- [Browse all]({BASE_URL}{hub_path})")
                    break
            lines.append("")

    lines.append("## Additional Resources")
    lines.append("")
    lines.append(f"- [About]({BASE_URL}/about.html)")
    lines.append(f"- [Contact]({BASE_URL}/contact.html)")
    lines.append(f"- [Privacy Policy]({BASE_URL}/privacy.html)")
    lines.append(f"- [Sitemap]({BASE_URL}/sitemap.xml)")
    lines.append(f"- [Full AI-readable site index]({BASE_URL}/llms-full.txt)")
    lines.append("")

    return "\n".join(lines)


def generate_llms_full_txt(categories, hub_urls):
    """Generate comprehensive llms-full.txt with every URL."""
    lines = []
    lines.append("# FixTheVuln — Full Site Index")
    lines.append("")
    lines.append("> Free cybersecurity education platform with interactive tools, certification study planners, practice quizzes, vulnerability tracking, and compliance guides.")
    lines.append("")
    lines.append("FixTheVuln (fixthevuln.com) helps security professionals and students learn cybersecurity through hands-on tools and structured study resources. The site covers 60+ certification paths across CompTIA, AWS, Microsoft, Cisco, ISC2, ISACA, GIAC, EC-Council, OffSec, Google Cloud, HashiCorp, and Kubernetes. All content is free.")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("")

    # Hub pages
    lines.append("## Hub & Navigation Pages")
    lines.append("")
    for url, title in sorted(hub_urls, key=lambda x: x[1]):
        lines.append(f"- [{title}]({url})")
    lines.append("")

    # Each category with all URLs
    category_order = [
        "Interactive Security Tools",
        "Security Guides",
        "Compliance & Framework Guides",
        "Practice Quizzes",
        "Certification Study Planners",
        "Certification Roadmaps",
        "Certification Comparisons",
        "Blog & Study Guides",
        "CVE & Vulnerability Pages",
        "Store",
    ]

    for cat_name in category_order:
        if cat_name in categories:
            items = categories[cat_name]
            lines.append(f"## {cat_name} ({len(items)} pages)")
            lines.append("")
            for url, title in sorted(items, key=lambda x: x[1]):
                lines.append(f"- [{title}]({url})")
            lines.append("")

    # Uncategorized
    if "Uncategorized" in categories:
        items = categories["Uncategorized"]
        lines.append(f"## Other Pages ({len(items)} pages)")
        lines.append("")
        for url, title in sorted(items, key=lambda x: x[1]):
            lines.append(f"- [{title}]({url})")
        lines.append("")

    total = sum(len(v) for v in categories.values()) + len(hub_urls)
    lines.append(f"---")
    lines.append(f"Total: {total} pages")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate llms.txt and llms-full.txt")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    if not os.path.exists(SITEMAP_PATH):
        print(f"Error: sitemap.xml not found at {SITEMAP_PATH}", file=sys.stderr)
        sys.exit(1)

    urls = parse_sitemap(SITEMAP_PATH)
    print(f"Parsed {len(urls)} URLs from sitemap.xml")

    categories, hub_urls = categorize_urls(urls)

    # Print category summary
    print(f"\nHub/navigation pages: {len(hub_urls)}")
    for cat_name, items in sorted(categories.items(), key=lambda x: -len(x[1])):
        print(f"  {cat_name}: {len(items)}")

    llms_txt = generate_llms_txt(categories, hub_urls)
    llms_full_txt = generate_llms_full_txt(categories, hub_urls)

    if args.dry_run:
        print("\n--- llms.txt preview (first 40 lines) ---")
        for line in llms_txt.split("\n")[:40]:
            print(line)
        print(f"\n--- llms-full.txt: {len(llms_full_txt.split(chr(10)))} lines ---")
        print("(Use without --dry-run to write files)")
    else:
        with open(LLMS_TXT_PATH, "w") as f:
            f.write(llms_txt)
        print(f"\nWrote {LLMS_TXT_PATH}")

        with open(LLMS_FULL_PATH, "w") as f:
            f.write(llms_full_txt)
        print(f"Wrote {LLMS_FULL_PATH}")


if __name__ == "__main__":
    main()
