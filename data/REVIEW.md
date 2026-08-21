# Daily KEV Review — 2026-08-21

**CVEs to review:** 2

---

## CVE-2026-72530: TrueConf Server

**CVSS:** 9.0
**Description:** TrueConf Server contains a code injection vulnerability that could allow an unauthorized remote attacker with network access via port 4307/TCP to use a specially crafted script to break out of the isolated environment and execute arbitrary code on the host system.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-03
**CISA Notes:** https://trueconf.com/blog/news/security-fixes-updates-and-advisories ; https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-breakout-from-isolated-environment/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-72530

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-72530)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-72530)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-72530)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-72530)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-72530)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-72530)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-72529: TrueConf Server

**CVSS:** 9.8
**Description:** TrueConf Server contains a missing authentication for critical function vulnerability which could allow a remote unauthorized attacker with network access via port 4307/TCP to execute an arbitrary script.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-23
**CISA Notes:** https://trueconf.com/blog/news/security-fixes-updates-and-advisories ; https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-missing-authentication-for-critical-function/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-72529

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-72529)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-72529)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-72529)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-72529)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-72529)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-72529)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```