# Daily KEV Review — 2026-11-24

**CVEs to review:** 3

---

## CVE-2026-132224: Optimizely Web Experimentation

**CVSS:** 8.7
**Description:** Optimizely Web Experimentation contains an external control of critical state data vulnerability in its account signup flow that could allow an attacker to impersonate existing customer users and modify Project JavaScript. Successful exploitation can result in attacker-controlled JavaScript being distributed through Optimizely-hosted assets and executed in browsers visiting affected customer websites.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-27
**CISA Notes:** https://pages.optimizely.com/rs/947-RKE-048/images/Security%20Incident%20Report%20-%20Optimizely%20Web%20Experimentation%20-%20Nov%2017%202026.pdf ; https://status.optimizely.com/incidents/ftw0fh9wx43z ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-132224

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-132224)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-132224)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-132224)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-132224)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-132224)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-132224)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-131914: Idunno AntiCsrf

**CVSS:** 9.8
**Description:** Idunno AntiCsrf contains a deserialization of untrusted data vulnerability that allows an unauthenticated remote attacker to execute arbitrary code via object injection. The impacted product(s) could be end-of-life (EoL) and/or end-of-service (EoS). Users are advised to discontinue use and/or transition to a supported version.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-27
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://github.com/mandiant/Vulnerability-Disclosures/blob/master/2026/MNDT-2026-0048.md ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-131914

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-131914)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-131914)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-131914)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-131914)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-131914)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-131914)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-132165: Drupal Core

**CVSS:** 
**Description:** Drupal Core contains a not failing securely vulnerability that could allow an unauthenticated attacker to take over an existing site or execute arbitrary code via the Drupal installer. Under specific conditions, the attacker can use install.php to attempt to reinstall Drupal on the site.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-27
**CISA Notes:** https://www.drupal.org/sa-core-2026-017 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-132165

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-132165)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-132165)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-132165)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-132165)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-132165)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-132165)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```