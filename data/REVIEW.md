# Daily KEV Review — 2026-08-05

**CVEs to review:** 3

---

## CVE-2026-18556: N-able N-central

**CVSS:** 7.4
**Description:** N-able N-central contains an authentication bypass using an alternate path or channel that allows for authentication bypass.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-07
**CISA Notes:** https://uptime.n-able.com/ ; https://status.n-able.com/2026/08/02/n-central-2026-3-hotfix-1-mitigation-for-cve-2026-18577/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-18556

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-18556)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-18556)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-18556)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-18556)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-18556)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-18556)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-34486: Apache Tomcat

**CVSS:** 9.8
**Description:** Apache Tomcat contains a missing encryption of sensitive data vulnerability that allows the bypass of the EncryptInterceptor.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-07
**CISA Notes:** https://lists.apache.org/thread/9510k5p5zdvt9pkkgtyp85mvwxo2qrly ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-34486

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-34486)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-34486)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-34486)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-34486)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-34486)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-34486)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-9198: IBM Langflow

**CVSS:** 9.8
**Description:** Langflow contains a code injection vulnerability that allows unauthenticated attackers to achieve full remote code execution on default Langflow deployments.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-07
**CISA Notes:** https://www.ibm.com/support/pages/node/7278927 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-9198

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-9198)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-9198)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-9198)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-9198)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-9198)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-9198)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```