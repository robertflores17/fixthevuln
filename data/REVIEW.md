# Daily KEV Review — 2026-07-17

**CVEs to review:** 3

---

## CVE-2026-58644: Microsoft SharePoint

**CVSS:** 9.8
**Description:** Microsoft SharePoint contains a deserialization of untrusted data vulnerability that allows an unauthorized attacker to execute code over a network.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-19
**CISA Notes:** https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-58644 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-58644

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-58644)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-58644)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-58644)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-58644)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-58644)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-58644)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-25089: Fortinet FortiSandbox

**CVSS:** 9.8
**Description:** Fortinet FortiSandbox, FortiSandbox Cloud, and FortiSandbox PaaS contain an OS command injection vulnerability that allows an unauthenticated attacker to execute unauthorized commands via specifically crafted HTTP requests.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-19
**CISA Notes:** https://fortiguard.fortinet.com/psirt/FG-IR-26-141 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-25089

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-25089)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-25089)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-25089)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-25089)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-25089)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-25089)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-39808: Fortinet FortiSandbox

**CVSS:** 9.8
**Description:** Fortinet FortiSandbox contains an OS command injection vulnerability that could allow an unauthenticated attacker to execute unauthorized code or commands via crafted HTTP requests.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-19
**CISA Notes:** https://fortiguard.fortinet.com/psirt/FG-IR-26-100 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-39808

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-39808)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-39808)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-39808)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-39808)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-39808)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-39808)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```