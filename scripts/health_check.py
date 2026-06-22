#!/usr/bin/env python3
"""Saturday health sweep for FixTheVuln. Stdlib only, no deps.

Checks pipeline + content health, writes a markdown findings report to --out,
and prints the finding count to stdout (consumed by health-check.yml).
Always exits 0 — findings are surfaced via the report/issue, not a red job.

Checks:
  1. KEV freshness   — data/kev-data.json lastChecked / lastUpdated drift
  2. CVE queue       — CVEs stuck in data/pending_review.json
  3. sitemap/llms    — CVE links pointing to missing pages, or orphan pages
  4. CI health       — workflow runs that failed in the last 7 days (GitHub API)
  5. urgent issues   — open tech-debt-urgent issues (GitHub API)

External broken links are intentionally NOT re-checked here — that is the
Monday page audit's job (audit_pages.py) and is slow.
"""
import argparse
import glob
import json
import os
import re
import urllib.request
from datetime import datetime, timezone, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
findings = []  # (severity, area, message)


def add(sev, area, msg):
    findings.append((sev, area, msg))


def _load_json(rel):
    try:
        with open(os.path.join(REPO_ROOT, rel), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        add("P3", "health-check", f"could not read {rel}: {e}")
        return None


def _date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _today():
    return datetime.now(timezone.utc).date()


def check_kev():
    d = _load_json("data/kev-data.json")
    if not isinstance(d, dict):
        add("P2", "KEV", "data/kev-data.json missing or not an object.")
        return
    lc, lu = _date(d.get("lastChecked")), _date(d.get("lastUpdated"))
    today = _today()
    if lc is None:
        add("P3", "KEV", f"lastChecked unparseable: {d.get('lastChecked')!r}")
    elif (today - lc).days > 3:
        add("P2", "KEV", f"KEV not checked in {(today - lc).days} days "
            f"(lastChecked {d.get('lastChecked')}) — daily fetch may be broken.")
    if lu and lc and (lc - lu).days > 7:
        add("P2", "KEV", f"lastUpdated ({d.get('lastUpdated')}) is {(lc - lu).days} "
            f"days behind lastChecked — CVE publish pipeline may be stalled.")


def check_pending():
    d = _load_json("data/pending_review.json")
    if d is None:
        return
    items = d if isinstance(d, list) else d.get("vulnerabilities", d.get("cves", []))
    today, stuck = _today(), []
    for v in items:
        cid = v.get("cve_id") or v.get("cveID") or v.get("id") or "?"
        dad = _date(v.get("date_added") or v.get("dateAdded"))
        if dad and (today - dad).days > 3:
            stuck.append(f"{cid} ({(today - dad).days}d)")
    if stuck:
        add("P3", "CVE queue", f"{len(stuck)} CVE(s) pending review >3 days: "
            + ", ".join(stuck[:8]))


def _cve_links(text):
    return set(re.findall(r"/cve/([A-Za-z0-9_\-.]+\.html)", text))


def check_sitemap_drift():
    sm = os.path.join(REPO_ROOT, "sitemap.xml")
    if not os.path.exists(sm):
        add("P2", "sitemap", "sitemap.xml missing.")
        return
    actual = {os.path.basename(p) for p in glob.glob(os.path.join(REPO_ROOT, "cve", "*.html"))}
    refs = _cve_links(open(sm, encoding="utf-8", errors="ignore").read())
    dead, orphan = refs - actual, actual - refs
    if dead:
        add("P2", "sitemap", f"{len(dead)} sitemap CVE link(s) point to missing pages "
            f"(crawler 404s): " + ", ".join(sorted(dead)[:5]))
    if orphan:
        add("P3", "sitemap", f"{len(orphan)} on-disk CVE page(s) absent from sitemap: "
            + ", ".join(sorted(orphan)[:5]))
    lf = os.path.join(REPO_ROOT, "llms-full.txt")
    if os.path.exists(lf):
        ldead = _cve_links(open(lf, encoding="utf-8", errors="ignore").read()) - actual
        if ldead:
            add("P2", "llms", f"{len(ldead)} llms-full.txt CVE link(s) point to missing pages.")


def _gh_api(path):
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY", "robertflores17/fixthevuln")
    if not token:
        return None
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}{path}",
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "FixTheVuln-HealthCheck"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


# The monitoring workflows' own failures are excluded — reporting them here is
# circular (a failed sweep can't email anyway, and GitHub's native run status
# already surfaces them), and it adds noise that drowns out real pipeline issues.
MONITORING_WORKFLOWS = {"Saturday Health Check", "Notify on workflow failure"}


def check_workflow_failures():
    data = _gh_api("/actions/runs?per_page=50")
    if not data:
        add("P3", "CI", "Could not query workflow runs (no token or API error).")
        return
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    fails = {}
    for run in data.get("workflow_runs", []):
        name = run.get("name", "?")
        if name in MONITORING_WORKFLOWS:
            continue
        if run.get("conclusion") != "failure" or run.get("event") == "pull_request":
            continue
        try:
            cd = datetime.strptime(run.get("created_at", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if cd >= cutoff:
            fails[name] = fails.get(name, 0) + 1
    for name, n in sorted(fails.items()):
        add("P1", "CI", f'Workflow "{name}" failed {n}x in the last 7 days.')


def check_urgent_issues():
    data = _gh_api("/issues?labels=tech-debt-urgent&state=open&per_page=30")
    if not isinstance(data, list):
        return
    urgent = [i for i in data if "pull_request" not in i]
    if urgent:
        lst = ", ".join(f"#{i['number']}" for i in urgent[:12])
        add("P2", "issues", f"{len(urgent)} open tech-debt-urgent issue(s): {lst}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="health-findings.md")
    args = ap.parse_args()

    for fn in (check_kev, check_pending, check_sitemap_drift,
               check_workflow_failures, check_urgent_issues):
        try:
            fn()
        except Exception as e:
            add("P3", "health-check", f"{fn.__name__} errored: {e}")

    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    findings.sort(key=lambda f: order.get(f[0], 9))
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = [f"## Saturday Health Sweep — {today}", ""]
    if findings:
        lines += [f"**{len(findings)} finding(s)** that need a look:", "",
                  "| Severity | Area | Finding |", "|---|---|---|"]
        def _cell(m):  # keep one finding per table row: no pipes, no newlines
            return m.replace("\n", " ").replace("\r", " ").replace("|", "\\|")
        lines += [f"| {s} | {a} | {_cell(m)} |" for s, a, m in findings]
    else:
        lines.append("All clear — no findings this week. ✅")
    lines += ["",
              "_Checks: KEV freshness, pending CVE queue, sitemap/llms drift, "
              "workflow failures (last 7d), open tech-debt-urgent issues. External "
              "broken links are covered by the Monday page audit._",
              "", "_Generated by `.github/workflows/health-check.yml`._"]

    with open(os.path.join(REPO_ROOT, args.out), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(len(findings))


if __name__ == "__main__":
    main()
