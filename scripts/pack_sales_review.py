#!/usr/bin/env python3
"""Pack vs bundle sales since the 2026-10-31 repricing (read-only; uses the logged-in `stripe` CLI, live mode).

Run on or after 2026-11-30 to answer: are the vendor packs ($79/$69/$59) replacing the $24.99 four-format bundles?
Buckets each paid checkout by what it contained: pack, bundle, single planner, or kit/other.
"""
import json, subprocess, sys, collections, datetime
since = int(datetime.datetime(2026, 10, 31, tzinfo=datetime.timezone.utc).timestamp())
out = subprocess.run(['stripe', 'checkout', 'sessions', 'list', '--live', '--limit', '100', '-d', f'created[gte]={since}'],
                     capture_output=True, text=True).stdout
d = json.loads(out)
c = collections.Counter(); revenue = collections.Counter()
for s in d['data']:
    if s.get('payment_status') != 'paid': continue
    items = ','.join(v for k, v in (s.get('metadata') or {}).items() if k.startswith('purchased_items')).split(',')
    kind = ('pack' if any('-complete__' in i for i in items) else
            'bundle' if any(i.endswith('__bundle') for i in items) else 'single' if any('__' in i for i in items) else 'kit/other')
    c[kind] += 1; revenue[kind] += (s.get('amount_total') or 0) / 100
print('paid sessions since 2026-10-31:', sum(c.values()), '| has_more:', d.get('has_more'))
for k in c: print(f'  {k:10s} {c[k]:3d} orders  ${revenue[k]:.2f}')
