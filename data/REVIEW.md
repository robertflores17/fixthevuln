# KEV Review - Week of 2026-01-16

**CVEs to review:** 4

---

## CVE-2026-20805: Microsoft Windows

**Description:** Microsoft Windows Desktop Windows Manager contains an information disclosure vulnerability that allows an authorized attacker to disclose information locally.
**Due Date:** 2026-02-03
**CISA Notes:** https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-20805 ; https://nvd.nist.gov/vuln/detail/CVE-2026-20805

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2026-20805)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2026-20805)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2026-20805)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2026-20805)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2026-20805)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2026-20805)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2026-20805",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2025-8110: Gogs Gogs

**Description:** Gogs contains a path traversal vulnerability affecting improper Symbolic link handling in the PutContents API that could allow for code execution.
**Due Date:** 2026-02-02
**CISA Notes:** https://github.com/gogs/gogs/commit/553707f3fd5f68f47f531cfcff56aa3ec294c6f6 ; https://nvd.nist.gov/vuln/detail/CVE-2025-8110

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-8110)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-8110)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-8110)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-8110)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-8110)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-8110)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2025-8110",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2009-0556: Microsoft Office

**Description:** Microsoft Office PowerPoint contains a code injection vulnerability that allows remote attackers to execute arbitrary code via a PowerPoint file with an OutlineTextRefAtom containing an invalid index value that triggers memory corruption.
**Due Date:** 2026-01-28
**CISA Notes:** https://learn.microsoft.com/en-us/security-updates/securitybulletins/2009/ms09-017 ; https://nvd.nist.gov/vuln/detail/CVE-2009-0556

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2009-0556)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2009-0556)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2009-0556)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2009-0556)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2009-0556)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2009-0556)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2009-0556",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## CVE-2025-37164: Hewlett Packard Enterprise (HPE) OneView

**Description:** Hewlett Packard Enterprise (HPE) OneView contains a code injection vulnerability that allows a remote unauthenticated user to perform remote code execution.
**Due Date:** 2026-01-28
**CISA Notes:** https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbgn04985en_us&docLocale=en_US ; https://nvd.nist.gov/vuln/detail/CVE-2025-37164

### Expert Reviews (click to check):
- [NVD - Official Details](https://nvd.nist.gov/vuln/detail/CVE-2025-37164)
- [AttackerKB - Exploitability Rating](https://attackerkb.com/topics/CVE-2025-37164)
- [BleepingComputer - News Coverage](https://www.bleepingcomputer.com/search/?q=CVE-2025-37164)
- [GreyNoise - Active Scanning](https://viz.greynoise.io/query?gnql=cve%3ACVE-2025-37164)
- [Rapid7 - Technical Analysis](https://www.rapid7.com/db/?q=CVE-2025-37164)
- [The Record - Threat Intel](https://therecord.media/?s=CVE-2025-37164)

### Your Review (fill in pending_review.json):
```json
"cveID": "CVE-2025-37164",
"cvss": "CVSS X.X",        // or "Zero-Day"
"short_description": "",   // Your 1-line summary
"fix": "",                 // Your remediation
"include_on_site": true
```

---

## Ready-to-Paste HTML

After filling in the fields above, run:
```bash
python scripts/generate_html.py
```

Or manually create cards in this format:
```html
<div class="kev-card">
    <h4>Vendor Product</h4>
    <div class="cve-id">CVE-XXXX-XXXXX | CVSS X.X</div>
    <p>Your short description.</p>
    <div class="kev-fix"><strong>Fix:</strong> Your remediation.</div>
</div>
```