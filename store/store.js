/* ============================================
   FixTheVuln Store — JavaScript
   Cart, Products, Stripe Checkout
   ============================================ */

// ─── STRIPE CONFIG ──────────────────────────
const STRIPE_PUBLISHABLE_KEY = 'pk_live_51T1bzYLBnrzacKtT0qGIOSxTYOp0ZUVdsAS5pYLKDYQpbIQs2PgypNZ7ARkcQeFNkyKLyl8qmBXBvOLf0Uaqqu0200xsCUOQk2';
const CHECKOUT_API_URL = 'https://fixthevuln-checkout.robertflores17.workers.dev';
// ─────────────────────────────────────────────

// ─── PRICING ────────────────────────────────
const PRICING = {
  standard: 5.99,
  adhd:     5.99,
  dark:     5.99,
  bundle:   11.99,  // Standard + Dark + ADHD for one cert — save ~$6
};

const VARIANT_LABELS = {
  standard: 'Standard',
  adhd:     'ADHD-Friendly',
  dark:     'Dark Mode',
  bundle:   '3-Format Bundle (Standard + Dark + ADHD)',
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
    icon: '🏆',
  },
  {
    id: 'comptia-a-plus',
    name: 'CompTIA A+ Complete',
    desc: 'Both A+ exams in one bundle — start your IT career',
    certs: ['CompTIA A+ Core 1', 'CompTIA A+ Core 2'],
    certIds: ['comptia-a-plus-1201', 'comptia-a-plus-1202'],
    certCount: 2,
    icon: '💻',
  },
  {
    id: 'comptia-security-track',
    name: 'CompTIA Security Track',
    desc: 'Full security progression from Security+ through CASP+',
    certs: ['CompTIA Security+', 'CompTIA CySA+', 'CompTIA PenTest+', 'CompTIA CASP+'],
    certIds: ['comptia-security-plus', 'comptia-cysa-plus', 'comptia-pentest-plus', 'comptia-casp-plus'],
    certCount: 4,
    icon: '🔐',
  },
  {
    id: 'security-pro',
    name: 'Security Pro',
    desc: 'Cross-vendor security combo: CompTIA Security+ and ISC2 CISSP',
    certs: ['CompTIA Security+', 'ISC2 CISSP'],
    certIds: ['comptia-security-plus', 'isc2-cissp'],
    certCount: 2,
    icon: '🛡️',
  },
  {
    id: 'aws-track',
    name: 'AWS Track',
    desc: 'AWS cloud career path: Practitioner → Architect → Developer',
    certs: ['AWS Cloud Practitioner', 'AWS Solutions Architect', 'AWS Developer'],
    certIds: ['aws-cloud-practitioner', 'aws-solutions-architect', 'aws-developer'],
    certCount: 3,
    icon: '☁️',
  },
  {
    id: 'azure-track',
    name: 'Azure Track',
    desc: 'Microsoft Azure path: Fundamentals → Admin → Architect',
    certs: ['Azure Fundamentals (AZ-900)', 'Azure Administrator (AZ-104)', 'Azure Architect (AZ-305)'],
    certIds: ['ms-az-900', 'ms-az-104', 'ms-az-305'],
    certCount: 3,
    icon: '🔷',
  },
  {
    id: 'cloud-fundamentals',
    name: 'Cloud Fundamentals',
    desc: 'Multi-cloud foundations: AWS, Azure, and Google Cloud in one bundle',
    certs: ['AWS Cloud Practitioner', 'Azure Fundamentals', 'Google Cloud Engineer'],
    certIds: ['aws-cloud-practitioner', 'ms-az-900', 'google-ace'],
    certCount: 3,
    icon: '🌐',
  },
  {
    id: 'isaca-grc',
    name: 'ISACA GRC',
    desc: 'Governance, Risk & Compliance trifecta: CISA, CISM, and CRISC',
    certs: ['ISACA CISA', 'ISACA CISM', 'ISACA CRISC'],
    certIds: ['isaca-cisa', 'isaca-cism', 'isaca-crisc'],
    certCount: 3,
    icon: '📊',
  },
  {
    id: 'isc2-path',
    name: 'ISC2 Path',
    desc: 'ISC2 progression: CC → SSCP → CISSP',
    certs: ['ISC2 CC', 'ISC2 SSCP', 'ISC2 CISSP'],
    certIds: ['isc2-cc', 'isc2-sscp', 'isc2-cissp'],
    certCount: 3,
    icon: '🎓',
  },
  {
    id: 'cisco-path',
    name: 'Cisco Path',
    desc: 'Cisco networking career: CCNA, CCNP ENCOR, and CyberOps',
    certs: ['Cisco CCNA', 'Cisco CCNP ENCOR', 'Cisco CyberOps'],
    certIds: ['cisco-ccna', 'cisco-ccnp-encor', 'cisco-cyberops'],
    certCount: 3,
    icon: '🌐',
  },
];

// Career path pricing by cert count and variant type
const CAREER_PATH_PRICING = {
  // { certCount: { single format price, bundle (3-format) price, individual total single, individual total bundle } }
  2: { single: 8.99,  bundle: 16.99, indivSingle: 11.98, indivBundle: 23.98 },
  3: { single: 12.99, bundle: 24.99, indivSingle: 17.97, indivBundle: 35.97 },
  4: { single: 16.99, bundle: 34.99, indivSingle: 23.96, indivBundle: 47.96 },
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

  // Microsoft
  { id: 'ms-az-900',               vendor: 'microsoft', name: 'Microsoft Azure Fundamentals', meta: 'AZ-900 · 3 domains',   popular: true,  tags: ['Cloud Concepts', 'Azure Services'] },
  { id: 'ms-az-104',               vendor: 'microsoft', name: 'Microsoft Azure Administrator',meta: 'AZ-104 · 5 domains',   popular: false, tags: ['Identity', 'Storage', 'Compute'] },
  { id: 'ms-az-305',               vendor: 'microsoft', name: 'Azure Solutions Architect',    meta: 'AZ-305 · 4 domains',   popular: false, tags: ['Design', 'Infrastructure', 'Data'] },
  { id: 'ms-sc-900',               vendor: 'microsoft', name: 'Security Fundamentals',        meta: 'SC-900 · 4 domains',   popular: false, tags: ['Security', 'Compliance', 'Identity'] },
  { id: 'ms-ai-900',               vendor: 'microsoft', name: 'Azure AI Fundamentals',        meta: 'AI-900 · 5 domains',   popular: false, tags: ['AI', 'Machine Learning', 'NLP'] },

  // Cisco
  { id: 'cisco-ccna',              vendor: 'cisco',     name: 'Cisco CCNA',                   meta: '200-301 · 6 domains',  popular: true,  tags: ['Networking', 'IP Connectivity', 'Security'] },
  { id: 'cisco-ccnp-encor',        vendor: 'cisco',     name: 'Cisco CCNP ENCOR',             meta: '350-401 · 6 domains',  popular: false, tags: ['Enterprise', 'Architecture', 'Automation'] },
  { id: 'cisco-cyberops',          vendor: 'cisco',     name: 'Cisco CyberOps Associate',     meta: '200-201 · 5 domains',  popular: false, tags: ['SOC', 'Threat Analysis', 'Monitoring'] },

  // ISACA
  { id: 'isaca-cisa',              vendor: 'isaca',     name: 'ISACA CISA',                   meta: 'CISA · 5 domains',     popular: false, tags: ['Audit', 'Governance', 'IS Management'] },
  { id: 'isaca-cism',              vendor: 'isaca',     name: 'ISACA CISM',                   meta: 'CISM 2026 · 4 domains', popular: false, tags: ['Governance', 'Risk', 'Incident Mgmt'] },
  { id: 'isaca-crisc',             vendor: 'isaca',     name: 'ISACA CRISC',                  meta: 'CRISC · 4 domains',    popular: false, tags: ['Risk', 'IT Controls', 'Monitoring'] },

  // GIAC
  { id: 'giac-gsec',               vendor: 'giac',      name: 'GIAC GSEC',                    meta: 'GSEC · 7 domains',     popular: false, tags: ['Defense', 'Networking', 'Incident Response'] },

  // Google Cloud
  { id: 'google-ace',              vendor: 'google',    name: 'Google Associate Cloud Engineer', meta: 'ACE · 5 domains',   popular: false, tags: ['GCP', 'Compute', 'Networking'] },
  { id: 'google-pca',              vendor: 'google',    name: 'Google Professional Cloud Architect', meta: 'PCA · 6 domains', popular: false, tags: ['Architecture', 'Design', 'Migration'] },
];

// ─── STATE ──────────────────────────────────
let cart = JSON.parse(localStorage.getItem('ftv_cart') || '[]');
let selectedVariant = localStorage.getItem('ftv_variant') || 'standard';
let selectedVendor = 'all';

// ─── DOM REFS ───────────────────────────────
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
const successModal  = document.getElementById('successModal');

// ─── INIT ───────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initFormatSelector();
  initVendorTabs();
  renderProducts();
  renderCareerPaths();
  updateCartUI();
  checkForSuccess();
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
  // Set initial active state
  cards.forEach(c => {
    if (c.dataset.variant === selectedVariant) c.classList.add('active');
    else c.classList.remove('active');
  });

  cards.forEach(card => {
    card.addEventListener('click', () => {
      cards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      selectedVariant = card.dataset.variant;
      localStorage.setItem('ftv_variant', selectedVariant);
      renderProducts();
      renderCareerPaths();
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
      renderProducts();
    });
  });
}

// ─── RENDER PRODUCTS ────────────────────────
function renderProducts() {
  const filtered = selectedVendor === 'all'
    ? PRODUCTS
    : PRODUCTS.filter(p => p.vendor === selectedVendor);

  const price = PRICING[selectedVariant];
  const variantLabel = VARIANT_LABELS[selectedVariant];

  productGrid.innerHTML = filtered.map(product => {
    const cartKey = `${product.id}__${selectedVariant}`;
    const inCart = cart.some(item => item.key === cartKey);

    return `
      <div class="product-card ${product.popular ? 'popular' : ''}" data-vendor="${product.vendor}">
        <div class="product-popular">Popular</div>
        <div class="product-vendor">${vendorDisplayName(product.vendor)}</div>
        <div class="product-name">${product.name}</div>
        <div class="product-meta">${product.meta}</div>
        <div class="product-features">
          ${product.tags.map(t => `<span class="product-tag">${t}</span>`).join('')}
        </div>
        ${selectedVariant === 'bundle' ? '<div class="product-bundle-note">📦 Standard + Dark + ADHD</div>' : ''}
        <div class="product-bottom">
          <div class="product-price">
            $${price.toFixed(2)}
            ${selectedVariant === 'bundle' ? `<span class="original">$${(PRICING.standard + PRICING.adhd + PRICING.dark).toFixed(2)}</span>` : ''}
          </div>
          <button class="btn-add ${inCart ? 'added' : ''}"
                  onclick="addToCart('${product.id}', '${escapeStr(product.name)}', '${selectedVariant}', ${price})"
                  ${inCart ? 'disabled' : ''}>
            ${inCart ? '✓ Added' : 'Add to Cart'}
          </button>
        </div>
      </div>
    `;
  }).join('');
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
  };
  return map[vendor] || vendor;
}

function escapeStr(str) {
  return str.replace(/'/g, "\\'");
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
    alert(`"${productName}" is already included in the "${overlappingPath.name}" in your cart. No need to add it separately!`);
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
  renderProducts();
  openCart();

  // Badge bounce animation
  cartBadge.classList.add('bump');
  setTimeout(() => cartBadge.classList.remove('bump'), 300);
}

function removeFromCart(key) {
  cart = cart.filter(item => item.key !== key);
  saveCart();
  updateCartUI();
  renderProducts();
  renderCareerPaths();
}

function saveCart() {
  localStorage.setItem('ftv_cart', JSON.stringify(cart));
}

function updateCartUI() {
  // Badge
  cartBadge.textContent = cart.length;
  cartBadge.setAttribute('data-count', cart.length);

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
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-variant">${item.variantLabel}</div>
          <div class="cart-item-price">$${item.price.toFixed(2)}</div>
        </div>
        <button class="cart-item-remove" onclick="removeFromCart('${item.key}')">Remove</button>
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

document.getElementById('cartToggle').addEventListener('click', openCart);
document.getElementById('cartClose').addEventListener('click', closeCart);
cartOverlay.addEventListener('click', closeCart);

// Close cart on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeCart();
});

// ─── RENDER CAREER PATHS ───────────────────
function renderCareerPaths() {
  const isBundle = selectedVariant === 'bundle';
  const variantLabel = VARIANT_LABELS[selectedVariant];

  careerPathGrid.innerHTML = CAREER_PATHS.map(path => {
    const tier = CAREER_PATH_PRICING[path.certCount];
    const price = isBundle ? tier.bundle : tier.single;
    const indivPrice = isBundle ? tier.indivBundle : tier.indivSingle;
    const savings = Math.round((1 - price / indivPrice) * 100);
    const cartKey = `cp__${path.id}__${selectedVariant}`;
    const inCart = cart.some(item => item.key === cartKey);

    return `
      <div class="career-card">
        <div class="career-card-header">
          <span class="career-icon">${path.icon}</span>
          <span class="savings-badge">Save ${savings}%</span>
        </div>
        <div class="career-name">${path.name}</div>
        <div class="career-desc">${path.desc}</div>
        <div class="career-certs">
          ${path.certs.map(c => `<div class="career-cert-item">✓ ${c}</div>`).join('')}
        </div>
        <div class="career-includes">${path.certCount} planners · ${variantLabel} format</div>
        <div class="product-bottom">
          <div class="product-price">
            $${price.toFixed(2)}
            <span class="original">$${indivPrice.toFixed(2)}</span>
          </div>
          <button class="btn-add btn-add-career ${inCart ? 'added' : ''}"
                  onclick="addCareerPathToCart('${path.id}', '${escapeStr(path.name)}', ${path.certCount})"
                  ${inCart ? 'disabled' : ''}>
            ${inCart ? '✓ Added' : 'Add to Cart'}
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function addCareerPathToCart(pathId, pathName, certCount) {
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
      const proceed = confirm(`You have ${names} individually in your cart (same format). The career path already includes ${overlaps.length === 1 ? 'it' : 'them'} — remove ${overlaps.length === 1 ? 'it' : 'them'} to avoid paying twice?`);
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
  renderProducts();
  renderCareerPaths();
  openCart();

  cartBadge.classList.add('bump');
  setTimeout(() => cartBadge.classList.remove('bump'), 300);
}

// ─── STRIPE CHECKOUT ────────────────────────
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
      alert(data.error);
      return;
    }

    // Redirect to Stripe Checkout
    const result = await stripe.redirectToCheckout({ sessionId: data.sessionId });
    if (result.error) {
      alert(result.error.message);
    }

  } catch (err) {
    console.error('Checkout error:', err);
    alert('Something went wrong. Please try again.');
  } finally {
    btnCheckout.disabled = false;
    btnCheckout.textContent = 'Proceed to Checkout →';
  }
});

// ─── CHECK FOR SUCCESS REDIRECT ─────────────
function checkForSuccess() {
  const params = new URLSearchParams(window.location.search);
  if (params.get('success') === 'true') {
    successModal.classList.add('active');
    // Clear cart after successful purchase
    cart = [];
    saveCart();
    updateCartUI();
    renderProducts();
    // Clean URL
    window.history.replaceState({}, '', window.location.pathname);
  }
}
