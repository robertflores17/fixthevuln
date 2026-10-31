// Sprint kit subscription delivery checks. Run: node --test store/worker.test.mjs
// Stripe, Resend and R2 are mocked; no network.
import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { createHash, createHmac } from 'node:crypto';
import worker from './cloudflare-worker.js';

const KIT_PRICE = 'price_1UWlNqLBnrzacKtTfxZZDmkg';
const WEBHOOK_SECRET = 'whsec_test';
let r2, sent, stripe;

const env = () => ({
  STRIPE_SECRET_KEY: 'sk_test', STRIPE_WEBHOOK_SECRET: WEBHOOK_SECRET,
  RESEND_API_KEY: 're_test', KIT_DELIVERY_SECRET: 'deliver-secret',
  PLANNERS: {
    list: async ({ prefix }) => ({ objects: [...r2.keys()].filter(k => k.startsWith(prefix)).map(key => ({ key })) }),
    head: async k => (r2.has(k) ? {} : null),
    get: async k => (r2.has(k) ? { body: r2.get(k) } : null),
    put: async (k, v) => { r2.set(k, v); },
  },
});

beforeEach(() => {
  r2 = new Map([['patch-sprint-kit-2026-09.pdf', 'pdf9'], ['patch-sprint-kit-2026-10.pdf', 'pdf10']]);
  sent = [];
  stripe = { lineItemPrice: KIT_PRICE, subscribers: ['a@example.com', 'b@example.com'], batchFails: false };
  globalThis.fetch = async (url, opts = {}) => {
    const ok = body => ({ ok: true, status: 200, json: async () => body });
    if (url === 'https://api.resend.com/emails/batch') {
      if (stripe.batchFails) return { ok: false, status: 500, json: async () => ({}) };
      sent.push(...JSON.parse(opts.body)); return ok({ data: [] });
    }
    if (url === 'https://api.resend.com/emails') { sent.push(JSON.parse(opts.body)); return ok({ id: 'x' }); }
    if (url.includes('/line_items')) return ok({ data: [{ price: { id: stripe.lineItemPrice } }] });
    if (url.includes('/v1/subscriptions')) {
      assert.match(url, new RegExp(`price=${KIT_PRICE}&status=active`));
      return ok({ has_more: false, data: stripe.subscribers.map((email, i) => ({ id: `sub_${i}`, customer: { email } })) });
    }
    throw new Error(`unexpected fetch ${url}`);
  };
});

function webhook(session) {
  const payload = JSON.stringify({ type: 'checkout.session.completed', data: { object: session } });
  const t = Math.floor(Date.now() / 1000);
  const v1 = createHmac('sha256', WEBHOOK_SECRET).update(`${t}.${payload}`).digest('hex');
  return new Request('https://w/webhook', { method: 'POST', body: payload, headers: { 'stripe-signature': `t=${t},v1=${v1}` } });
}

const deliver = (body, auth = 'Bearer deliver-secret') =>
  new Request('https://w/sprint-kit/deliver', { method: 'POST', body: JSON.stringify(body), headers: { Authorization: auth } });

const subSession = { id: 'cs_1', mode: 'subscription', customer_details: { email: 'new@example.com' }, amount_total: 499, metadata: {} };

test('kit subscription checkout sends welcome with latest kit + seller notice', async () => {
  await worker.fetch(webhook(subSession), env());
  const welcome = sent.find(m => m.to[0] === 'new@example.com');
  assert.ok(welcome, 'welcome email sent');
  assert.match(welcome.html, /patch-sprint-kit-2026-10\.pdf/);
  assert.ok(sent.find(m => m.to[0] === 'hello@fixthevuln.com' && /Sprint Kit/.test(m.subject)));
});

test('welcome link downloads the kit', async () => {
  await worker.fetch(webhook(subSession), env());
  const href = sent.find(m => m.to[0] === 'new@example.com').html.match(/href="([^"]*download[^"]*)"/)[1].replaceAll('&amp;', '&');
  const res = await worker.fetch(new Request(href), env());
  assert.equal(res.status, 200);
  assert.equal(await res.text(), 'pdf10');
});

test('CyberFolio subscription on the shared Stripe account is ignored', async () => {
  stripe.lineItemPrice = 'price_cyberfolio';
  await worker.fetch(webhook(subSession), env());
  assert.equal(sent.length, 0);
});

test('deliver rejects a bad secret', async () => {
  const res = await worker.fetch(deliver({ month: '2026-10' }, 'Bearer nope'), env());
  assert.equal(res.status, 401);
  assert.equal(sent.length, 0);
});

test('deliver validates month and kit existence', async () => {
  assert.equal((await worker.fetch(deliver({ month: '2026-13' }), env())).status, 400);
  assert.equal((await worker.fetch(deliver({ month: '2026-11' }), env())).status, 404);
});

test('dry run counts subscribers without sending', async () => {
  const res = await worker.fetch(deliver({ month: '2026-10', dry_run: true }), env());
  assert.deepEqual(await res.json(), { month: '2026-10', dry_run: true, subscribers: 2 });
  assert.equal(sent.length, 0);
});

test('deliver emails each subscriber once, rerun is a no-op', async () => {
  const e = env();
  const res = await worker.fetch(deliver({ month: '2026-10' }), e);
  assert.deepEqual(await res.json(), { month: '2026-10', sent: 2, failed: 0 });
  assert.deepEqual(sent.map(m => m.to[0]).sort(), ['a@example.com', 'b@example.com']);
  assert.match(sent[0].subject, /October 2026/);

  const again = await worker.fetch(deliver({ month: '2026-10' }), e);
  assert.equal((await again.json()).skipped, 'already delivered');
  assert.equal(sent.length, 2);
});

test('kit token cannot be used for a different file', async () => {
  await worker.fetch(webhook(subSession), env());
  const href = sent.find(m => m.to[0] === 'new@example.com').html.match(/href="([^"]*download[^"]*)"/)[1].replaceAll('&amp;', '&');
  const res = await worker.fetch(new Request(href.replace('2026-10', '2026-09')), env());
  assert.equal(res.status, 403);
});

test('failed batch: 502, seller gets the addresses, rerun does not resend', async () => {
  const e = env();
  stripe.batchFails = true;
  const res = await worker.fetch(deliver({ month: '2026-10' }), e);
  assert.equal(res.status, 502);
  assert.deepEqual(await res.json(), { month: '2026-10', sent: 0, failed: 2 });
  const notice = sent.find(m => m.to[0] === 'hello@fixthevuln.com');
  assert.match(notice.html, /a@example\.com/);

  stripe.batchFails = false;
  const again = await worker.fetch(deliver({ month: '2026-10' }), e);
  assert.equal((await again.json()).skipped, 'already delivered');
  assert.equal(sent.length, 1); // only the seller notice
});

test('planner token cannot download a kit', async () => {
  const payload = Buffer.from(JSON.stringify({ sessionId: 'cs_x', items: ['ccna__standard'], expiry: Date.now() + 60000 })).toString('base64');
  const sig = createHmac('sha256', WEBHOOK_SECRET).update(payload).digest('hex');
  const res = await worker.fetch(new Request(`https://w/download?token=${encodeURIComponent(`${payload}.${sig}`)}&file=patch-sprint-kit-2026-10.pdf`), env());
  assert.equal(res.status, 403);
});

// Checkout pricing: server-side prices, vendor packs sold only as the all-formats bundle.
let ipSeq = 0; // the checkout rate limiter is per IP, so each call gets its own
async function checkout(items) {
  let body;
  globalThis.fetch = async (url, opts) => {
    body = new URLSearchParams(opts.body);
    return { ok: true, status: 200, json: async () => ({ id: 'cs_t', url: 'https://stripe.test' }) };
  };
  const res = await worker.fetch(new Request('https://w/checkout', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://fixthevuln.com', 'CF-Connecting-IP': `10.0.0.${++ipSeq}` }, body: JSON.stringify({ items }),
  }), env());
  return { res, body };
}

test('single planner is $9.99 and 4-format bundle is $24.99', async () => {
  const a = await checkout([{ productId: 'comptia-security-plus', variant: 'standard' }]);
  assert.equal(a.res.status, 200);
  assert.equal(a.body.get('line_items[0][price_data][unit_amount]'), '999');
  const b = await checkout([{ productId: 'comptia-security-plus', variant: 'bundle' }]);
  assert.equal(b.body.get('line_items[0][price_data][unit_amount]'), '2499');
});

test('vendor packs charge $79/$69/$59 and expand to every cert as a bundle zip', async () => {
  for (const [id, cents, certs] of [['comptia-complete', '7900', 14], ['microsoft-complete', '6900', 12], ['aws-complete', '5900', 8]]) {
    const { res, body } = await checkout([{ productId: id, variant: 'bundle' }]);
    assert.equal(res.status, 200, id);
    assert.equal(body.get('line_items[0][price_data][unit_amount]'), cents, id);
    assert.equal(body.get('metadata[purchased_items]'), `${id}__bundle`);
  }
  const { res } = await checkout([{ productId: 'comptia-complete', variant: 'standard' }]);
  assert.equal(res.status, 400, 'pack is not sold in a single format');
});

// Stripe caps a metadata value at 500 chars; a full 20-line bundle cart must span several keys and read back whole.
const twentyBundles = [
  'comptia-a-plus-1201', 'comptia-a-plus-1202', 'comptia-security-plus', 'comptia-network-plus', 'comptia-linux-plus',
  'comptia-cloud-plus', 'comptia-cysa-plus', 'comptia-pentest-plus', 'comptia-casp-plus', 'comptia-server-plus',
  'aws-cloud-practitioner', 'aws-solutions-architect', 'aws-developer', 'aws-cloudops', 'aws-security-specialty',
  'aws-database-specialty', 'aws-machine-learning', 'aws-data-engineer', 'ms-az-900', 'ms-az-104',
].map(productId => ({ productId, variant: 'bundle' }));

test('a 20-line bundle cart splits its purchase record across metadata keys under 500 chars', async () => {
  const { res, body } = await checkout(twentyBundles);
  assert.equal(res.status, 200);
  const keys = [...body.keys()].filter(k => /^metadata\[purchased_items(_\d+)?\]$/.test(k));
  assert.ok(keys.length >= 2, 'spans more than one key');
  for (const k of keys) assert.ok(body.get(k).length <= 500, `${k} within Stripe's 500 char limit`);
  const joined = keys.flatMap(k => body.get(k).split(','));
  assert.deepEqual(joined.sort(), twentyBundles.map(i => `${i.productId}__bundle`).sort());
});

test('webhook reads a purchase record split across metadata keys', async () => {
  globalThis.fetch = async (url, opts = {}) => {
    if (url === 'https://api.resend.com/emails') { sent.push(JSON.parse(opts.body)); return { ok: true, status: 200, json: async () => ({ id: 'x' }) }; }
    throw new Error(`unexpected fetch ${url}`);
  };
  await worker.fetch(webhook({
    id: 'cs_split', mode: 'payment', customer_details: { email: 'buyer@example.com' }, amount_total: 5000,
    metadata: { purchased_items: 'comptia-security-plus__bundle', purchased_items_2: 'aws-developer__bundle' },
  }), env());
  const mail = sent.find(m => m.to[0] === 'buyer@example.com');
  assert.ok(mail, 'customer email sent');
  assert.match(mail.html, /comptia-security-plus_bundle\.zip/);
  assert.match(mail.html, /aws-developer_bundle\.zip/);
});

// Delivery email: big orders link to the success page instead of embedding every signed download link.
async function emailFor(metadata, workerEnv = env()) {
  globalThis.fetch = async (url, opts = {}) => {
    if (url === 'https://api.resend.com/emails') { sent.push(JSON.parse(opts.body)); return { ok: true, status: 200, json: async () => ({ id: 'x' }) }; }
    throw new Error(`unexpected fetch ${url}`);
  };
  await worker.fetch(webhook({
    id: 'cs_mail', mode: 'payment', customer_details: { email: 'buyer@example.com' }, amount_total: 7900, metadata,
  }), workerEnv);
  return sent.find(m => m.to[0] === 'buyer@example.com');
}

test('a 14-file pack order emails one link to the success page, not 14 signed links', async () => {
  const mail = await emailFor({ purchased_items: 'comptia-complete__bundle' });
  assert.match(mail.html, /success\.html\?session_id=cs_mail/);
  assert.doesNotMatch(mail.html, /download\?token=/);
  assert.match(mail.html, /CompTIA Security\+/);
  assert.ok(mail.html.length < 30000, `compact email is ${mail.html.length} chars`);
});

test('a small order keeps per-file download links in the email', async () => {
  const mail = await emailFor({ purchased_items: 'comptia-security-plus__standard' });
  assert.match(mail.html, /download\?token=/);
  assert.doesNotMatch(mail.html, /View and download your files/);
});

test('three packs at once stay well under the Gmail clipping limit', async () => {
  const mail = await emailFor({ purchased_items: 'comptia-complete__bundle,microsoft-complete__bundle,aws-complete__bundle' });
  assert.ok(mail.html.length < 60000, `email is ${mail.html.length} chars`);
});

test('email threshold: 12 files keep inline links, 13 switch to the success page link', async () => {
  const twelve = await emailFor({ purchased_items: 'microsoft-complete__bundle' });
  assert.match(twelve.html, /download\?token=/);
  assert.doesNotMatch(twelve.html, /View and download your files/);
  sent.length = 0;
  const thirteen = await emailFor({ purchased_items: 'microsoft-complete__bundle,comptia-security-plus__bundle' });
  assert.match(thirteen.html, /View and download your files/);
  assert.doesNotMatch(thirteen.html, /download\?token=/);
});

// One-click zip: store-only archive streamed from R2 using a precomputed CRC manifest.
import { execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

function crc32(buf) {
  let c, crc = 0xffffffff;
  for (const byte of buf) { c = (crc ^ byte) & 0xff; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; crc = (crc >>> 8) ^ c; }
  return (crc ^ 0xffffffff) >>> 0;
}

const md5 = buf => createHash('md5').update(buf).digest('hex'); // R2's ETag for single-part uploads

function zipEnv(files, manifest) {
  const e = env();
  const all = new Map(files);
  all.set('_zip-manifest.json', Buffer.from(JSON.stringify(manifest)));
  e.PLANNERS = {
    head: async k => (all.has(k) ? { size: all.get(k).length, etag: md5(all.get(k)) } : null),
    get: async k => (all.has(k)
      ? { size: all.get(k).length, etag: md5(all.get(k)), body: new Blob([all.get(k)]).stream(), json: async () => JSON.parse(all.get(k).toString()) }
      : null),
  };
  return e;
}

const zipFiles = () => new Map([
  ['comptia-security-plus_bundle.zip', Buffer.from('PK-fake-security-plus-'.repeat(5000))],
  ['aws-developer_bundle.zip', Buffer.from('aws-developer-planner-bytes-'.repeat(3000))],
]);
const zipManifest = files => Object.fromEntries([...files].map(([n, b]) => [n, { size: b.length, crc: crc32(b), md5: md5(b) }]));

const zipOrder = { purchased_items: 'comptia-security-plus__bundle,aws-developer__bundle' };

async function zipLinkFromEmail() {
  const files = zipFiles();
  const mail = await emailFor(zipOrder, zipEnv(files, zipManifest(files)));
  return mail.html.match(/href="([^"]*download-all[^"]*)"/)[1].replaceAll('&amp;', '&');
}

test('zip link in the email downloads a valid archive with every purchased file', async () => {
  const href = await zipLinkFromEmail();
  const files = zipFiles();
  const res = await worker.fetch(new Request(href), zipEnv(files, zipManifest(files)));
  assert.equal(res.status, 200);
  assert.equal(res.headers.get('content-type'), 'application/zip');
  const path = join(mkdtempSync(join(tmpdir(), 'ftvzip-')), 'out.zip');
  writeFileSync(path, Buffer.from(await res.arrayBuffer()));
  // Python's zipfile checks the central directory, offsets and every CRC
  const out = execFileSync('python3', ['-I', '-c', `
import sys, zipfile, hashlib
z = zipfile.ZipFile(sys.argv[1])
print(z.testzip())
print(sorted(z.namelist()))
print(sorted(hashlib.sha256(z.read(n)).hexdigest()[:8] for n in z.namelist()))
`, path]).toString().trim().split('\n');
  assert.equal(out[0], 'None', 'testzip reports no bad file');
  assert.equal(out[1], "['aws-developer_bundle.zip', 'comptia-security-plus_bundle.zip']");
  const sha = b => execFileSync('python3', ['-I', '-c', 'import sys,hashlib;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest()[:8])'], { input: b }).toString().trim();
  assert.equal(out[2], JSON.stringify([...files.values()].map(sha).sort()).replaceAll('"', "'").replaceAll(',', ', '));
});

test('zip is refused when the manifest is stale or a file is missing, and with a bad token', async () => {
  const href = await zipLinkFromEmail();
  const files = zipFiles();
  const stale = zipManifest(files);
  stale['aws-developer_bundle.zip'].size += 1;
  assert.equal((await worker.fetch(new Request(href), zipEnv(files, stale))).status, 409);
  const missing = new Map(files); missing.delete('aws-developer_bundle.zip');
  assert.equal((await worker.fetch(new Request(href), zipEnv(missing, zipManifest(files)))).status, 409);
  const tampered = href.replace(/token=[^&]*/, m => m.slice(0, -2) + 'xx');
  assert.equal((await worker.fetch(new Request(tampered), zipEnv(files, zipManifest(files)))).status, 403);
  assert.equal((await worker.fetch(new Request(href.replace(/\?.*/, '')), zipEnv(files, zipManifest(files)))).status, 400);
});

test('a single-file order has no zip button', async () => {
  const mail = await emailFor({ purchased_items: 'comptia-security-plus__standard' });
  assert.doesNotMatch(mail.html, /download-all/);
});

test('/verify returns a zip link for 2+ files and none for a single file', async () => {
  let n = 0;
  const files = zipFiles();
  const verify = async (purchased_items, workerEnv = zipEnv(files, zipManifest(files))) => {
    globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => ({ payment_status: 'paid', mode: 'payment', created: Math.floor(Date.now() / 1000), metadata: { purchased_items } }) });
    const res = await worker.fetch(new Request('https://w/verify', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': `10.1.0.${++n}` }, body: JSON.stringify({ sessionId: 'cs_v' }),
    }), workerEnv);
    return res.json();
  };
  const two = await verify('comptia-security-plus__bundle,aws-developer__bundle');
  assert.equal(two.downloads.length, 2);
  assert.match(two.zipUrl, /^https:\/\/fixthevuln-checkout\..*\/download-all\?token=/);
  assert.doesNotMatch(two.zipUrl, /file=/);
  assert.equal((await verify('comptia-security-plus__standard')).zipUrl, null);
  const stale = zipManifest(files);
  stale['aws-developer_bundle.zip'].size += 1;
  assert.equal((await verify('comptia-security-plus__bundle,aws-developer__bundle', zipEnv(files, stale))).zipUrl, null, 'no dead zip button');
});

test('no zip link is offered when the manifest is stale or a file is missing', async () => {
  const files = zipFiles();
  const stale = zipManifest(files);
  stale['aws-developer_bundle.zip'].crc = undefined;
  const mail = await emailFor(zipOrder, zipEnv(files, stale));
  assert.doesNotMatch(mail.html, /download-all/);
  assert.match(mail.html, /download\?token=/, 'per-file links are still there');
});

test('a file replaced after the check aborts the zip instead of producing a bad archive', async () => {
  const href = await zipLinkFromEmail();
  const files = zipFiles();
  const e = zipEnv(files, zipManifest(files));
  const realGet = e.PLANNERS.get;
  let gets = 0; // 1 = manifest, 2 = first file; the second file comes back a different size
  e.PLANNERS.get = async k => {
    const object = await realGet(k);
    return ++gets === 3 ? { ...object, size: object.size + 5 } : object;
  };
  const res = await worker.fetch(new Request(href), e);
  assert.equal(res.status, 200);
  await assert.rejects(async () => { await res.arrayBuffer(); }, 'download errors out instead of finishing');
});

test('a replacement file of the same size is caught by its ETag', async () => {
  const href = await zipLinkFromEmail();
  const files = zipFiles();
  const manifest = zipManifest(files);
  const old = files.get('aws-developer_bundle.zip');
  files.set('aws-developer_bundle.zip', Buffer.from(old.toString().replace(/a/g, 'b'))); // same length, different bytes
  assert.equal(files.get('aws-developer_bundle.zip').length, old.length);
  assert.equal((await worker.fetch(new Request(href), zipEnv(files, manifest))).status, 409);
  sent.length = 0; // emailFor returns the first buyer email captured, so drop the one zipLinkFromEmail made
  const mail = await emailFor(zipOrder, zipEnv(files, manifest));
  assert.doesNotMatch(mail.html, /download-all/, 'no zip link for a stale file');
});

test('a file swapped for different bytes of the same size mid-download aborts the zip', async () => {
  const href = await zipLinkFromEmail();
  const files = zipFiles();
  const e = zipEnv(files, zipManifest(files));
  const realGet = e.PLANNERS.get;
  let gets = 0;
  e.PLANNERS.get = async k => {
    const object = await realGet(k);
    return ++gets === 3 ? { ...object, etag: 'f'.repeat(32) } : object;
  };
  const res = await worker.fetch(new Request(href), e);
  await assert.rejects(async () => { await res.arrayBuffer(); }, 'download errors out instead of finishing');
});

test('a hung storage check cannot hold up the order email: no zip link, email still sent', async () => {
  const files = zipFiles();
  const e = zipEnv(files, zipManifest(files));
  e.PLANNERS.head = () => new Promise(() => {}); // never resolves
  const started = Date.now();
  const mail = await emailFor(zipOrder, e);
  assert.ok(mail, 'customer email was sent');
  assert.doesNotMatch(mail.html, /download-all/);
  assert.match(mail.html, /download\?token=/, 'per-file links still there');
  assert.ok(Date.now() - started < 8000, 'bounded by the 3 s zip-check timeout');
});
