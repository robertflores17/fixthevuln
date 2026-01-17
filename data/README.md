# Vulnerability Data

This folder contains vulnerability data fetched from CISA's Known Exploited Vulnerabilities (KEV) catalog.

## Files

| File | Purpose |
|------|---------|
| `kev.json` | Full CISA KEV catalog (auto-fetched, reference only) |
| `pending_review.json` | New CVEs awaiting your review |
| `reviewed_kev.json` | CVEs you've already reviewed |
| `REVIEW_SUMMARY.md` | Auto-generated summary of new entries |

## Review Workflow

1. **GitHub Action runs daily** - Fetches latest KEV data
2. **PR is created/updated** - With new vulnerabilities
3. **Friday reminder** - Issue created to remind you
4. **Weekend review** - You review pending items

## How to Review

Edit `pending_review.json` for each vulnerability:

```json
{
  "cveID": "CVE-2024-XXXXX",
  "reviewed": true,           // Mark as reviewed
  "include_on_site": true,    // Set to true to publish
  "custom_remediation": "...", // Your remediation text
  "priority": "high"          // high, medium, or low
}
```

After reviewing, move the entry to `reviewed_kev.json` to prevent it from appearing again.

## Updating the Site

After merging the PR, the reviewed vulnerabilities need to be manually added to `index.html` in the KEV section. Future enhancement: auto-generate this section from the JSON data.
