# Daily KEV Review — 2026-09-11

**CVEs to review:** 2

---

## CVE-2026-86060: MikroTik RouterOS

**CVSS:** 9.8
**Description:** MikroTik RouterOS contains an improper neutralization of argument delimiters in a command vulnerability which allows an attacked to change the trusted RouterOS policy mask, leading to privilege escalation.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-13
**CISA Notes:**  ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-86060

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-86060)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-86060)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-86060)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-86060)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-86060)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-86060)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-67277: MikroTik RouterOS

**CVSS:** 8.2
**Description:** MikroTik RouterOS contains a missing authenticaion for critical function vulnerability which allows kernel memory disclosure and denial of service in the btest service.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-13
**CISA Notes:** https://mikrotik.com/supportsec/september-2026-vulnerability/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-67277

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-67277)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-67277)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-67277)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-67277)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-67277)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-67277)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```