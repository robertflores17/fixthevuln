# Daily KEV Review — 2026-09-12

**CVEs to review:** 4

---

## CVE-2026-84869: ConnectWise ScreenConnect

**CVSS:** 9.9
**Description:** ConnectWise ScreenConnect contains both an improper privilege management and missing authorization vulnerability that may allow an attacker to file transfer and execution through an active remote sessions without authorization or host confirmation.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-14
**CISA Notes:** https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-84869

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-84869)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-84869)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-84869)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-84869)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-84869)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-84869)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-42016: JFrog Artifactory

**CVSS:** 8.1
**Description:** JFrog Artifactory contains an incorrect authorization vulnerability that allows leads to privilege escalation attack due to a validation check of the token signature/issuer and not the token’s scope.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-25
**CISA Notes:** https://docs.jfrog.com/releases/docs/jfrog-security-advisories ; https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-42016

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-42016)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-42016)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-42016)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-42016)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-42016)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-42016)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-42018: JFrog Artifactory

**CVSS:** 7.5
**Description:** JFrog Artifactory contains an improper authentication vulnerability that could return an internal anonymous-user token to an unauthenticated caller when anonymous access is disabled, potentially exposing sensitive resources.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-25
**CISA Notes:** https://docs.jfrog.com/releases/docs/jfrog-security-advisories ; https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-42018

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-42018)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-42018)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-42018)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-42018)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-42018)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-42018)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-85706: GitLab Community Edition and Enterprise Edition

**CVSS:** 10.0
**Description:** GitLab Community Edition and Enterprise Edition contains a path traversal vulnerability that allows an unauthenticated user to read arbitrary files due to an improper path confinement and missing authentication enforcement in the repository commits API.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-14
**CISA Notes:** https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-85706

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-85706)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-85706)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-85706)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-85706)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-85706)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-85706)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```