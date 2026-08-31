# Daily KEV Review — 2026-08-31

**CVEs to review:** 2

---

## CVE-2026-82078: PaperCut NG/MF

**CVSS:** 9.1
**Description:** PaperCut NG/MF contains an unsafe reflection vulnerability that allows an attacker to manipulate system configuration parameters and execute arbitrary Java bytecode residing on the application classpath under the security context of the PaperCut server process. This vulnerability can be chained with CVE-2026-81578.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-14
**CISA Notes:** https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/?lid=2oneu2wt0ct4 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-82078

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-82078)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-82078)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-82078)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-82078)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-82078)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-82078)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-81578: PaperCut NG/MF

**CVSS:** 9.8
**Description:** PaperCut NG/MF contains a missing authentication for critical function vulnerability which allows an unauthenticated remote attacker to modify certain system configurations. This vulnerability can be chained with CVE-2026-82078.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-14
**CISA Notes:** https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-81578

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-81578)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-81578)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-81578)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-81578)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-81578)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-81578)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```