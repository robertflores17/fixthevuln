# Daily KEV Review — 2026-06-10

**CVEs to review:** 3

---

## CVE-2026-11645: Google Chromium V8

**CVSS:** 8.8
**Description:** Google Chromium V8 out-of-bounds read and write vulnerability that could allow a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. This vulnerability could affect multiple web browsers that utilize Chromium, including, but not limited to, Google Chrome, Microsoft Edge, and Opera.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-23
**CISA Notes:** https://chromereleases.googleblog.com/2026/06/stable-channel-update-for-desktop_0153744567.html ; https://issues.chromium.org/issues/506689381 ; https://nvd.nist.gov/vuln/detail/CVE-2026-11645

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-11645)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-11645)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-11645)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-11645)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-11645)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-11645)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-7473: Arista Extensible Operating System

**CVSS:** 5.8
**Description:** Arista Extensible Operating System (EOS) contains an incomplete comparison with missing factors vulnerability when the switch incorrectly decapsulate and forwards other unexpected tunneled packet with a destination IP matching its configured decapsulation IP.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-23
**CISA Notes:** https://www.arista.com/en/support/advisories-notices/security-advisory/24005-security-advisory-0137 ; https://nvd.nist.gov/vuln/detail/CVE-2026-7473

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-7473)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-7473)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-7473)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-7473)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-7473)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-7473)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-20245: Cisco Catalyst SD-WAN Manager

**CVSS:** 7.8
**Description:** Cisco Catalyst SD-WAN Manager formerly SD-WAN vManage contains an improper encoding or escaping of output vulnerability. This vulnerability could allow an authenticated, local attacker to execute arbitrary commands as root by supplying a crafted file to the affected system.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-23
**CISA Notes:** https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-privesc-4uxFrdzx ; https://nvd.nist.gov/vuln/detail/CVE-2026-20245

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-20245)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-20245)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-20245)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-20245)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-20245)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-20245)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```