// Sprint kit subscription delivery checks. Run: node --test store/worker.test.mjs
// Stripe, Resend and R2 are mocked; no network.
import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import worker from './cloudflare-worker.js';

const KIT_PRICE = 'price_1T45YOLBnrzacKtTCA08o8PY';
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
