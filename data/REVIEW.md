# Daily KEV Review — 2026-04-15

**CVEs to review:** 2

---

## CVE-2009-0238: Microsoft Office

**CVSS:** 8.8
**Description:** Microsoft Office Excel contains a remote code execution vulnerability that could allow an attacker to take complete control of an affected system if a user opens a specially crafted Excel file that includes a malformed object.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-04-28
**CISA Notes:** https://learn.microsoft.com/en-us/security-updates/securitybulletins/2009/ms09-009 ; https://nvd.nist.gov/vuln/detail/CVE-2009-0238

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2009-0238)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2009-0238)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2009-0238)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2009-0238)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2009-0238)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2009-0238)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-32201: Microsoft SharePoint Server

**CVSS:** 6.5
**Description:** Microsoft SharePoint Server contains an improper input validation vulnerability that allows an unauthorized attacker to perform spoofing over a network.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-04-28
**CISA Notes:** https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-32201 ; https://nvd.nist.gov/vuln/detail/CVE-2026-32201

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-32201)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-32201)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-32201)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-32201)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-32201)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-32201)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```