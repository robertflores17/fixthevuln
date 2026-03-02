#!/usr/bin/env python3
"""
Inject quiz practice links into guide/tool pages that don't have them.
Maps each page to 1-3 relevant quizzes based on content topic.

Usage:
    python3 scripts/inject_quiz_links.py           # Dry run
    python3 scripts/inject_quiz_links.py --apply    # Apply changes
"""

import sys
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRY_RUN = '--apply' not in sys.argv

# Mapping: page filename -> list of (quiz_file, quiz_label)
PAGE_QUIZ_MAP = {
    # Security guides
    'api-security.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('cysa-plus-quiz.html', 'CySA+ Practice Quiz'),
    ],
    'cloud-security.html': [
        ('aws-security-quiz.html', 'AWS Security Specialty Quiz'),
        ('az500-quiz.html', 'AZ-500 Practice Quiz'),
        ('cloud-plus-quiz.html', 'Cloud+ Practice Quiz'),
    ],
    'container-security.html': [
        ('cka-quiz.html', 'CKA Practice Quiz'),
        ('cks-quiz.html', 'CKS Practice Quiz'),
    ],
    'database-security.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('aws-dbs-quiz.html', 'AWS Database Specialty Quiz'),
    ],
    'encryption-cheatsheet.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('cissp-quiz.html', 'CISSP Practice Quiz'),
    ],
    'incident-response.html': [
        ('cysa-plus-quiz.html', 'CySA+ Practice Quiz'),
        ('gcih-quiz.html', 'GCIH Practice Quiz'),
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'linux-hardening.html': [
        ('linux-plus-quiz.html', 'Linux+ Practice Quiz'),
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'log-management.html': [
        ('cysa-plus-quiz.html', 'CySA+ Practice Quiz'),
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'osi-layer-attacks.html': [
        ('network-plus-quiz.html', 'Network+ Practice Quiz'),
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'password-policy.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('cissp-quiz.html', 'CISSP Practice Quiz'),
    ],
    'port-security.html': [
        ('network-plus-quiz.html', 'Network+ Practice Quiz'),
        ('ccna-quiz.html', 'CCNA Practice Quiz'),
    ],
    'secrets-management.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('vault-quiz.html', 'HashiCorp Vault Practice Quiz'),
    ],
    'security-headers.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('cysa-plus-quiz.html', 'CySA+ Practice Quiz'),
    ],
    'ssl-tls.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('network-plus-quiz.html', 'Network+ Practice Quiz'),
    ],
    'windows-hardening.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('cysa-plus-quiz.html', 'CySA+ Practice Quiz'),
    ],
    'wordpress-security.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('pentest-plus-quiz.html', 'PenTest+ Practice Quiz'),
    ],
    'xss-playground.html': [
        ('pentest-plus-quiz.html', 'PenTest+ Practice Quiz'),
        ('ceh-quiz.html', 'CEH Practice Quiz'),
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'sql-injection-simulator.html': [
        ('pentest-plus-quiz.html', 'PenTest+ Practice Quiz'),
        ('ceh-quiz.html', 'CEH Practice Quiz'),
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],

    # Compliance guides
    'cis-controls.html': [
        ('cissp-quiz.html', 'CISSP Practice Quiz'),
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'gdpr-guide.html': [
        ('cism-quiz.html', 'CISM Practice Quiz'),
        ('cissp-quiz.html', 'CISSP Practice Quiz'),
    ],
    'hipaa-guide.html': [
        ('cism-quiz.html', 'CISM Practice Quiz'),
        ('cissp-quiz.html', 'CISSP Practice Quiz'),
    ],
    'nist-framework.html': [
        ('cissp-quiz.html', 'CISSP Practice Quiz'),
        ('cism-quiz.html', 'CISM Practice Quiz'),
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'pci-dss.html': [
        ('cissp-quiz.html', 'CISSP Practice Quiz'),
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'soc2-basics.html': [
        ('cisa-quiz.html', 'CISA Practice Quiz'),
        ('cism-quiz.html', 'CISM Practice Quiz'),
    ],

    # Tools
    'base64-tool.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'certificate-decoder.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'cve-lookup.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('cysa-plus-quiz.html', 'CySA+ Practice Quiz'),
    ],
    'cvss-calculator.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
        ('cysa-plus-quiz.html', 'CySA+ Practice Quiz'),
    ],
    'hash-generator.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'jwt-decoder.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'password-generator.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'password-strength.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'regex-tester.html': [
        ('security-quiz.html', 'Security+ Practice Quiz'),
    ],
    'subnet-calculator.html': [
        ('network-plus-quiz.html', 'Network+ Practice Quiz'),
        ('ccna-quiz.html', 'CCNA Practice Quiz'),
    ],
}


def build_quiz_section(quizzes):
    """Build the HTML for the quiz link section."""
    links = []
    for quiz_file, label in quizzes:
        links.append(
            f'                <a href="{quiz_file}" style="padding: 0.75rem; '
            f'background: var(--bg-tertiary); border-radius: 6px; text-decoration: none; '
            f'color: var(--text-primary); border: 1px solid var(--border-color); '
            f'transition: border-color 0.2s;">{label}</a>'
        )
    links_html = '\n'.join(links)
    return f'''
            <!-- Quiz Links -->
            <section style="margin-top: 1.5rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 10px;">
                <h3 style="color: var(--text-primary); margin-bottom: 1rem;">Test Your Knowledge</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
{links_html}
                </div>
            </section>
'''


def inject(filepath, quizzes):
    """Inject quiz section into a page."""
    text = filepath.read_text(encoding='utf-8')

    # Already has quiz links?
    if '<!-- Quiz Links -->' in text:
        return False, 'already has quiz links'

    section_html = build_quiz_section(quizzes)

    # Strategy 1: Insert before <!-- Blog Cross-Links -->
    if '<!-- Blog Cross-Links -->' in text:
        text = text.replace(
            '<!-- Blog Cross-Links -->',
            section_html + '            <!-- Blog Cross-Links -->',
            1
        )
    # Strategy 2: Insert before back-link
    elif 'class="back-link"' in text:
        # Find the first back-link and insert before it
        import re
        match = re.search(r'(\n\s*<a href="[^"]*" class="back-link")', text)
        if match:
            text = text[:match.start()] + section_html + text[match.start():]
        else:
            return False, 'could not find insertion point'
    # Strategy 3: Insert before <!-- Store CTA -->
    elif '<!-- Store CTA -->' in text:
        text = text.replace(
            '<!-- Store CTA -->',
            section_html + '\n        <!-- Store CTA -->',
            1
        )
    else:
        return False, 'no insertion point found'

    if not DRY_RUN:
        filepath.write_text(text, encoding='utf-8')
    return True, 'injected'


def main():
    mode = 'DRY RUN' if DRY_RUN else 'APPLYING'
    print(f'Quiz Link Injection ({mode})')
    print('=' * 50)

    injected = 0
    skipped = 0
    errors = 0

    for page, quizzes in sorted(PAGE_QUIZ_MAP.items()):
        filepath = REPO_ROOT / page
        if not filepath.exists():
            print(f'  SKIP {page} — file not found')
            skipped += 1
            continue

        # Verify quiz files exist
        missing_quizzes = [q for q, _ in quizzes if not (REPO_ROOT / q).exists()]
        if missing_quizzes:
            print(f'  ERROR {page} — quiz files missing: {missing_quizzes}')
            errors += 1
            continue

        success, msg = inject(filepath, quizzes)
        if success:
            print(f'  OK {page} — {len(quizzes)} quiz links ({msg})')
            injected += 1
        else:
            print(f'  SKIP {page} — {msg}')
            skipped += 1

    print()
    print(f'Results: {injected} injected, {skipped} skipped, {errors} errors')
    if DRY_RUN and injected > 0:
        print(f'Run with --apply to write changes.')


if __name__ == '__main__':
    main()
