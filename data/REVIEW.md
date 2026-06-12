# Daily KEV Review — 2026-06-12

**CVEs to review:** 2

---

## [RANSOMWARE] CVE-2026-35273: Oracle  PeopleSoft Enterprise PeopleTools

**CVSS:** 
**Description:** Oracle PeopleSoft Enterprise PeopleTools contains a missing authentication for critical function vulnerability which could allow an unauthenticated attacker to obtain takeover of PeopleSoft Enterprise PeopleTools.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-06-15
**CISA Notes:** https://www.oracle.com/security-alerts/alert-cve-2026-35273.html ; https://support.oracle.com/signin/ ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-35273

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-35273)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-35273)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-35273)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-35273)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-35273)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-35273)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-10520: Ivanti Sentry

**CVSS:** 
**Description:** Ivanti Sentry (formerly known as MobileIron Sentry) contains an OS command injection vulnerability which could allow a remote unauthenticated user to achieve root-level remote code execution. This vulnerability can be successfully exploited in cases where the Sentry appliance is in an unmanaged state with its endpoints externally reachable. The use of mTLS with EPMM or restricted HTTPS access through Neurons for MDM makes interfaces inaccessible to external actors.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-06-14
**CISA Notes:** https://hub.ivanti.com/s/article/Security-Advisory-Ivanti-Sentry-CVE-2026-10520-CVE-2026-10523?language=en_US ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-10520

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-10520)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-10520)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-10520)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-10520)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-10520)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-10520)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```