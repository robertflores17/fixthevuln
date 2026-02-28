---
name: audit-pages
description: Run the weekly educational page audit — checks for broken links, stale content, and outdated version references across all FixTheVuln pages
user_invocable: true
---

# Educational Page Audit

Run `scripts/audit_pages.py` to audit all educational pages on fixthevuln.com.

## What it checks
1. **Broken external links** — HTTP HEAD/GET to verify all outbound links
2. **Stale pages** — flags pages where "Last updated" date exceeds freshness threshold
3. **Version references** — finds exam codes, TLS versions, NIST SPs, and other references that may become outdated

## Commands

Full audit (includes link checking — takes a few minutes):
```bash
python3 scripts/audit_pages.py
```

Fast mode (skip link checking):
```bash
python3 scripts/audit_pages.py --skip-links
```

JSON output:
```bash
python3 scripts/audit_pages.py --skip-links --json
```

## After running
- Review the report output
- For broken links: fix or remove them from the affected pages
- For stale pages: update the content and bump the "Last updated" date
- For version references: verify they match current exam codes / standards
- The GitHub Actions workflow (`.github/workflows/audit-pages.yml`) runs this automatically every Monday at 8 AM Pacific
