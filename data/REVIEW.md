# Daily KEV Review — 2026-05-02

**CVEs to review:** 1

---

## CVE-2026-31431: Linux Kernel

**CVSS:** 7.8
**Description:** Linux Kernel contains an incorrect resource transfer between spheres vulnerability that could allow for privilege escalation.
**Fix:** "Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-05-15
**CISA Notes:** https://lore.kernel.org/linux-cve-announce/2026042214-CVE-2026-31431-3d65@gregkh/; https://xint.io/blog/copy-fail-linux-distributions#the-fix-6 ; https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/about/ ; https://nvd.nist.gov/vuln/detail/CVE-2026-31431

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-31431)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-31431)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-31431)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-31431)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-31431)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-31431)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```