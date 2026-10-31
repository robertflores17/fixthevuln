#!/usr/bin/env python3
"""Build _zip-manifest.json: {filename: {size, crc, md5}} for every planner file in the R2 bucket.

The checkout worker's GET /download-all streams a store-only zip and needs each file's CRC32 and size
up front (hashing in the worker would exceed the free plan's CPU budget). Re-run this whenever a planner
PDF or bundle zip in the bucket is added or replaced; a size mismatch makes the worker refuse the zip
(the individual download links keep working), so a stale manifest fails safe.

Usage:
  python3 scripts/build_zip_manifest.py --out /path/manifest.json            # build only
  python3 scripts/build_zip_manifest.py --out /path/manifest.json --upload   # build, then put it in R2

Downloads every file once (about 840 MB) through `wrangler r2 object get --remote`.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKER = ROOT / 'store' / 'cloudflare-worker.js'
BUCKET = 'fixthevuln-planners'
MANIFEST_KEY = '_zip-manifest.json'
SUFFIX = {'standard': '', 'adhd': '_adhd', 'dark': '_dark', 'adhd_dark': '_adhd_dark'}


def block(src, name):
    return re.search(r'const ' + name + r' = \{(.*?)\n\};', src, re.S).group(1)


def expected_files():
    """Mirror the worker's getFilename() over every real product (packs and bundles have no file of their own)."""
    src = WORKER.read_text()
    ids = re.findall(r"^\s*'([^']+)':", block(src, 'CERT_NAMES'), re.M)
    formats = {pid: re.findall(r"'(\w+)'", f) for pid, f in re.findall(r"'([\w-]+)':\s+\[([^\]]*)\]", block(src, 'PRODUCT_FORMATS'))}
    composite = set(re.findall(r"'([\w-]+)': \{ items:", block(src, 'PRODUCT_BUNDLE_PRICING')))
    names = []
    for pid in ids:
        if pid in composite:
            continue
        for variant in formats.get(pid, [*SUFFIX, 'bundle']):
            names.append(f'{pid}_bundle.zip' if variant == 'bundle' else f'{pid}{SUFFIX[variant]}_study_planner.pdf')
    return names


def fingerprint(name, tmp):
    path = Path(tmp) / name
    result = subprocess.run(
        ['npx', 'wrangler', 'r2', 'object', 'get', f'{BUCKET}/{name}', '--remote', '--file', str(path)],
        capture_output=True, text=True, cwd=ROOT / 'store')
    if result.returncode != 0 or not path.exists():
        return name, None
    data = path.read_bytes()
    path.unlink()
    # md5 is R2's ETag for single-part uploads; the worker compares it to catch a same-size replacement
    return name, {'size': len(data), 'crc': zlib.crc32(data) & 0xFFFFFFFF, 'md5': hashlib.md5(data).hexdigest()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, help='where to write the manifest JSON')
    ap.add_argument('--upload', action='store_true', help='put the manifest into the R2 bucket')
    ap.add_argument('--jobs', type=int, default=6)
    args = ap.parse_args()

    names = expected_files()
    print(f'{len(names)} expected files', file=sys.stderr)
    manifest, missing = {}, []
    with tempfile.TemporaryDirectory() as tmp, ThreadPoolExecutor(args.jobs) as pool:
        for i, (name, fp) in enumerate(pool.map(lambda n: fingerprint(n, tmp), names), 1):
            if fp:
                manifest[name] = fp
            else:
                missing.append(name)
            if i % 25 == 0:
                print(f'  {i}/{len(names)}', file=sys.stderr)
    Path(args.out).write_text(json.dumps(manifest, sort_keys=True))
    print(f'wrote {len(manifest)} entries to {args.out}', file=sys.stderr)
    if missing:
        print(f'NOT IN BUCKET ({len(missing)}): {missing}', file=sys.stderr)

    if args.upload:
        subprocess.run(['npx', 'wrangler', 'r2', 'object', 'put', f'{BUCKET}/{MANIFEST_KEY}', '--remote',
                        '--file', args.out, '--content-type', 'application/json'], check=True, cwd=ROOT / 'store')
        print('uploaded', MANIFEST_KEY, file=sys.stderr)


if __name__ == '__main__':
    main()
