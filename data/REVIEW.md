# Daily KEV Review — 2026-11-20

**CVEs to review:** 4

---

## CVE-2026-129448: Apache Roller

**CVSS:** 9.8
**Description:** Apache Roller contains a deserialization of untrusted data vulnerability that allows an unauthenticated remote attacker to execute arbitrary code via the XML-RPC endpoint, which accepts and deserializes vendor extension types before authentication. This CVE covers the same underlying vulnerability as CVE-2026-82384 but applies to a broader range of affected versions.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-23
**CISA Notes:** https://lists.apache.org/thread/cc0jck13nb9vvcmzxzwotr6n16mx28z9 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-129448

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-129448)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-129448)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-129448)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-129448)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-129448)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-129448)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-123890: Broadcom VMware vCenter

**CVSS:** 9.8
**Description:** Broadcom VMware vCenter contains an authentication bypass using an alternate path or channel vulnerability in the VMware Directory Service that allows an unauthenticated attacker with network access to vCenter to bypass authentication and gain unauthorized access to the system.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines
**Due Date:** 2026-11-23
**CISA Notes:** https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/39495 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-123890

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-123890)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-123890)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-123890)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-123890)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-123890)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-123890)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-42884: SAP NetWeaver

**CVSS:** 6.5
**Description:** SAP NetWeaver Enterprise Portal contains an improper neutralization of special elements in data query logic vulnerability that allows an unauthenticated attacker to disclose or modify server information via injected JNDI environment properties or a URL used during JNDI lookup operations.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-23
**CISA Notes:** https://support.sap.com/en/my-support/knowledge-base/security-notes-news/bulletin-2025.html ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2025-42884

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-42884)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-42884)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-42884)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-42884)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-42884)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-42884)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-76466: Cisco Expressway Series

**CVSS:** 9.8
**Description:** Cisco Expressway Series contains a use of hard-coded credentials vulnerability that allows an unauthenticated, remote attacker with persistent cookies and network access to execute commands as root on a clustered device via the database service.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-23
**CISA Notes:** https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-vcs-static-cred-hr7EWZ8t ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-76466

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-76466)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-76466)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-76466)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-76466)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-76466)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-76466)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```