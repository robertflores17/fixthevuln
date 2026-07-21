# Daily KEV Review — 2026-07-21

**CVEs to review:** 4

---

## CVE-2026-60137: WordPress Core

**CVSS:** 5.9
**Description:** WordPress Core contains a SQL injection vulnerability when a plugin or theme passes untrusted input to the parameter. This vulnerability can be chained with CVE-2026-63030 to allow an unauthenticated attacker to gain remote code execution on default WordPress installations.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-04
**CISA Notes:** https://wordpress.org/news/2026/07/wordpress-7-0-2-release/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-60137

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-60137)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-60137)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-60137)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-60137)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-60137)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-60137)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-63030: WordPress Core

**CVSS:** 9.8
**Description:** WordPress Core contains an interpretation conflict vulnerability that could allow an attacker to perform SQL Injection and achieve Remote Code Execution. This vulnerability can be chained with CVE-2026-60137.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-24
**CISA Notes:** https://wordpress.org/news/2026/07/wordpress-7-0-2-release/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-63030

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-63030)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-63030)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-63030)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-63030)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-63030)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-63030)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-0770: Langflow Langflow

**CVSS:** 9.8
**Description:** Langflow contains an inclusion of functionality from untrusted control sphere vulnerability that allows remote attackers to execute arbitrary code on affected installations. 
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-24
**CISA Notes:** https://github.com/langflow-ai/langflow/releases/tag/v1.9.0 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-0770 

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-0770)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-0770)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-0770)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-0770)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-0770)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-0770)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2021-27137: DD-WRT DD-WRT

**CVSS:** 8.1
**Description:** DD-WRT contains a stack-based buffer overflow vulnerability that could allow an unauthenticated attacker to overflow an internal buffer used by UPnP and trigger a code execution vulnerability.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-24
**CISA Notes:** This vulnerability affects a common open-source component, third-party library, proprietary implementation, or a protocol used by different products. Please check with specific vendors for information on patching status. For more information, please see: https://svn.dd-wrt.com/changeset/45724 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2021-27137

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2021-27137)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2021-27137)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2021-27137)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2021-27137)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2021-27137)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2021-27137)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```