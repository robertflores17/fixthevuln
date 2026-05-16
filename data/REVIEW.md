# Daily KEV Review — 2026-05-16

**CVEs to review:** 1

---

## CVE-2026-42897: Microsoft Microsoft

**CVSS:** 8.1
**Description:** Microsoft Exchange Server contains a cross-site scripting vulnerability during web page generation in Outlook Web Access and when certain interaction conditions are met, arbitrary JavaScript can be executed in the browser context.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-29
**CISA Notes:** https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-42897 ; https://learn.microsoft.com/en-us/exchange/plan-and-deploy/post-installation-tasks/security-best-practices/exchange-emergency-mitigation-service ; https://nvd.nist.gov/vuln/detail/CVE-2026-42897

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-42897)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-42897)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-42897)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-42897)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-42897)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-42897)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```