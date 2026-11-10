# Daily KEV Review — 2026-11-10

**CVEs to review:** 6

---

## CVE-2026-124194: Microsoft Office

**CVSS:** 
**Description:** Microsoft Office Outlook contains a missing user interaction for potentially unsafe action vulnerability that allows an unauthorized attacker to perform spoofing over a network.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-24
**CISA Notes:** https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-124194 ; https://nvd.nist.gov/vuln/detail/CVE-2026-124194

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-124194)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-124194)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-124194)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-124194)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-124194)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-124194)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-111793: Openwave Messaging Limited Webtop Media Transcoder

**CVSS:** 4.3
**Description:** Openwave Messaging Limited Webtop Media Transcoder contains an incorrect resource transfer between spheres vulnerability that may allow an authenticated user to process and convert unintended document types if bypassing the Webmail experience.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-24
**CISA Notes:** https://github.com/GISOpenwave/security-advisories-public/blob/main/CAN-2026-2032674.md ; https://jvn.jp/en/vu/JVNVU93403064/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-111793

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-111793)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-111793)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-111793)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-111793)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-111793)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-111793)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-20320: Cisco BroadWorks

**CVSS:** 7.5
**Description:** Cisco BroadWorks contains an improper restriction of XML external entity reference vulnerability that could allow an unauthenticated, remote attacker to read sensitive configuration information on an affected system.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-24
**CISA Notes:** https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-bworks-xxe-uwUd7CEt ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-20320

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-20320)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-20320)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-20320)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-20320)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-20320)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-20320)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-111560: Barracuda Networks Multiple Products

**CVSS:** 8.6
**Description:** Barracuda Networks Email Security Gateway (ESG), Load Balancer, Application Delivery Controller (ADC), Message Archiver (BMA), WAF Control Center (WCC), Web Application Firewall (WAF), and Web Security Gateway (WSG) contain an OS command injection vulnerability. This vulnerability could allow an authenticated administrator to inject OS commands that execute with root privileges when the crafted timezone value is subsequently processed. This vulnerability can be chained with CVE-2026-116606
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-13
**CISA Notes:** https://trust.barracuda.com/security/pre-authentication-authorization-bypass-command-injection ; https://github.com/mandiant/Vulnerability-Disclosures/blob/master/2026/MNDT-2026-0041.md ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-111560

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-111560)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-111560)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-111560)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-111560)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-111560)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-111560)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-116606: Barracuda Networks Barracuda Email Security Gateway (ESG)

**CVSS:** 
**Description:** Barracuda Networks Email Security Gateway (ESG) contains an authentication bypass using an alternate path or channel that could allow an unauthenticated remote attacker to invoke a configuration-import function and restore a crafted, compatible backup archive, resulting in unauthorized modification of the appliance’s global configuration. This vulnerability can be chained with CVE-2026-111560.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-13
**CISA Notes:** https://trust.barracuda.com/security/pre-authentication-authorization-bypass-command-injection ; https://github.com/mandiant/Vulnerability-Disclosures/blob/master/2026/MNDT-2026-0042.md ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-116606

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-116606)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-116606)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-116606)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-116606)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-116606)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-116606)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-125350: Google Chromium

**CVSS:** 8.8
**Description:** Google Chromium contains a use-after-free vulnerability in the XML component that could allow a remote attacker to execute arbitrary code inside the sandbox via a specially crafted webpage. This vulnerability could affect multiple web browsers that utilize Chromium, including, but not limited to, Google Chrome, Microsoft Edge, and Opera.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-24
**CISA Notes:** https://chromereleases.googleblog.com/2026/11/stable-channel-update-for-desktop_018223192.html ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-125350

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-125350)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-125350)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-125350)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-125350)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-125350)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-125350)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```