// ============================================
// FixTheVuln Store — Cloudflare Worker
// Stripe Checkout + PDF Delivery from R2
// ============================================
// Environment variables needed:
//   STRIPE_SECRET_KEY    - your Stripe secret key
//   STRIPE_WEBHOOK_SECRET - webhook signing secret
//   RESEND_API_KEY       - Resend API key for emails
//   KIT_DELIVERY_SECRET  - bearer secret for POST /sprint-kit/deliver (also a GitHub secret)
// R2 bucket binding:
//   PLANNERS - bound to fixthevuln-planners R2 bucket
// ============================================

const CERT_NAMES = {
  // CompTIA
  'comptia-a-plus-1201': 'CompTIA A+ Core 1',
  'comptia-a-plus-1202': 'CompTIA A+ Core 2',
  'comptia-security-plus': 'CompTIA Security+',
  'comptia-network-plus': 'CompTIA Network+',
  'comptia-linux-plus': 'CompTIA Linux+',
  'comptia-cloud-plus': 'CompTIA Cloud+',
  'comptia-cysa-plus': 'CompTIA CySA+',
  'comptia-pentest-plus': 'CompTIA PenTest+',
  'comptia-casp-plus': 'CompTIA CASP+',
  'comptia-server-plus': 'CompTIA Server+',
  'comptia-data-plus': 'CompTIA Data+',
  'comptia-project-plus': 'CompTIA Project+',
  'comptia-itf-plus': 'CompTIA ITF+',
  'comptia-secai-plus': 'CompTIA SecAI+',
  // ISC2
  'isc2-cc': 'ISC2 CC',
  'isc2-sscp': 'ISC2 SSCP',
  'isc2-cissp': 'ISC2 CISSP',
  'isc2-ccsp': 'ISC2 CCSP',
  // AWS
  'aws-cloud-practitioner': 'AWS Cloud Practitioner',
  'aws-solutions-architect': 'AWS Solutions Architect',
  'aws-developer': 'AWS Developer Associate',
  'aws-cloudops': 'AWS CloudOps Engineer',
  'aws-security-specialty': 'AWS Security Specialty',
  'aws-database-specialty': 'AWS Database Specialty',
  'aws-machine-learning': 'AWS Machine Learning Specialty',
  'aws-data-engineer': 'AWS Data Engineer Associate',
  // Microsoft
  'ms-az-900': 'Azure Fundamentals',
  'ms-az-104': 'Azure Administrator',
  'ms-az-305': 'Azure Solutions Architect',
  'ms-sc-900': 'Security Fundamentals',
  'ms-ai-900': 'Azure AI Fundamentals',
  'ms-az-500': 'Azure Security Engineer',
  'ms-az-204': 'Azure Developer Associate',
  'ms-az-400': 'Azure DevOps Engineer',
  'ms-dp-900': 'Azure Data Fundamentals',
  'ms-ms-900': 'Microsoft 365 Fundamentals',
  'ms-sc-300': 'Identity & Access Admin',
  'ms-ai-102': 'Azure AI Engineer',
  // Cisco
  'cisco-ccna': 'Cisco CCNA',
  'cisco-ccnp-encor': 'Cisco CCNP ENCOR',
  'cisco-cyberops': 'Cisco CyberOps',
  'cisco-ccnp-security': 'Cisco CCNP Security SCOR',
  'cisco-devnet': 'Cisco DevNet Associate',
  // ISACA
  'isaca-cisa': 'ISACA CISA',
  'isaca-cism': 'ISACA CISM',
  'isaca-crisc': 'ISACA CRISC',
  // PECB
  'pecb-iso27001-li': 'PECB ISO/IEC 27001 Lead Implementer',
  'pecb-iso27001-la': 'PECB ISO/IEC 27001 Lead Auditor',
  // GIAC
  'giac-gsec': 'GIAC GSEC',
  'giac-gcih': 'GIAC GCIH',
  'giac-gpen': 'GIAC GPEN',
  'giac-gcia': 'GIAC GCIA',
  // Google Cloud
  'google-ace': 'Google Cloud Engineer',
  'google-pca': 'Google Cloud Architect',
  'google-cdl': 'Google Cloud Digital Leader',
  'google-pde': 'Google Professional Data Engineer',
  'google-pse': 'Google Cloud Security Engineer',
  // EC-Council
  'ec-ceh': 'EC-Council CEH v13',
  'ec-chfi': 'EC-Council CHFI v11',
  'ec-cnd': 'EC-Council CND v3',
  // OffSec
  'offsec-oscp': 'OffSec OSCP',
  'offsec-oswa': 'OffSec OSWA',
  'offsec-oswe': 'OffSec OSWE',
  // HashiCorp
  'hashicorp-terraform': 'HashiCorp Terraform Associate',
  'hashicorp-vault': 'HashiCorp Vault Associate',
  // Kubernetes
  'k8s-cka': 'Kubernetes CKA',
  'k8s-ckad': 'Kubernetes CKAD',
  'k8s-cks': 'Kubernetes CKS',
  // Security Ops
  'vuln-remediation-planner': 'Vulnerability Remediation Planner',
  // Lifestyle & Productivity
  'budget-binder': 'Budget Binder',
  'wellness-journal': 'Wellness Journal',
  '2026-digital-planner': '2026 Digital Planner',
  'business-templates': 'Business Templates',
  // Education
  'teacher-planner': 'Teacher Planner',
  'student-planner': 'Student Planner',
  'adhd-student-planner': 'ADHD Student Planner Spring 2026',
  // Bundles
  'lifestyle-bundle': 'Productivity Bundle (Budget Binder + 2026 Planner + Wellness Journal)',
  'comptia-complete': 'CompTIA Complete (all 14 planners)',
  'microsoft-complete': 'Microsoft Complete (all 12 planners)',
  'aws-complete': 'AWS Complete (all 8 planners)',
};

const VARIANT_LABELS = {
  standard:  'Standard',
  adhd:      'ADHD-Friendly',
  dark:      'Dark Mode',
  adhd_dark: 'ADHD-Friendly Dark',
  bundle:    '4-Format Bundle',
};

// ─── CAREER PATH BUNDLES ───────────────────────
const CAREER_PATHS = {
  'comptia-trifecta':      ['comptia-a-plus-1201', 'comptia-a-plus-1202', 'comptia-network-plus', 'comptia-security-plus'],
  'comptia-a-plus':        ['comptia-a-plus-1201', 'comptia-a-plus-1202'],
  'comptia-security-track':['comptia-security-plus', 'comptia-cysa-plus', 'comptia-pentest-plus', 'comptia-casp-plus'],
  'security-pro':          ['comptia-security-plus', 'isc2-cissp'],
  'aws-track':             ['aws-cloud-practitioner', 'aws-solutions-architect', 'aws-developer'],
  'azure-track':           ['ms-az-900', 'ms-az-104', 'ms-az-305'],
  'cloud-fundamentals':    ['aws-cloud-practitioner', 'ms-az-900', 'google-ace'],
  'isaca-grc':             ['isaca-cisa', 'isaca-cism', 'isaca-crisc'],
  'isc2-path':             ['isc2-cc', 'isc2-sscp', 'isc2-cissp'],
  'cisco-path':            ['cisco-ccna', 'cisco-ccnp-encor', 'cisco-cyberops'],
};

const CAREER_PATH_NAMES = {
  'comptia-trifecta':       'CompTIA Trifecta',
  'comptia-a-plus':         'CompTIA A+ Complete',
  'comptia-security-track': 'CompTIA Security Track',
  'security-pro':           'Security Pro',
  'aws-track':              'AWS Track',
  'azure-track':            'Azure Track',
  'cloud-fundamentals':     'Cloud Fundamentals',
  'isaca-grc':              'ISACA GRC',
  'isc2-path':              'ISC2 Path',
  'cisco-path':             'Cisco Path',
};

// Stripe caps a metadata value at 500 chars, so a long purchase list spans purchased_items,
// purchased_items_2, ... (whole items only, never split mid-id). Stripe allows 50 keys; the cart cap is 20 lines.
function purchasedItemsMetadata(rawItems) {
  const chunks = [''];
  for (const item of rawItems) {
    const next = chunks[chunks.length - 1] ? `${chunks[chunks.length - 1]},${item}` : item;
    if (next.length <= 480) chunks[chunks.length - 1] = next;
    else chunks.push(item);
  }
  return Object.fromEntries(chunks.map((c, i) => [i ? `purchased_items_${i + 1}` : 'purchased_items', c]));
}

function readPurchasedItems(metadata) {
  const index = key => (key === 'purchased_items' ? 1 : Number(key.slice('purchased_items_'.length)));
  return Object.keys(metadata || {})
    .filter(key => /^purchased_items(_\d+)?$/.test(key))
    .sort((a, b) => index(a) - index(b))
    .flatMap(key => String(metadata[key]).split(','))
    .filter(Boolean);
}

// Expand career path items (cp:pathId:variant) into individual cert items (certId__variant)
function expandPurchasedItems(rawItems) {
  const expanded = new Set();
  for (const item of rawItems) {
    if (item.startsWith('cp:')) {
      // Career path format: cp:pathId:variant
      const parts = item.split(':');
      const pathId = parts[1];
      const variant = parts[2];
      const certs = CAREER_PATHS[pathId] || [];
      for (const certId of certs) {
        if (variant === 'bundle') {
          expanded.add(`${certId}__bundle`);
        } else {
          expanded.add(`${certId}__${variant}`);
        }
      }
    } else {
      // Multi-planner product bundles deliver their component planners in the purchased format
      const [productId, variant] = item.split('__');
      const pb = PRODUCT_BUNDLE_PRICING[productId];
      if (pb) {
        for (const id of pb.items) expanded.add(`${id}__${variant}`);
      } else {
        expanded.add(item);
      }
    }
  }
  return [...expanded];
}

// ─── SERVER-SIDE PRICING (source of truth) ──────
const PRICING = {
  standard:  999,  // cents
  adhd:      999,
  dark:      999,
  adhd_dark: 999,
  bundle:    2499,
};

// Career path pricing by cert count (cents)
const CP_PRICING = {
  2: { single: 1499, bundle: 2699 },
  3: { single: 2199, bundle: 3699 },
  4: { single: 2899, bundle: 4699 },
};

// Multi-planner bundles sold as one product (cents): 25% off the planners bought separately.
// Delivered as the component planners (expandPurchasedItems), so no bundle file of its own exists in R2.
// The *-complete vendor packs are sold only in the 4-format bundle variant (see PRODUCT_FORMATS) and are
// priced as the anchor tier above the $24.99 per-cert bundle.
const PRODUCT_BUNDLE_PRICING = {
  'lifestyle-bundle': { items: ['budget-binder', '2026-digital-planner', 'wellness-journal'], single: 2247 },
  'comptia-complete': { items: ['comptia-a-plus-1201', 'comptia-a-plus-1202', 'comptia-security-plus', 'comptia-network-plus', 'comptia-linux-plus', 'comptia-cloud-plus', 'comptia-cysa-plus', 'comptia-pentest-plus', 'comptia-casp-plus', 'comptia-server-plus', 'comptia-data-plus', 'comptia-project-plus', 'comptia-itf-plus', 'comptia-secai-plus'], single: 7900 },
  'microsoft-complete': { items: ['ms-az-900', 'ms-az-104', 'ms-az-305', 'ms-sc-900', 'ms-ai-900', 'ms-az-500', 'ms-az-204', 'ms-az-400', 'ms-dp-900', 'ms-ms-900', 'ms-sc-300', 'ms-ai-102'], single: 6900 },
  'aws-complete': { items: ['aws-cloud-practitioner', 'aws-solutions-architect', 'aws-developer', 'aws-cloudops', 'aws-security-specialty', 'aws-database-specialty', 'aws-machine-learning', 'aws-data-engineer'], single: 5900 },
};

// Formats that actually exist in R2 for products that don't have all five (checked 2026-10-21).
// Products not listed have every format.
const PRODUCT_FORMATS = {
  'budget-binder':        ['standard', 'adhd', 'dark'],
  'wellness-journal':     ['standard', 'adhd', 'dark'],
  '2026-digital-planner': ['standard', 'adhd', 'dark'],
  'business-templates':   ['standard', 'adhd', 'dark', 'adhd_dark'],
  'lifestyle-bundle':     ['standard', 'adhd', 'dark'],
  'comptia-complete':     ['bundle'],
  'microsoft-complete':   ['bundle'],
  'aws-complete':         ['bundle'],
  'teacher-planner':      ['standard', 'adhd', 'dark', 'adhd_dark'],
  'student-planner':      ['standard', 'adhd', 'dark', 'adhd_dark'],
  'adhd-student-planner': ['standard', 'dark'],
};

// Valid product IDs = all keys in CERT_NAMES
const VALID_CERT_IDS = new Set(Object.keys(CERT_NAMES));

function getServerPrice(productId, variant) {
  if (productId.startsWith('cp:')) {
    const pathId = productId.replace('cp:', '');
    const certs = CAREER_PATHS[pathId];
    if (!certs) return null;
    const tier = CP_PRICING[certs.length];
    if (!tier) return null;
    return variant === 'bundle' ? tier.bundle : tier.single;
  }
  // Reject unknown product IDs
  if (!VALID_CERT_IDS.has(productId)) return null;
  const pb = PRODUCT_BUNDLE_PRICING[productId];
  // Own-property checks: a client variant like 'constructor' must not match an inherited member
  if (!Object.hasOwn(PRICING, variant)) return null;
  // Refuse to sell a format we can't deliver
  if (Object.hasOwn(PRODUCT_FORMATS, productId) && !PRODUCT_FORMATS[productId].includes(variant)) return null;
  if (pb) return pb.single;
  return PRICING[variant];
}

function getServerProductName(productId) {
  if (productId.startsWith('cp:')) {
    const pathId = productId.replace('cp:', '');
    return (CAREER_PATH_NAMES[pathId] || pathId) + ' Career Path';
  }
  return CERT_NAMES[productId] || productId;
}

const ALLOWED_ORIGINS = [
  'https://fixthevuln.com',
  'http://localhost',
  'http://127.0.0.1',
];

function getCorsHeaders(request) {
  const origin = request.headers.get('Origin') || '';
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
  };
}

export default {
  async fetch(request, env) {
    const cors = getCorsHeaders(request);
    const url = new URL(request.url);

    // Handle preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }

    // ─── ROUTE: POST /checkout ──────────────────
    // Creates a Stripe Checkout Session
    if (request.method === 'POST' && (url.pathname === '/' || url.pathname === '/checkout')) {
      return handleCheckout(request, env, cors);
    }

    // ─── ROUTE: POST /verify ────────────────────
    // Verifies payment and returns download links
    if (request.method === 'POST' && url.pathname === '/verify') {
      return handleVerify(request, env, cors);
    }

    // ─── ROUTE: POST /webhook ──────────────────
    // Stripe webhook for purchase notifications
    if (request.method === 'POST' && url.pathname === '/webhook') {
      return handleWebhook(request, env);
    }

    // ─── ROUTE: GET /download ───────────────────
    // Serves a PDF from R2 after verifying the token
    if (request.method === 'GET' && url.pathname === '/download') {
      return handleDownload(request, env, cors);
    }

    // ─── ROUTE: POST /errors ──────────────────
    // Client error reporting
    if (request.method === 'POST' && url.pathname === '/errors') {
      return handleClientError(request, env, cors);
    }

    // ─── ROUTE: GET /errors ──────────────────
    // Admin error log (protected by secret header)
    if (request.method === 'GET' && url.pathname === '/errors') {
      return handleAdminErrors(request, env, cors);
    }

    // ─── ROUTE: POST /quiz/submit ──────────────
    // Quiz analytics: session + per-question events
    if (request.method === 'POST' && url.pathname === '/quiz/submit') {
      return handleQuizSubmit(request, env, cors);
    }

    // ─── ROUTE: GET /quiz-analytics ────────────
    // Admin quiz analytics dashboard (protected by secret key param)
    if (request.method === 'GET' && url.pathname === '/quiz-analytics') {
      return handleQuizAnalytics(request, env, cors);
    }

    // ─── ROUTE: POST /classifier-feedback ──────
    // Vulnerability classifier user feedback (Phase 3 CyberMoE RLHF loop)
    if (request.method === 'POST' && url.pathname === '/classifier-feedback') {
      return handleClassifierFeedback(request, env, cors);
    }

    // ─── ROUTE: POST /sprint-kit/deliver ───────
    // Monthly kit email to active subscribers (called by generate-sprint-kit.yml)
    if (request.method === 'POST' && url.pathname === '/sprint-kit/deliver') {
      return handleKitDelivery(request, env);
    }

    return new Response(JSON.stringify({ error: 'Not found' }), {
      status: 404,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  },
};

// ─── CHECKOUT HANDLER ───────────────────────────
const CHECKOUT_RATE_LIMIT = new Map(); // IP -> { count, resetAt }

async function handleCheckout(request, env, cors) {
  // Rate limit: 5 requests/minute per IP (each call hits Stripe API)
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const now = Date.now();
  const limit = CHECKOUT_RATE_LIMIT.get(ip);
  if (limit) {
    if (now < limit.resetAt) {
      if (limit.count >= 5) {
        return new Response(JSON.stringify({ error: 'Too many requests. Please try again later.' }), {
          status: 429, headers: { ...cors, 'Content-Type': 'application/json' },
        });
      }
      limit.count++;
    } else {
      CHECKOUT_RATE_LIMIT.set(ip, { count: 1, resetAt: now + 60000 });
    }
  } else {
    CHECKOUT_RATE_LIMIT.set(ip, { count: 1, resetAt: now + 60000 });
  }
  if (CHECKOUT_RATE_LIMIT.size > 500) {
    for (const [k, v] of CHECKOUT_RATE_LIMIT) {
      if (now > v.resetAt) CHECKOUT_RATE_LIMIT.delete(k);
    }
  }

  try {
    const { items, utm } = await request.json();

    if (!items || !items.length) {
      return new Response(JSON.stringify({ error: 'No items provided' }), {
        status: 400,
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }

    // Cap items to prevent abuse
    if (items.length > 20) {
      return new Response(JSON.stringify({ error: 'Too many items (max 20)' }), {
        status: 400,
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }

    // Build line items using SERVER-SIDE pricing + names (never trust client values)
    const line_items = [];
    for (const item of items) {
      const unitAmount = getServerPrice(item.productId, item.variant);
      if (!unitAmount) {
        return new Response(JSON.stringify({ error: 'Invalid product or variant' }), {
          status: 400,
          headers: { ...cors, 'Content-Type': 'application/json' },
        });
      }
      // Server-side name + variant lookup (don't trust any client-provided display values)
      const productName = getServerProductName(item.productId);
      const variantLabel = Object.hasOwn(VARIANT_LABELS, item.variant) ? VARIANT_LABELS[item.variant] : null;
      if (!variantLabel) {
        return new Response(JSON.stringify({ error: 'Invalid variant' }), {
          status: 400,
          headers: { ...cors, 'Content-Type': 'application/json' },
        });
      }
      line_items.push({
        price_data: {
          currency: 'usd',
          unit_amount: unitAmount,
          product_data: {
            name: `${productName} — ${variantLabel}`,
            description: `Certification Study Planner (${variantLabel} format)`,
            metadata: {
              cert_id: item.productId,
              variant: item.variant,
            },
          },
        },
        quantity: 1,
      });
    }

    // Store product info in session metadata for later retrieval
    // Career paths use compact format: cp:pathId:variant
    const purchasedItems = items.map(item => {
      if (item.productId.startsWith('cp:')) {
        return `${item.productId}:${item.variant}`;
      }
      return `${item.productId}__${item.variant}`;
    });

    const params = new URLSearchParams();
    params.append('mode', 'payment');
    params.append('success_url', 'https://fixthevuln.com/store/success.html?session_id={CHECKOUT_SESSION_ID}');
    params.append('cancel_url', 'https://fixthevuln.com/store/store.html');
    for (const [key, value] of Object.entries(purchasedItemsMetadata(purchasedItems))) {
      params.append(`metadata[${key}]`, value);
    }
    // Referral attribution (optional). Only short slug-like values reach Stripe metadata.
    for (const key of ['source', 'medium', 'campaign']) {
      const value = utm?.[key];
      if (typeof value === 'string' && /^[\w.-]{1,50}$/.test(value)) {
        params.append(`metadata[utm_${key}]`, value);
      }
    }
    params.append('automatic_tax[enabled]', 'true');
    params.append('allow_promotion_codes', 'true');

    line_items.forEach((item, i) => {
      params.append(`line_items[${i}][price_data][currency]`, item.price_data.currency);
      params.append(`line_items[${i}][price_data][unit_amount]`, item.price_data.unit_amount);
      params.append(`line_items[${i}][price_data][tax_behavior]`, 'exclusive');
      params.append(`line_items[${i}][price_data][product_data][name]`, item.price_data.product_data.name);
      params.append(`line_items[${i}][price_data][product_data][description]`, item.price_data.product_data.description);
      params.append(`line_items[${i}][price_data][product_data][tax_code]`, 'txcd_10010001');
      params.append(`line_items[${i}][price_data][product_data][metadata][cert_id]`, item.price_data.product_data.metadata.cert_id);
      params.append(`line_items[${i}][price_data][product_data][metadata][variant]`, item.price_data.product_data.metadata.variant);
      params.append(`line_items[${i}][quantity]`, item.quantity);
    });

    const stripeResponse = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: params.toString(),
    });

    const session = await stripeResponse.json();

    if (session.error) {
      // Type and code only: the message and params can echo cart or customer data
      console.error('Stripe checkout error:', session.error.type, session.error.code);
      return new Response(JSON.stringify({ error: 'Could not start checkout. Please try again, or email hello@fixthevuln.com.' }), {
        status: 400,
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({ sessionId: session.id, url: session.url }), {
      status: 200,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });

  } catch (err) {
    console.error('Checkout error:', err.message);
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  }
}

// ─── VERIFY HANDLER ─────────────────────────────
// Checks with Stripe that payment succeeded, returns download info
async function handleVerify(request, env, cors) {
  // Rate limit: 10 requests/minute per IP (each call hits Stripe API)
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const now = Date.now();
  const limit = CHECKOUT_RATE_LIMIT.get(`verify:${ip}`);
  if (limit) {
    if (now < limit.resetAt) {
      if (limit.count >= 10) {
        return new Response(JSON.stringify({ error: 'Too many requests. Please try again later.' }), {
          status: 429, headers: { ...cors, 'Content-Type': 'application/json' },
        });
      }
      limit.count++;
    } else {
      CHECKOUT_RATE_LIMIT.set(`verify:${ip}`, { count: 1, resetAt: now + 60000 });
    }
  } else {
    CHECKOUT_RATE_LIMIT.set(`verify:${ip}`, { count: 1, resetAt: now + 60000 });
  }
  if (CHECKOUT_RATE_LIMIT.size > 500) {
    for (const [k, v] of CHECKOUT_RATE_LIMIT) {
      if (now > v.resetAt) CHECKOUT_RATE_LIMIT.delete(k);
    }
  }

  try {
    const { sessionId } = await request.json();

    if (!sessionId) {
      return new Response(JSON.stringify({ error: 'No session ID provided' }), {
        status: 400,
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }

    // Retrieve checkout session from Stripe
    const stripeResponse = await fetch(
      `https://api.stripe.com/v1/checkout/sessions/${encodeURIComponent(sessionId)}`,
      {
        headers: {
          'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}`,
        },
      }
    );

    const session = await stripeResponse.json();

    if (session.error || session.payment_status !== 'paid') {
      return new Response(JSON.stringify({ error: 'Payment not verified' }), {
        status: 403,
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }

    // Get purchased items from session metadata and expand career paths
    const rawItems = readPurchasedItems(session.metadata);
    const items = expandPurchasedItems(rawItems);

    // Anchor expiry to session creation time (not current time) to prevent unlimited replays
    const sessionCreatedMs = (session.created || Math.floor(Date.now() / 1000)) * 1000;
    const downloads = await generateDownloadLinks(sessionId, items, rawItems, env.STRIPE_WEBHOOK_SECRET, sessionCreatedMs);

    return new Response(JSON.stringify({
      verified: true,
      mode: session.mode,
      downloads,
    }), {
      status: 200,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: 'Verification failed' }), {
      status: 500,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  }
}

// ─── DOWNLOAD HANDLER ───────────────────────────
// Serves a PDF from R2 after verifying the download token
async function handleDownload(request, env, cors) {
  try {
    const url = new URL(request.url);
    const token = url.searchParams.get('token');
    const file = url.searchParams.get('file');

    if (!token || !file) {
      return new Response('Missing token or file', { status: 400 });
    }

    // Verify HMAC signature and decode token
    const dotIndex = token.lastIndexOf('.');
    if (dotIndex === -1) {
      return new Response('Invalid token', { status: 403 });
    }
    const payload = token.substring(0, dotIndex);
    const sig = token.substring(dotIndex + 1);

    const validSig = await verifyTokenHmac(payload, sig, env.STRIPE_WEBHOOK_SECRET);
    if (!validSig) {
      return new Response('Invalid token', { status: 403 });
    }

    let tokenData;
    try {
      tokenData = JSON.parse(atob(payload));
    } catch {
      return new Response('Invalid token', { status: 403 });
    }

    // Check expiry
    if (Date.now() > tokenData.expiry) {
      return new Response('Download link expired. Please contact hello@fixthevuln.com for a new link.', { status: 403 });
    }

    // Verify the file was part of the purchase
    const requestedFile = decodeURIComponent(file);
    const validFiles = tokenData.items.map(item => {
      const [certId, variant] = item.split('__');
      return getFilename(certId, variant);
    });

    if (!validFiles.includes(requestedFile)) {
      return new Response('File not part of purchase', { status: 403 });
    }

    // Fetch from R2
    const object = await env.PLANNERS.get(requestedFile);

    if (!object) {
      return new Response('File not found. Please contact hello@fixthevuln.com for assistance.', { status: 404 });
    }

    const contentType = requestedFile.endsWith('.zip') ? 'application/zip' : 'application/pdf';
    return new Response(object.body, {
      headers: {
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${requestedFile}"`,
        'Cache-Control': 'no-store',
      },
    });

  } catch (err) {
    return new Response('Download failed', { status: 500 });
  }
}

// ─── FILENAME MAPPING ───────────────────────────
// Maps cert_id + variant to the PDF filename in R2
function getFilename(certId, variant) {
  // Sprint kit tokens are only minted server-side (kitDownloadUrl), never from cart input
  if (certId === 'sprint-kit') {
    return `patch-sprint-kit-${variant}.pdf`;
  }
  // Bundle variant returns a zip with all 4 formats
  if (variant === 'bundle') {
    return `${certId}_bundle.zip`;
  }
  const variantSuffix = {
    standard:  '',
    adhd:      '_adhd',
    dark:      '_dark',
    adhd_dark: '_adhd_dark',
  };
  return `${certId}${variantSuffix[variant] || ''}_study_planner.pdf`;
}

// ─── TOKEN HMAC SIGNING ─────────────────────────
async function createTokenHmac(data, secret) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw', encoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false, ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(data));
  return Array.from(new Uint8Array(sig))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

async function verifyTokenHmac(data, signature, secret) {
  const expected = await createTokenHmac(data, secret);
  if (expected.length !== signature.length) return false;
  let mismatch = 0;
  for (let i = 0; i < expected.length; i++) {
    mismatch |= expected.charCodeAt(i) ^ signature.charCodeAt(i);
  }
  return mismatch === 0;
}

// ─── SHARED: GENERATE DOWNLOAD LINKS ────────────
async function generateDownloadLinks(sessionId, items, rawItems, secret, sessionCreatedMs) {
  // Expiry anchored to session creation time, not current time — prevents unlimited replay
  const expiry = (sessionCreatedMs || Date.now()) + 24 * 60 * 60 * 1000;
  const payload = btoa(JSON.stringify({ sessionId, items, expiry }));
  const sig = await createTokenHmac(payload, secret);
  const token = `${payload}.${sig}`;

  // Build a map: certId → careerPathId for grouping on the success page
  const certToPath = {};
  if (rawItems) {
    for (const raw of rawItems) {
      if (raw.startsWith('cp:')) {
        const parts = raw.split(':');
        const pathId = parts[1];
        const certs = CAREER_PATHS[pathId] || [];
        for (const certId of certs) {
          certToPath[certId] = pathId;
        }
      }
    }
  }

  return items.map(item => {
    const [certId, variant] = item.split('__');
    const filename = getFilename(certId, variant);
    const dl = {
      certId,
      variant,
      filename,
      url: `https://fixthevuln-checkout.robertflores17.workers.dev/download?token=${encodeURIComponent(token)}&file=${encodeURIComponent(filename)}`,
    };
    if (certToPath[certId]) {
      dl.careerPathId = certToPath[certId];
      dl.careerPathName = CAREER_PATH_NAMES[certToPath[certId]] || certToPath[certId];
    }
    return dl;
  });
}

// ─── STRIPE SIGNATURE VERIFICATION ──────────────
async function verifyStripeSignature(payload, sigHeader, secret) {
  if (!sigHeader) return false;

  const parts = {};
  for (const pair of sigHeader.split(',')) {
    const [key, value] = pair.split('=');
    parts[key] = value;
  }

  const timestamp = parts['t'];
  const signature = parts['v1'];
  if (!timestamp || !signature) return false;

  // Reject timestamps older than 5 minutes
  const age = Math.abs(Date.now() / 1000 - parseInt(timestamp, 10));
  if (age > 300) return false;

  // Compute expected signature
  const signedPayload = `${timestamp}.${payload}`;
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const mac = await crypto.subtle.sign('HMAC', key, encoder.encode(signedPayload));
  const expected = Array.from(new Uint8Array(mac))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');

  // Constant-time comparison
  if (expected.length !== signature.length) return false;
  let mismatch = 0;
  for (let i = 0; i < expected.length; i++) {
    mismatch |= expected.charCodeAt(i) ^ signature.charCodeAt(i);
  }
  return mismatch === 0;
}

// ─── WEBHOOK HANDLER ────────────────────────────
async function handleWebhook(request, env) {
  const payload = await request.text();
  const sigHeader = request.headers.get('stripe-signature');

  const valid = await verifyStripeSignature(payload, sigHeader, env.STRIPE_WEBHOOK_SECRET);
  if (!valid) {
    return new Response(JSON.stringify({ error: 'Invalid signature' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Always return 200 to prevent Stripe retries
  try {
    const event = JSON.parse(payload);

    if (event.type === 'checkout.session.completed') {
      const session = event.data.object;
      const customerEmail = session.customer_details?.email;
      const amountCents = session.amount_total;
      const rawItems = readPurchasedItems(session.metadata);
      const items = expandPurchasedItems(rawItems);

      if (items.length > 0) {
        const sessionCreatedMs = (session.created || Math.floor(Date.now() / 1000)) * 1000;
        const downloads = await generateDownloadLinks(session.id, items, rawItems, env.STRIPE_WEBHOOK_SECRET, sessionCreatedMs);

        // Send customer email + seller notification in parallel
        const promises = [];

        if (customerEmail) {
          promises.push(sendCustomerEmail(env, customerEmail, downloads, items));
        }
        promises.push(sendSellerNotification(env, customerEmail, downloads, items, amountCents, session.metadata?.utm_source));

        await Promise.allSettled(promises);
      }

      // Sprint kit subscription: welcome email with the current kit. The Stripe
      // account is shared with CyberFolio, so match on the kit's price, not mode.
      if (session.mode === 'subscription' && customerEmail && await isKitSession(env, session.id)) {
        const month = await latestKitMonth(env);
        await Promise.allSettled([
          resendPost(env, 'emails', kitEmail(customerEmail, month, month && await kitDownloadUrl(env, month), true)),
          sendSellerNotification(env, customerEmail, [{ certId: 'Patch Tuesday Sprint Kit', variant: 'monthly subscription' }], [], amountCents, session.metadata?.utm_source),
        ]);
      }
    }
  } catch (err) {
    // Log but still return 200 to prevent retries
    console.error('Webhook processing error:', err);
  }

  return new Response(JSON.stringify({ received: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}

// ─── CUSTOMER EMAIL ─────────────────────────────
async function sendCustomerEmail(env, toEmail, downloads, items) {
  // Group downloads by career path for nicer email layout
  const grouped = {};
  const individual = [];
  for (const dl of downloads) {
    if (dl.careerPathId) {
      if (!grouped[dl.careerPathId]) grouped[dl.careerPathId] = [];
      grouped[dl.careerPathId].push(dl);
    } else {
      individual.push(dl);
    }
  }

  function renderRow(dl) {
    const certName = CERT_NAMES[dl.certId] || dl.certId;
    const variantLabel = VARIANT_LABELS[dl.variant] || dl.variant;
    return `
      <tr>
        <td style="padding:12px 16px;border-bottom:1px solid #e5e7eb;">
          <strong style="color:#1e293b;">${escapeHtml(certName)}</strong>
          <span style="display:inline-block;background:#eff6ff;color:#2563eb;padding:2px 8px;border-radius:50px;font-size:11px;font-weight:600;margin-left:6px;">${escapeHtml(variantLabel)}</span>
          <br><span style="color:#64748b;font-size:13px;">${escapeHtml(dl.filename)}</span>
        </td>
        <td style="padding:12px 16px;border-bottom:1px solid #e5e7eb;text-align:right;">
          <a href="${escapeHtml(dl.url)}" style="display:inline-block;background:#2563eb;color:#ffffff;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">Download</a>
        </td>
      </tr>`;
  }

  function renderGroupHeader(name) {
    return `
      <tr>
        <td colspan="2" style="padding:16px 16px 8px;background:#f8fafc;border-bottom:1px solid #e5e7eb;">
          <strong style="color:#1e293b;font-size:15px;">${escapeHtml(name)} Career Path</strong>
        </td>
      </tr>`;
  }

  let itemRows = '';
  for (const [pathId, dls] of Object.entries(grouped)) {
    const pathName = CAREER_PATH_NAMES[pathId] || pathId;
    itemRows += renderGroupHeader(pathName);
    itemRows += dls.map(renderRow).join('');
  }
  if (individual.length > 0) {
    if (Object.keys(grouped).length > 0) {
      itemRows += renderGroupHeader('Individual Planners');
    }
    itemRows += individual.map(renderRow).join('');
  }

  const html = `
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <div style="max-width:600px;margin:0 auto;padding:40px 20px;">
    <div style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
      <!-- Header -->
      <div style="background:#2563eb;padding:32px 24px;text-align:center;">
        <h1 style="color:#ffffff;margin:0;font-size:24px;font-weight:700;">FixTheVuln</h1>
        <p style="color:rgba(255,255,255,0.85);margin:8px 0 0;font-size:15px;">Your study planners are ready!</p>
      </div>
      <!-- Body -->
      <div style="padding:32px 24px;">
        <p style="color:#1e293b;font-size:16px;line-height:1.6;margin:0 0 24px;">
          Thank you for your purchase! Your certification study planners are ready to download. Click the buttons below to save your files.
        </p>
        <table style="width:100%;border-collapse:collapse;margin-bottom:24px;">
          ${itemRows}
        </table>
        <div style="background:#fef3c7;border:1px solid #fde68a;border-radius:8px;padding:14px 16px;margin-bottom:24px;">
          <p style="margin:0;color:#92400e;font-size:13px;">
            ⏰ <strong>Download links expire in 24 hours.</strong> Please save your files after downloading.
          </p>
        </div>
        <p style="color:#64748b;font-size:14px;line-height:1.6;margin:0;">
          If you have any questions, reply to this email or contact us at
          <a href="mailto:hello@fixthevuln.com" style="color:#2563eb;">hello@fixthevuln.com</a>
        </p>
      </div>
      <!-- Footer -->
      <div style="border-top:1px solid #e5e7eb;padding:20px 24px;text-align:center;">
        <p style="margin:0;color:#94a3b8;font-size:12px;">&copy; 2026 FixTheVuln &middot; Educational resources for security professionals</p>
      </div>
    </div>
  </div>
</body>
</html>`;

  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'FixTheVuln <hello@fixthevuln.com>',
      to: [toEmail],
      subject: 'Your FixTheVuln Study Planners Are Ready!',
      html,
    }),
  });
}

// ─── SELLER NOTIFICATION ────────────────────────
async function sendSellerNotification(env, customerEmail, downloads, items, amountCents, utmSource) {
  // Build subject: prefer career path names over listing every cert
  const pathNames = [...new Set(downloads.filter(dl => dl.careerPathName).map(dl => dl.careerPathName))];
  const individualNames = downloads.filter(dl => !dl.careerPathId).map(dl => CERT_NAMES[dl.certId] || dl.certId);
  const certNames = [...pathNames.map(n => `${n} Path`), ...individualNames].join(', ') || 'Unknown';

  const itemList = [];
  if (pathNames.length > 0) {
    for (const name of pathNames) {
      const pathDls = downloads.filter(dl => dl.careerPathName === name);
      const variant = VARIANT_LABELS[pathDls[0]?.variant] || pathDls[0]?.variant;
      itemList.push(`• ${name} Career Path (${variant}) — ${pathDls.length} planners`);
    }
  }
  for (const dl of downloads.filter(d => !d.careerPathId)) {
    const certName = CERT_NAMES[dl.certId] || dl.certId;
    const variantLabel = VARIANT_LABELS[dl.variant] || dl.variant;
    itemList.push(`• ${certName} (${variantLabel})`);
  }
  const itemListStr = itemList.join('\n');

  const amount = amountCents ? `$${(amountCents / 100).toFixed(2)}` : 'N/A';

  const html = `
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <div style="max-width:600px;margin:0 auto;padding:40px 20px;">
    <div style="background:#ffffff;border-radius:12px;padding:32px 24px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
      <h2 style="color:#1e293b;margin:0 0 20px;font-size:20px;">New Sale! 🎉</h2>
      <table style="width:100%;border-collapse:collapse;">
        <tr>
          <td style="padding:8px 0;color:#64748b;font-size:14px;width:120px;">Customer</td>
          <td style="padding:8px 0;color:#1e293b;font-size:14px;font-weight:600;">${escapeHtml(customerEmail || 'No email provided')}</td>
        </tr>
        <tr>
          <td style="padding:8px 0;color:#64748b;font-size:14px;">Amount</td>
          <td style="padding:8px 0;color:#1e293b;font-size:14px;font-weight:600;">${amount}</td>
        </tr>
        <tr>
          <td style="padding:8px 0;color:#64748b;font-size:14px;">Source</td>
          <td style="padding:8px 0;color:#1e293b;font-size:14px;font-weight:600;">${escapeHtml(utmSource || 'Direct / unknown')}</td>
        </tr>
        <tr>
          <td style="padding:8px 0;color:#64748b;font-size:14px;vertical-align:top;">Items</td>
          <td style="padding:8px 0;color:#1e293b;font-size:14px;white-space:pre-line;">${escapeHtml(itemListStr)}</td>
        </tr>
      </table>
    </div>
  </div>
</body>
</html>`;

  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'FixTheVuln Store <hello@fixthevuln.com>',
      to: ['hello@fixthevuln.com'],
      subject: `New Sale: ${certNames}`,
      html,
    }),
  });
}

// ─── PATCH TUESDAY SPRINT KIT SUBSCRIPTION ─────
const KIT_PRICE_ID = 'price_1T45YOLBnrzacKtTCA08o8PY';
const KIT_LINK_TTL_MS = 7 * 24 * 60 * 60 * 1000;

async function stripeGet(env, path) {
  const res = await fetch(`https://api.stripe.com/v1/${path}`, {
    headers: { 'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}` },
  });
  const data = await res.json();
  if (!res.ok) throw new Error(`Stripe ${path.split('?')[0]}: ${data.error?.message || res.status}`);
  return data;
}

async function isKitSession(env, sessionId) {
  const items = await stripeGet(env, `checkout/sessions/${encodeURIComponent(sessionId)}/line_items`);
  return items.data.some(li => li.price?.id === KIT_PRICE_ID);
}

// Latest kit in R2, as YYYY-MM (keys sort chronologically)
async function latestKitMonth(env) {
  const { objects } = await env.PLANNERS.list({ prefix: 'patch-sprint-kit-' });
  const months = objects.map(o => o.key.match(/^patch-sprint-kit-(\d{4}-\d{2})\.pdf$/)?.[1]).filter(Boolean);
  return months.sort().pop() || null;
}

async function kitDownloadUrl(env, month) {
  const payload = btoa(JSON.stringify({ sessionId: `kit-${month}`, items: [`sprint-kit__${month}`], expiry: Date.now() + KIT_LINK_TTL_MS }));
  const token = `${payload}.${await createTokenHmac(payload, env.STRIPE_WEBHOOK_SECRET)}`;
  return `https://fixthevuln-checkout.robertflores17.workers.dev/download?token=${encodeURIComponent(token)}&file=${encodeURIComponent(getFilename('sprint-kit', month))}`;
}

function kitMonthLabel(month) {
  const [y, m] = month.split('-').map(Number);
  return new Date(Date.UTC(y, m - 1, 1)).toLocaleString('en-US', { month: 'long', year: 'numeric', timeZone: 'UTC' });
}

// Builds one kit email. url is null only for a welcome sent before any kit exists.
function kitEmail(toEmail, month, url, welcome) {
  const label = month ? kitMonthLabel(month) : '';
  const subject = welcome
    ? 'Welcome to the Patch Tuesday Sprint Kit'
    : `Your ${label} Patch Tuesday Sprint Kit`;
  const intro = welcome
    ? 'Thanks for subscribing. Each new kit arrives by email the day after Patch Tuesday.'
      + (url ? ` Here's the current one (${escapeHtml(label)}) so you can start now.` : '')
    : `The ${escapeHtml(label)} kit is ready: this cycle's CISA KEV additions, pre-filled triage matrix, 14-day sprint calendar and executive summary.`;
  const button = url ? `
        <p style="text-align:center;margin:0 0 24px;">
          <a href="${escapeHtml(url)}" style="display:inline-block;background:#2563eb;color:#ffffff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;font-size:15px;">Download the ${escapeHtml(label)} kit</a>
        </p>
        <p style="color:#92400e;font-size:13px;margin:0 0 24px;">This link expires in 7 days. Please save the PDF after downloading.</p>` : '';

  const html = `
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <div style="max-width:600px;margin:0 auto;padding:40px 20px;">
    <div style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
      <div style="background:#2563eb;padding:32px 24px;text-align:center;">
        <h1 style="color:#ffffff;margin:0;font-size:24px;font-weight:700;">FixTheVuln</h1>
        <p style="color:rgba(255,255,255,0.85);margin:8px 0 0;font-size:15px;">Patch Tuesday Sprint Kit</p>
      </div>
      <div style="padding:32px 24px;">
        <p style="color:#1e293b;font-size:16px;line-height:1.6;margin:0 0 24px;">${intro}</p>${button}
        <p style="color:#64748b;font-size:14px;line-height:1.6;margin:0;">
          Questions? Reply to this email or contact
          <a href="mailto:hello@fixthevuln.com" style="color:#2563eb;">hello@fixthevuln.com</a>
        </p>
      </div>
      <div style="border-top:1px solid #e5e7eb;padding:20px 24px;text-align:center;">
        <p style="margin:0;color:#94a3b8;font-size:12px;">&copy; 2026 FixTheVuln &middot; Educational resources for security professionals</p>
      </div>
    </div>
  </div>
</body>
</html>`;

  return { from: 'FixTheVuln <hello@fixthevuln.com>', to: [toEmail], subject, html };
}

// path is 'emails' (one message) or 'emails/batch' (array of up to 100)
async function resendPost(env, path, body) {
  const res = await fetch(`https://api.resend.com/${path}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Resend ${res.status}`);
}

async function activeKitSubscriberEmails(env) {
  const emails = new Set();
  let after = '';
  while (true) {
    const page = await stripeGet(env, `subscriptions?price=${KIT_PRICE_ID}&status=active&limit=100&expand[]=data.customer${after}`);
    for (const sub of page.data) {
      if (sub.customer?.email) emails.add(sub.customer.email);
    }
    if (!page.has_more) break;
    after = `&starting_after=${page.data[page.data.length - 1].id}`;
  }
  return [...emails];
}

function safeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let mismatch = 0;
  for (let i = 0; i < a.length; i++) mismatch |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return mismatch === 0;
}

// POST { month: 'YYYY-MM', dry_run?: bool } with Authorization: Bearer KIT_DELIVERY_SECRET.
// An R2 marker per month, claimed before sending, makes reruns and overlapping
// calls no-ops: a crash mid-send means a missed month, never a duplicate.
async function handleKitDelivery(request, env) {
  const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
  const auth = request.headers.get('Authorization') || '';
  if (!env.KIT_DELIVERY_SECRET || !safeEqual(auth, `Bearer ${env.KIT_DELIVERY_SECRET}`)) {
    return json({ error: 'Unauthorized' }, 401);
  }

  let body;
  try { body = await request.json(); } catch { return json({ error: 'Invalid JSON' }, 400); }
  const month = body.month;
  if (typeof month !== 'string' || !/^\d{4}-(0[1-9]|1[0-2])$/.test(month)) {
    return json({ error: 'month must be YYYY-MM' }, 400);
  }
  if (!await env.PLANNERS.head(getFilename('sprint-kit', month))) {
    return json({ error: `No kit in R2 for ${month}` }, 404);
  }
  const marker = `sprint-kit-deliveries/${month}.json`;
  if (await env.PLANNERS.head(marker)) {
    return json({ month, skipped: 'already delivered' });
  }

  const emails = await activeKitSubscriberEmails(env);
  if (body.dry_run) return json({ month, dry_run: true, subscribers: emails.length });

  await env.PLANNERS.put(marker, JSON.stringify({ status: 'sending', startedAt: new Date().toISOString() }));

  // Resend batch: 100 messages per call keeps us far under Workers' subrequest cap and Resend's 2 req/s
  const url = await kitDownloadUrl(env, month);
  const failed = [];
  for (let i = 0; i < emails.length; i += 100) {
    const chunk = emails.slice(i, i + 100);
    try { await resendPost(env, 'emails/batch', chunk.map(e => kitEmail(e, month, url, false))); } catch { failed.push(...chunk); }
  }
  await env.PLANNERS.put(marker, JSON.stringify({ status: 'done', deliveredAt: new Date().toISOString(), sent: emails.length - failed.length, failed: failed.length }));

  if (failed.length) {
    // ponytail: no automatic retry; failed addresses go to the seller inbox (not the public Actions log) for a manual resend
    await resendPost(env, 'emails', {
      from: 'FixTheVuln Store <hello@fixthevuln.com>',
      to: ['hello@fixthevuln.com'],
      subject: `Sprint kit ${month}: ${failed.length} delivery failure(s)`,
      html: `<p>Kit emails failed for:</p><pre>${escapeHtml(failed.join('\n'))}</pre>`,
    }).catch(err => console.error('Failure notice not sent:', err.message));
  }
  return json({ month, sent: emails.length - failed.length, failed: failed.length }, failed.length ? 502 : 200);
}

// ─── CLIENT ERROR REPORTING ────────────────────
const ADMIN_EMAIL = 'robertflores17@hotmail.com';
const ERROR_RATE_LIMIT = new Map(); // IP -> { count, resetAt }

async function handleClientError(request, env, cors) {
  // Rate limit: 10 errors/minute per IP
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const now = Date.now();
  const limit = ERROR_RATE_LIMIT.get(ip);
  if (limit) {
    if (now < limit.resetAt) {
      if (limit.count >= 10) {
        return new Response('', { status: 429, headers: cors });
      }
      limit.count++;
    } else {
      ERROR_RATE_LIMIT.set(ip, { count: 1, resetAt: now + 60000 });
    }
  } else {
    ERROR_RATE_LIMIT.set(ip, { count: 1, resetAt: now + 60000 });
  }
  // Evict stale entries
  if (ERROR_RATE_LIMIT.size > 500) {
    for (const [k, v] of ERROR_RATE_LIMIT) {
      if (now > v.resetAt) ERROR_RATE_LIMIT.delete(k);
    }
  }

  if (!env.DB) {
    return new Response('', { status: 204, headers: cors });
  }

  try {
    const text = await request.text();
    const body = JSON.parse(text);
    const message = String(body.message || '').slice(0, 1000);
    const source = String(body.source || '').slice(0, 500);
    const lineno = parseInt(body.lineno) || 0;
    const colno = parseInt(body.colno) || 0;
    const stack = String(body.stack || '').slice(0, 2000);
    const page = String(body.page || '').slice(0, 200);
    const ua = (request.headers.get('User-Agent') || '').slice(0, 300);

    await env.DB.prepare(
      `INSERT INTO error_log (message, source, lineno, colno, stack, page, user_agent, ip)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(message, source, lineno, colno, stack, page, ua, ip).run();

    // Check if we should send an email alert (5+ identical errors in last hour)
    const hourAgo = new Date(now - 3600000).toISOString();
    const countResult = await env.DB.prepare(
      `SELECT COUNT(*) as cnt FROM error_log WHERE message = ? AND created_at > ?`
    ).bind(message, hourAgo).first();

    if (countResult && countResult.cnt === 5) {
      // Check if alert already sent for this error
      const alertSent = await env.DB.prepare(
        `SELECT id FROM error_alert_sent WHERE message_hash = ? AND sent_at > ?`
      ).bind(message.slice(0, 200), hourAgo).first();

      if (!alertSent) {
        await env.DB.prepare(
          `INSERT INTO error_alert_sent (message_hash) VALUES (?)`
        ).bind(message.slice(0, 200)).run();

        // Send email alert via Resend
        try {
          await fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${env.RESEND_API_KEY}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              from: 'FixTheVuln Alerts <hello@fixthevuln.com>',
              to: [ADMIN_EMAIL],
              subject: `[FixTheVuln] Error Alert: ${message.slice(0, 80)}`,
              html: `<h3>Recurring Error Detected</h3>
<p><strong>Message:</strong> ${escapeHtml(message)}</p>
<p><strong>Page:</strong> ${escapeHtml(page)}</p>
<p><strong>Source:</strong> ${escapeHtml(source)}:${lineno}:${colno}</p>
<p><strong>Occurrences:</strong> 5+ in last hour</p>
<p><strong>Stack:</strong></p>
<pre style="background:#f1f5f9;padding:12px;border-radius:8px;font-size:12px;overflow-x:auto;">${escapeHtml(stack)}</pre>`,
            }),
          });
        } catch { /* email failure shouldn't block error logging */ }
      }
    }

    return new Response('', { status: 204, headers: cors });
  } catch {
    return new Response('', { status: 400, headers: cors });
  }
}

function escapeHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

async function handleAdminErrors(request, env, cors) {
  const url = new URL(request.url);
  const secret = url.searchParams.get('key');
  if (!env.ADMIN_KEY || secret !== env.ADMIN_KEY) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  }

  if (!env.DB) {
    return new Response(JSON.stringify({ errors: [] }), {
      status: 200,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  }

  const page = parseInt(url.searchParams.get('page')) || 1;
  const limit = Math.min(parseInt(url.searchParams.get('limit')) || 50, 100);
  const offset = (page - 1) * limit;

  const { results } = await env.DB.prepare(
    `SELECT * FROM error_log ORDER BY created_at DESC LIMIT ? OFFSET ?`
  ).bind(limit, offset).all();

  const { cnt } = await env.DB.prepare(`SELECT COUNT(*) as cnt FROM error_log`).first();

  return new Response(JSON.stringify({ errors: results, total: cnt, page, limit }), {
    status: 200,
    headers: { ...cors, 'Content-Type': 'application/json' },
  });
}

// ─── QUIZ ANALYTICS ────────────────────────────
const QUIZ_RATE_LIMIT = new Map(); // IP -> { count, resetAt }

async function handleQuizSubmit(request, env, cors) {
  // Rate limit: 20 submissions/minute per IP
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const now = Date.now();
  const limit = QUIZ_RATE_LIMIT.get(ip);
  if (limit) {
    if (now < limit.resetAt) {
      if (limit.count >= 20) {
        return new Response('', { status: 429, headers: cors });
      }
      limit.count++;
    } else {
      QUIZ_RATE_LIMIT.set(ip, { count: 1, resetAt: now + 60000 });
    }
  } else {
    QUIZ_RATE_LIMIT.set(ip, { count: 1, resetAt: now + 60000 });
  }
  if (QUIZ_RATE_LIMIT.size > 500) {
    for (const [k, v] of QUIZ_RATE_LIMIT) {
      if (now > v.resetAt) QUIZ_RATE_LIMIT.delete(k);
    }
  }

  if (!env.DB) {
    return new Response('', { status: 204, headers: cors });
  }

  try {
    const text = await request.text();
    const body = JSON.parse(text);

    // Validate session fields
    const sessionId = String(body.session_id || '').slice(0, 64);
    const quizId = String(body.quiz_id || '').slice(0, 50);
    const totalQuestions = parseInt(body.total_questions) || 0;
    const correctCount = parseInt(body.correct_count) || 0;
    const scorePct = Math.min(Math.max(parseInt(body.score_pct) || 0, 0), 100);
    const timeSeconds = Math.min(parseInt(body.time_seconds) || 0, 36000);
    const domainFilter = String(body.domain_filter || 'all').slice(0, 20);
    const difficultyFilter = String(body.difficulty_filter || 'mixed').slice(0, 20);

    if (!sessionId || !quizId || totalQuestions < 1) {
      return new Response(JSON.stringify({ error: 'Invalid session data' }), {
        status: 400,
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }

    // Insert session
    await env.DB.prepare(
      `INSERT INTO quiz_sessions (id, quiz_id, total_questions, correct_count, score_pct, time_seconds, domain_filter, difficulty_filter)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(sessionId, quizId, totalQuestions, correctCount, scorePct, timeSeconds, domainFilter, difficultyFilter).run();

    // Insert events (batch)
    const events = Array.isArray(body.events) ? body.events.slice(0, 200) : [];
    if (events.length > 0) {
      const stmt = env.DB.prepare(
        `INSERT INTO quiz_events (session_id, quiz_id, question_id, domain, difficulty, selected_option, correct_option, is_correct, time_ms)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`
      );
      const batch = events.map(e => stmt.bind(
        sessionId,
        quizId,
        parseInt(e.question_id) || 0,
        e.domain != null ? parseInt(e.domain) : null,
        e.difficulty ? String(e.difficulty).slice(0, 20) : null,
        parseInt(e.selected_option) || 0,
        parseInt(e.correct_option) || 0,
        e.is_correct ? 1 : 0,
        Math.min(parseInt(e.time_ms) || 0, 600000)
      ));
      await env.DB.batch(batch);
    }

    return new Response(JSON.stringify({ success: true, session_id: sessionId, events_inserted: events.length }), {
      status: 201,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  } catch (err) {
    // Duplicate session ID = quiz already submitted (idempotent)
    if (err.message && err.message.includes('UNIQUE constraint')) {
      return new Response(JSON.stringify({ success: true, duplicate: true }), {
        status: 200,
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }
    return new Response(JSON.stringify({ error: 'Bad request' }), {
      status: 400,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  }
}

// ─── QUIZ ANALYTICS (ADMIN) ────────────────────
// Backs analytics.html, which was calling this route before it existed on the worker.
async function handleQuizAnalytics(request, env, cors) {
  const url = new URL(request.url);
  const secret = url.searchParams.get('key');
  if (!env.ADMIN_KEY || secret !== env.ADMIN_KEY) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  }

  if (!env.DB) {
    return new Response(JSON.stringify({ error: 'Not configured' }), {
      status: 200,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  }

  const view = url.searchParams.get('view') || 'summary';

  try {
    if (view === 'hardest') {
      // Per-question difficulty across all quizzes. quiz_events has no question text,
      // so analytics.html falls back to showing quiz_id + question_id (it already
      // handles a missing question_text field).
      const { results } = await env.DB.prepare(
        `SELECT quiz_id, question_id,
                AVG(is_correct) as correct_rate,
                COUNT(*) as total
         FROM quiz_events
         GROUP BY quiz_id, question_id
         HAVING total >= 3
         ORDER BY correct_rate ASC
         LIMIT 20`
      ).all();
      return new Response(JSON.stringify({ questions: results }), {
        status: 200,
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }

    if (view === 'domains') {
      const { results } = await env.DB.prepare(
        `SELECT domain,
                AVG(is_correct) as avg_correct_rate,
                COUNT(DISTINCT question_id) as question_count
         FROM quiz_events
         WHERE domain IS NOT NULL
         GROUP BY domain
         ORDER BY domain ASC`
      ).all();
      return new Response(JSON.stringify({ domains: results }), {
        status: 200,
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }

    // view === 'summary' (default)
    const stats = await env.DB.prepare(
      `SELECT COUNT(*) as total_sessions, AVG(score_pct) as avg_score, AVG(time_seconds) as avg_duration
       FROM quiz_sessions`
    ).first();

    const eventStats = await env.DB.prepare(`SELECT COUNT(*) as total_events FROM quiz_events`).first();
    const quizCount = await env.DB.prepare(`SELECT COUNT(DISTINCT quiz_id) as unique_quizzes FROM quiz_sessions`).first();

    const { results: quizzes } = await env.DB.prepare(
      `SELECT quiz_id, COUNT(*) as attempts, AVG(score_pct) as avg_score, AVG(time_seconds) as avg_duration
       FROM quiz_sessions
       GROUP BY quiz_id
       ORDER BY attempts DESC
       LIMIT 50`
    ).all();

    const { results: sessions } = await env.DB.prepare(
      `SELECT quiz_id, score_pct as score, time_seconds as duration, total_questions, created_at
       FROM quiz_sessions
       ORDER BY created_at DESC
       LIMIT 20`
    ).all();

    return new Response(JSON.stringify({
      stats: {
        total_sessions: stats.total_sessions || 0,
        total_events: eventStats.total_events || 0,
        unique_quizzes: quizCount.unique_quizzes || 0,
        avg_score: stats.avg_score,
        avg_duration: stats.avg_duration,
        // No "quiz started" event exists (only completed submissions are recorded),
        // so a real completion rate can't be derived from this data. analytics.html
        // renders '-' when this is null rather than showing a fabricated number.
        completion_rate: null,
      },
      quizzes,
      recent_sessions: sessions,
    }), {
      status: 200,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Query failed' }), {
      status: 500,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  }
}

// ─── CLASSIFIER FEEDBACK ───────────────────────
// Backs vuln-classifier.html's feedback button (Phase 3 CyberMoE RLHF loop).
const CLASSIFIER_RATE_LIMIT = new Map(); // IP -> { count, resetAt }

async function handleClassifierFeedback(request, env, cors) {
  // Rate limit: 10 submissions/minute per IP
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const now = Date.now();
  const limit = CLASSIFIER_RATE_LIMIT.get(ip);
  if (limit) {
    if (now < limit.resetAt) {
      if (limit.count >= 10) {
        return new Response('', { status: 429, headers: cors });
      }
      limit.count++;
    } else {
      CLASSIFIER_RATE_LIMIT.set(ip, { count: 1, resetAt: now + 60000 });
    }
  } else {
    CLASSIFIER_RATE_LIMIT.set(ip, { count: 1, resetAt: now + 60000 });
  }
  if (CLASSIFIER_RATE_LIMIT.size > 500) {
    for (const [k, v] of CLASSIFIER_RATE_LIMIT) {
      if (now > v.resetAt) CLASSIFIER_RATE_LIMIT.delete(k);
    }
  }

  if (!env.DB) {
    return new Response('', { status: 204, headers: cors });
  }

  try {
    const text = await request.text();
    const body = JSON.parse(text);

    const predicted = String(body.predicted || '').slice(0, 50);
    const isCorrect = body.correct ? 1 : 0;
    const correction = body.corrected_domain ? String(body.corrected_domain).slice(0, 50) : null;
    const snippet = String(body.text_snippet || '').slice(0, 500);
    const scores = body.scores && typeof body.scores === 'object' ? body.scores : {};
    const confidence = typeof scores[predicted] === 'number' ? scores[predicted] : null;

    if (!predicted || !snippet) {
      return new Response('', { status: 400, headers: cors });
    }

    await env.DB.prepare(
      `INSERT INTO classifier_feedback (input_text, predicted_domain, confidence, is_correct, correction, entities_json)
       VALUES (?, ?, ?, ?, ?, ?)`
    ).bind(snippet, predicted, confidence, isCorrect, correction, JSON.stringify(scores)).run();

    return new Response(JSON.stringify({ success: true }), {
      status: 201,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  } catch {
    return new Response('', { status: 400, headers: cors });
  }
}
