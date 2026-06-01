# Daily KEV Review — 2026-06-01

**CVEs to review:** 1

---

## CVE-2024-21182: Oracle WebLogic Server

**CVSS:** 7.5
**Description:** Oracle WebLogic contains an unspecified vulnerability that could allow an unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server. Successful attacks of this vulnerability can result in unauthorized access to critical data or complete access to all Oracle WebLogic Server accessible data.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-04
**CISA Notes:** https://www.oracle.com/security-alerts/cpujul2024.html ; https://nvd.nist.gov/vuln/detail/CVE-2024-21182

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2024-21182)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2024-21182)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2024-21182)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2024-21182)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2024-21182)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2024-21182)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```