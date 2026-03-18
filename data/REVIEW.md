# Daily KEV Review — 2026-03-18

**CVEs to review:** 1

---

## CVE-2025-47813: Wing FTP Server Wing FTP Server

**CVSS:** 4.3
**Description:** Wing FTP Server contains a generation of error message containing sensitive information vulnerability when using a long value in the UID cookie.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-03-30
**CISA Notes:** https://www.wftpserver.com/serverhistory.htm ; https://nvd.nist.gov/vuln/detail/CVE-2025-47813

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-47813)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-47813)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-47813)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-47813)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-47813)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-47813)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```