# AppSec Review — 2026-09-27

**Reviewer:** Robert Flores, CISSP  
**Review Date:** 2026-09-27  
**CVEs Reviewed:** 1  
**Cumulative Database:** 240 vulnerabilities (231 active, 9 archived)

---

## Severity Breakdown

| Priority | Count |
|----------|-------|
| Critical | 0     |
| High     | 1     |
| Medium   | 0     |
| Low      | 0     |

---

## CVE Summary

| CVE ID         | Vendor    | Priority | Vulnerability Class              |
|----------------|-----------|----------|----------------------------------|
| CVE-2026-87902 | WordPress | High     | Remote File Inclusion (CWE-98) / RCE |

---

## CVE Detail

**CVE-2026-87902 — WordPress Core Remote File Inclusion**  
CVSS 8.1 (v3.1). An unauthenticated attacker can manipulate page-template resolution to include an arbitrary readable local `.php` file outside active theme directories, achieving remote code execution. WordPress powers an estimated 43%+ of the public web; exploitation at scale is highly probable given active KEV listing. CISA referenced BOD 26-04 forensic triage requirements, indicating federal scope beyond standard patching SLAs. Due date is 2026-09-28 — patch window is extremely tight.

---

## Trend Analysis

This week's single-entry batch continues a pattern of CISA KEV additions targeting high-profile CMS and web-application infrastructure. WordPress Core RFI (CWE-98) represents a classic yet persistent class: despite decades of awareness, path-traversal and file-inclusion primitives resurface in new architectural contexts (theme resolution, plugin hooks, REST endpoints). The unauthenticated vector without any precondition beyond a readable local `.php` file lowers the bar dramatically for opportunistic mass exploitation. Combined with WordPress's extraordinary market share, the attack surface is effectively every unpatched instance on the internet. The BOD 26-04 citation and forensic triage language signal that CISA is treating this as an active intrusion vector requiring IR readiness, not merely routine patching.

---

## Blog Post Candidates

1. **"CWE-98 in 2026: Why Remote File Inclusion Never Died"** — Walk through the historical arc of RFI (PHP register_globals era → modern theme/plugin surface), explain how page-template resolution became the new attack surface in WordPress Core, and provide detection signatures (access log patterns, EDR indicators) for defenders. High SEO value given WordPress's installed base.

2. **"BOD 26-04 Deep Dive: What CISA's New Patching Directive Means for Federal IT Teams"** — CVE-2026-87902 is the first KEV entry explicitly referencing BOD 26-04 forensic triage requirements. A timely explainer on the directive's dual mandate (patch prioritization + forensic readiness) would capture search traffic from federal IT and FISMA-scoped practitioners.

3. **"CISA KEV Due Dates Are Getting Shorter: A 3-Day Patch Window Analysis"** — CVE-2026-87902 has a one-day notice before its due date (added 2026-09-25, due 2026-09-28). Analyze the distribution of KEV due dates over 2025–2026 and discuss operational implications for vulnerability management programs lacking automated patching pipelines.

---

## Newsletter Snippet

**This week in the CISA KEV catalog:** One new critical web vulnerability was added — CVE-2026-87902, a Remote File Inclusion flaw in WordPress Core rated CVSS 8.1. The vulnerability allows an unauthenticated attacker to force WordPress's page-template resolution to include an attacker-chosen local PHP file, effectively achieving remote code execution without credentials. With WordPress running on over 43% of all websites, the blast radius of this vulnerability cannot be overstated. CISA's due date of September 28 gives affected organizations essentially 72 hours from disclosure — organizations without automated patching pipelines should treat this as an emergency change.

For federal agencies, CISA explicitly invoked BOD 26-04's forensic triage requirements alongside the standard patch mandate, signaling that evidence preservation and IR readiness are expected alongside remediation. If you haven't patched yet: update to the latest WordPress Core release, audit template-include hooks in active themes and plugins, and review web server access logs for anomalous `?template=` or `?page_template=` parameter activity. The FixTheVuln CVE detail page for CVE-2026-87902 includes remediation steps, OWASP mapping, and curated threat intelligence links.
