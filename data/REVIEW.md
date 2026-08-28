# Daily KEV Review — 2026-08-28

**CVEs to review:** 10

---

## CVE-2023-49105: ownCloud ownCloud

**CVSS:** 9.8
**Description:** ownCloud contains an improper authentication vulnerability that allows an attacker to access, modify, or delete any file without authentication if the username of a victim is known, and the victim has no signing-key configured.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-30
**CISA Notes:** https://owncloud.org/security ; https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2023-49105

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2023-49105)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2023-49105)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2023-49105)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2023-49105)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2023-49105)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2023-49105)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-53362: Linux Kernel

**CVSS:** 7.8
**Description:** Linux Kernel contains an unspecified vulnerability that can allow for privilege escalation via IPv6 networking subsystem. This vulnerability can impact multiple products, including but not limited to Suse, Red Hat, and other products using Linux. 
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-30
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: ; https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962; https://git.kernel.org/stable/c/65fb14cbebb0cd0eff903a22d33537ddc8b95769; https://git.kernel.org/stable/c/46f201f8b4c39633a1fa3dc12459f506d470993d; https://git.kernel.org/stable/c/6374fb9edf72c67a118a2c214a0dddd04c921e0a; https://git.kernel.org/stable/c/e9eacf19281ea2498b36291b56c9606118c2d74e; https://git.kernel.org/stable/c/736b380e28d0480c7bc3e022f1950f31fe53a7c5 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-53362

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-53362)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-53362)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-53362)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-53362)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-53362)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-53362)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-66384: JFrog Artifactory

**CVSS:** 5.3
**Description:** JFrog Artifactory contains an improper limitation of a pathname to a restricted directory vulnerability. This can allow an authenticated user to write data outside the intended Docker cache path under specific remote-repository conditions.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-10
**CISA Notes:** https://docs.jfrog.com/releases/docs/jfrog-security-advisories ; https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-66384

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-66384)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-66384)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-66384)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-66384)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-66384)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-66384)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2021-23758: Ajax.NET Professional Ajax.NET Professional

**CVSS:** 8.1
**Description:** Ajax.NET Professional (AjaxPro) contains a deserialization of untrusted data vulnerability that could allow for remote code execution via arbitrary .NET classes. The impacted product(s) could be end-of-life (EoL) and/or end-of-service (EoS). Users are advised to discontinue use and/or transition to a supported version.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-09
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://github.com/michaelschwarz/Ajax.NET-Professional/commit/b0e63be5f0bb20dfce507cb8a1a9568f6e73de57 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2021-23758

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2021-23758)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2021-23758)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2021-23758)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2021-23758)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2021-23758)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2021-23758)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2015-3246: Red Hat Libuser

**CVSS:** 5.1
**Description:** Red Hat libuser contains a race condition vulnerability that allows authenticated local users to corrupt the /etc/passwd file to cause a denial of service or privilege escalation. 
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-09
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://access.redhat.com/articles/1537873 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2015-3246

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2015-3246)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2015-3246)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2015-3246)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2015-3246)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2015-3246)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2015-3246)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2015-5287: Red Hat Automatic Bug Reporting Tool

**CVSS:** 7.8
**Description:** Red Hat Automatic Bug Reporting Tool (ABRT) contains a privilege escalation vulnerability that could allow local users with certain permissions to gain privileges via a symlink attack on a file with a predictable name. The impacted product(s) could be end-of-life (EoL) and/or end-of-service (EoS). Users are advised to discontinue use and/or transition to a supported version.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-09
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://github.com/abrt/abrt/commit/3c1b60cfa62d39e5fff5a53a5bc53dae189e740e ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2015-5287

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2015-5287)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2015-5287)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2015-5287)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2015-5287)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2015-5287)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2015-5287)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2022-0995: Linux Kernel

**CVSS:** 7.8
**Description:** Linux Kernel contains an out-of-bounds memory write vulnerability which could allow a local user to gain privileged access or cause a denial of service on the system.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-09-09
**CISA Notes:** This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=93ce93587d36493f2f86921fa79921b3cba63fbb ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2022-0995

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2022-0995)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2022-0995)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2022-0995)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2022-0995)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2022-0995)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2022-0995)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-8452: Citrix NetScaler ADC and NetScaler Gateway

**CVSS:** 9.8
**Description:** Citrix NetScaler ADC and NetScaler Gateway contain an improper restriction of operations within the bounds of a memory buffer vulnerability which could lead to denial of service. 
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-29
**CISA Notes:** https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-8452

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-8452)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-8452)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-8452)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-8452)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-8452)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-8452)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2019-1068: Microsoft SQL Server

**CVSS:** 8.8
**Description:** Microsoft SQL Server contains a remote code execution vulnerability that could allow an attacker to execute code in the context of the SQL Server Database Engine service account.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-29
**CISA Notes:** https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2019-1068

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2019-1068)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2019-1068)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2019-1068)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2019-1068)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2019-1068)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2019-1068)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-60004: Gitea Gitea

**CVSS:** 9.8
**Description:** Gitea contains a code injection vulnerability that allows an attacker with repository write access to send a malicious patch to the diffpatch API endpoint to plant an executable Git hook and run shell commands as the Gitea service account.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-28
**CISA Notes:** https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-60004

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-60004)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-60004)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-60004)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-60004)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-60004)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-60004)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```