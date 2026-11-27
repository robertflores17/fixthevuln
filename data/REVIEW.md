# Daily KEV Review — 2026-11-27

**CVEs to review:** 3

---

## CVE-2026-120705: OSGeo GeoServer

**CVSS:** 
**Description:** OsGeo GeoServer contains an XML injection vulnerability that allows an unauthenticated remote attacker to cause the server to read local text files accessible to the GeoServer process or fetch attacker-specified HTTP or HTTPS URLs via a crafted ID parameter in the WFS 2.0 GetFeatureById stored query. This vulnerability can be chained with CVE-2026-129244, CVE-2026-129243, CVE-2026-129245, and CVE-2026-129242 to achieve unauthenticated remote code execution on an affected GeoServer instance.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-30
**CISA Notes:** https://geoserver.org/vulnerability/2026/11/23/cve-update.html ; https://github.com/geoserver/geoserver/security/advisories/GHSA-39mw-5chv-jh47 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-120705

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-120705)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-120705)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-120705)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-120705)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-120705)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-120705)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-129243: OSGeo GeoServer

**CVSS:** 
**Description:** GeoServer contains an incorrect authorization vulnerability that allows an unauthenticated remote attacker to bypass service-level role checks and invoke operations protected solely by those checks via a request with a prefixed service parameter. This vulnerability can be chained with CVE-2026-129244, CVE-2026-120705, CVE-2026-129245, and CVE-2026-129242 to achieve unauthenticated remote code execution on an affected GeoServer instance.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-30
**CISA Notes:** https://geoserver.org/vulnerability/2026/11/23/cve-update.html ; https://github.com/geoserver/geoserver/security/advisories/GHSA-rv5g-g2r9-58rj ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-129243

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-129243)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-129243)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-129243)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-129243)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-129243)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-129243)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## CVE-2026-136716: Drupal Core

**CVSS:** 9.8
**Description:** Drupal Core contains an improper check for unusual or exceptional conditions vulnerability that allows an unauthenticated remote attacker to take over a site via the exposed Drupal installer when the site is in one of the affected unusual or incomplete installation states.
**Fix:** Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
**Due Date:** 2026-11-30
**CISA Notes:** https://www.drupal.org/sa-core-2026-019 ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-136716

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-136716)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-136716)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-136716)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-136716)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-136716)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-136716)

### Your Review:
Fields are auto-filled. Edit in pending_review.json if needed,
then set `include_on_site` to `true`.

---

## Publish to Site

After setting `include_on_site: true`, run:
```bash
python scripts/generate_html.py
```