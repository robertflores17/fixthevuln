# Daily KEV Review — 2026-10-27

**CVEs to review:** 2

---

## CVE-2026-109618: PHP Group PHP

**CVSS:** 9.8
**Description:** PHP contains an out-of-memory corruption vulnerability that allows for unauthenticated remote code execution.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-29
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://www.php.net/ ; https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ;  https://nvd.nist.gov/vuln/detail/CVE-2026-109618

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-109618)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-109618)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-109618)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-109618)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-109618)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-109618)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-109619: PHP Group PHP

**CVSS:** 8.1
**Description:** PHP contains a stale internal request-state vulnerability that allows for unauthenticated remote code execution.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-10-29
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://www.php.net/ ; https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ;  https://nvd.nist.gov/vuln/detail/CVE-2026-109619

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-109619)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-109619)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-109619)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-109619)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-109619)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-109619)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```