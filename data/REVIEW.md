# Daily KEV Review — 2026-05-27

**CVEs to review:** 4

---

## CVE-2026-48027: Nx Nx Console

**CVSS:** 9.3
**Description:** Nx Console contains an embedded malicious code vulnerability that allowed a malicious version of Nx Console to be published. The compromised extension fetched an obfuscated payload that could harvested credentials from multiple sources on disk and in memory.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-10
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://github.com/nrwl/nx-console/security/advisories/GHSA-c9j4-9m59-847w ; https://nvd.nist.gov/vuln/detail/CVE-2026-48027

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-48027)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-48027)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-48027)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-48027)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-48027)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-48027)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-45321: TanStack TanStack

**CVSS:** 9.6
**Description:** TanStack contains an unspecified vulnerability that allowed malicious versions of the product to be published to the npm registry to publish credential-stealing malware under a trusted identity.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-10
**CISA Notes:** This vulnerability could affect an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products. For more information, please see: https://github.com/TanStack/router/security/advisories/GHSA-g7cv-rxg3-hmpx ; https://nvd.nist.gov/vuln/detail/CVE-2026-45321

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-45321)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-45321)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-45321)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-45321)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-45321)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-45321)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-8398: Daemon Daemon Tools Lite

**CVSS:** 9.8
**Description:** Daemon Tools contains an unspecified vulnerability that has a high impact on confidentiality, integrity, and availability.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-30
**CISA Notes:** https://blog.daemon-tools.cc/post/security-incident ; https://nvd.nist.gov/vuln/detail/CVE-2026-8398

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-8398)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-8398)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-8398)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-8398)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-8398)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-8398)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-48172: LiteSpeed cPanel Plugin

**CVSS:** 9.8
**Description:** LiteSpeed cPanel Plugin contains privilege escalation vulnerability that is exposed via the user-end cPanel plugin, which can be abused by any cPanel user account to execute arbitrary scripts with root privileges.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-29
**CISA Notes:** https://blog.litespeedtech.com/2026/05/21/security-update-for-litespeed-cpanel-plugin/ ; https://nvd.nist.gov/vuln/detail/CVE-2026-48172

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-48172)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-48172)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-48172)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-48172)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-48172)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-48172)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```