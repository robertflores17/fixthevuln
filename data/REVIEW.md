# Daily KEV Review — 2026-11-24

**CVEs to review:** 2

---

## CVE-2026-133968: Project MONAI MONAI Label

**CVSS:** 9.8
**Description:** Project MONAI MONAI Label contains a path traversal vulnerability that allows an unauthenticated remote attacker to write arbitrary files outside the intended datastore directory, potentially resulting in remote code execution.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-26
**CISA Notes:** https://github.com/Project-MONAI/MONAILabel/security/advisories/GHSA-qc22-rmgc-vg94 ; https://github.com/Project-MONAI/MONAILabel/pull/1915 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-133968

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-133968)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-133968)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-133968)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-133968)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-133968)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-133968)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-134624: N-able MailAssure

**CVSS:** 9.3
**Description:** N-able MailAssure (SpamExperts) contains a server-side request forgery vulnerability in the LDAP synchronization connection check that allows an authenticated API user to connect to arbitrary internal hosts and ports, determine which are reachable, and send crafted data to internal services.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-26
**CISA Notes:** https://me.n-able.com/s/security-advisory/aArVy0000002mrlKAA ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-134624

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-134624)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-134624)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-134624)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-134624)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-134624)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-134624)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```