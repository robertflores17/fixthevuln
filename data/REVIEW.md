# Daily KEV Review — 2026-11-04

**CVEs to review:** 2

---

## CVE-2024-27834: Apple Multiple Products

**CVSS:** 5.5
**Description:** Apple iOS, iPadOS, macOS, Safari, tvOS and watchOS 10.5 contain an improper authentication vulnerability which could allow an attacker with arbitrary read and write capability to bypass pointer authentication.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-18
**CISA Notes:** https://support.apple.com/en-us/120896 ; https://support.apple.com/en-us/120898 ; https://support.apple.com/en-us/120901 ; https://support.apple.com/en-us/120902 ; https://support.apple.com/en-us/120903 ; https://support.apple.com/en-us/120905 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2024-27834

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2024-27834)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2024-27834)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2024-27834)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2024-27834)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2024-27834)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2024-27834)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-119977: WordPress WordPress Core

**CVSS:** 8.1
**Description:** WordPress WordPress Core contains a time-of-check time-of-use (TOCTOU) race condition vulnerability that could allow unauthenticated attackers to execute code on the server during the upgrade window. This is due to predictable, web-accessible staging paths used during full-package core upgrades.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-06
**CISA Notes:** https://wordpress.org/news/2026/10/wordpress-7-1-4 ; https://www.wordfence.com/threat-intel/vulnerabilities/wordpress-core/wordpress-core-470-713-unauthenticated-upgrade-window-staged-installer-remote-code-execution ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-119977

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-119977)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-119977)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-119977)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-119977)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-119977)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-119977)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```