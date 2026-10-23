# Daily KEV Review — 2026-10-23

**CVEs to review:** 1

---

## CVE-2026-114625: Arista VeloCloud Orchestrator

**CVSS:** 9.9
**Description:** Arista VeloCloud Orchestrator on-prem contains a SQL injection vulnerability that may allow a remote attacker to access privileged internal functionality and impact the VCO host. Successful exploitation may compromise the confidentiality, integrity, and availability of the orchestrator and data managed by the orchestrator.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-26
**CISA Notes:** https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199 ; ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-114625

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-114625)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-114625)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-114625)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-114625)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-114625)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-114625)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```