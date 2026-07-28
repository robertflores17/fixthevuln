# Daily KEV Review — 2026-07-28

**CVEs to review:** 2

---

## CVE-2025-68686: Fortinet FortiOS

**CVSS:** 5.9
**Description:** Fortinet FortiOS contains an exposure of sensitive information to an unauthorized actor vulnerability. This may allow a remote unauthenticated attacker to bypass the patch developed for the symbolic link persistency mechanism observed in some post-exploit cases, via crafted HTTP requests. An attacker would need first to have compromised the product via another vulnerability, at filesystem level.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-08-10
**CISA Notes:** https://fortiguard.fortinet.com/psirt/FG-IR-25-934 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2025-68686

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-68686)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-68686)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-68686)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-68686)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-68686)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-68686)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-16812: Arista VeloCloud Orchestrator

**CVSS:** 10.0
**Description:** Arista VeloCloud Orchestrator On-Prem contains an OS command injection vulnerability that may allow a remote attacker to access privileged internal functionality and impact the VCO host. Successful exploitation may compromise the confidentiality, integrity, and availability of the orchestrator and data managed by the orchestrator.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-07-30
**CISA Notes:** https://www.arista.com/en/support/advisories-notices/security-advisory/24364-security-advisory-0144 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-16812

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-16812)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-16812)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-16812)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-16812)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-16812)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-16812)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```