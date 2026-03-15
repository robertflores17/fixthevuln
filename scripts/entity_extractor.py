#!/usr/bin/env python3
"""
Entity extractor for CVE descriptions.

Extracts structured entities (CVEs, CWEs, versions, vendors, IPs, URLs) from
CVE text and classifies each entry into attack domains using weighted keyword
scoring.

Entity extraction regex and domain classification patterns adapted from CyberMoE
(https://github.com/guerilla7/CyberMoE) by Ron F. del Rosario — MIT License.

Used in FixTheVuln's CVE pipeline to enrich kev-data.json with entity metadata
and attack domain classification for quiz/guide cross-linking.

Usage:
  python scripts/entity_extractor.py data/kev-data.json
  python scripts/entity_extractor.py data/kev-data.json --output data/cve-entities.json
  python scripts/entity_extractor.py data/kev-data.json --verbose
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Regex patterns for entity extraction
# ---------------------------------------------------------------------------

RE_CVE = re.compile(r'CVE-\d{4}-\d{4,7}', re.IGNORECASE)
RE_CWE = re.compile(r'CWE-\d+', re.IGNORECASE)
RE_VERSION = re.compile(
    r'(?:before|prior to|through|up to(?: and including)?|versions?\s+)'
    r'\s*'
    r'(\d+(?:\.\d+){1,5}(?:[-_.]\w+)?)',
    re.IGNORECASE,
)
RE_VERSION_RANGE = re.compile(
    r'(\d+(?:\.\d+){1,5}(?:[-_.]\w+)?)'
    r'\s*(?:to|through|-)\s*'
    r'(\d+(?:\.\d+){1,5}(?:[-_.]\w+)?)',
    re.IGNORECASE,
)
RE_IP = re.compile(
    r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
    r'(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b'
)
RE_URL = re.compile(r'https?://[^\s)<>\]]+', re.IGNORECASE)
RE_VENDOR_PRODUCT = re.compile(
    r'^(.+?)\s+'                        # vendor/product name
    r'(?:before|prior to|through|version)',  # version anchor
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Attack domain definitions (keyword -> weight, 1-4 scale)
#   4 = highly specific to this domain
#   3 = strong indicator
#   2 = moderate indicator
#   1 = generic, could appear in multiple domains
# ---------------------------------------------------------------------------

DOMAIN_KEYWORDS = {
    "Network Security": {
        "firewall": 4, "tcp": 3, "udp": 3, "port": 2, "router": 4,
        "dns": 3, "packet": 3, "traffic": 2, "lateral movement": 4,
        "network": 2, "vpn": 4, "ipsec": 4, "bgp": 4, "snmp": 4,
        "routing": 3, "switching": 3, "arp": 3, "icmp": 3,
    },
    "Web Application": {
        "xss": 4, "sql injection": 4, "csrf": 4, "ssrf": 4, "idor": 4,
        "authentication bypass": 3, "session": 2, "cookie": 2, "api": 2,
        "http": 2, "html": 2, "javascript": 2, "deserialization": 3,
        "injection": 2, "web": 2, "servlet": 3, "php": 3, "asp": 3,
    },
    "Cloud Security": {
        "aws": 4, "azure": 4, "gcp": 4, "s3": 4, "ec2": 4,
        "iam": 3, "container": 3, "kubernetes": 4, "docker": 3,
        "lambda": 4, "serverless": 4, "cloud": 3, "bucket": 4,
        "blob": 3, "saas": 3, "paas": 3, "iaas": 3, "terraform": 4,
    },
    "Identity & Access": {
        "authentication": 3, "authorization": 3, "privilege escalation": 4,
        "credential": 3, "password": 3, "mfa": 4, "sso": 4,
        "ldap": 4, "kerberos": 4, "saml": 4, "oauth": 4,
        "rbac": 4, "access control": 3, "identity": 2,
    },
    "Malware & Exploit": {
        "malware": 4, "ransomware": 4, "buffer overflow": 4,
        "use-after-free": 4, "shellcode": 4, "payload": 3,
        "exploit": 2, "trojan": 4, "backdoor": 4, "rootkit": 4,
        "heap": 3, "stack": 2, "memory corruption": 4,
        "rce": 3, "code execution": 3, "arbitrary code": 4,
    },
}

# CWE -> domain mapping (common CWEs)
CWE_DOMAIN_MAP = {
    "CWE-79":  "Web Application",
    "CWE-89":  "Web Application",
    "CWE-22":  "Web Application",
    "CWE-352": "Web Application",
    "CWE-918": "Web Application",
    "CWE-502": "Web Application",
    "CWE-287": "Identity & Access",
    "CWE-269": "Identity & Access",
    "CWE-306": "Identity & Access",
    "CWE-862": "Identity & Access",
    "CWE-78":  "Malware & Exploit",
    "CWE-120": "Malware & Exploit",
    "CWE-416": "Malware & Exploit",
    "CWE-94":  "Malware & Exploit",
    "CWE-119": "Malware & Exploit",
    "CWE-190": "Malware & Exploit",
    "CWE-787": "Malware & Exploit",
    "CWE-125": "Malware & Exploit",
    "CWE-20":  "Web Application",
    "CWE-434": "Web Application",
    "CWE-601": "Web Application",
    "CWE-611": "Web Application",
    "CWE-776": "Web Application",
    "CWE-200": "Web Application",
    "CWE-522": "Identity & Access",
    "CWE-798": "Identity & Access",
    "CWE-307": "Identity & Access",
}

# Domain -> related FixTheVuln guide pages
DOMAIN_GUIDES = {
    "Network Security": [
        "port-security.html",
        "linux-hardening.html",
        "windows-hardening.html",
    ],
    "Web Application": [
        "owasp-top10.html",
        "api-security.html",
        "security-headers.html",
        "wordpress-security.html",
    ],
    "Cloud Security": [
        "cloud-security.html",
        "container-security.html",
        "secrets-management.html",
    ],
    "Identity & Access": [
        "password-policy.html",
        "encryption-cheatsheet.html",
    ],
    "Malware & Exploit": [
        "incident-response.html",
        "log-management.html",
        "vuln-tracking.html",
    ],
}


# ---------------------------------------------------------------------------
# Entity extraction
# ---------------------------------------------------------------------------

def extract_entities(text):
    """
    Extract structured entities from a CVE description or free text.

    Returns dict with keys: cves, cwes, versions, vendors, ips, urls
    """
    if not text:
        return {
            "cves": [], "cwes": [], "versions": [],
            "vendors": [], "ips": [], "urls": [],
        }

    cves = sorted(set(RE_CVE.findall(text)))
    cwes = sorted(set(m.upper() for m in RE_CWE.findall(text)))

    # Versions: "before 4.2.1", "prior to 10.0", ranges like "4.0 to 4.2.1"
    versions = sorted(set(RE_VERSION.findall(text)))
    for start, end in RE_VERSION_RANGE.findall(text):
        if start not in versions:
            versions.append(start)
        if end not in versions:
            versions.append(end)
    versions = sorted(set(versions))

    ips = sorted(set(RE_IP.findall(text)))
    urls = sorted(set(RE_URL.findall(text)))

    # Vendor/product: try to extract from the beginning of the description
    vendors = []
    match = RE_VENDOR_PRODUCT.match(text)
    if match:
        raw = match.group(1).strip()
        # Clean up common leading noise
        raw = re.sub(r'^(?:A |An |The )\s*', '', raw, flags=re.IGNORECASE).strip()
        # Remove trailing punctuation or incomplete words
        raw = raw.rstrip(' ,;:')
        if raw and len(raw) > 1:
            vendors.append(raw)

    return {
        "cves": cves,
        "cwes": cwes,
        "versions": versions,
        "vendors": vendors,
        "ips": ips,
        "urls": urls,
    }


# ---------------------------------------------------------------------------
# Attack domain classification
# ---------------------------------------------------------------------------

def classify_domain(text):
    """
    Classify text into attack domains using weighted keyword scoring.

    Returns dict with:
      - scores: {domain: 0-100 normalized score}
      - primary: highest-scoring domain (or None if no matches)
      - matched_keywords: {domain: [keywords found]}
    """
    if not text:
        return {"scores": {}, "primary": None, "matched_keywords": {}}

    text_lower = text.lower()
    raw_scores = {}
    matched = {}

    for domain, keywords in DOMAIN_KEYWORDS.items():
        domain_score = 0
        domain_matched = []
        for keyword, weight in keywords.items():
            # Use word boundary matching for short keywords to avoid false hits
            if len(keyword) <= 3:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    domain_score += weight
                    domain_matched.append(keyword)
            else:
                if keyword in text_lower:
                    domain_score += weight
                    domain_matched.append(keyword)
        raw_scores[domain] = domain_score
        matched[domain] = domain_matched

    # Normalize to 0-100 per domain
    # Max possible score per domain = sum of all weights in that domain
    scores = {}
    for domain, raw in raw_scores.items():
        max_possible = sum(DOMAIN_KEYWORDS[domain].values())
        scores[domain] = round((raw / max_possible) * 100, 1) if max_possible > 0 else 0.0

    # Primary domain = highest raw score (not normalized, to avoid bias from
    # domains with fewer keywords)
    primary = None
    if any(v > 0 for v in raw_scores.values()):
        primary = max(raw_scores, key=raw_scores.get)

    return {
        "scores": scores,
        "primary": primary,
        "matched_keywords": {d: kws for d, kws in matched.items() if kws},
    }


# ---------------------------------------------------------------------------
# CVE enrichment
# ---------------------------------------------------------------------------

def enrich_cve(cve_entry, nvd_data=None):
    """
    Enrich a single CVE entry from kev-data.json format.

    Args:
        cve_entry: dict with at least 'id', 'description', 'title'
        nvd_data: optional NVD API response for this CVE (for CWE extraction)

    Returns:
        dict with original fields + cwes, vendor, product, attack_domains,
        related_guides
    """
    enriched = dict(cve_entry)

    # Build text corpus from available fields
    description = cve_entry.get("description", "") or ""
    title = cve_entry.get("title", "") or ""
    corpus = f"{title} {description}".strip()

    # Extract entities
    entities = extract_entities(corpus)

    # CWEs: prefer NVD data if available, fall back to regex extraction
    cwes = []
    if nvd_data:
        weaknesses = nvd_data.get("weaknesses", [])
        for w in weaknesses:
            for desc in w.get("description", []):
                val = desc.get("value", "")
                if val.startswith("CWE-") and val != "NVD-CWE-Other" and val != "NVD-CWE-noinfo":
                    cwes.append(val.upper())
    if not cwes:
        cwes = entities["cwes"]
    cwes = sorted(set(cwes))

    # Vendor/product: use title-based extraction (title format is usually
    # "Vendor Product Vulnerability Type")
    vendor = ""
    product = ""
    if entities["vendors"]:
        vendor_product = entities["vendors"][0]
        # Try to split "Vendor Product" if it looks like two+ words
        parts = vendor_product.split()
        if len(parts) >= 2:
            vendor = parts[0]
            product = " ".join(parts[1:])
        else:
            vendor = vendor_product

    # Fallback: try to extract vendor from title directly
    if not vendor and title:
        # Common pattern: "VendorName ProductName Vuln Type"
        # Take first word as vendor
        title_words = title.strip().split()
        if title_words:
            vendor = title_words[0]
            if len(title_words) >= 2:
                product = title_words[1]

    # Domain classification
    classification = classify_domain(corpus)

    # Boost domain score if CWEs map to a known domain
    cwe_domains = set()
    for cwe in cwes:
        mapped = CWE_DOMAIN_MAP.get(cwe)
        if mapped:
            cwe_domains.add(mapped)

    # If CWE mapping disagrees with keyword primary, CWE wins (more precise)
    if cwe_domains and classification["primary"] not in cwe_domains:
        # Pick the CWE-mapped domain with the highest keyword score as tiebreak
        best_cwe_domain = max(
            cwe_domains,
            key=lambda d: classification["scores"].get(d, 0),
        )
        classification["primary"] = best_cwe_domain

    # If no keyword matches but CWE gives us a domain, use it
    if not classification["primary"] and cwe_domains:
        classification["primary"] = sorted(cwe_domains)[0]

    # Collect related guides from primary domain + CWE-mapped domains
    guide_domains = set()
    if classification["primary"]:
        guide_domains.add(classification["primary"])
    guide_domains.update(cwe_domains)

    related_guides = []
    seen_guides = set()
    for domain in sorted(guide_domains):
        for guide in DOMAIN_GUIDES.get(domain, []):
            if guide not in seen_guides:
                related_guides.append(guide)
                seen_guides.add(guide)

    # Build attack_domains as a compact dict: {domain: score} for non-zero
    attack_domains = {}
    if classification["primary"]:
        attack_domains["primary"] = classification["primary"]
    attack_domains["scores"] = {
        d: s for d, s in classification["scores"].items() if s > 0
    }

    # Only add enrichment fields (don't overwrite existing vendor/product
    # if they already exist in the source data)
    if cwes:
        enriched["cwes"] = cwes
    if vendor and "vendor" not in enriched:
        enriched["vendor"] = vendor
    if product and "product" not in enriched:
        enriched["product"] = product
    if attack_domains.get("scores"):
        enriched["attack_domains"] = attack_domains
    if related_guides:
        enriched["related_guides"] = related_guides

    return enriched


# ---------------------------------------------------------------------------
# Entity graph builder
# ---------------------------------------------------------------------------

def build_entity_graph(enriched_vulns):
    """
    Build the entity graph from a list of enriched CVE entries.

    Returns dict mapping:
      - cve_to_cwes: {CVE-ID: [CWE-IDs]}
      - cve_to_vendor: {CVE-ID: {vendor, product}}
      - cwe_to_domain: {CWE-ID: domain}
      - cve_to_domains: {CVE-ID: {primary, scores}}
      - cve_to_guides: {CVE-ID: [guide pages]}
      - domain_stats: {domain: count}
    """
    cve_to_cwes = {}
    cve_to_vendor = {}
    cwe_to_domain = dict(CWE_DOMAIN_MAP)  # Start with known mappings
    cve_to_domains = {}
    cve_to_guides = {}
    domain_stats = {}

    for vuln in enriched_vulns:
        cve_id = vuln.get("id", "")
        if not cve_id:
            continue

        cwes = vuln.get("cwes", [])
        if cwes:
            cve_to_cwes[cve_id] = cwes

        vendor = vuln.get("vendor", "")
        product = vuln.get("product", "")
        if vendor:
            cve_to_vendor[cve_id] = {"vendor": vendor, "product": product}

        # Enrich cwe_to_domain with any CWEs we see
        attack_domains = vuln.get("attack_domains", {})
        primary = attack_domains.get("primary")
        if primary:
            for cwe in cwes:
                if cwe not in cwe_to_domain:
                    cwe_to_domain[cwe] = primary

        if attack_domains:
            cve_to_domains[cve_id] = attack_domains

        guides = vuln.get("related_guides", [])
        if guides:
            cve_to_guides[cve_id] = guides

        # Count domain occurrences
        if primary:
            domain_stats[primary] = domain_stats.get(primary, 0) + 1

    return {
        "cve_to_cwes": cve_to_cwes,
        "cve_to_vendor": cve_to_vendor,
        "cwe_to_domain": cwe_to_domain,
        "cve_to_domains": cve_to_domains,
        "cve_to_guides": cve_to_guides,
        "domain_stats": domain_stats,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Extract entities and classify attack domains from CVE data"
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to kev-data.json (or any JSON with a 'vulnerabilities' array)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output path for entity graph JSON (default: data/cve-entities.json)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print per-CVE enrichment details",
    )
    args = parser.parse_args()

    # Load input
    input_path = args.input_file
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        return 1

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vulns = data.get("vulnerabilities", [])
    if not vulns:
        print(f"No vulnerabilities found in {input_path}")
        return 0

    print(f"Enriching {len(vulns)} CVEs from {input_path.name}...")

    # Enrich each CVE
    enriched = []
    domain_counter = {}

    for vuln in vulns:
        result = enrich_cve(vuln)
        enriched.append(result)

        primary = result.get("attack_domains", {}).get("primary")
        if primary:
            domain_counter[primary] = domain_counter.get(primary, 0) + 1

        if args.verbose:
            cve_id = vuln.get("id", "?")
            cwes = result.get("cwes", [])
            vendor = result.get("vendor", "-")
            product = result.get("product", "-")
            guides = result.get("related_guides", [])
            print(
                f"  {cve_id:<22} "
                f"CWEs: {', '.join(cwes) if cwes else '-':<20} "
                f"Domain: {primary or '-':<20} "
                f"Vendor: {vendor}"
            )
            if guides:
                print(f"  {'':>22} Guides: {', '.join(guides)}")

    # Build entity graph
    graph = build_entity_graph(enriched)

    # Summary
    print(f"\nEntity extraction complete:")
    print(f"  CVEs with CWEs:    {len(graph['cve_to_cwes'])}/{len(vulns)}")
    print(f"  CVEs with vendor:  {len(graph['cve_to_vendor'])}/{len(vulns)}")
    print(f"  CVEs with domain:  {len(graph['cve_to_domains'])}/{len(vulns)}")
    print(f"  CVEs with guides:  {len(graph['cve_to_guides'])}/{len(vulns)}")
    print(f"\n  Domain distribution:")
    for domain in sorted(domain_counter, key=domain_counter.get, reverse=True):
        count = domain_counter[domain]
        pct = (count / len(vulns)) * 100
        print(f"    {domain:<20} {count:>4} ({pct:.1f}%)")

    # Determine output path
    output_path = args.output
    if output_path is None:
        output_path = input_path.parent / "cve-entities.json"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write entity graph
    output_data = {
        "source": str(input_path.name),
        "total_cves": len(vulns),
        "entity_graph": graph,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\nEntity graph written to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
