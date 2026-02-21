# KEV Review - Week of 2026-02-21

**CVEs to review:** 9

---

## [RANSOMWARE] CVE-2026-1731: BeyondTrust Remote Support (RS) and Privileged Remote Access (PRA)

**CVSS:** 9.8
**Description:** BeyondTrust Remote Support (RS) and Privileged Remote Access (PRA)contain an OS command injection vulnerability. Successful exploitation could allow an unauthenticated remote attacker to execute operating system commands in the context of the site user. Successful exploitation requires no authentication or user interaction and may lead to system compromise, including unauthorized access, data exfiltration, and service disruption.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-02-16
**CISA Notes:** Please adhere to the vendor's guidelines to assess exposure and mitigate risks. Check for signs of potential compromise on all internet accessible BeyondTrust products affected by this vulnerability. For more information please: see: https://www.beyondtrust.com/trust-center/security-advisories/bt26-02 ; https://nvd.nist.gov/vuln/detail/CVE-2026-1731

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-1731)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-1731)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-1731)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-1731)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-1731)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-1731)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-49113: Roundcube Webmail

**CVSS:** 9.9
**Description:** RoundCube Webmail contains a deserialization of untrusted data vulnerability that allows remote code execution by authenticated users because the _from parameter in a URL is not validated in program/actions/settings/upload.php.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-13
**CISA Notes:** https://roundcube.net/news/2025/06/01/security-updates-1.6.11-and-1.5.10 ; https://github.com/roundcube/roundcubemail/releases/tag/1.5.10 ; https://github.com/roundcube/roundcubemail/releases/tag/1.6.11 ; https://nvd.nist.gov/vuln/detail/CVE-2025-49113

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-49113)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-49113)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-49113)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-49113)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-49113)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-49113)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-68461: Roundcube Webmail

**CVSS:** 7.2
**Description:** RoundCube Webmail contains a cross-site scripting vulnerability via the animate tag in an SVG document.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-13
**CISA Notes:** https://roundcube.net/news/2025/12/13/security-updates-1.6.12-and-1.5.12 ; https://github.com/roundcube/roundcubemail/commit/bfa032631c36b900e7444dfa278340b33cbf7cdb ; https://nvd.nist.gov/vuln/detail/CVE-2025-68461

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-68461)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-68461)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-68461)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-68461)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-68461)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-68461)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2021-22175: GitLab GitLab

**CVSS:** 6.8
**Description:** GitLab contains a server-side request forgery (SSRF) vulnerability when requests to the internal network for webhooks are enabled.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-11
**CISA Notes:** https://gitlab.com/gitlab-org/cves/-/blob/master/2021/CVE-2021-22175.json ; https://nvd.nist.gov/vuln/detail/CVE-2021-22175

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2021-22175)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2021-22175)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2021-22175)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2021-22175)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2021-22175)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2021-22175)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-22769: Dell RecoverPoint for Virtual Machines (RP4VMs)

**CVSS:** 10.0
**Description:** Dell RecoverPoint for Virtual Machines (RP4VMs) contains an use of hard-coded credentials vulnerability that could allow an unauthenticated remote attacker to gain unauthorized access to the underlying operating system and root-level persistence.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-02-21
**CISA Notes:** https://www.dell.com/support/kbdoc/en-us/000426773/dsa-2026-079 ; https://www.dell.com/support/kbdoc/en-us/000426742/recoverpoint-for-vms-apply-the-remediation-script-for-dsa ; https://cloud.google.com/blog/topics/threat-intelligence/unc6201-exploiting-dell-recoverpoint-zero-day ; https://nvd.nist.gov/vuln/detail/CVE-2026-22769

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-22769)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-22769)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-22769)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-22769)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-22769)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-22769)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2020-7796: Synacor Zimbra Collaboration Suite

**CVSS:** 9.8
**Description:** Synacor Zimbra Collaboration Suite (ZCS) contains a server-side request forgery vulnerability if WebEx zimlet installed and zimlet JSP is enabled.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-10
**CISA Notes:** https://wiki.zimbra.com/wiki/Zimbra_Releases/8.8.15/P7 ; https://nvd.nist.gov/vuln/detail/CVE-2020-7796

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2020-7796)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2020-7796)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2020-7796)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2020-7796)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2020-7796)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2020-7796)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2024-7694: TeamT5 ThreatSonar Anti-Ransomware

**CVSS:** 7.2
**Description:** TeamT5 ThreatSonar Anti-Ransomware contains an unrestricted upload of file with dangerous type vulnerability. ThreatSonar Anti-Ransomware does not properly validate the content of uploaded files. Remote attackers with administrator privileges on the product platform can upload malicious files, which can be used to execute arbitrary system commands on the server.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-10
**CISA Notes:** https://teamt5.org/en/posts/vulnerability-notice-threat-sonar-anti-ransomware-20240715/ ; https://www.twcert.org.tw/en/cp-139-8000-e5a5c-2.html ; https://nvd.nist.gov/vuln/detail/CVE-2024-7694

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2024-7694)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2024-7694)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2024-7694)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2024-7694)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2024-7694)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2024-7694)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2008-0015: Microsoft Windows

**CVSS:** 8.8
**Description:** Microsoft Windows Video ActiveX Control contains a remote code execution vulnerability. An attacker could exploit the vulnerability by constructing a specially crafted Web page. When a user views the Web page, the vulnerability could allow remote code execution. An attacker who successfully exploited this vulnerability could gain the same user rights as the logged-on user.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-10
**CISA Notes:** https://web.archive.org/web/20110305211119/https://www.microsoft.com/technet/security/bulletin/ms09-032.mspx ; https://nvd.nist.gov/vuln/detail/CVE-2008-0015

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2008-0015)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2008-0015)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2008-0015)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2008-0015)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2008-0015)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2008-0015)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-2441: Google Chromium

**CVSS:** 8.8
**Description:** Google Chromium CSS contains a use-after-free vulnerability that could allow a remote attacker to potentially exploit heap corruption via a crafted HTML page. This vulnerability could affect multiple web browsers that utilize Chromium, including, but not limited to, Google Chrome, Microsoft Edge, and Opera.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-10
**CISA Notes:** https://chromereleases.googleblog.com/2026/02/stable-channel-update-for-desktop_13.html ; https://nvd.nist.gov/vuln/detail/CVE-2026-2441

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-2441)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-2441)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-2441)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-2441)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-2441)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-2441)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```