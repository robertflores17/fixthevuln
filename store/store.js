/* ============================================
   FixTheVuln Store — JavaScript
   Cart, Products, Stripe Checkout
   ============================================ */

// ─── PAGE CONFIG (set by category pages before loading this script) ──
const PAGE_CONFIG = Object.assign({
  vendors: null,        // null = show all vendors (hub or legacy)
  showVendorTabs: true, // show vendor filter tabs
  showHubCards: false,   // render hub vendor showcase cards
  showOpsKit: false,     // show ops kit section (hub only)
}, window.PAGE_CONFIG || {});

// ─── VENDOR META (hub cards, routing) ────────────────────
const VENDOR_META = {
  comptia:    { name: 'CompTIA',      icon: '🏆', color: '#e53e3e', url: 'comptia.html',             desc: 'A+, Security+, Network+, CySA+, PenTest+, CASP+ and more' },
  aws:        { name: 'AWS',          icon: '☁️', color: '#ff9900', url: 'aws.html',                 desc: 'Cloud Practitioner, Solutions Architect, Security Specialty' },
  microsoft:  { name: 'Microsoft',    icon: '🔷', color: '#0078d4', url: 'microsoft.html',           desc: 'Azure Fundamentals, Administrator, Security Engineer, AI' },
  cisco:      { name: 'Cisco',        icon: '🌐', color: '#049fd9', url: 'cisco.html',               desc: 'CCNA, CCNP ENCOR, CyberOps, DevNet' },
  google:     { name: 'Google Cloud', icon: '🔵', color: '#4285f4', url: 'google-cloud.html',        desc: 'Cloud Engineer, Architect, Data Engineer, Security' },
  'security-governance': { name: 'Security & Governance', icon: '🛡️', color: '#805ad5', url: 'security-governance.html', desc: 'ISC2 CISSP/CCSP, ISACA CISA/CISM, GIAC GSEC/GCIH' },
  'offensive-devops':    { name: 'Offensive & DevOps',    icon: '💻', color: '#d53f8c', url: 'offensive-devops.html',    desc: 'EC-Council CEH, OffSec OSCP, HashiCorp Terraform, Kubernetes CKA' },
  lifestyle:  { name: 'Lifestyle & Productivity', icon: '📓', color: '#38a169', url: 'lifestyle.html',   desc: 'Budget Binder, Wellness Journal, Digital Planner, Business Templates' },
  education:  { name: 'Education',    icon: '📚', color: '#d69e2e', url: 'education.html',           desc: 'Teacher Planner, Student Planner, ADHD Student Planner' },
};

// Mapping of hub group key → actual vendor IDs in PRODUCTS
const VENDOR_GROUP_MAP = {
  comptia: ['comptia'],
  aws: ['aws'],
  microsoft: ['microsoft'],
  cisco: ['cisco'],
  google: ['google'],
  'security-governance': ['isc2', 'isaca', 'giac'],
  'offensive-devops': ['ec-council', 'offsec', 'hashicorp', 'k8s'],
  lifestyle: ['lifestyle', 'bundles'],
  education: ['education'],
};

// ─── STRIPE CONFIG ──────────────────────────
const STRIPE_PUBLISHABLE_KEY = 'pk_live_51T1bzYLBnrzacKtT0qGIOSxTYOp0ZUVdsAS5pYLKDYQpbIQs2PgypNZ7ARkcQeFNkyKLyl8qmBXBvOLf0Uaqqu0200xsCUOQk2';
const CHECKOUT_API_URL = 'https://fixthevuln-checkout.robertflores17.workers.dev';
// ─────────────────────────────────────────────

// ─── PRICING ────────────────────────────────
const PRICING = {
  standard:  5.99,
  adhd:      5.99,
  dark:      5.99,
  adhd_dark: 5.99,
  bundle:    15.99,  // All 4 formats for one cert — save ~$8
};

const VARIANT_LABELS = {
  standard:  'Standard',
  adhd:      'ADHD-Friendly',
  dark:      'Dark Mode',
  adhd_dark: 'ADHD-Friendly Dark',
  bundle:    '4-Format Bundle',
};

// ─── CAREER PATH BUNDLES ────────────────────
const CAREER_PATHS = [
  {
    id: 'comptia-trifecta',
    name: 'CompTIA Trifecta',
    desc: 'The essential IT foundation: A+ (both cores), Network+, and Security+',
    certs: ['CompTIA A+ Core 1', 'CompTIA A+ Core 2', 'CompTIA Network+', 'CompTIA Security+'],
    certIds: ['comptia-a-plus-1201', 'comptia-a-plus-1202', 'comptia-network-plus', 'comptia-security-plus'],
    certCount: 4,
    vendors: ['comptia'],
    icon: '🏆',
  },
  {
    id: 'comptia-a-plus',
    name: 'CompTIA A+ Complete',
    desc: 'Both A+ exams in one bundle — start your IT career',
    certs: ['CompTIA A+ Core 1', 'CompTIA A+ Core 2'],
    certIds: ['comptia-a-plus-1201', 'comptia-a-plus-1202'],
    certCount: 2,
    vendors: ['comptia'],
    icon: '💻',
  },
  {
    id: 'comptia-security-track',
    name: 'CompTIA Security Track',
    desc: 'Full security progression from Security+ through CASP+',
    certs: ['CompTIA Security+', 'CompTIA CySA+', 'CompTIA PenTest+', 'CompTIA CASP+'],
    certIds: ['comptia-security-plus', 'comptia-cysa-plus', 'comptia-pentest-plus', 'comptia-casp-plus'],
    certCount: 4,
    vendors: ['comptia'],
    icon: '🔐',
  },
  {
    id: 'security-pro',
    name: 'Security Pro',
    desc: 'Cross-vendor security combo: CompTIA Security+ and ISC2 CISSP',
    certs: ['CompTIA Security+', 'ISC2 CISSP'],
    certIds: ['comptia-security-plus', 'isc2-cissp'],
    certCount: 2,
    vendors: ['comptia', 'isc2'],
    icon: '🛡️',
  },
  {
    id: 'aws-track',
    name: 'AWS Track',
    desc: 'AWS cloud career path: Practitioner → Architect → Developer',
    certs: ['AWS Cloud Practitioner', 'AWS Solutions Architect', 'AWS Developer'],
    certIds: ['aws-cloud-practitioner', 'aws-solutions-architect', 'aws-developer'],
    certCount: 3,
    vendors: ['aws'],
    icon: '☁️',
  },
  {
    id: 'azure-track',
    name: 'Azure Track',
    desc: 'Microsoft Azure path: Fundamentals → Admin → Architect',
    certs: ['Azure Fundamentals (AZ-900)', 'Azure Administrator (AZ-104)', 'Azure Architect (AZ-305)'],
    certIds: ['ms-az-900', 'ms-az-104', 'ms-az-305'],
    certCount: 3,
    vendors: ['microsoft'],
    icon: '🔷',
  },
  {
    id: 'cloud-fundamentals',
    name: 'Cloud Fundamentals',
    desc: 'Multi-cloud foundations: AWS, Azure, and Google Cloud in one bundle',
    certs: ['AWS Cloud Practitioner', 'Azure Fundamentals', 'Google Cloud Engineer'],
    certIds: ['aws-cloud-practitioner', 'ms-az-900', 'google-ace'],
    certCount: 3,
    vendors: ['aws', 'microsoft', 'google'],
    icon: '🌐',
  },
  {
    id: 'isaca-grc',
    name: 'ISACA GRC',
    desc: 'Governance, Risk & Compliance trifecta: CISA, CISM, and CRISC',
    certs: ['ISACA CISA', 'ISACA CISM', 'ISACA CRISC'],
    certIds: ['isaca-cisa', 'isaca-cism', 'isaca-crisc'],
    certCount: 3,
    vendors: ['isaca'],
    icon: '📊',
  },
  {
    id: 'isc2-path',
    name: 'ISC2 Path',
    desc: 'ISC2 progression: CC → SSCP → CISSP',
    certs: ['ISC2 CC', 'ISC2 SSCP', 'ISC2 CISSP'],
    certIds: ['isc2-cc', 'isc2-sscp', 'isc2-cissp'],
    certCount: 3,
    vendors: ['isc2'],
    icon: '🎓',
  },
  {
    id: 'cisco-path',
    name: 'Cisco Path',
    desc: 'Cisco networking career: CCNA, CCNP ENCOR, and CyberOps',
    certs: ['Cisco CCNA', 'Cisco CCNP ENCOR', 'Cisco CyberOps'],
    certIds: ['cisco-ccna', 'cisco-ccnp-encor', 'cisco-cyberops'],
    certCount: 3,
    vendors: ['cisco'],
    icon: '🌐',
  },
];

// Career path pricing by cert count and variant type
const CAREER_PATH_PRICING = {
  // { certCount: { single format price, bundle (4-format) price, individual total single, individual total bundle } }
  2: { single: 8.99,  bundle: 16.99, indivSingle: 11.98, indivBundle: 31.98 },
  3: { single: 12.99, bundle: 24.99, indivSingle: 17.97, indivBundle: 47.97 },
  4: { single: 16.99, bundle: 34.99, indivSingle: 23.96, indivBundle: 63.96 },
};

// ─── PRODUCT CATALOG ────────────────────────
const PRODUCTS = [
  // CompTIA
  { id: 'comptia-a-plus-1201',     vendor: 'comptia',   name: 'CompTIA A+ Core 1',           meta: '220-1201 · 5 domains', popular: true,  tags: ['Hardware', 'Networking', 'Troubleshooting'] },
  { id: 'comptia-a-plus-1202',     vendor: 'comptia',   name: 'CompTIA A+ Core 2',           meta: '220-1202 · 4 domains', popular: false, tags: ['OS', 'Security', 'Software'] },
  { id: 'comptia-security-plus',   vendor: 'comptia',   name: 'CompTIA Security+',           meta: 'SY0-701 · 5 domains',  popular: true,  tags: ['Cybersecurity', 'Risk', 'Cryptography'] },
  { id: 'comptia-network-plus',    vendor: 'comptia',   name: 'CompTIA Network+',            meta: 'N10-009 · 5 domains',  popular: true,  tags: ['Networking', 'Infrastructure', 'Security'] },
  { id: 'comptia-linux-plus',      vendor: 'comptia',   name: 'CompTIA Linux+',              meta: 'XK0-006 · 4 domains',  popular: false, tags: ['Linux', 'Scripting', 'Administration'] },
  { id: 'comptia-cloud-plus',      vendor: 'comptia',   name: 'CompTIA Cloud+',              meta: 'CV0-004 · 4 domains',  popular: false, tags: ['Cloud', 'Deployment', 'Security'] },
  { id: 'comptia-cysa-plus',       vendor: 'comptia',   name: 'CompTIA CySA+',               meta: 'CS0-003 · 4 domains',  popular: false, tags: ['Threat Detection', 'Analytics', 'IR'] },
  { id: 'comptia-pentest-plus',    vendor: 'comptia',   name: 'CompTIA PenTest+',            meta: 'PT0-003 · 5 domains',  popular: false, tags: ['Pen Testing', 'Exploits', 'Reporting'] },
  { id: 'comptia-casp-plus',       vendor: 'comptia',   name: 'CompTIA CASP+',               meta: 'CAS-005 · 4 domains',  popular: false, tags: ['Architecture', 'Engineering', 'Governance'] },
  { id: 'comptia-server-plus',    vendor: 'comptia',   name: 'CompTIA Server+',             meta: 'SK0-005 · 4 domains',  popular: false, tags: ['Server Hardware', 'Administration', 'Security'] },
  { id: 'comptia-data-plus',      vendor: 'comptia',   name: 'CompTIA Data+',               meta: 'DA0-001 · 5 domains',  popular: false, tags: ['Data Concepts', 'Mining', 'Visualization'] },
  { id: 'comptia-project-plus',   vendor: 'comptia',   name: 'CompTIA Project+',            meta: 'PK0-005 · 5 domains',  popular: false, tags: ['Project Management', 'Agile', 'Risk'] },
  { id: 'comptia-itf-plus',       vendor: 'comptia',   name: 'CompTIA ITF+',                meta: 'FC0-U71 · 6 domains',  popular: false, tags: ['IT Concepts', 'Infrastructure', 'Security Basics'] },

  // ISC2
  { id: 'isc2-cc',                 vendor: 'isc2',      name: 'ISC2 CC',                     meta: 'CC · 5 domains',       popular: false, tags: ['Entry-Level', 'Security Principles'] },
  { id: 'isc2-sscp',               vendor: 'isc2',      name: 'ISC2 SSCP',                   meta: 'SSCP · 7 domains',     popular: false, tags: ['Operations', 'Administration'] },
  { id: 'isc2-cissp',              vendor: 'isc2',      name: 'ISC2 CISSP',                  meta: 'CISSP 2026 · 8 domains', popular: true,  tags: ['Management', 'Architecture', 'Risk'] },
  { id: 'isc2-ccsp',               vendor: 'isc2',      name: 'ISC2 CCSP',                   meta: 'CCSP · 6 domains',     popular: false, tags: ['Cloud Security', 'Architecture'] },

  // AWS
  { id: 'aws-cloud-practitioner',  vendor: 'aws',       name: 'AWS Cloud Practitioner',      meta: 'CLF-C02 · 4 domains',  popular: true,  tags: ['Cloud Concepts', 'AWS Services'] },
  { id: 'aws-solutions-architect', vendor: 'aws',       name: 'AWS Solutions Architect',      meta: 'SAA-C03 · 4 domains',  popular: true,  tags: ['Architecture', 'Resilience', 'Cost'] },
  { id: 'aws-developer',           vendor: 'aws',       name: 'AWS Developer Associate',      meta: 'DVA-C02 · 4 domains',  popular: false, tags: ['Development', 'Deployment', 'Security'] },
  { id: 'aws-cloudops',            vendor: 'aws',       name: 'AWS CloudOps Engineer',        meta: 'SOA-C03 · 6 domains',  popular: false, tags: ['Monitoring', 'Automation', 'Networking'] },
  { id: 'aws-security-specialty',  vendor: 'aws',       name: 'AWS Security Specialty',       meta: 'SCS-C03 · 6 domains',  popular: false, tags: ['IAM', 'Data Protection', 'Logging'] },
  { id: 'aws-database-specialty', vendor: 'aws',       name: 'AWS Database Specialty',       meta: 'DBS-C01 · 5 domains',  popular: false, tags: ['Databases', 'Migration', 'Monitoring'] },
  { id: 'aws-machine-learning',   vendor: 'aws',       name: 'AWS Machine Learning',         meta: 'MLS-C01 · 4 domains',  popular: false, tags: ['ML', 'Data Engineering', 'Modeling'] },
  { id: 'aws-data-engineer',      vendor: 'aws',       name: 'AWS Data Engineer',            meta: 'DEA-C01 · 4 domains',  popular: false, tags: ['Data Pipelines', 'Analytics', 'Governance'] },

  // Microsoft
  { id: 'ms-az-900',               vendor: 'microsoft', name: 'Microsoft Azure Fundamentals', meta: 'AZ-900 · 3 domains',   popular: true,  tags: ['Cloud Concepts', 'Azure Services'] },
  { id: 'ms-az-104',               vendor: 'microsoft', name: 'Microsoft Azure Administrator',meta: 'AZ-104 · 5 domains',   popular: false, tags: ['Identity', 'Storage', 'Compute'] },
  { id: 'ms-az-305',               vendor: 'microsoft', name: 'Azure Solutions Architect',    meta: 'AZ-305 · 4 domains',   popular: false, tags: ['Design', 'Infrastructure', 'Data'] },
  { id: 'ms-sc-900',               vendor: 'microsoft', name: 'Security Fundamentals',        meta: 'SC-900 · 4 domains',   popular: false, tags: ['Security', 'Compliance', 'Identity'] },
  { id: 'ms-ai-900',               vendor: 'microsoft', name: 'Azure AI Fundamentals',        meta: 'AI-900 · 5 domains',   popular: false, tags: ['AI', 'Machine Learning', 'NLP'] },
  { id: 'ms-az-500',               vendor: 'microsoft', name: 'Azure Security Engineer',     meta: 'AZ-500 · 4 domains',   popular: false, tags: ['Identity', 'Network Security', 'Data Protection'] },
  { id: 'ms-az-204',               vendor: 'microsoft', name: 'Azure Developer Associate',   meta: 'AZ-204 · 5 domains',   popular: false, tags: ['App Development', 'Storage', 'Monitoring'] },
  { id: 'ms-az-400',               vendor: 'microsoft', name: 'Azure DevOps Engineer',       meta: 'AZ-400 · 8 domains',   popular: false, tags: ['CI/CD', 'Source Control', 'Automation'] },
  { id: 'ms-dp-900',               vendor: 'microsoft', name: 'Azure Data Fundamentals',     meta: 'DP-900 · 3 domains',   popular: false, tags: ['Data Concepts', 'Relational', 'Analytics'] },
  { id: 'ms-ms-900',               vendor: 'microsoft', name: 'Microsoft 365 Fundamentals',  meta: 'MS-900 · 4 domains',   popular: false, tags: ['M365 Services', 'Security', 'Pricing'] },
  { id: 'ms-sc-300',               vendor: 'microsoft', name: 'Identity & Access Admin',     meta: 'SC-300 · 4 domains',   popular: false, tags: ['Azure AD', 'Identity', 'Access Management'] },
  { id: 'ms-ai-102',               vendor: 'microsoft', name: 'Azure AI Engineer',           meta: 'AI-102 · 5 domains',   popular: false, tags: ['Cognitive Services', 'Bot Service', 'NLP'] },

  // Cisco
  { id: 'cisco-ccna',              vendor: 'cisco',     name: 'Cisco CCNA',                   meta: '200-301 · 6 domains',  popular: true,  tags: ['Networking', 'IP Connectivity', 'Security'] },
  { id: 'cisco-ccnp-encor',        vendor: 'cisco',     name: 'Cisco CCNP ENCOR',             meta: '350-401 · 6 domains',  popular: false, tags: ['Enterprise', 'Architecture', 'Automation'] },
  { id: 'cisco-cyberops',          vendor: 'cisco',     name: 'Cisco CyberOps Associate',     meta: '200-201 · 5 domains',  popular: false, tags: ['SOC', 'Threat Analysis', 'Monitoring'] },
  { id: 'cisco-ccnp-security',    vendor: 'cisco',     name: 'Cisco CCNP Security SCOR',    meta: '350-701 · 5 domains',  popular: false, tags: ['Network Security', 'Cloud Security', 'VPN'] },
  { id: 'cisco-devnet',           vendor: 'cisco',     name: 'Cisco DevNet Associate',       meta: '200-901 · 6 domains',  popular: false, tags: ['APIs', 'Automation', 'Network Programmability'] },

  // ISACA
  { id: 'isaca-cisa',              vendor: 'isaca',     name: 'ISACA CISA',                   meta: 'CISA · 5 domains',     popular: false, tags: ['Audit', 'Governance', 'IS Management'] },
  { id: 'isaca-cism',              vendor: 'isaca',     name: 'ISACA CISM',                   meta: 'CISM 2026 · 4 domains', popular: false, tags: ['Governance', 'Risk', 'Incident Mgmt'] },
  { id: 'isaca-crisc',             vendor: 'isaca',     name: 'ISACA CRISC',                  meta: 'CRISC · 4 domains',    popular: false, tags: ['Risk', 'IT Controls', 'Monitoring'] },

  // GIAC
  { id: 'giac-gsec',               vendor: 'giac',      name: 'GIAC GSEC',                    meta: 'GSEC · 7 domains',     popular: false, tags: ['Defense', 'Networking', 'Incident Response'] },
  { id: 'giac-gcih',               vendor: 'giac',      name: 'GIAC GCIH',                    meta: 'GCIH · 6 domains',     popular: false, tags: ['Incident Handling', 'Hacker Tools', 'Exploits'] },
  { id: 'giac-gpen',               vendor: 'giac',      name: 'GIAC GPEN',                    meta: 'GPEN · 6 domains',     popular: false, tags: ['Pen Testing', 'Recon', 'Exploitation'] },
  { id: 'giac-gcia',               vendor: 'giac',      name: 'GIAC GCIA',                    meta: 'GCIA · 6 domains',     popular: false, tags: ['Intrusion Analysis', 'Network Forensics', 'Monitoring'] },

  // Google Cloud
  { id: 'google-ace',              vendor: 'google',    name: 'Google Associate Cloud Engineer', meta: 'ACE · 5 domains',   popular: false, tags: ['GCP', 'Compute', 'Networking'] },
  { id: 'google-pca',              vendor: 'google',    name: 'Google Professional Cloud Architect', meta: 'PCA · 6 domains', popular: false, tags: ['Architecture', 'Design', 'Migration'] },
  { id: 'google-cdl',              vendor: 'google',    name: 'Google Cloud Digital Leader',  meta: 'CDL · 3 domains',      popular: false, tags: ['Cloud Strategy', 'Business Value', 'GCP Services'] },
  { id: 'google-pde',              vendor: 'google',    name: 'Google Professional Data Engineer', meta: 'PDE · 4 domains', popular: false, tags: ['BigQuery', 'Data Pipelines', 'ML Models'] },
  { id: 'google-pse',              vendor: 'google',    name: 'Google Cloud Security Engineer', meta: 'PSE · 6 domains',   popular: false, tags: ['IAM', 'Data Protection', 'Security Operations'] },

  // EC-Council
  { id: 'ec-ceh',                  vendor: 'ec-council', name: 'EC-Council CEH v13',          meta: 'CEH · 20 modules',     popular: true,  tags: ['Ethical Hacking', 'Reconnaissance', 'System Hacking'] },
  { id: 'ec-chfi',                 vendor: 'ec-council', name: 'EC-Council CHFI v11',         meta: 'CHFI · 14 modules',    popular: false, tags: ['Digital Forensics', 'Evidence', 'Incident Response'] },
  { id: 'ec-cnd',                  vendor: 'ec-council', name: 'EC-Council CND v3',           meta: 'CND · 14 modules',     popular: false, tags: ['Network Defense', 'Threat Management', 'Perimeter Security'] },

  // OffSec
  { id: 'offsec-oscp',             vendor: 'offsec',    name: 'OffSec OSCP',                  meta: 'PEN-200 · Practical exam', popular: true, tags: ['Penetration Testing', 'Exploitation', 'Active Directory'] },
  { id: 'offsec-oswa',             vendor: 'offsec',    name: 'OffSec OSWA',                  meta: 'WEB-200 · Practical exam', popular: false, tags: ['Web App Security', 'SQL Injection', 'XSS'] },
  { id: 'offsec-oswe',             vendor: 'offsec',    name: 'OffSec OSWE',                  meta: 'WEB-300 · Practical exam', popular: false, tags: ['Advanced Web', 'Code Review', 'Exploitation'] },

  // HashiCorp
  { id: 'hashicorp-terraform',     vendor: 'hashicorp', name: 'HashiCorp Terraform Associate', meta: 'TA-003 · 9 objectives', popular: true, tags: ['IaC', 'Terraform', 'Cloud Provisioning'] },
  { id: 'hashicorp-vault',         vendor: 'hashicorp', name: 'HashiCorp Vault Associate',    meta: 'VA-002 · 10 objectives', popular: false, tags: ['Secrets Management', 'Encryption', 'Authentication'] },

  // Kubernetes
  { id: 'k8s-cka',                 vendor: 'k8s',       name: 'Kubernetes CKA',               meta: 'CKA · Performance-based', popular: true, tags: ['Cluster Admin', 'Networking', 'Scheduling'] },
  { id: 'k8s-ckad',                vendor: 'k8s',       name: 'Kubernetes CKAD',              meta: 'CKAD · Performance-based', popular: false, tags: ['App Design', 'Deployment', 'Services'] },
  { id: 'k8s-cks',                 vendor: 'k8s',       name: 'Kubernetes CKS',               meta: 'CKS · Performance-based', popular: false, tags: ['Cluster Security', 'System Hardening', 'Runtime'] },

  // Security Ops
  { id: 'vuln-remediation-planner', vendor: 'secops',   name: 'Vulnerability Remediation Planner', meta: 'Remediation tracker · SLA deadlines', popular: true, tags: ['Remediation Tracker', 'SLA Deadlines', 'Scan Import Log', 'Owner Assignment'] },

  // Lifestyle & Productivity
  { id: 'budget-binder',            vendor: 'lifestyle', name: 'Budget Binder',                    meta: 'Monthly budgets · Expense tracking', popular: true, tags: ['Budget', 'Expense Tracking', 'Savings Goals', 'Debt Payoff'] },
  { id: 'wellness-journal',         vendor: 'lifestyle', name: 'Wellness Journal',                 meta: 'Daily check-ins · Habit tracking', popular: false, tags: ['Mood Tracker', 'Gratitude', 'Sleep Log', 'Self-Care'] },
  { id: '2026-digital-planner',     vendor: 'lifestyle', name: '2026 Digital Planner',             meta: 'Full year · Monthly & weekly views', popular: false, tags: ['Calendar', 'Goals', 'To-Do Lists', 'Habit Tracker'] },
  { id: 'business-templates',       vendor: 'lifestyle', name: 'Business Templates',               meta: 'Invoice · Proposal · Tracker', popular: false, tags: ['Invoice', 'Project Tracker', 'Meeting Notes', 'Proposal'] },

  // Education
  { id: 'teacher-planner',          vendor: 'education', name: 'Teacher Planner',                  meta: 'Lesson plans · Grade tracking', popular: true, tags: ['Lesson Plans', 'Grade Book', 'Seating Charts', 'Parent Contact'] },
  { id: 'student-planner',          vendor: 'education', name: 'Student Planner',                  meta: 'Assignments · Semester schedule', popular: true, tags: ['Assignment Tracker', 'Study Schedule', 'GPA Calculator', 'Exam Prep'] },
  { id: 'adhd-student-planner',     vendor: 'education', name: 'ADHD Student Planner Spring 2026', meta: 'Focus tools · Break reminders', popular: false, tags: ['Focus Blocks', 'Energy Tracking', 'Reward System', 'Break Timer'] },

  // Lifestyle Bundle
  { id: 'lifestyle-bundle',         vendor: 'bundles',   name: 'Productivity Bundle',             meta: '3 planners · Save 25%', popular: true, tags: ['Budget Binder', '2026 Planner', 'Wellness Journal'] },
];

// ─── STATE ──────────────────────────────────
let cart = JSON.parse(localStorage.getItem('ftv_cart') || '[]');
let selectedVariant = localStorage.getItem('ftv_variant') || 'standard';
let selectedVendor = 'all';

// ─── DOM REFS (null-safe for hub page) ──────
const productGrid     = document.getElementById('productGrid');
const careerPathGrid  = document.getElementById('careerPathGrid');
const cartBadge     = document.getElementById('cartBadge');
const cartSidebar   = document.getElementById('cartSidebar');
const cartOverlay   = document.getElementById('cartOverlay');
const cartItems     = document.getElementById('cartItems');
const cartEmpty     = document.getElementById('cartEmpty');
const cartFooter    = document.getElementById('cartFooter');
const cartTotal     = document.getElementById('cartTotal');
const btnCheckout   = document.getElementById('btnCheckout');
const hubGrid       = document.getElementById('hubGrid');
const featuredGrid  = document.getElementById('featuredGrid');

// ─── HTML SANITIZATION ─────────────────────
function esc(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

// ─── TOAST & CONFIRM HELPERS ────────────────
function showToast(message, type = 'info', duration = 4000) {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast${type !== 'info' ? ` toast-${type}` : ''}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('toast-out');
    toast.addEventListener('animationend', () => toast.remove());
  }, duration);
}

function showConfirm(message) {
  return new Promise(resolve => {
    const overlay = document.getElementById('confirmOverlay');
    document.getElementById('confirmMessage').textContent = message;
    overlay.classList.add('active');
    const okBtn = document.getElementById('confirmOk');
    const cancelBtn = document.getElementById('confirmCancel');
    function cleanup(result) {
      overlay.classList.remove('active');
      okBtn.removeEventListener('click', onOk);
      cancelBtn.removeEventListener('click', onCancel);
      resolve(result);
    }
    function onOk() { cleanup(true); }
    function onCancel() { cleanup(false); }
    okBtn.addEventListener('click', onOk);
    cancelBtn.addEventListener('click', onCancel);
  });
}

// ─── PAGE-SCOPED PRODUCT FILTER ─────────────
function getPageProducts() {
  if (!PAGE_CONFIG.vendors) return PRODUCTS;
  return PRODUCTS.filter(p => PAGE_CONFIG.vendors.includes(p.vendor));
}

function getPageCareerPaths() {
  if (!PAGE_CONFIG.vendors) return CAREER_PATHS;
  return CAREER_PATHS.filter(p => p.vendors.some(v => PAGE_CONFIG.vendors.includes(v)));
}

// ─── INIT ───────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initFormatSelector();

  if (PAGE_CONFIG.showHubCards) {
    // Hub page mode
    renderHubCards();
    renderFeaturedProducts();
  } else {
    // Category or legacy page mode
    if (PAGE_CONFIG.showVendorTabs) initVendorTabs();
    if (productGrid) renderProducts();
    if (careerPathGrid) renderCareerPaths();
  }

  updateCartUI();
});

// ─── THEME TOGGLE ───────────────────────────
function initTheme() {
  const saved = localStorage.getItem('ftv_theme');
  if (saved === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
    document.getElementById('themeToggle').textContent = '🌙';
  }

  document.getElementById('themeToggle').addEventListener('click', () => {
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    if (isLight) {
      document.documentElement.removeAttribute('data-theme');
      document.getElementById('themeToggle').textContent = '☀️';
      localStorage.setItem('ftv_theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      document.getElementById('themeToggle').textContent = '🌙';
      localStorage.setItem('ftv_theme', 'light');
    }
  });
}

// ─── FORMAT SELECTOR ────────────────────────
function initFormatSelector() {
  const cards = document.querySelectorAll('.format-card');
  if (!cards.length) return;

  // Set initial active state
  cards.forEach(c => {
    const isActive = c.dataset.variant === selectedVariant;
    c.classList.toggle('active', isActive);
    c.setAttribute('aria-checked', String(isActive));
  });

  cards.forEach(card => {
    card.addEventListener('click', () => {
      cards.forEach(c => { c.classList.remove('active'); c.setAttribute('aria-checked', 'false'); });
      card.classList.add('active');
      card.setAttribute('aria-checked', 'true');
      selectedVariant = card.dataset.variant;
      localStorage.setItem('ftv_variant', selectedVariant);
      if (productGrid) renderProducts();
      if (careerPathGrid) renderCareerPaths();
      if (featuredGrid) renderFeaturedProducts();
    });
  });
}

// ─── VENDOR TABS ────────────────────────────
function initVendorTabs() {
  const tabs = document.querySelectorAll('.vendor-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      selectedVendor = tab.dataset.vendor;
      if (productGrid) renderProducts();
      if (careerPathGrid) renderCareerPaths();
    });
  });
}

// ─── RENDER PRODUCTS ────────────────────────
function renderProducts() {
  if (!productGrid) return;

  // Start with page-scoped products, then apply vendor tab filter
  let pool = getPageProducts();
  const filtered = selectedVendor === 'all'
    ? pool
    : pool.filter(p => p.vendor === selectedVendor);

  const price = PRICING[selectedVariant];
  const variantLabel = VARIANT_LABELS[selectedVariant];

  productGrid.innerHTML = filtered.map(product => {
    const cartKey = `${product.id}__${selectedVariant}`;
    const inCart = cart.some(item => item.key === cartKey);

    return `
      <div class="product-card ${product.popular ? 'popular' : ''}" data-vendor="${esc(product.vendor)}">
        <div class="product-popular">Popular</div>
        <div class="product-vendor">${esc(vendorDisplayName(product.vendor))}</div>
        <div class="product-name">${esc(product.name)}</div>
        <div class="product-meta">${esc(product.meta)}</div>
        <div class="product-features">
          ${product.tags.map(t => `<span class="product-tag">${esc(t)}</span>`).join('')}
        </div>
        ${selectedVariant === 'bundle' ? '<div class="product-bundle-note">📦 Standard + ADHD + Dark + ADHD Dark</div>' : ''}
        <div class="product-bottom">
          <div class="product-price">
            $${price.toFixed(2)}
            ${selectedVariant === 'bundle' ? `<span class="original">$${(PRICING.standard + PRICING.adhd + PRICING.dark + PRICING.adhd_dark).toFixed(2)}</span>` : ''}
          </div>
          <button class="btn-add ${inCart ? 'added' : ''}"
                  data-product-id="${esc(product.id)}"
                  data-product-name="${esc(product.name)}"
                  data-variant="${esc(selectedVariant)}"
                  data-price="${price}"
                  ${inCart ? 'disabled' : ''}>
            ${inCart ? '✓ Added' : 'Add to Cart'}
          </button>
        </div>
      </div>
    `;
  }).join('');
}

// ─── EVENT DELEGATION ──────────────────────
if (productGrid) {
  productGrid.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-add');
    if (!btn || btn.disabled) return;
    addToCart(btn.dataset.productId, btn.dataset.productName, btn.dataset.variant, parseFloat(btn.dataset.price));
  });
}

if (careerPathGrid) {
  careerPathGrid.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-add-career');
    if (!btn || btn.disabled) return;
    addCareerPathToCart(btn.dataset.pathId, btn.dataset.pathName, parseInt(btn.dataset.certCount, 10));
  });
}

function vendorDisplayName(vendor) {
  const map = {
    comptia: 'CompTIA',
    isc2: 'ISC2',
    aws: 'AWS',
    microsoft: 'Microsoft',
    cisco: 'Cisco',
    isaca: 'ISACA',
    giac: 'GIAC',
    google: 'Google Cloud',
    'ec-council': 'EC-Council',
    offsec: 'OffSec',
    hashicorp: 'HashiCorp',
    k8s: 'Kubernetes',
    secops: 'Security Ops',
    lifestyle: 'Lifestyle',
    education: 'Education',
    bundles: 'Bundles',
  };
  return map[vendor] || vendor;
}

// ─── CART MANAGEMENT ────────────────────────
function addToCart(productId, productName, variant, price) {
  const key = `${productId}__${variant}`;
  if (cart.some(item => item.key === key)) return;

  // Check if a career path in cart already includes this cert
  const overlappingPath = cart.find(item => {
    if (!item.productId.startsWith('cp:')) return false;
    if (item.variant !== variant) return false;
    const cpId = item.productId.replace('cp:', '');
    const path = CAREER_PATHS.find(p => p.id === cpId);
    return path && path.certIds.includes(productId);
  });
  if (overlappingPath) {
    showToast(`"${productName}" is already included in the "${overlappingPath.name}" in your cart.`, 'warning');
    return;
  }

  cart.push({
    key,
    productId,
    name: productName,
    variant,
    variantLabel: VARIANT_LABELS[variant],
    price,
  });

  saveCart();
  updateCartUI();
  if (productGrid) renderProducts();
  openCart();

  // Badge bounce animation
  cartBadge.classList.add('bump');
  setTimeout(() => cartBadge.classList.remove('bump'), 300);
}

function removeFromCart(key) {
  cart = cart.filter(item => item.key !== key);
  saveCart();
  updateCartUI();
  if (productGrid) renderProducts();
  if (careerPathGrid) renderCareerPaths();
}

function saveCart() {
  localStorage.setItem('ftv_cart', JSON.stringify(cart));
}

function updateCartUI() {
  // Badge
  cartBadge.textContent = cart.length;
  cartBadge.setAttribute('data-count', cart.length);
  cartBadge.setAttribute('aria-label', `${cart.length} item${cart.length !== 1 ? 's' : ''} in cart`);

  // Cart items
  if (cart.length === 0) {
    cartItems.innerHTML = '';
    cartEmpty.classList.add('active');
    cartFooter.classList.remove('active');
  } else {
    cartEmpty.classList.remove('active');
    cartFooter.classList.add('active');

    cartItems.innerHTML = cart.map(item => `
      <div class="cart-item">
        <div class="cart-item-info">
          <div class="cart-item-name">${esc(item.name)}</div>
          <div class="cart-item-variant">${esc(item.variantLabel)}</div>
          <div class="cart-item-price">$${Number(item.price).toFixed(2)}</div>
        </div>
        <button class="cart-item-remove" data-cart-key="${esc(item.key)}">Remove</button>
      </div>
    `).join('');

    // Total
    const total = cart.reduce((sum, item) => sum + item.price, 0);
    cartTotal.textContent = `$${total.toFixed(2)}`;
  }
}

// ─── CART OPEN/CLOSE ────────────────────────
function openCart() {
  cartSidebar.classList.add('active');
  cartOverlay.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeCart() {
  cartSidebar.classList.remove('active');
  cartOverlay.classList.remove('active');
  document.body.style.overflow = '';
}

cartItems.addEventListener('click', (e) => {
  const btn = e.target.closest('.cart-item-remove');
  if (!btn) return;
  removeFromCart(btn.dataset.cartKey);
});

document.getElementById('cartToggle').addEventListener('click', openCart);
document.getElementById('cartClose').addEventListener('click', closeCart);
cartOverlay.addEventListener('click', closeCart);

// Close cart on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeCart();
});

// ─── RENDER CAREER PATHS ───────────────────
function renderCareerPaths() {
  if (!careerPathGrid) return;

  const isBundle = selectedVariant === 'bundle';
  const variantLabel = VARIANT_LABELS[selectedVariant];

  // Start with page-scoped paths, then apply vendor tab filter
  let pool = getPageCareerPaths();
  const filtered = selectedVendor === 'all'
    ? pool
    : pool.filter(p => p.vendors.includes(selectedVendor));

  // Show/hide career section if no paths match
  const careerSection = careerPathGrid.closest('.career-section');
  if (careerSection) careerSection.style.display = filtered.length === 0 ? 'none' : '';

  careerPathGrid.innerHTML = filtered.map(path => {
    const tier = CAREER_PATH_PRICING[path.certCount];
    const price = isBundle ? tier.bundle : tier.single;
    const indivPrice = isBundle ? tier.indivBundle : tier.indivSingle;
    const savings = Math.round((1 - price / indivPrice) * 100);
    const cartKey = `cp__${path.id}__${selectedVariant}`;
    const inCart = cart.some(item => item.key === cartKey);

    return `
      <div class="career-card">
        <div class="career-card-header">
          <span class="career-icon">${esc(path.icon)}</span>
          <span class="savings-badge">Save ${savings}%</span>
        </div>
        <div class="career-name">${esc(path.name)}</div>
        <div class="career-desc">${esc(path.desc)}</div>
        <div class="career-certs">
          ${path.certs.map(c => `<div class="career-cert-item">✓ ${esc(c)}</div>`).join('')}
        </div>
        <div class="career-includes">${path.certCount} planners · ${esc(variantLabel)} format</div>
        <div class="product-bottom">
          <div class="product-price">
            $${price.toFixed(2)}
            <span class="original">$${indivPrice.toFixed(2)}</span>
          </div>
          <button class="btn-add btn-add-career ${inCart ? 'added' : ''}"
                  data-path-id="${esc(path.id)}"
                  data-path-name="${esc(path.name)}"
                  data-cert-count="${path.certCount}"
                  ${inCart ? 'disabled' : ''}>
            ${inCart ? '✓ Added' : 'Add to Cart'}
          </button>
        </div>
      </div>
    `;
  }).join('');
}

async function addCareerPathToCart(pathId, pathName, certCount) {
  const key = `cp__${pathId}__${selectedVariant}`;
  if (cart.some(item => item.key === key)) return;

  // Check for individual certs in cart that overlap with this career path
  const path = CAREER_PATHS.find(p => p.id === pathId);
  if (path) {
    const overlaps = cart.filter(item => {
      if (item.productId.startsWith('cp:')) return false;
      if (item.variant !== selectedVariant) return false;
      return path.certIds.includes(item.productId);
    });
    if (overlaps.length > 0) {
      const names = overlaps.map(o => o.name).join(', ');
      const proceed = await showConfirm(`You have ${names} individually in your cart (same format). The career path already includes ${overlaps.length === 1 ? 'it' : 'them'} — remove ${overlaps.length === 1 ? 'it' : 'them'} to avoid paying twice?`);
      if (proceed) {
        overlaps.forEach(o => { cart = cart.filter(item => item.key !== o.key); });
      }
    }
  }

  const isBundle = selectedVariant === 'bundle';
  const tier = CAREER_PATH_PRICING[certCount];
  const price = isBundle ? tier.bundle : tier.single;

  cart.push({
    key,
    productId: `cp:${pathId}`,
    name: `${pathName} Career Path`,
    variant: selectedVariant,
    variantLabel: VARIANT_LABELS[selectedVariant],
    price,
  });

  saveCart();
  updateCartUI();
  if (productGrid) renderProducts();
  if (careerPathGrid) renderCareerPaths();
  openCart();

  cartBadge.classList.add('bump');
  setTimeout(() => cartBadge.classList.remove('bump'), 300);
}

// ─── HUB: VENDOR SHOWCASE CARDS ─────────────
function renderHubCards() {
  if (!hubGrid) return;

  hubGrid.innerHTML = Object.entries(VENDOR_META).map(([key, meta]) => {
    const vendorIds = VENDOR_GROUP_MAP[key] || [];
    const count = PRODUCTS.filter(p => vendorIds.includes(p.vendor)).length;

    return `
      <a href="${esc(meta.url)}" class="hub-card" style="--hub-accent: ${meta.color}">
        <div class="hub-card-icon">${meta.icon}</div>
        <div class="hub-card-name">${esc(meta.name)}</div>
        <div class="hub-card-desc">${esc(meta.desc)}</div>
        <div class="hub-card-stats">${count} planner${count !== 1 ? 's' : ''}</div>
        <span class="hub-card-browse">Browse &rarr;</span>
      </a>
    `;
  }).join('');
}

// ─── HUB: FEATURED PRODUCTS ────────────────
function renderFeaturedProducts() {
  if (!featuredGrid) return;

  const price = PRICING[selectedVariant];
  const featured = PRODUCTS.filter(p => p.popular).slice(0, 6);

  featuredGrid.innerHTML = featured.map(product => {
    const cartKey = `${product.id}__${selectedVariant}`;
    const inCart = cart.some(item => item.key === cartKey);

    return `
      <div class="product-card ${product.popular ? 'popular' : ''}" data-vendor="${esc(product.vendor)}">
        <div class="product-popular">Popular</div>
        <div class="product-vendor">${esc(vendorDisplayName(product.vendor))}</div>
        <div class="product-name">${esc(product.name)}</div>
        <div class="product-meta">${esc(product.meta)}</div>
        <div class="product-features">
          ${product.tags.map(t => `<span class="product-tag">${esc(t)}</span>`).join('')}
        </div>
        ${selectedVariant === 'bundle' ? '<div class="product-bundle-note">📦 Standard + ADHD + Dark + ADHD Dark</div>' : ''}
        <div class="product-bottom">
          <div class="product-price">
            $${price.toFixed(2)}
            ${selectedVariant === 'bundle' ? `<span class="original">$${(PRICING.standard + PRICING.adhd + PRICING.dark + PRICING.adhd_dark).toFixed(2)}</span>` : ''}
          </div>
          <button class="btn-add ${inCart ? 'added' : ''}"
                  data-product-id="${esc(product.id)}"
                  data-product-name="${esc(product.name)}"
                  data-variant="${esc(selectedVariant)}"
                  data-price="${price}"
                  ${inCart ? 'disabled' : ''}>
            ${inCart ? '✓ Added' : 'Add to Cart'}
          </button>
        </div>
      </div>
    `;
  }).join('');
}

// Event delegation for featured grid (hub page)
if (featuredGrid) {
  featuredGrid.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-add');
    if (!btn || btn.disabled) return;
    addToCart(btn.dataset.productId, btn.dataset.productName, btn.dataset.variant, parseFloat(btn.dataset.price));
  });
}

// ─── STRIPE CHECKOUT ────────────────────────
if (btnCheckout) {
  btnCheckout.addEventListener('click', async () => {
    if (cart.length === 0) return;

    btnCheckout.disabled = true;
    btnCheckout.textContent = 'Processing...';

    try {
      const stripe = Stripe(STRIPE_PUBLISHABLE_KEY);

      const response = await fetch(CHECKOUT_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          items: cart.map(item => ({
            productId: item.productId,
            name: item.name,
            variant: item.variant,
            variantLabel: item.variantLabel,
            price: item.price,
          })),
        }),
      });

      const data = await response.json();

      if (data.error) {
        showToast(data.error, 'error');
        return;
      }

      // Redirect to Stripe Checkout
      const result = await stripe.redirectToCheckout({ sessionId: data.sessionId });
      if (result.error) {
        showToast(result.error.message, 'error');
      }

    } catch (err) {
      console.error('Checkout error:', err);
      showToast('Something went wrong. Please try again.', 'error');
    } finally {
      btnCheckout.disabled = false;
      btnCheckout.textContent = 'Proceed to Checkout →';
    }
  });
}
