// Cart overlap rules for vendor packs. Run: node --test store/cart.test.mjs
// Loads store.js in a vm with a stubbed browser (no DOM; the script is null-safe without one).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

// Every property read or call on a DOM element returns another no-op, so the render code runs without a DOM.
const noop = new Proxy(function () {}, { get: () => noop, apply: () => noop, set: () => true });

function load({ confirm = true } = {}) {
  const storage = new Map();
  const toasts = [];
  const ctx = {
    console, setTimeout,
    window: {}, location: { search: '' },
    localStorage: { getItem: k => storage.get(k) ?? null, setItem: (k, v) => storage.set(k, String(v)), removeItem: k => storage.delete(k) },
    document: { getElementById: () => noop, querySelectorAll: () => [], addEventListener: () => {}, body: noop,
      createElement: () => { let t = ''; return { set textContent(v) { t = String(v); }, get innerHTML() { return t; } }; } },
    URLSearchParams,
  };
  vm.createContext(ctx);
  const src = readFileSync(new URL('./store.js', import.meta.url), 'utf8') + `
    showToast = (m, t) => globalThis.__toasts.push(m);
    showConfirm = async () => (typeof globalThis.__confirm === 'function' ? globalThis.__confirm() : globalThis.__confirm);
    globalThis.__api = { addToCart, addCareerPathToCart, cart: () => cart };`;
  ctx.__toasts = toasts; ctx.__confirm = confirm;
  vm.runInContext(src, ctx);
  return { api: ctx.__api, toasts };
}
const names = api => Array.from(api.cart(), i => i.productId); // host-realm array so deepEqual works across the vm

test('a cert already inside a pack in the cart is blocked', async () => {
  const { api, toasts } = load();
  await api.addToCart('comptia-complete', 'CompTIA Complete', 'bundle', 79);
  await api.addToCart('comptia-security-plus', 'CompTIA Security+', 'bundle', 24.99);
  assert.deepEqual(names(api), ['comptia-complete']);
  assert.match(toasts[0], /already included in "CompTIA Complete"/);
});

test('a cert from another vendor is still allowed next to a pack', async () => {
  const { api } = load();
  await api.addToCart('comptia-complete', 'CompTIA Complete', 'bundle', 79);
  await api.addToCart('aws-developer', 'AWS Developer', 'bundle', 24.99);
  assert.deepEqual(names(api), ['comptia-complete', 'aws-developer']);
});

test('adding a pack offers to drop covered certs and career paths; accepting removes them', async () => {
  const { api } = load({ confirm: true });
  await api.addToCart('comptia-security-plus', 'CompTIA Security+', 'standard', 9.99);
  await api.addToCart('aws-developer', 'AWS Developer', 'standard', 9.99);
  await api.addCareerPathToCart('comptia-a-plus', 'CompTIA A+ Complete', 2);
  await api.addToCart('comptia-complete', 'CompTIA Complete', 'bundle', 79);
  assert.deepEqual(names(api), ['aws-developer', 'comptia-complete']);
});

test('declining the prompt keeps the covered items', async () => {
  const { api } = load({ confirm: false });
  await api.addToCart('comptia-security-plus', 'CompTIA Security+', 'standard', 9.99);
  await api.addToCart('comptia-complete', 'CompTIA Complete', 'bundle', 79);
  assert.deepEqual(names(api), ['comptia-security-plus', 'comptia-complete']);
});

test('a career path inside a pack in the cart is blocked; a cross-vendor path is not', async () => {
  const { api, toasts } = load();
  await api.addToCart('comptia-complete', 'CompTIA Complete', 'bundle', 79);
  await api.addCareerPathToCart('comptia-trifecta', 'CompTIA Trifecta', 4);
  assert.deepEqual(names(api), ['comptia-complete']);
  assert.match(toasts[0], /already included in "CompTIA Complete"/);
  await api.addCareerPathToCart('cloud-fundamentals', 'Cloud Fundamentals', 3);
  assert.deepEqual(names(api), ['comptia-complete', 'cp:cloud-fundamentals']);
});

test('the Productivity Bundle is not treated as an all-formats pack', async () => {
  const { api } = load();
  await api.addToCart('lifestyle-bundle', 'Productivity Bundle', 'standard', 22.47);
  await api.addToCart('budget-binder', 'Budget Binder', 'dark', 9.99);
  assert.deepEqual(names(api), ['lifestyle-bundle', 'budget-binder']);
});

test('two quick adds of the same pack while the confirm dialog is open leave one pack in the cart', async () => {
  let answer;
  const dialog = new Promise(resolve => { answer = resolve; }); // one dialog, answered once, like the real modal
  const { api } = load({ confirm: () => dialog });
  await api.addToCart('comptia-security-plus', 'CompTIA Security+', 'standard', 9.99);
  const first = api.addToCart('comptia-complete', 'CompTIA Complete', 'bundle', 79);
  const second = api.addToCart('comptia-complete', 'CompTIA Complete', 'bundle', 79);
  answer(true);
  await Promise.all([first, second]);
  assert.deepEqual(names(api), ['comptia-complete']);
});
