"""
Shared state store for the AI vulnerability intel signal queue
(data/ai-vuln-intel.json). Every aggregator (OWASP staleness, MITRE ATLAS
diff, framework GHSA advisories) writes into the same queue via add_entry,
which dedups by `id` so re-running an aggregator never double-queues the
same signal. record_loop_round enforces the 3-round claim-verification
loop cap from the design spec (section 5): past 3 rounds an entry flips to
needs_human_review instead of looping forever or force-publishing.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
STATE_FILE = DATA_DIR / "ai-vuln-intel.json"

LOOP_CAP = 3


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_updated": None, "entries": []}


def save_state(state):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def _find(state, entry_id):
    for e in state["entries"]:
        if e["id"] == entry_id:
            return e
    return None


def add_entry(state, entry):
    """Add entry if entry['id'] isn't already queued. Returns True if added."""
    if _find(state, entry["id"]) is not None:
        return False
    entry.setdefault("loop_rounds", 0)
    entry.setdefault("notes", "")
    state["entries"].append(entry)
    return True


def get_entries(state, status=None):
    if status is None:
        return list(state["entries"])
    return [e for e in state["entries"] if e["status"] == status]


def set_status(state, entry_id, status, notes=""):
    e = _find(state, entry_id)
    if e is None:
        return False
    e["status"] = status
    if notes:
        e["notes"] = notes
    return True


def record_loop_round(state, entry_id):
    """Increment loop_rounds for entry_id. Returns the resulting status:
    'in_review' while loop_rounds <= LOOP_CAP, 'needs_human_review' once
    it exceeds LOOP_CAP."""
    e = _find(state, entry_id)
    if e is None:
        raise KeyError(f"No entry with id {entry_id!r}")
    e["loop_rounds"] += 1
    e["status"] = "in_review" if e["loop_rounds"] <= LOOP_CAP else "needs_human_review"
    return e["status"]
