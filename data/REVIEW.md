# Daily KEV Review — 2026-09-26

**CVEs to review:** 1

---

## CVE-2026-87902: WordPress Core

**CVSS:** 8.1
**Description:** WordPress Core contains a remote file inclusion vulnerability which could allow an unauthenticated attacker to make page-template resolution include a chosen readable local `.php` file outside the active theme directories, leading to remote code execution.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-28
**CISA Notes:** https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp ; ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-87902

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-87902)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-87902)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-87902)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-87902)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-87902)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-87902)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```