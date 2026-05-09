# Daily KEV Review — 2026-05-09

**CVEs to review:** 1

---

## CVE-2026-42208: BerriAI LiteLLM

**CVSS:** 9.8
**Description:** BerriAI LiteLLM contains a SQL injection vulnerability that allows an attacker to read data from the proxy's database and potentially modify it, leading to unauthorised access to the proxy and the credentials it manages.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-11
**CISA Notes:** https://github.com/BerriAI/litellm/security/advisories/GHSA-r75f-5x8p-qvmc ; https://nvd.nist.gov/vuln/detail/CVE-2026-42208

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-42208)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-42208)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-42208)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-42208)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-42208)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-42208)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```