// ============================================
// FixTheVuln Store — Cloudflare Worker
// Stripe Checkout + PDF Delivery from R2
// ============================================
// Environment variables needed:
//   STRIPE_SECRET_KEY    - your Stripe secret key
//   STRIPE_WEBHOOK_SECRET - webhook signing secret
//   RESEND_API_KEY       - Resend API key for emails
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
      expanded.add(item);
    }
  }
  return [...expanded];
}

// ─── SERVER-SIDE PRICING (source of truth) ──────
const PRICING = {
  standard:  599,  // cents
  adhd:      599,
  dark:      599,
  adhd_dark: 599,
  bundle:    1599,
};

// Career path pricing by cert count (cents)
const CP_PRICING = {
  2: { single: 899,  bundle: 1699 },
  3: { single: 1299, bundle: 2499 },
  4: { single: 1699, bundle: 3499 },
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
  return PRICING[variant] || null;
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
  const allowed = ALLOWED_ORIGINS.some(o => origin.startsWith(o)) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
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

    return new Response(JSON.stringify({ error: 'Not found' }), {
      status: 404,
      headers: { ...cors, 'Content-Type': 'application/json' },
    });
  },
};

// ─── CHECKOUT HANDLER ───────────────────────────
async function handleCheckout(request, env, cors) {
  try {
    const { items } = await request.json();

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
      const variantLabel = VARIANT_LABELS[item.variant];
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
    }).join(',');

    const params = new URLSearchParams();
    params.append('mode', 'payment');
    params.append('success_url', 'https://fixthevuln.com/store/success.html?session_id={CHECKOUT_SESSION_ID}');
    params.append('cancel_url', 'https://fixthevuln.com/store/store.html');
    params.append('metadata[purchased_items]', purchasedItems);
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
      return new Response(JSON.stringify({ error: session.error.message }), {
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
    const purchasedItems = session.metadata.purchased_items || '';
    const rawItems = purchasedItems.split(',').filter(Boolean);
    const items = expandPurchasedItems(rawItems);

    // Anchor expiry to session creation time (not current time) to prevent unlimited replays
    const sessionCreatedMs = (session.created || Math.floor(Date.now() / 1000)) * 1000;
    const downloads = await generateDownloadLinks(sessionId, items, rawItems, env.STRIPE_WEBHOOK_SECRET, sessionCreatedMs);

    return new Response(JSON.stringify({
      verified: true,
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
      const purchasedItems = session.metadata?.purchased_items || '';
      const rawItems = purchasedItems.split(',').filter(Boolean);
      const items = expandPurchasedItems(rawItems);

      if (items.length > 0) {
        const sessionCreatedMs = (session.created || Math.floor(Date.now() / 1000)) * 1000;
        const downloads = await generateDownloadLinks(session.id, items, rawItems, env.STRIPE_WEBHOOK_SECRET, sessionCreatedMs);

        // Send customer email + seller notification in parallel
        const promises = [];

        if (customerEmail) {
          promises.push(sendCustomerEmail(env, customerEmail, downloads, items));
        }
        promises.push(sendSellerNotification(env, customerEmail, downloads, items, amountCents));

        await Promise.allSettled(promises);
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
          <strong style="color:#1e293b;">${certName}</strong>
          <span style="display:inline-block;background:#eff6ff;color:#2563eb;padding:2px 8px;border-radius:50px;font-size:11px;font-weight:600;margin-left:6px;">${variantLabel}</span>
          <br><span style="color:#64748b;font-size:13px;">${dl.filename}</span>
        </td>
        <td style="padding:12px 16px;border-bottom:1px solid #e5e7eb;text-align:right;">
          <a href="${dl.url}" style="display:inline-block;background:#2563eb;color:#ffffff;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">Download</a>
        </td>
      </tr>`;
  }

  function renderGroupHeader(name) {
    return `
      <tr>
        <td colspan="2" style="padding:16px 16px 8px;background:#f8fafc;border-bottom:1px solid #e5e7eb;">
          <strong style="color:#1e293b;font-size:15px;">${name} Career Path</strong>
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
async function sendSellerNotification(env, customerEmail, downloads, items, amountCents) {
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
          <td style="padding:8px 0;color:#1e293b;font-size:14px;font-weight:600;">${customerEmail || 'No email provided'}</td>
        </tr>
        <tr>
          <td style="padding:8px 0;color:#64748b;font-size:14px;">Amount</td>
          <td style="padding:8px 0;color:#1e293b;font-size:14px;font-weight:600;">${amount}</td>
        </tr>
        <tr>
          <td style="padding:8px 0;color:#64748b;font-size:14px;vertical-align:top;">Items</td>
          <td style="padding:8px 0;color:#1e293b;font-size:14px;white-space:pre-line;">${itemListStr}</td>
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
