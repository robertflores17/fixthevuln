# KEV Review - Week of 2026-01-31

**CVEs to review:** 8

---

## CVE-2026-1281: Ivanti Endpoint Manager Mobile (EPMM)

**Description:** Ivanti Endpoint Manager Mobile (EPMM) contains a code injection vulnerability that could allow attackers to achieve unauthenticated remote code execution.
**Due Date:** 2026-02-01
**CISA Notes:** Please adhere to Ivanti's guidelines to assess exposure and mitigate risks. Check for signs of potential compromise on all internet accessible Ivanti products affected by this vulnerability. Apply any final mitigations provided by the vendor as soon as possible. For more information please: see: https://forums.ivanti.com/s/article/Security-Advisory-Ivanti-Endpoint-Manager-Mobile-EPMM-CVE-2026-1281-CVE-2026-1340 ; https://support.mobileiron.com/mi/vsp/AB1771634/ivanti-security-update-1761642-1.0.0S-5.noarch.rpm ; https://support.mobileiron.com/mi/vsp/AB1771634/ivanti-security-update-1761642-1.0.0L-5.noarch.rpm ; https://nvd.nist.gov/vuln/detail/CVE-2026-1281

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-1281)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-1281)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-1281)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-1281)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-1281)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-1281)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2026-1281",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2026-24858: Fortinet Multiple Products

**Description:** Fortinet FortiAnalyzer, FortiManager, FortiOS, and FortiProxy contain an authentication bypass using an alternate path or channel that could allow an attacker with a FortiCloud account and a registered device to log into other devices registered to other accounts, if FortiCloud SSO authentication is enabled on those devices.
**Due Date:** 2026-01-30
**CISA Notes:** Please adhere to Fortinet's guidelines to assess exposure and mitigate risks. Check for signs of potential compromise on all internet accessible Fortinet products affected by this vulnerability. Apply any final mitigations provided by the vendor as soon as they become available. For more information please see: https://fortiguard.fortinet.com/psirt/FG-IR-26-060 ; https://www.fortinet.com/blog/psirt-blogs/analysis-of-sso-abuse-on-fortios ; https://nvd.nist.gov/vuln/detail/CVE-2026-24858

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-24858)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-24858)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-24858)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-24858)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-24858)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-24858)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2026-24858",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2018-14634: Linux Kernal

**Description:** Linux Kernel contains an integer overflow vulnerability in the create_elf_tables() function which could allow an unprivileged local user with access to SUID (or otherwise privileged) binary to escalate their privileges on the system.
**Due Date:** 2026-02-16
**CISA Notes:** This vulnerability affects a common open-source component, third-party library, or a protocol used by different products. Please check with specific vendors for information on patching status. For more information, please see: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/about/ ; https://www.kernel.org/ ; https://www.cve.org/CVERecord?id=CVE-2018-14634; https://access.redhat.com/errata/RHSA-2018:3540 ; https://nvd.nist.gov/vuln/detail/CVE-2018-14634

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2018-14634)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2018-14634)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2018-14634)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2018-14634)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2018-14634)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2018-14634)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2018-14634",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2025-52691: SmarterTools SmarterMail

**Description:** SmarterTools SmarterMail contains an unrestricted upload of file with dangerous type vulnerability that could allow an unauthenticated attacker to upload arbitrary files to any location on the mail server, potentially enabling remote code execution.
**Due Date:** 2026-02-16
**CISA Notes:** https://www.smartertools.com/smartermail/release-notes/current ; https://www.csa.gov.sg/alerts-and-advisories/alerts/al-2025-124/ ; https://nvd.nist.gov/vuln/detail/CVE-2025-52691

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-52691)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-52691)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-52691)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-52691)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-52691)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-52691)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2025-52691",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2026-23760: SmarterTools SmarterMail

**Description:** SmarterTools SmarterMail contains an authentication bypass using an alternate path or channel vulnerability in the password reset API. The force-reset-password endpoint permits anonymous requests and fails to verify the existing password or a reset token when resetting system administrator accounts. This could allow an unauthenticated attacker to supply a target administrator username and a new password to reset the account, resulting in full administrative compromise of the SmarterMail instance.
**Due Date:** 2026-02-16
**CISA Notes:** https://www.smartertools.com/smartermail/release-notes/current ; https://nvd.nist.gov/vuln/detail/CVE-2026-23760

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-23760)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-23760)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-23760)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-23760)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-23760)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-23760)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2026-23760",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2026-24061: GNU InetUtils

**Description:** GNU InetUtils contains an argument injection vulnerability in telnetd that could allow for remote authentication bypass via a "-f root" value for the USER environment variable.
**Due Date:** 2026-02-16
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://cgit.git.savannah.gnu.org/cgit/inetutils.git ; https://codeberg.org/inetutils/inetutils/commit/ccba9f748aa8d50a38d7748e2e60362edd6a32cc; https://codeberg.org/inetutils/inetutils/commit/fd702c02497b2f398e739e3119bed0b23dd7aa7b ; https://nvd.nist.gov/vuln/detail/CVE-2026-24061

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-24061)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-24061)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-24061)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-24061)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-24061)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-24061)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2026-24061",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2026-21509: Microsoft Office

**Description:** Microsoft Office contains a security feature bypass vulnerability in which reliance on untrusted inputs in a security decision in Microsoft Office could allow an unauthorized attacker to bypass a security feature locally. Some of the impacted product(s) could be end-of-life (EoL) and/or end-of-service (EoS). Users are advised to discontinue use and/or transition to a supported version.
**Due Date:** 2026-02-16
**CISA Notes:** Please adhere to Microsoft’s recommended guidelines to address this vulnerability. Implement all final mitigations provided by the vendor for Office 2021, and apply the interim corresponding mitigations for Office 2016 and Office 2019 until the final patch becomes available. For more information please see: https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-21509 ; https://nvd.nist.gov/vuln/detail/CVE-2026-21509

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-21509)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-21509)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-21509)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-21509)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-21509)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-21509)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2026-21509",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2024-37079: Broadcom VMware vCenter Server

**Description:** Broadcom VMware vCenter Server contains an out-of-bounds write vulnerability in the implementation of the DCERPC protocol. This could allow a malicious actor with network access to vCenter Server to send specially crafted network packets, potentially leading to remote code execution.
**Due Date:** 2026-02-13
**CISA Notes:** https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/24453 ; https://nvd.nist.gov/vuln/detail/CVE-2024-37079

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2024-37079)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2024-37079)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2024-37079)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2024-37079)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2024-37079)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2024-37079)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2024-37079",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## Ready-to-Paste HTML

After filling in the fields above, run:
```bash
python scripts/generate_html.py
```

Or manually create cards in this format:
```html
<div class="kev-card">
    <h4>Vendor Product</h4>
    <div class="cve-id">CVE-XXXX-XXXXX | CVSS X.X</div>
    <p>Your short description.</p>
    <div class="kev-fix"><strong>Fix:</strong> Your remediation.</div>
</div>
```