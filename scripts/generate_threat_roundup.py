#!/usr/bin/env python3
"""
Weekly Threat Roundup Generator for FixTheVuln.com
Auto-generates a blog post draft from CISA KEV data.

Usage:
    python3 scripts/generate_threat_roundup.py              # Generate roundup
    python3 scripts/generate_threat_roundup.py --dry-run    # Preview without writing
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parent.parent
    dry_run = '--dry-run' in sys.argv

    kev_path = repo_root / 'data' / 'kev-data.json'
    drafts_dir = repo_root / 'drafts'
    drafts_dir.mkdir(exist_ok=True)

    if not kev_path.exists():
        print('  No kev-data.json found, skipping threat roundup.')
        return

    kev_data = json.loads(kev_path.read_text(encoding='utf-8'))
    vulns = kev_data.get('vulnerabilities', [])

    if not vulns:
        print('  No vulnerabilities in kev-data.json, skipping.')
        return

    # Get date range for this week's roundup
    today = datetime.now()
    week_ago = today - timedelta(days=14)  # 14-day lookback to catch Saturday fetch
    today_str = today.strftime('%Y-%m-%d')
    week_start = week_ago.strftime('%Y-%m-%d')

    # Filter recent active vulns
    recent = []
    for v in vulns:
        if v.get('archived', False):
            continue
        date_added = v.get('dateAdded', '')
        if date_added >= week_start:
            recent.append(v)

    # If no recent vulns, use all active (non-archived) ones
    if not recent:
        recent = [v for v in vulns if not v.get('archived', False)]
        if not recent:
            print('  No active vulnerabilities for roundup.')
            return
        # Take the most recent 6
        recent = sorted(recent, key=lambda v: v.get('dateAdded', ''), reverse=True)[:6]

    # Sort by CVSS descending
    recent.sort(key=lambda v: float(v.get('cvss', 0)), reverse=True)

    # Generate slug and check if already exists
    slug = f"weekly-threat-roundup-{today.strftime('%Y-%m-%d')}"
    draft_path = drafts_dir / f"{slug}.md"

    # Check if already generated this week
    if draft_path.exists() or (drafts_dir / f"{slug}.md.published").exists():
        print(f'  Roundup for {today_str} already exists, skipping.')
        return

    # Stats
    count = len(recent)
    highest_cvss = max(float(v.get('cvss', 0)) for v in recent)
    zero_days = [v for v in recent if v.get('isZeroDay', False)]
    critical = [v for v in recent if float(v.get('cvss', 0)) >= 9.0]
    high = [v for v in recent if 7.0 <= float(v.get('cvss', 0)) < 9.0]

    # Date formatting
    week_start_display = week_ago.strftime('%b %d')
    week_end_display = today.strftime('%b %d, %Y')
    month_year = today.strftime('%B %Y')

    # Build severity summary
    if critical:
        severity_msg = f"This week includes **{len(critical)} critical-severity** vulnerabilities (CVSS 9.0+) that require immediate attention."
    elif high:
        severity_msg = f"This week includes **{len(high)} high-severity** vulnerabilities (CVSS 7.0+). Review your exposure and prioritize patching."
    else:
        severity_msg = "No critical-severity vulnerabilities this week, but stay vigilant — patch what you can."

    # Build the vulnerability list
    vuln_entries = []
    for v in recent:
        cvss = float(v.get('cvss', 0))
        if cvss >= 9.0:
            severity_label = "CRITICAL"
        elif cvss >= 7.0:
            severity_label = "HIGH"
        elif cvss >= 4.0:
            severity_label = "MEDIUM"
        else:
            severity_label = "LOW"

        zero_day_tag = " (Zero-Day)" if v.get('isZeroDay', False) else ""
        entry = f"""### {v['id']} — {v.get('title', 'Unknown')}{zero_day_tag}

- **CVSS Score**: {v.get('cvss', 'N/A')} ({severity_label})
- **Date Added**: {v.get('dateAdded', 'Unknown')}
- **Description**: {v.get('description', 'No description available.')}
- **Required Action**: {v.get('fix', 'Apply vendor patches and mitigations.')}"""
        vuln_entries.append(entry)

    vuln_list = '\n\n'.join(vuln_entries)

    # What this means section
    if highest_cvss >= 9.0:
        action_msg = """If you run any of the affected products, **patch immediately**. Critical-severity vulnerabilities are actively exploited in the wild — CISA adds them to the KEV catalog specifically because they represent real, current threats.

Use the [CVSS Calculator](/cvss-calculator.html) to assess how these scores apply to your specific environment."""
    elif highest_cvss >= 7.0:
        action_msg = """These are serious vulnerabilities that warrant prompt attention. Check if your organization uses any affected products and prioritize patching within your maintenance windows.

Use the [CVSS Calculator](/cvss-calculator.html) to contextualize these scores for your environment."""
    else:
        action_msg = """While none of this week's additions are critical severity, they're in the KEV catalog because they've been exploited. Don't deprioritize them — schedule patches in your next maintenance window."""

    # Studying section based on count
    if count >= 4:
        study_angle = f"""This week's {count} new KEV entries touch multiple attack surfaces — from authentication bypasses to command injection. If you're studying for Security+, this is a live case study in **Domain 2: Threats, Vulnerabilities, and Mitigations** (22% of the exam).

Map each CVE to a vulnerability type from the SY0-701 objectives. That's how you build real exam intuition."""
    else:
        study_angle = f"""Even with just {count} new entries, each one maps to real Security+ exam objectives. Practice identifying the vulnerability type (injection, authentication bypass, deserialization) — that's **Domain 2** material."""

    # Assemble the full draft
    markdown = f"""---
title: "This Week in Threats: {week_start_display}–{week_end_display}"
description: "{count} new CISA KEV vulnerabilities this week. Highest CVSS: {highest_cvss}. Review the latest threats added to the Known Exploited Vulnerabilities catalog."
keywords: "CISA KEV, weekly threat roundup, vulnerability management, cybersecurity threats, {month_year}"
date: "{today_str}"
slug: "{slug}"
author: "FixTheVuln Team"
sources: "CISA Known Exploited Vulnerabilities Catalog, NVD"
cta_section: "comptia"
---

## Weekly Threat Summary

**{count} vulnerabilities** were added to the CISA Known Exploited Vulnerabilities (KEV) catalog this period. The highest CVSS score is **{highest_cvss}**.{' ' + str(len(zero_days)) + ' zero-day(s) identified.' if zero_days else ''}

{severity_msg}

## This Week's Vulnerabilities

{vuln_list}

## What This Means for You

{action_msg}

## Security+ Study Angle

{study_angle}

## Tools to Help

- [CVSS Calculator](/cvss-calculator.html) — Score these vulnerabilities for your specific environment
- [Security+ Practice Quiz](/security-quiz.html) — Test your knowledge of vulnerability types and mitigations

## Stay Updated

This roundup is published every Tuesday. Bookmark the [FixTheVuln Blog](/blog/) to stay on top of the latest threats — or subscribe via [RSS](/blog/feed.xml).
"""

    if dry_run:
        print(f'  DRY-RUN would write {draft_path.relative_to(repo_root)}')
        print(f'  Title: This Week in Threats: {week_start_display}–{week_end_display}')
        print(f'  CVEs: {count}, Highest CVSS: {highest_cvss}')
    else:
        draft_path.write_text(markdown, encoding='utf-8')
        print(f'  GENERATED {draft_path.relative_to(repo_root)}')
        print(f'  Title: This Week in Threats: {week_start_display}–{week_end_display}')
        print(f'  CVEs: {count}, Highest CVSS: {highest_cvss}')


if __name__ == '__main__':
    main()
