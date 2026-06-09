# Daily KEV Review — 2026-06-09

**CVEs to review:** 2

---

## [RANSOMWARE] CVE-2026-50751: Check Point Security Gateway

**CVSS:** 9.3
**Description:** Check Point Security Gateway contains an improper authentication vulnerability in IKEv1 key exchange that could allow an unauthenticated remote attacker to bypass user authentication and establish a remote access VPN connection without a valid user password.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-11
**CISA Notes:** https://blog.checkpoint.com/security/check-point-releases-important-hotfix-for-vulnerabilities-in-deprecated-ikev1-vpn-protocol/ ; https://support.checkpoint.com/results/sk/sk185033?_gl=1*1wqeqhc*_gcl_au*MTI1MzE5MjI2LjE3ODA5MzQ1NTM. ; https://nvd.nist.gov/vuln/detail/CVE-2026-50751

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-50751)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-50751)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-50751)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-50751)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-50751)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-50751)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-42271: BerriAI LiteLLM

**CVSS:** 8.8
**Description:** BerriAI LiteLLM contains a command injection vulnerability that could allow any authenticated user, including holders of low-privilege internal-user keys, to run arbitrary commands on the host.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-06-22
**CISA Notes:** This vulnerability affects a common open-source component, third-party library, or a protocol used by different products. Please check with specific vendors for information on patching status. For more information, please see: https://github.com/BerriAI/litellm/security/advisories/GHSA-v4p8-mg3p-g94g ; https://github.com/BerriAI/litellm/releases/tag/v1.83.7-stable ; https://nvd.nist.gov/vuln/detail/CVE-2026-42271

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-42271)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-42271)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-42271)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-42271)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-42271)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-42271)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```