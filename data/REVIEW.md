# Daily KEV Review — 2026-11-25

**CVEs to review:** 10

---

## CVE-2026-103406: Hewlett Packard Enterprise (HPE) Juniper Session Smart Conductor and Session Smart Router

**CVSS:** 9.8
**Description:** Hewlett Packard Enterprise (HPE) Juniper Session Smart Conductor and Session Smart Router contain an OS command injection vulnerability that could allow a remote attacker to execute arbitrary commands as root via a specially crafted salt minion ID.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-28
**CISA Notes:** https://supportportal.juniper.net/s/article/2026-10-On-Demand-Security-Bulletin-Session-Smart-Router-and-Session-Smart-Conductor-Multiple-internally-discovered-vulnerabilities-resolved ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-103406

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-103406)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-103406)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-103406)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-103406)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-103406)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-103406)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-133469: Vates Xen Orchestra

**CVSS:** 9.8
**Description:** Vates Xen Orchestra contains an improper validation of specified type of input vulnerability that could allow an unauthenticated attacker to bypass authentication and perform actions with administrative privileges via a specially crafted authentication token containing an empty JSON object.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-28
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://docs.vates.tech/security-advisories/advisories/2026/vates-sa-2026-062/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-133469

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-133469)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-133469)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-133469)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-133469)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-133469)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-133469)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-41450: Danfoss AK-SM 800A Series

**CVSS:** 7.5
**Description:** Danfoss AK-SM 800A Series contains an improper authentication vulnerability that could allow an attacker to generate a web report exposing sensitive information, including internal IP addresses, usernames, and store names.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-12-09
**CISA Notes:** https://www.danfoss.com/en/service-and-support/coordinated-vulnerability-disclosure/danfoss-security-advisories/dsa-2025-03-01 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2025-41450

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-41450)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-41450)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-41450)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-41450)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-41450)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-41450)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2023-25914: Danfoss AK-SM 800A Series

**CVSS:** 8.8
**Description:** Danfoss AK-SM 800A Series contains a path traversal vulnerability that could allow an attacker to access and read underlying server system files via the XML interface.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-28
**CISA Notes:** https://www.danfoss.com/en/service-and-support/coordinated-vulnerability-disclosure/danfoss-security-advisories/dsa-2023-08-01 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2023-25914

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2023-25914)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2023-25914)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2023-25914)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2023-25914)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2023-25914)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2023-25914)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2023-25915: Danfoss AK-SM 800A Series

**CVSS:** 8.8
**Description:** Danfoss AK-SM 800A Series contains an improper input validation vulnerability that could allow a remote attacker to run arbitrary commands on the affected system.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-28
**CISA Notes:** https://www.danfoss.com/en/service-and-support/coordinated-vulnerability-disclosure/danfoss-security-advisories/dsa-2023-08-01 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2023-25915

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2023-25915)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2023-25915)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2023-25915)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2023-25915)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2023-25915)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2023-25915)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-133324: Mitel MiCollab

**CVSS:** 5.3
**Description:** Mitel MiCollab contains a not failing securely vulnerability in the Audio, Web and Video Conferencing (AWV) component that could allow an unauthenticated attacker to bypass authentication controls and perform unauthorized actions.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-28
**CISA Notes:** https://www.mitel.com/support/security-advisories/mitel-product-security-advisory-misa-2026-0012 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-133324

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-133324)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-133324)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-133324)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-133324)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-133324)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-133324)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-133275: Mitel MiCollab

**CVSS:** 5.3
**Description:** Mitel MiCollab contains an unrestricted upload of file with dangerous type vulnerability in the Audio, Web and Video Conferencing (AWV) component due to insufficient file type validation that could allow an unauthenticated attacker to upload arbitrary files.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-28
**CISA Notes:** https://www.mitel.com/support/security-advisories/mitel-product-security-advisory-misa-2026-0012 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-133275

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-133275)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-133275)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-133275)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-133275)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-133275)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-133275)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-133311: Mitel MiCollab

**CVSS:** 5.9
**Description:** Mitel MiCollab contains a weak authentication vulnerability in the Audio, Web and Video Conferencing (AWV) component that could allow an unauthenticated attacker to access sensitive information using a specific system-generated random identifier or pre-staged content.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-12-09
**CISA Notes:** https://www.mitel.com/support/security-advisories/mitel-product-security-advisory-misa-2026-0012 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-133311

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-133311)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-133311)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-133311)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-133311)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-133311)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-133311)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-133303: Mitel MiCollab

**CVSS:** 9.8
**Description:** Mitel MiCollab contains an XML injection vulnerability in its Audio, Web, and Video Conferencing (AWV) component that could allow an unauthenticated attacker to execute arbitrary commands using pre-staged malicious content.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-28
**CISA Notes:** https://www.mitel.com/support/security-advisories/mitel-product-security-advisory-misa-2026-0012 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-133303

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-133303)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-133303)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-133303)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-133303)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-133303)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-133303)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-133323: Mitel MiCollab

**CVSS:** 9.8
**Description:** Mitel MiCollab contains an improper neutralization of special elements used in an OS command (OS command injection) vulnerability in its Audio, Web, and Video Conferencing (AWV) component that could allow an unauthenticated attacker to execute arbitrary system commands.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-28
**CISA Notes:** https://www.mitel.com/support/security-advisories/mitel-product-security-advisory-misa-2026-0012 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-133323

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-133323)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-133323)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-133323)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-133323)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-133323)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-133323)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```