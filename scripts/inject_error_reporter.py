#!/usr/bin/env python3
"""Inject error-reporter.js script tag into all HTML pages.

Usage:
    python scripts/inject_error_reporter.py          # dry run
    python scripts/inject_error_reporter.py --apply   # actually modify files
"""
import os
import sys
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ROOT should be the repo root (parent of scripts/)
SCRIPT_TAG = '<script src="/js/error-reporter.js"></script>'
# For store pages, use relative path since they're in /store/
STORE_SCRIPT_TAG = '<script src="/js/error-reporter.js"></script>'
SKIP_FILES = {'data/kev_cards.html'}

def main():
    apply = '--apply' in sys.argv
    modified = 0
    skipped = 0
    already = 0

    for dirpath, _, filenames in os.walk(ROOT):
        # Skip hidden dirs, .wrangler, .claude, node_modules
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir != '.' and any(part.startswith('.') for part in rel_dir.split(os.sep)):
            continue
        if 'node_modules' in rel_dir:
            continue

        for fname in filenames:
            if not fname.endswith('.html'):
                continue

            rel_path = os.path.relpath(os.path.join(dirpath, fname), ROOT)
            if rel_path in SKIP_FILES:
                skipped += 1
                continue

            filepath = os.path.join(dirpath, fname)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                skipped += 1
                continue

            if 'error-reporter.js' in content:
                already += 1
                continue

            if '</body>' not in content:
                skipped += 1
                continue

            # Insert script tag before </body>
            new_content = content.replace('</body>', f'  {SCRIPT_TAG}\n</body>', 1)

            if apply:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

            modified += 1
            if not apply:
                print(f'  Would modify: {rel_path}')

    print(f'\nResults: {modified} {"modified" if apply else "would modify"}, '
          f'{already} already have it, {skipped} skipped')

    if not apply and modified > 0:
        print('\nRun with --apply to make changes.')

if __name__ == '__main__':
    main()
