# KEV Review - Week of 2026-02-14

**CVEs to review:** 1

---

## CVE-2026-1731: BeyondTrust Remote Support (RS) and Privileged Remote Access (PRA)

**CVSS:** 9.9
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

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```