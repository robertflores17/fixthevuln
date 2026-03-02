#!/usr/bin/env python3
"""Inject SEO question blocks + FAQPage schema into hand-crafted quiz pages.

Reads each quiz's JSON data file, picks 10 diverse questions, and injects:
1. A <div class="seo-questions" id="seoQuestions"> block after #question-container
2. FAQPage schema in <head>
3. hasPart array added to existing Quiz schema

Also bumps quiz.css cache-bust to ?v=3.
"""

import json
import re
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Hand-crafted quiz pages: (html_file, json_data_file, display_name, exam_code)
HAND_CRAFTED = [
    ('security-quiz.html',      'data/security-plus-questions.json',   'CompTIA Security+',            'SY0-701'),
    ('aplus-quiz.html',         'data/aplus-questions.json',           'CompTIA A+ Core 1',            '220-1101'),
    ('network-plus-quiz.html',  'data/network-plus-questions.json',    'CompTIA Network+',             'N10-009'),
    ('linux-plus-quiz.html',    'data/linux-plus-questions.json',      'CompTIA Linux+',               'XK0-005'),
    ('cysa-plus-quiz.html',     'data/cysa-plus-questions.json',       'CompTIA CySA+',                'CS0-003'),
    ('pentest-plus-quiz.html',  'data/pentest-plus-questions.json',    'CompTIA PenTest+',             'PT0-002'),
    ('casp-plus-quiz.html',     'data/casp-plus-questions.json',       'CompTIA CASP+',                'CAS-004'),
    ('cissp-quiz.html',         'data/cissp-questions.json',           'ISC2 CISSP',                   'CISSP'),
    ('ccna-quiz.html',          'data/ccna-questions.json',            'Cisco CCNA',                   '200-301'),
    ('ccnp-quiz.html',          'data/ccnp-questions.json',            'Cisco CCNP ENCOR',             '350-401'),
    ('ceh-quiz.html',           'data/ceh-questions.json',             'EC-Council CEH',               'CEH'),
    ('cism-quiz.html',          'data/cism-questions.json',            'ISACA CISM',                   'CISM'),
    ('oscp-quiz.html',          'data/oscp-questions.json',            'OffSec OSCP',                  'OSCP'),
    ('aws-clf-quiz.html',       'data/aws-clf-questions.json',         'AWS Cloud Practitioner',       'CLF-C02'),
    ('aws-saa-quiz.html',       'data/aws-saa-questions.json',         'AWS Solutions Architect',      'SAA-C03'),
    ('aws-security-quiz.html',  'data/aws-security-questions.json',    'AWS Security Specialty',       'SCS-C02'),
    ('az900-quiz.html',         'data/az900-questions.json',           'Microsoft AZ-900',             'AZ-900'),
    ('sc900-quiz.html',         'data/sc900-questions.json',           'Microsoft SC-900',             'SC-900'),
    ('cpts-quiz.html',          'data/cpts-questions.json',            'HTB CPTS',                     'CPTS'),
]


def pick_seo_questions(questions, count=10):
    """Pick a diverse sample — one per domain first, then fill."""
    by_domain = {}
    for q in questions:
        d = str(q.get('domain', 1))
        if d not in by_domain:
            by_domain[d] = []
        by_domain[d].append(q)
    selected = []
    for dk in sorted(by_domain.keys(), key=lambda x: int(x) if x.isdigit() else 999):
        if by_domain[dk]:
            selected.append(by_domain[dk][0])
    picked_ids = {q['id'] for q in selected}
    for q in questions:
        if len(selected) >= count:
            break
        if q['id'] not in picked_ids:
            selected.append(q)
            picked_ids.add(q['id'])
    return selected[:count]


def build_seo_html(seo_qs, name, exam):
    """Build the static HTML block with sample Q&As."""
    items = []
    for q in seo_qs:
        correct_idx = q.get('correct', 0)
        options = q.get('options', [])
        answer = options[correct_idx] if correct_idx < len(options) else 'See explanation'
        explanation = q.get('explanation', '')
        items.append(
            f'        <details>\n'
            f'            <summary>Q: {escape(q["question"])}</summary>\n'
            f'            <p><strong>A: {escape(answer)}</strong> &mdash; {escape(explanation)}</p>\n'
            f'        </details>'
        )
    return (
        f'    <div class="seo-questions" id="seoQuestions">\n'
        f'        <h3>Sample {escape(name)} {escape(exam)} Practice Questions</h3>\n'
        + '\n'.join(items) + '\n'
        f'    </div>'
    )


def build_faq_schema(seo_qs):
    """Build FAQPage schema JSON string."""
    entities = []
    for q in seo_qs:
        correct_idx = q.get('correct', 0)
        options = q.get('options', [])
        answer = options[correct_idx] if correct_idx < len(options) else 'See explanation'
        explanation = q.get('explanation', '')
        entities.append({
            "@type": "Question",
            "name": q['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"{answer}. {explanation}"
            }
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }, indent=4, ensure_ascii=False)


def build_quiz_haspart(seo_qs):
    """Build hasPart array for Quiz schema."""
    parts = []
    for q in seo_qs:
        correct_idx = q.get('correct', 0)
        options = q.get('options', [])
        suggested = []
        for i, opt in enumerate(options):
            suggested.append({
                "@type": "Answer",
                "text": opt,
                "encodingFormat": "text/plain",
                "comment": {"@type": "Comment", "text": "Correct" if i == correct_idx else "Incorrect"}
            })
        parts.append({
            "@type": "Question",
            "eduQuestionType": "Multiple choice",
            "text": q['question'],
            "suggestedAnswer": [s for s in suggested if s["comment"]["text"] == "Incorrect"],
            "acceptedAnswer": suggested[correct_idx] if correct_idx < len(suggested) else suggested[0]
        })
    return parts


def inject_page(html_file, json_file, name, exam):
    """Inject SEO content into a single hand-crafted quiz page."""
    html_path = REPO / html_file
    json_path = REPO / json_file

    if not html_path.exists():
        print(f"  SKIP {html_file} — file not found")
        return False
    if not json_path.exists():
        print(f"  SKIP {html_file} — {json_file} not found")
        return False

    # Load questions
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    questions = data.get('questions', [])
    if len(questions) < 5:
        print(f"  SKIP {html_file} — too few questions ({len(questions)})")
        return False

    html = html_path.read_text(encoding='utf-8')

    # Skip if already injected
    if 'id="seoQuestions"' in html:
        print(f"  ALREADY {html_file}")
        return False

    seo_qs = pick_seo_questions(questions)
    seo_html = build_seo_html(seo_qs, name, exam)
    faq_schema = build_faq_schema(seo_qs)
    has_part = build_quiz_haspart(seo_qs)

    # 1. Inject SEO block after #question-container (handle both self-closing and multi-line)
    marker = '<div id="question-container"></div>'
    if marker in html:
        html = html.replace(marker, marker + '\n' + seo_html, 1)
    else:
        # Multi-line variant: <div id="question-container">\n...\n</div>
        mc_pattern = r'(<div id="question-container">.*?</div>)'
        mc_match = re.search(mc_pattern, html, re.DOTALL)
        if mc_match:
            html = html[:mc_match.end()] + '\n' + seo_html + html[mc_match.end():]
        else:
            print(f"  WARN {html_file} — question-container not found")
            return False

    # 2. Inject FAQPage schema before </head>
    faq_tag = f'    <script type="application/ld+json">\n{faq_schema}\n</script>\n'
    html = html.replace('</head>', faq_tag + '</head>', 1)

    # 3. Add hasPart to existing Quiz schema
    quiz_pattern = r'("@type":\s*"Quiz"[^}]*"assesses":\s*\[[^\]]*\])'
    match = re.search(quiz_pattern, html, re.DOTALL)
    if match:
        has_part_json = json.dumps(has_part, indent=4, ensure_ascii=False)
        replacement = match.group(1) + ',\n    "hasPart": ' + has_part_json
        html = html[:match.start()] + replacement + html[match.end():]

    # 4. Bump quiz.css to ?v=3
    html = re.sub(r'quiz\.css\?v=\d+', 'quiz.css?v=3', html)

    html_path.write_text(html, encoding='utf-8')
    print(f"  OK   {html_file} ({len(seo_qs)} SEO questions injected)")
    return True


def main():
    injected = 0
    for html_file, json_file, name, exam in HAND_CRAFTED:
        if inject_page(html_file, json_file, name, exam):
            injected += 1
    print(f"\nDone: {injected}/{len(HAND_CRAFTED)} hand-crafted quizzes updated")


if __name__ == '__main__':
    main()
