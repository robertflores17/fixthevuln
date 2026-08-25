# Daily KEV Review — 2026-08-25

**CVEs to review:** 1

---

## CVE-2026-21962: Oracle HTTP Server and Oracle Weblogic Server Proxy Plug-in

**CVSS:** 10.0
**Description:** Oracle HTTP Server and Oracle Weblogic Server Proxy Plug-in contain an improper access control vulnerability that can result in unauthorized creation, deletion or modification access to critical data as well as unauthorized access to critical data or complete access to all Oracle HTTP Server and Oracle Weblogic Server Proxy Plug-in accessible data.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-08-27
**CISA Notes:** https://www.oracle.com/security-alerts/cpujan2026.html ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-21962

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-21962)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-21962)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-21962)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-21962)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-21962)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-21962)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```