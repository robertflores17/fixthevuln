#!/usr/bin/env bash
# Deterministic self-QA: every check here is automatable and exits nonzero on
# failure. Run before declaring work done; the shared pre-push hook also runs it.
# Judgment checks (XSS, secrets, localStorage) live in /pre-push-review, and
# post-deploy checks in /deploy. See .claude/skills/self-qa.md for the rest.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
fail=0
ok()  { echo "  PASS $1"; }
bad() { echo "  FAIL $1"; fail=1; }

echo "== FixTheVuln self-QA"

# Local venv (gitignored, built from requirements.txt) supplies reportlab for the full test run.
# Trusted-local-only: it goes first on PATH, so never point it at a venv you did not build yourself.
if [ -d .venv/bin ]; then
    PATH="$PWD/.venv/bin:$PATH"
else
    echo "  note: no .venv, reportlab tests will be skipped (python3 -m venv .venv && .venv/bin/pip install -r requirements.txt)"
fi

broken=0
for s in scripts/*.py scripts/lib/*.py; do
    python3 -c "import py_compile,sys; py_compile.compile(sys.argv[1], doraise=True)" "$s" 2>/dev/null \
        || { echo "    does not compile: $s"; broken=1; }
done
[ $broken = 0 ] && ok "Python scripts compile" || bad "Python scripts compile"

python3 - <<'PY' || fail=1
# Unit tests (tests/test_*.py). No CI workflow runs these, so this is their only
# automatic run. test_sprint_kit_cycle needs reportlab (installed only for the
# sprint-kit PDF workflow); it is skipped visibly when reportlab is missing here.
import importlib.util, io, unittest
suite = unittest.TestLoader().discover("tests")
skip = importlib.util.find_spec("reportlab") is None
def keep(t):
    return not (skip and "test_sprint_kit_cycle" in t.id())
def flat(s):
    for t in s:
        yield from (flat(t) if isinstance(t, unittest.TestSuite) else [t])
tests = [t for t in flat(suite) if keep(t)]
result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(unittest.TestSuite(tests))
bad = result.failures + result.errors
if bad:
    print(f"  FAIL unit tests ({len(bad)} of {result.testsRun})")
    for t, _ in bad[:10]:
        print(f"    {t.id()}")
    raise SystemExit(1)
print(f"  PASS unit tests ({result.testsRun})")
if skip:
    print("  SKIP test_sprint_kit_cycle (reportlab not installed here, so it is NOT being run; install reportlab to cover it)")
PY

python3 -I - <<'PY' || fail=1
import glob, json, os, re, sys

fail = False
def report(name, problems):
    global fail
    if problems:
        fail = True
        print(f"  FAIL {name} ({len(problems)})")
        for p in problems[:10]:
            print(f"    {p}")
    else:
        print(f"  PASS {name}")

problems = []
for f in glob.glob("data/*.json"):
    try:
        json.load(open(f))
    except Exception as e:
        problems.append(f"{f}: {str(e)[:80]}")
report("data/*.json parses", problems)

pages = [p for p in glob.glob("**/*.html", recursive=True)
         if not p.startswith(("node_modules/", "data/"))]

problems = []
for f in pages:
    for i, block in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                                         open(f, errors="ignore").read(), re.S)):
        try:
            json.loads(block)
        except Exception as e:
            problems.append(f"{f} block {i + 1}: {str(e)[:60]}")
report("JSON-LD parses", problems)

# Tag balance via the stdlib HTML parser, so payloads inside attributes and
# <script> (teaching pages have '<body onload=...>' in onclick) aren't counted.
from html.parser import HTMLParser
class TagCount(HTMLParser):
    def __init__(self):
        super().__init__()
        self.n = {t: [0, 0] for t in ("html", "head", "body", "main")}
    def handle_starttag(self, tag, attrs):
        if tag in self.n: self.n[tag][0] += 1
    def handle_endtag(self, tag):
        if tag in self.n: self.n[tag][1] += 1
problems = []
for f in pages:
    p = TagCount()
    p.feed(open(f, errors="ignore").read())
    problems += [f"{f}: <{t}> {o} open, {c} close" for t, (o, c) in p.n.items() if o != c]
report("HTML tag balance", problems)

# Internal links resolve to a file on disk. Skip Cloudflare-injected paths and
# JS template literals (href="/certs/${esc(id)}.html").
problems = []
for f in pages:
    for link in re.findall(r'href="(/[^"#?]*)', open(f, errors="ignore").read()):
        if link.startswith("/cdn-cgi/") or "${" in link:
            continue
        t = link.lstrip("/")
        if link == "/" or os.path.isfile(t) or os.path.isfile(t + ".html") or os.path.isfile(os.path.join(t, "index.html")):
            continue
        problems.append(f"{f} -> {link}")
report("internal links resolve", problems)

# Generators read STYLE_CSS_VERSION; pages must match it or the next
# regeneration silently reverts them.
want = re.search(r"STYLE_CSS_VERSION\s*=\s*(\S+)", open("scripts/lib/constants.py").read()).group(1).strip("'\"")
problems = sorted({f"{f}: v={v}" for f in pages
                   for v in re.findall(r"style\.min\.css\?v=([0-9A-Za-z.]+)", open(f, errors="ignore").read())
                   if v != want})
report(f"style.min.css?v= matches STYLE_CSS_VERSION ({want})", problems)

# Dark-mode link fix present in the built CSS (tokens + rule). Count
# occurrences, not lines: style.min.css is a single line.
n = open("style.min.css").read().count("link-color")
report("style.min.css has link-color fix (>= 3)", [] if n >= 3 else [f"found {n}"])

sys.exit(1 if fail else 0)
PY

out="$(python3 scripts/audit_pages.py --skip-links 2>&1)"
errs="$(echo "$out" | grep -oE '[0-9]+ errors' | head -1 | grep -oE '[0-9]+')"
if [ "${errs:-x}" = "0" ]; then ok "page audit: 0 errors"; else bad "page audit errors: ${errs:-could not parse audit output}"; fi

[ $fail = 0 ] && echo "self-QA: all checks passed" || echo "self-QA: FAILED"
exit $fail
