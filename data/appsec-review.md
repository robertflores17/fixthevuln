# AppSec Review — 2026-04-15

**Reviewer:** Robert Flores, CISSP  
**Pipeline run:** 2026-04-15  
**CVEs reviewed:** 2  
**Total KEV database:** 82 vulnerabilities

---

## Severity Breakdown

| Priority | Count | CVEs |
|----------|-------|------|
| Critical | 0 | — |
| High | 1 | CVE-2009-0238 |
| Medium | 1 | CVE-2026-32201 |
| Low | 0 | — |

---

## CVE Summary

| CVE ID | Vendor | Product | Priority | Vulnerability Class |
|--------|--------|---------|----------|---------------------|
| CVE-2009-0238 | Microsoft | Office (Excel) | High | Remote Code Execution |
| CVE-2026-32201 | Microsoft | SharePoint Server | Medium | Improper Input Validation / Spoofing |

---

## CVE Details

**CVE-2009-0238** — Microsoft Office Excel RCE (CVSS 8.8, CWE-94: Code Injection)  
Remote code execution via a malformed object embedded in a crafted Excel file. Exploitation requires user interaction (opening the file), making it a classic spear-phishing payload. Grants complete system control on success. Legacy 2009 CVE added to KEV in April 2026, signaling renewed active exploitation — likely targeting organizations running end-of-life Office deployments or relying on legacy macro workflows.

**CVE-2026-32201** — Microsoft SharePoint Server Improper Input Validation (CVSS 6.5, CWE-20)  
Improper input validation in SharePoint Server allows an unauthenticated network attacker to perform spoofing. SharePoint's enterprise ubiquity elevates the real-world risk beyond the CVSS score; spoofing primitives in identity-integrated platforms can facilitate credential theft, session hijacking, or lateral movement when chained with other vulnerabilities.

---

## Trend Analysis

This batch continues a pattern of Microsoft enterprise platform vulnerabilities reaching active exploitation status. The inclusion of CVE-2009-0238 — a 17-year-old Excel flaw — is notable: CISA's addition signals that threat actors are deliberately reaching back into legacy CVE catalogs to target unpatched or end-of-life environments, a tactic increasingly observed in ransomware pre-positioning and APT campaigns. Organizations that have not fully deprecated Office 2007/2010 deployments remain exposed. CVE-2026-32201 reinforces the ongoing pressure on SharePoint Server, which has been a recurring KEV contributor; the spoofing primitive in an identity-integrated platform represents a meaningful lateral movement stepping stone even at medium severity. Together, the batch underscores two enduring challenges: legacy software debt and the attack surface of core enterprise collaboration infrastructure.

---

## Blog Post Candidates

1. **"Why CISA Is Adding 17-Year-Old CVEs to KEV in 2026"** — Explores the strategic rationale behind legacy CVE additions, what it signals about threat actor TTPs, and how organizations should audit for long-tail unpatched exposure.
2. **"SharePoint Server as an Attack Surface: A Recurring KEV Theme"** — Reviews the history of SharePoint entries in KEV, maps the common vulnerability classes (injection, auth bypass, spoofing), and provides a hardening checklist.
3. **"Excel as a Delivery Vehicle: The Enduring Risk of Office-Based RCE"** — Covers the phishing-to-RCE kill chain using malformed Office documents, why macro/object-based attacks persist, and modern mitigations (MOTW, attack surface reduction rules, ASR policies).

---

## Newsletter Snippet

**CISA KEV Update — April 15, 2026:** Two new vulnerabilities were added to CISA's Known Exploited Vulnerabilities catalog this week, both affecting Microsoft products. CVE-2009-0238, a remote code execution flaw in Microsoft Office Excel, was added 17 years after its original disclosure — a stark reminder that threat actors are actively weaponizing legacy vulnerabilities against organizations running outdated software. CVE-2026-32201, an improper input validation vulnerability in Microsoft SharePoint Server, enables unauthenticated network spoofing and continues a troubling pattern of SharePoint being targeted in enterprise environments. All U.S. federal agencies under BOD 22-01 must remediate by April 28, 2026.

For security teams, this week's additions carry a clear message: your patch management program must account for software that is no longer actively maintained or monitored. Both CVEs are straightforward to address — apply vendor patches or discontinue the affected product — but discovery risk is highest in organizations with shadow IT, decentralized patch governance, or large legacy estates. Review your Office and SharePoint Server inventory now, prioritize CVE-2009-0238 for any internet-connected or high-value workstations, and treat CVE-2026-32201 as a signal to audit SharePoint authentication and network segmentation controls.
