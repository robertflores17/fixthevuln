# KEV Review - Week of 2026-02-03

**CVEs to review:** 4

---

## CVE-2021-39935: GitLab Community and Enterprise Editions

**CVSS:** 6.8
**Description:** GitLab Community and Enterprise Editions contain a server-side request forgery vulnerability which could allow unauthorized external users to perform Server Side Requests via the CI Lint API. 
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-02-24
**CISA Notes:** https://about.gitlab.com/releases/2021/12/06/security-release-gitlab-14-5-2-released/ ; https://nvd.nist.gov/vuln/detail/CVE-2021-39935

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2021-39935)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2021-39935)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2021-39935)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2021-39935)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2021-39935)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2021-39935)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-64328: Sangoma FreePBX

**CVSS:** 
**Description:** Sangoma FreePBX Endpoint Manager contains an OS command injection vulnerability that could allow for a post-authentication command injection by an authenticated known user via the testconnection -> check_ssh_connect() function. An attacker can leverage this vulnerability to potentially obtain remote access to the system as an asterisk user. 
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-02-24
**CISA Notes:** https://github.com/FreePBX/security-reporting/security/advisories/GHSA-vm9p-46mv-5xvw ; https://nvd.nist.gov/vuln/detail/CVE-2025-64328

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-64328)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-64328)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-64328)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-64328)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-64328)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-64328)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2019-19006: Sangoma FreePBX

**CVSS:** 9.8
**Description:** Sangoma FreePBX contains an improper authentication vulnerability that potentially allows unauthorized users to bypass password authentication and access services provided by the FreePBX admin.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-02-24
**CISA Notes:** https://wiki.freepbx.org/display/FOP/2019-11-20%2BRemote%2BAdmin%2BAuthentication%2BBypass ; https://nvd.nist.gov/vuln/detail/CVE-2019-19006

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2019-19006)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2019-19006)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2019-19006)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2019-19006)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2019-19006)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2019-19006)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2025-40551: SolarWinds Web Help Desk

**CVSS:** 9.8
**Description:** SolarWinds Web Help Desk contains a deserialization of untrusted data vulnerability that could lead to remote code execution, which would allow an attacker to run commands on the host machine. This could be exploited without authentication.
**Fix:** Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable.
**Due Date:** 2026-02-06
**CISA Notes:** https://www.solarwinds.com/trust-center/security-advisories/cve-2025-40551 ; https://nvd.nist.gov/vuln/detail/CVE-2025-40551

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-40551)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-40551)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-40551)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-40551)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-40551)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-40551)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```