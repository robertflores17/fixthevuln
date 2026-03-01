#!/usr/bin/env python3
"""Inject data-product-id and data-cert-name attributes into quiz pages
so quiz-engine.js can render planner CTAs after quiz completion."""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

QUIZ_MAP = {
    'security-quiz.html':      ('comptia-security-plus',   'CompTIA Security+'),
    'aplus-quiz.html':         ('comptia-a-plus-1201',     'CompTIA A+ Core 1'),
    'network-plus-quiz.html':  ('comptia-network-plus',    'CompTIA Network+'),
    'linux-plus-quiz.html':    ('comptia-linux-plus',      'CompTIA Linux+'),
    'cysa-plus-quiz.html':     ('comptia-cysa-plus',       'CompTIA CySA+'),
    'pentest-plus-quiz.html':  ('comptia-pentest-plus',    'CompTIA PenTest+'),
    'casp-plus-quiz.html':     ('comptia-casp-plus',       'CompTIA CASP+'),
    'cissp-quiz.html':         ('isc2-cissp',              'ISC2 CISSP'),
    'ccna-quiz.html':          ('cisco-ccna',              'Cisco CCNA'),
    'ccnp-quiz.html':          ('cisco-ccnp-encor',        'Cisco CCNP ENCOR'),
    'ceh-quiz.html':           ('ec-ceh',                  'EC-Council CEH'),
    'cism-quiz.html':          ('isaca-cism',              'ISACA CISM'),
    'oscp-quiz.html':          ('offsec-oscp',             'OffSec OSCP'),
    'aws-clf-quiz.html':       ('aws-cloud-practitioner',  'AWS Cloud Practitioner'),
    'aws-saa-quiz.html':       ('aws-solutions-architect', 'AWS Solutions Architect'),
    'aws-security-quiz.html':  ('aws-security-specialty',  'AWS Security Specialty'),
    'az900-quiz.html':         ('ms-az-900',               'Microsoft Azure Fundamentals'),
    'sc900-quiz.html':         ('ms-sc-900',               'Microsoft Security Fundamentals'),
    # cpts-quiz.html has no matching planner — skip
}

def inject_attributes(filepath, product_id, cert_name):
    text = filepath.read_text(encoding='utf-8')

    # Check if already injected
    if 'data-product-id' in text:
        print(f"  SKIP {filepath.name} — already has data-product-id")
        return False

    # Find quiz-container div and add attributes
    pattern = r'(<div\s+class="quiz-container"\s+id="quiz-container")'
    replacement = rf'\1 data-product-id="{product_id}" data-cert-name="{cert_name}"'
    new_text, count = re.subn(pattern, replacement, text, count=1)

    if count == 0:
        print(f"  WARN {filepath.name} — could not find quiz-container div")
        return False

    filepath.write_text(new_text, encoding='utf-8')
    print(f"  OK   {filepath.name} → {product_id}")
    return True

def main():
    print("Injecting quiz planner CTA attributes...\n")
    injected = 0
    skipped = 0
    for filename, (product_id, cert_name) in QUIZ_MAP.items():
        filepath = REPO / filename
        if not filepath.exists():
            print(f"  MISS {filename} — file not found")
            continue
        if inject_attributes(filepath, product_id, cert_name):
            injected += 1
        else:
            skipped += 1

    print(f"\nDone: {injected} injected, {skipped} skipped")

if __name__ == '__main__':
    main()
