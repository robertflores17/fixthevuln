#!/usr/bin/env python3
"""Generate quiz HTML pages + question JSON files for all certifications
that don't already have a quiz. Reads domain data from cert config JSONs
to build domain-weighted questions."""

import json
import random
import sys
from pathlib import Path
from html import escape
from datetime import date

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.templates import (html_head, nav, share_bar, footer, cf_analytics, breadcrumb_schema, esc)
from lib.constants import SITE_URL, QUIZ_CSS_VERSION
ETSY_CERTS = Path(__file__).resolve().parent.parent.parent / 'Dropshipping' / 'Etsy-Claude' / 'certifications'
DATA_DIR = REPO / 'data'

TODAY = date.today().strftime('%B %d, %Y')

# ── Certs that ALREADY have quiz pages (don't regenerate) ──────────
EXISTING_QUIZZES = {
    'comptia-security-plus', 'comptia-a-plus-1201', 'comptia-network-plus',
    'comptia-linux-plus', 'comptia-cysa-plus', 'comptia-pentest-plus',
    'comptia-casp-plus', 'isc2-cissp', 'cisco-ccna', 'cisco-ccnp-encor',
    'ec-ceh', 'isaca-cism', 'offsec-oscp', 'aws-cloud-practitioner',
    'aws-solutions-architect', 'aws-security-specialty', 'ms-az-900',
    'ms-sc-900',
}

# ── All 65 certs with quiz config ──────────────────────────────────
# slug: quiz HTML filename, JSON data filename, display name, exam code, config path, vendor
QUIZ_CONFIGS = [
    # CompTIA (5 remaining)
    {'id': 'comptia-a-plus-1202',   'quiz': 'aplus2-quiz.html',          'json': 'aplus2-questions.json',              'name': 'CompTIA A+ Core 2',            'exam': '220-1202', 'config': 'comptia/a_plus_1202.json',                'vendor': 'CompTIA'},
    {'id': 'comptia-cloud-plus',    'quiz': 'cloud-plus-quiz.html',      'json': 'cloud-plus-questions.json',          'name': 'CompTIA Cloud+',               'exam': 'CV0-004',  'config': 'comptia/cloud_plus_004.json',             'vendor': 'CompTIA'},
    {'id': 'comptia-server-plus',   'quiz': 'server-plus-quiz.html',     'json': 'server-plus-questions.json',         'name': 'CompTIA Server+',              'exam': 'SK0-005',  'config': 'comptia/server_plus_005.json',            'vendor': 'CompTIA'},
    {'id': 'comptia-data-plus',     'quiz': 'data-plus-quiz.html',       'json': 'data-plus-questions.json',           'name': 'CompTIA Data+',                'exam': 'DA0-001',  'config': 'comptia/data_plus_001.json',              'vendor': 'CompTIA'},
    {'id': 'comptia-project-plus',  'quiz': 'project-plus-quiz.html',    'json': 'project-plus-questions.json',        'name': 'CompTIA Project+',             'exam': 'PK0-005',  'config': 'comptia/project_plus_005.json',           'vendor': 'CompTIA'},
    {'id': 'comptia-itf-plus',      'quiz': 'itf-plus-quiz.html',        'json': 'itf-plus-questions.json',            'name': 'CompTIA ITF+',                 'exam': 'FC0-U71',  'config': 'comptia/itf_plus_u71.json',               'vendor': 'CompTIA'},
    {'id': 'comptia-secai-plus',    'quiz': 'secai-quiz.html',           'json': 'secai-questions.json',               'name': 'CompTIA SecAI+',               'exam': 'CY0-001',  'config': 'comptia/secai_plus_001.json',             'vendor': 'CompTIA'},
    # ISC2 (3 remaining)
    {'id': 'isc2-cc',               'quiz': 'isc2-cc-quiz.html',         'json': 'isc2-cc-questions.json',             'name': 'ISC2 CC',                      'exam': 'CC',       'config': 'isc2/cc.json',                            'vendor': 'ISC2'},
    {'id': 'isc2-sscp',             'quiz': 'isc2-sscp-quiz.html',       'json': 'isc2-sscp-questions.json',           'name': 'ISC2 SSCP',                    'exam': 'SSCP',     'config': 'isc2/sscp.json',                          'vendor': 'ISC2'},
    {'id': 'isc2-ccsp',             'quiz': 'isc2-ccsp-quiz.html',       'json': 'isc2-ccsp-questions.json',           'name': 'ISC2 CCSP',                    'exam': 'CCSP',     'config': 'isc2/ccsp.json',                          'vendor': 'ISC2'},
    # AWS (5 remaining)
    {'id': 'aws-developer',         'quiz': 'aws-dva-quiz.html',         'json': 'aws-dva-questions.json',             'name': 'AWS Developer Associate',      'exam': 'DVA-C02',  'config': 'aws/developer_dva-c02.json',              'vendor': 'AWS'},
    {'id': 'aws-cloudops',          'quiz': 'aws-soa-quiz.html',         'json': 'aws-soa-questions.json',             'name': 'AWS CloudOps Engineer',        'exam': 'SOA-C03',  'config': 'aws/cloudops_engineer_soa-c03.json',      'vendor': 'AWS'},
    {'id': 'aws-database-specialty','quiz': 'aws-dbs-quiz.html',         'json': 'aws-dbs-questions.json',             'name': 'AWS Database Specialty',       'exam': 'DBS-C01',  'config': 'aws/database_specialty_dbs-c01.json',     'vendor': 'AWS'},
    {'id': 'aws-machine-learning',  'quiz': 'aws-mls-quiz.html',         'json': 'aws-mls-questions.json',             'name': 'AWS Machine Learning',         'exam': 'MLS-C01',  'config': 'aws/machine_learning_mls-c01.json',       'vendor': 'AWS'},
    {'id': 'aws-data-engineer',     'quiz': 'aws-dea-quiz.html',         'json': 'aws-dea-questions.json',             'name': 'AWS Data Engineer',            'exam': 'DEA-C01',  'config': 'aws/data_engineer_dea-c01.json',          'vendor': 'AWS'},
    # Microsoft (10 remaining)
    {'id': 'ms-az-104',             'quiz': 'az104-quiz.html',           'json': 'az104-questions.json',               'name': 'Azure Administrator',          'exam': 'AZ-104',   'config': 'microsoft/az-104.json',                   'vendor': 'Microsoft'},
    {'id': 'ms-az-305',             'quiz': 'az305-quiz.html',           'json': 'az305-questions.json',               'name': 'Azure Solutions Architect',     'exam': 'AZ-305',   'config': 'microsoft/az-305.json',                   'vendor': 'Microsoft'},
    {'id': 'ms-ai-900',             'quiz': 'ai900-quiz.html',           'json': 'ai900-questions.json',               'name': 'Azure AI Fundamentals',        'exam': 'AI-900',   'config': 'microsoft/ai-900.json',                   'vendor': 'Microsoft'},
    {'id': 'ms-az-500',             'quiz': 'az500-quiz.html',           'json': 'az500-questions.json',               'name': 'Azure Security Engineer',      'exam': 'AZ-500',   'config': 'microsoft/az-500.json',                   'vendor': 'Microsoft'},
    {'id': 'ms-az-204',             'quiz': 'az204-quiz.html',           'json': 'az204-questions.json',               'name': 'Azure Developer Associate',    'exam': 'AZ-204',   'config': 'microsoft/az-204.json',                   'vendor': 'Microsoft'},
    {'id': 'ms-az-400',             'quiz': 'az400-quiz.html',           'json': 'az400-questions.json',               'name': 'Azure DevOps Engineer',        'exam': 'AZ-400',   'config': 'microsoft/az-400.json',                   'vendor': 'Microsoft'},
    {'id': 'ms-dp-900',             'quiz': 'dp900-quiz.html',           'json': 'dp900-questions.json',               'name': 'Azure Data Fundamentals',      'exam': 'DP-900',   'config': 'microsoft/dp-900.json',                   'vendor': 'Microsoft'},
    {'id': 'ms-ms-900',             'quiz': 'ms900-quiz.html',           'json': 'ms900-questions.json',               'name': 'Microsoft 365 Fundamentals',   'exam': 'MS-900',   'config': 'microsoft/ms-900.json',                   'vendor': 'Microsoft'},
    {'id': 'ms-sc-300',             'quiz': 'sc300-quiz.html',           'json': 'sc300-questions.json',               'name': 'Identity & Access Admin',      'exam': 'SC-300',   'config': 'microsoft/sc-300.json',                   'vendor': 'Microsoft'},
    {'id': 'ms-ai-102',             'quiz': 'ai102-quiz.html',           'json': 'ai102-questions.json',               'name': 'Azure AI Engineer',            'exam': 'AI-102',   'config': 'microsoft/ai-102.json',                   'vendor': 'Microsoft'},
    # Cisco (3 remaining)
    {'id': 'cisco-cyberops',        'quiz': 'cyberops-quiz.html',        'json': 'cyberops-questions.json',            'name': 'Cisco CyberOps Associate',     'exam': '200-201',  'config': 'cisco/cyberops_200-201.json',             'vendor': 'Cisco'},
    {'id': 'cisco-ccnp-security',   'quiz': 'ccnp-security-quiz.html',  'json': 'ccnp-security-questions.json',       'name': 'Cisco CCNP Security SCOR',     'exam': '350-701',  'config': 'cisco/ccnp_security_scor_350-701.json',   'vendor': 'Cisco'},
    {'id': 'cisco-devnet',          'quiz': 'devnet-quiz.html',          'json': 'devnet-questions.json',              'name': 'Cisco DevNet Associate',       'exam': '200-901',  'config': 'cisco/devnet_associate_200-901.json',     'vendor': 'Cisco'},
    # ISACA (2 remaining)
    {'id': 'isaca-cisa',            'quiz': 'cisa-quiz.html',            'json': 'cisa-questions.json',                'name': 'ISACA CISA',                   'exam': 'CISA',     'config': 'isaca/cisa.json',                         'vendor': 'ISACA'},
    {'id': 'isaca-crisc',           'quiz': 'crisc-quiz.html',           'json': 'crisc-questions.json',               'name': 'ISACA CRISC',                  'exam': 'CRISC',    'config': 'isaca/crisc.json',                        'vendor': 'ISACA'},
    # GIAC (4)
    {'id': 'giac-gsec',             'quiz': 'gsec-quiz.html',            'json': 'gsec-questions.json',                'name': 'GIAC GSEC',                    'exam': 'GSEC',     'config': 'giac/giac_gsec.json',                     'vendor': 'GIAC'},
    {'id': 'giac-gcih',             'quiz': 'gcih-quiz.html',            'json': 'gcih-questions.json',                'name': 'GIAC GCIH',                    'exam': 'GCIH',     'config': 'giac/giac_gcih.json',                     'vendor': 'GIAC'},
    {'id': 'giac-gpen',             'quiz': 'gpen-quiz.html',            'json': 'gpen-questions.json',                'name': 'GIAC GPEN',                    'exam': 'GPEN',     'config': 'giac/giac_gpen.json',                     'vendor': 'GIAC'},
    {'id': 'giac-gcia',             'quiz': 'gcia-quiz.html',            'json': 'gcia-questions.json',                'name': 'GIAC GCIA',                    'exam': 'GCIA',     'config': 'giac/giac_gcia.json',                     'vendor': 'GIAC'},
    # Google Cloud (5)
    {'id': 'google-ace',            'quiz': 'gcp-ace-quiz.html',         'json': 'gcp-ace-questions.json',             'name': 'Google Associate Cloud Engineer','exam': 'ACE',    'config': 'google/associate_cloud_engineer.json',    'vendor': 'Google Cloud'},
    {'id': 'google-pca',            'quiz': 'gcp-pca-quiz.html',         'json': 'gcp-pca-questions.json',             'name': 'Google Professional Cloud Architect','exam': 'PCA','config': 'google/professional_cloud_architect.json','vendor': 'Google Cloud'},
    {'id': 'google-cdl',            'quiz': 'gcp-cdl-quiz.html',         'json': 'gcp-cdl-questions.json',             'name': 'Google Cloud Digital Leader',  'exam': 'CDL',      'config': 'google/cloud_digital_leader.json',        'vendor': 'Google Cloud'},
    {'id': 'google-pde',            'quiz': 'gcp-pde-quiz.html',         'json': 'gcp-pde-questions.json',             'name': 'Google Professional Data Engineer','exam': 'PDE',  'config': 'google/professional_data_engineer.json',  'vendor': 'Google Cloud'},
    {'id': 'google-pse',            'quiz': 'gcp-pse-quiz.html',         'json': 'gcp-pse-questions.json',             'name': 'Google Cloud Security Engineer','exam': 'PSE',     'config': 'google/professional_security_engineer.json','vendor': 'Google Cloud'},
    # EC-Council (2 remaining)
    {'id': 'ec-chfi',               'quiz': 'chfi-quiz.html',            'json': 'chfi-questions.json',                'name': 'EC-Council CHFI v11',          'exam': 'CHFI',     'config': 'ec-council/chfi_v11.json',                'vendor': 'EC-Council'},
    {'id': 'ec-cnd',                'quiz': 'cnd-quiz.html',             'json': 'cnd-questions.json',                 'name': 'EC-Council CND v3',            'exam': 'CND',      'config': 'ec-council/cnd_v3.json',                  'vendor': 'EC-Council'},
    # OffSec (2 remaining)
    {'id': 'offsec-oswa',           'quiz': 'oswa-quiz.html',            'json': 'oswa-questions.json',                'name': 'OffSec OSWA',                  'exam': 'WEB-200',  'config': 'offsec/oswa_web-200.json',                'vendor': 'OffSec'},
    {'id': 'offsec-oswe',           'quiz': 'oswe-quiz.html',            'json': 'oswe-questions.json',                'name': 'OffSec OSWE',                  'exam': 'WEB-300',  'config': 'offsec/oswe_web-300.json',                'vendor': 'OffSec'},
    # HashiCorp (2)
    {'id': 'hashicorp-terraform',   'quiz': 'terraform-quiz.html',       'json': 'terraform-questions.json',           'name': 'HashiCorp Terraform Associate','exam': 'TA-003',   'config': 'hashicorp/terraform_associate_003.json',  'vendor': 'HashiCorp'},
    {'id': 'hashicorp-vault',       'quiz': 'vault-quiz.html',           'json': 'vault-questions.json',               'name': 'HashiCorp Vault Associate',    'exam': 'VA-002',   'config': 'hashicorp/vault_associate_003.json',      'vendor': 'HashiCorp'},
    # Kubernetes (3)
    {'id': 'k8s-cka',               'quiz': 'cka-quiz.html',             'json': 'cka-questions.json',                 'name': 'Kubernetes CKA',               'exam': 'CKA',      'config': 'kubernetes/cka.json',                     'vendor': 'Kubernetes'},
    {'id': 'k8s-ckad',              'quiz': 'ckad-quiz.html',            'json': 'ckad-questions.json',                'name': 'Kubernetes CKAD',              'exam': 'CKAD',     'config': 'kubernetes/ckad.json',                    'vendor': 'Kubernetes'},
    {'id': 'k8s-cks',               'quiz': 'cks-quiz.html',             'json': 'cks-questions.json',                 'name': 'Kubernetes CKS',               'exam': 'CKS',      'config': 'kubernetes/cks.json',                     'vendor': 'Kubernetes'},
]


def load_cert_config(config_path):
    """Load cert config JSON."""
    full_path = ETSY_CERTS / config_path
    if not full_path.exists():
        return None
    try:
        with open(full_path, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def generate_questions(domains, cert_name, exam_code):
    """Generate 30 practice questions from domain/objective data."""
    questions = []
    qid = 1

    for domain in domains:
        dom_num = domain.get('number', 1)
        dom_name = domain.get('name', f'Domain {dom_num}')
        objectives = domain.get('objectives', [])
        key_concepts = domain.get('key_concepts', [])
        pct = domain.get('percentage', '0%')

        # How many questions per domain (proportional to weight, min 3)
        try:
            weight = int(pct.replace('%', ''))
        except (ValueError, AttributeError):
            weight = 15
        num_qs = max(3, round(weight * 30 / 100))

        for i in range(num_qs):
            obj_ref = objectives[i % len(objectives)] if objectives else f'{dom_num}.1'
            obj_short = obj_ref.split(' ', 1)[0] if ' ' in obj_ref else f'{dom_num}.{i+1}'
            obj_text = obj_ref.split(' ', 1)[1] if ' ' in obj_ref else obj_ref

            # Pick difficulty
            difficulty = ['easy', 'medium', 'medium', 'hard'][i % 4]

            # Generate contextual question from objective text
            q_text, options, correct, explanation = _make_question(
                dom_num, dom_name, obj_text, key_concepts, cert_name, difficulty, i
            )

            questions.append({
                'id': qid,
                'domain': dom_num,
                'objective': obj_short,
                'difficulty': difficulty,
                'question': q_text,
                'options': options,
                'correct': correct,
                'explanation': explanation,
                'link': 'start-here.html'
            })
            qid += 1

    return questions


def _make_question(dom_num, dom_name, obj_text, concepts, cert_name, difficulty, idx):
    """Create a question based on objective text and key concepts."""
    # Question templates that work across all cert types
    templates = [
        {
            'q': f'Which of the following best describes the purpose of "{obj_text}" in {dom_name}?',
            'options': [
                f'To implement and manage {obj_text.lower()} processes',
                f'To evaluate compliance with {dom_name.lower()} standards',
                f'To document risk assessment procedures',
                f'To audit external vendor relationships'
            ],
            'correct': 0,
            'explanation': f'{obj_text} is a key objective in {dom_name}. Understanding this concept is essential for the exam.'
        },
        {
            'q': f'A professional is tasked with {obj_text.lower() if obj_text else dom_name.lower()}. What should be the first step?',
            'options': [
                'Assess the current state and identify requirements',
                'Implement the solution immediately',
                'Document the findings in a report',
                'Escalate to senior management'
            ],
            'correct': 0,
            'explanation': f'The first step in any {dom_name.lower()} task is to assess the current state before implementing changes.'
        },
        {
            'q': f'Which concept in {dom_name} is most closely related to {obj_text.lower()}?',
            'options': [
                f'{dom_name} governance and oversight',
                f'{dom_name} implementation and operations',
                f'{dom_name} assessment and testing',
                f'{dom_name} risk management'
            ],
            'correct': 1,
            'explanation': f'{obj_text} falls under the implementation and operations aspect of {dom_name}.'
        },
        {
            'q': f'In the context of {cert_name}, what is the primary goal of {obj_text.lower()}?',
            'options': [
                f'To ensure proper {dom_name.lower()} controls are in place',
                f'To reduce operational costs',
                f'To increase system performance',
                f'To simplify user interfaces'
            ],
            'correct': 0,
            'explanation': f'The primary goal of {obj_text.lower()} is to ensure proper controls and processes are in place within {dom_name}.'
        },
        {
            'q': f'Which of the following is a key consideration when working with {obj_text.lower()}?',
            'options': [
                'Following industry best practices and standards',
                'Minimizing documentation requirements',
                'Reducing the number of team members involved',
                'Avoiding automated tools'
            ],
            'correct': 0,
            'explanation': f'When working with {obj_text.lower()}, following industry best practices ensures consistent and reliable results.'
        },
    ]

    # Use concepts to create more specific questions if available
    if concepts and len(concepts) >= 4 and idx % 3 == 0:
        shuffled = list(concepts)
        random.seed(dom_num * 100 + idx)
        random.shuffle(shuffled)
        correct_concept = shuffled[0]
        wrong_concepts = shuffled[1:4]
        return (
            f'Which of the following is a key concept within {dom_name} (Domain {dom_num})?',
            [correct_concept] + wrong_concepts,
            0,
            f'{correct_concept} is a key concept in {dom_name}. This domain covers topics essential for the {cert_name} exam.'
        )

    template = templates[idx % len(templates)]
    return template['q'], template['options'], template['correct'], template['explanation']


def pick_seo_questions(questions, domains_js, count=10):
    """Pick a diverse sample of questions for the SEO block (one per domain, then fill)."""
    by_domain = {}
    for q in questions:
        d = str(q.get('domain', 1))
        if d not in by_domain:
            by_domain[d] = []
        by_domain[d].append(q)
    selected = []
    # One from each domain first
    for dk in sorted(by_domain.keys(), key=int):
        if by_domain[dk]:
            selected.append(by_domain[dk][0])
    # Fill remaining from all questions
    picked_ids = {q['id'] for q in selected}
    for q in questions:
        if len(selected) >= count:
            break
        if q['id'] not in picked_ids:
            selected.append(q)
            picked_ids.add(q['id'])
    return selected[:count]


def build_seo_html(seo_qs, name, exam):
    """Build the static HTML block with sample Q&As for crawlers."""
    items = []
    for q in seo_qs:
        correct_idx = q.get('correct', 0)
        options = q.get('options', [])
        answer = options[correct_idx] if correct_idx < len(options) else 'See explanation'
        explanation = q.get('explanation', '')
        items.append(
            f'            <details>\n'
            f'                <summary>Q: {escape(q["question"])}</summary>\n'
            f'                <p><strong>A: {escape(answer)}</strong> &mdash; {escape(explanation)}</p>\n'
            f'            </details>'
        )
    return (
        f'        <div class="seo-questions" id="seoQuestions">\n'
        f'            <h3>Sample {name} {exam} Practice Questions</h3>\n'
        + '\n'.join(items) + '\n'
        f'        </div>'
    )


def build_faq_schema(seo_qs):
    """Build FAQPage schema from the SEO questions."""
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


def generate_quiz_html(cfg, domains_js, total_questions, questions):
    """Generate the quiz HTML page."""
    name = cfg['name']
    exam = cfg['exam']
    quiz_file = cfg['quiz']
    json_file = cfg['json']
    vendor = cfg['vendor']
    cert_id = cfg['id']
    storage_key = f'fixthevuln_{cert_id.replace("-", "_")}_quiz'

    # Build domain buttons HTML
    domain_buttons = '                    <button class="category-btn active" data-domain="all">All Domains</button>\n'
    for dk, dv in sorted(domains_js.items(), key=lambda x: int(x[0])):
        domain_buttons += f'                    <button class="category-btn" data-domain="{dk}">{dk}.0 {escape(dv["name"])} ({dv["weight"]}%)</button>\n'

    # Build domains JS object
    domains_obj_lines = []
    for dk, dv in sorted(domains_js.items(), key=lambda x: int(x[0])):
        domains_obj_lines.append(f"                {dk}: {{name: '{dv['name']}', weight: {dv['weight']}}}")
    domains_obj = ',\n'.join(domains_obj_lines)

    # Pick 10 diverse questions for SEO block
    seo_qs = pick_seo_questions(questions, domains_js)
    seo_html = build_seo_html(seo_qs, name, exam)
    faq_schema_json = build_faq_schema(seo_qs)

    # Build Quiz schema with hasPart
    assesses_list = [dv['name'] for _, dv in sorted(domains_js.items(), key=lambda x: int(x[0]))]
    has_part = []
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
        has_part.append({
            "@type": "Question",
            "eduQuestionType": "Multiple choice",
            "text": q['question'],
            "suggestedAnswer": [s for s in suggested if s["comment"]["text"] == "Incorrect"],
            "acceptedAnswer": suggested[correct_idx] if correct_idx < len(suggested) else suggested[0]
        })
    quiz_schema_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "Quiz",
        "name": f"{name} Practice Quiz",
        "about": {"@type": "Thing", "name": name},
        "educationalLevel": "Professional",
        "numberOfQuestions": total_questions,
        "assesses": assesses_list,
        "hasPart": has_part,
    }, indent=4, ensure_ascii=False)

    q_desc = f'Free {name} {exam} practice quiz with {total_questions} questions mapped to all exam domains. Test your knowledge with explanations and progress tracking.'
    q_canonical = f'{SITE_URL}/{quiz_file}'
    q_schema = [
        breadcrumb_schema([("Home", f"{SITE_URL}/"), ("Quizzes", f"{SITE_URL}/practice-tests.html"), (f"{name} Quiz", None)]),
        quiz_schema_json,
        faq_schema_json,
    ]
    q_head = html_head(f'Free {name} Practice Quiz &mdash; {exam} Questions', q_desc, q_canonical,
                       extra_css=[f'quiz.css?v={QUIZ_CSS_VERSION}'],
                       schema_blocks=q_schema, depth=0)

    return f'''<!DOCTYPE html>
<html lang="en">
{q_head}
<body>
{nav(depth=0)}
{share_bar()}

    <header>
        <div class="container">
            <a href="index.html" style="text-decoration: none; color: inherit;"><h1>FixTheVuln</h1></a>
            <p class="tagline">{name} {exam} Practice Quiz &mdash; {total_questions} Questions</p>
            <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">Last updated: {TODAY}</p>
        </div>
    </header>

    <main class="container">
        <a href="practice-tests.html" class="back-link">&larr; All Practice Quizzes</a>

        <section class="intro">
            <h2>Test Your {name} Knowledge</h2>
            <p>{total_questions} practice questions mapped to all {exam} exam domains. Weighted random selection matches real exam distribution. Filter by domain, choose your question count, and track your progress.</p>
        </section>

        <div class="quiz-container" id="quiz-container" data-product-id="{cert_id}" data-cert-name="{name}">
            <div id="start-screen" class="start-screen">
                <h2>Choose Your Quiz</h2>
                <p>Select a domain and question count. Weighted random selection matches the real {exam} exam distribution when you choose "All Domains".</p>
                <p id="question-pool-info" style="font-size:0.85rem;color:#667eea;font-weight:600;margin-bottom:1rem;">Loading question bank...</p>

                <h4 style="color:#555;margin-bottom:0.5rem;font-size:0.9rem;">{exam} Domain</h4>
                <div class="category-select">
{domain_buttons}                </div>

                <h4 style="color:#555;margin-bottom:0.5rem;font-size:0.9rem;">Difficulty</h4>
                <div class="difficulty-select">
                    <div class="difficulty-btn active" data-difficulty="mixed">
                        <h4>Mixed</h4>
                        <p>All levels</p>
                    </div>
                    <div class="difficulty-btn" data-difficulty="easy">
                        <h4>Easy</h4>
                        <p>Fundamentals</p>
                    </div>
                    <div class="difficulty-btn" data-difficulty="medium">
                        <h4>Medium</h4>
                        <p>Exam-level</p>
                    </div>
                    <div class="difficulty-btn" data-difficulty="hard">
                        <h4>Hard</h4>
                        <p>Advanced</p>
                    </div>
                </div>

                <h4 style="color:#555;margin-bottom:0.5rem;font-size:0.9rem;">Questions</h4>
                <div class="category-select" id="count-select">
                    <button class="category-btn active" data-count="10">10</button>
                    <button class="category-btn" data-count="25">25</button>
                </div>

                <button class="btn btn-primary" onclick="startQuiz()">Start Quiz</button>
            </div>

            <div id="quiz-screen" style="display: none;">
                <div class="quiz-header">
                    <div class="quiz-stats">
                        <div class="stat-box">
                            <div class="stat-value" id="current-question">1</div>
                            <div class="stat-label">Question</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value" id="score">0</div>
                            <div class="stat-label">Score</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value timer" id="timer">--</div>
                            <div class="stat-label">Time</div>
                        </div>
                    </div>
                </div>
                <div class="progress-section">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progress-fill" style="width: 10%;"></div>
                    </div>
                    <p class="progress-text"><span id="answered">0</span> of <span id="total-questions">10</span> answered</p>
                </div>
                <div id="question-container"></div>
{seo_html}
                <div class="quiz-actions">
                    <button class="btn btn-secondary" onclick="skipQuestion()" id="skip-btn">Skip</button>
                    <button class="btn btn-primary" onclick="nextQuestion()" id="next-btn" style="display: none;">Next Question</button>
                    <button class="btn btn-primary" onclick="showResults()" id="finish-btn" style="display: none;">See Results</button>
                </div>
            </div>

            <div id="results-screen" class="results-card">
                <div class="results-score" id="final-score">0%</div>
                <div class="results-grade" id="grade">Keep Learning!</div>
                <p id="grade-message">Review the explanations to strengthen your knowledge.</p>
                <div class="results-breakdown">
                    <div class="breakdown-item">
                        <div class="breakdown-value" id="correct-count">0</div>
                        <div class="breakdown-label">Correct</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="breakdown-value" id="incorrect-count">0</div>
                        <div class="breakdown-label">Incorrect</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="breakdown-value" id="time-taken">0:00</div>
                        <div class="breakdown-label">Time</div>
                    </div>
                </div>
                <div class="share-section">
                    <p>Share your score:</p>
                    <div class="share-buttons">
                        <a href="#" class="share-btn share-twitter" id="share-twitter" target="_blank">Twitter</a>
                        <a href="#" class="share-btn share-linkedin" id="share-linkedin" target="_blank">LinkedIn</a>
                    </div>
                </div>
                <div style="margin-top: 2rem;">
                    <button class="btn btn-secondary" style="background: white; color: #667eea;" onclick="restartQuiz()">Try Again</button>
                    <a href="start-here.html" class="btn btn-secondary" style="background: rgba(255,255,255,0.2); color: white; text-decoration: none; display: inline-block; margin-left: 1rem;">Study More</a>
                </div>
            </div>
        </div>

        <section class="vulnerability-card">
            <h2>Track Your Progress</h2>
            <p>Your quiz history is saved locally. Keep practicing to improve your scores!</p>
            <div id="quiz-history" style="margin-top: 1rem;"></div>
        </section>

        <section class="cta">
            <h2>Ready to Go Deeper?</h2>
            <p>Explore study guides, practice labs, and exam preparation resources.</p>
            <a href="career-paths.html" class="cta-button">View All Certifications &rarr;</a>
        </section>

        <!-- CyberFolio CTA -->
        <div style="border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 12px; text-align: center; margin-top: 1.5rem;">
            <p style="text-transform: uppercase; letter-spacing: 2px; font-size: 0.65rem; opacity: 0.5; margin-bottom: 0.3rem;">CyberFolio</p>
            <p style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Passing the exam? Show employers what you know.</p>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">Build a shareable cybersecurity portfolio that highlights your certifications, projects, and skills &mdash; free.</p>
            <a href="https://cyberfolio.io" style="display:inline-block;background:#06b6d4;color:white;padding:0.6rem 1.5rem;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.95rem;" target="_blank" rel="noopener">Build Your Portfolio &rarr;</a>
        </div>
    </main>

{footer(affiliate_disclosure=True, quiz_disclaimer=vendor)}

    <script src="js/quiz-engine.js"></script>
    <script>
        function startQuiz() {{ QuizEngine.startQuiz(); }}
        function skipQuestion() {{ QuizEngine.skipQuestion(); }}
        function nextQuestion() {{ QuizEngine.nextQuestion(); }}
        function showResults() {{ QuizEngine.showResults(); }}
        function restartQuiz() {{ QuizEngine.restartQuiz(); }}

        QuizEngine.init({{
            jsonPath: 'data/{json_file}',
            examCode: '{exam}',
            storageKey: '{storage_key}',
            shareText: 'I scored {{percentage}}% on the FixTheVuln {name} Quiz ({{quizSize}} questions)! Test your {exam} knowledge:',
            shareUrl: 'https://fixthevuln.com/{quiz_file}',
            domains: {{
{domains_obj}
            }},
            fallbackQuestions: []
        }});
    </script>
{cf_analytics()}
</body>
</html>'''


def main():
    DATA_DIR.mkdir(exist_ok=True)
    generated_html = 0
    generated_json = 0
    skipped = 0

    for cfg in QUIZ_CONFIGS:
        if cfg['id'] in EXISTING_QUIZZES:
            print(f"  SKIP {cfg['quiz']} (already exists)")
            skipped += 1
            continue

        # Load domain data from cert config
        config = load_cert_config(cfg['config'])
        if not config:
            print(f"  NOCONFIG {cfg['id']} — skipping quiz generation")
            continue

        domains = config.get('domains', [])
        if not domains:
            print(f"  NODOMAINS {cfg['id']} — skipping")
            continue

        # Build domains JS object
        domains_js = {}
        for d in domains:
            num = d.get('number', 1)
            pct_str = d.get('percentage', '0%')
            try:
                weight = int(pct_str.replace('%', ''))
            except (ValueError, AttributeError):
                weight = round(100 / len(domains))
            domains_js[str(num)] = {
                'name': d['name'],
                'weight': weight
            }

        # Generate questions
        questions = generate_questions(domains, cfg['name'], cfg['exam'])
        total_questions = len(questions)

        # Write JSON
        json_path = DATA_DIR / cfg['json']
        domain_counts = {}
        for q in questions:
            d = str(q['domain'])
            domain_counts[d] = domain_counts.get(d, 0) + 1

        json_data = {
            'metadata': {
                'title': f'{cfg["name"]} {cfg["exam"]} Practice Questions',
                'version': '1.0',
                'total_questions': total_questions,
                'exam': cfg['exam'],
                'domains': {
                    dk: {
                        'name': dv['name'],
                        'weight': dv['weight'],
                        'count': domain_counts.get(dk, 0)
                    }
                    for dk, dv in sorted(domains_js.items(), key=lambda x: int(x[0]))
                }
            },
            'questions': questions
        }
        json_path.write_text(json.dumps(json_data, indent=2), encoding='utf-8')
        generated_json += 1

        # Write HTML
        html_path = REPO / cfg['quiz']
        html_content = generate_quiz_html(cfg, domains_js, total_questions, questions)
        html_path.write_text(html_content, encoding='utf-8')
        generated_html += 1

        print(f"  OK   {cfg['quiz']} + data/{cfg['json']} ({total_questions} questions)")

    print(f"\nDone: {generated_html} quiz pages, {generated_json} question files ({skipped} skipped)")


if __name__ == '__main__':
    main()
