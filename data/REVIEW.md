# Daily KEV Review — 2026-07-16

**CVEs to review:** 2

---

## CVE-2026-46817: Oracle E-Business Suite

**CVSS:** 9.8
**Description:** Oracle E-Business Suite contains an improper privilege management vulnerability that allows an unauthenticated attacker with network access via HTTP to compromise Oracle Payments. Successful attacks of this vulnerability can result in takeover of Oracle Payments.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-18
**CISA Notes:** https://www.oracle.com/security-alerts/cspumay2026.html ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-46817

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-46817)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-46817)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-46817)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-46817)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-46817)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-46817)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2023-4346: KNX Association KNX Protocol Connection Authorization Option 1

**CVSS:** 7.5
**Description:** KNX Association KNX Protocol Connection Authorization Option 1 contains an overly restrictive account lockout mechanism vulnerability that could allow an attacker to purge all devices without additional security options enabled and set a BCU key to lock the device. 
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-29
**CISA Notes:** https://www.cisa.gov/news-events/ics-advisories/icsa-23-236-01 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2023-4346

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2023-4346)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2023-4346)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2023-4346)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2023-4346)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2023-4346)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2023-4346)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```