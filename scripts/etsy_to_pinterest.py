#!/usr/bin/env python3
"""
Etsy → Pinterest Auto-Pinner
Pins all active Etsy listing primary photos to Pinterest boards.
Routes listings to the correct board based on keyword matching.
Auto-creates boards that don't exist yet.
Skips listings already pinned (tracked in pinner_log.json + board scan).

Requirements:
    pip install requests

Usage:
    python3 etsy_to_pinterest.py --init       # Create config template
    python3 etsy_to_pinterest.py --auth       # One-time Pinterest OAuth
    python3 etsy_to_pinterest.py --dry-run    # Preview what will be pinned
    python3 etsy_to_pinterest.py              # Pin all listings
    python3 etsy_to_pinterest.py --status     # Show progress
"""

import argparse
import base64
import json
import os
import secrets
import sys
import threading
import time
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    import requests
except ImportError:
    print("Missing dependency. Install it with:\n  pip install requests")
    sys.exit(1)

# ── Paths ───────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "pinner_config.json")
TOKENS_PATH = os.path.join(SCRIPT_DIR, "pinner_tokens.json")
LOG_PATH = os.path.join(SCRIPT_DIR, "pinner_log.json")

ETSY_API_BASE = "https://openapi.etsy.com/v3"
PINTEREST_API_BASE = "https://api.pinterest.com/v5"
PINTEREST_AUTH_URL = "https://www.pinterest.com/oauth/"


# ── Config ──────────────────────────────────────────────────────────────────

def init_config():
    """Create pinner_config.json with board mapping template."""
    if os.path.exists(CONFIG_PATH):
        print(f"Config already exists: {CONFIG_PATH}")
        print("Edit it directly, or delete it and re-run --init.")
        return

    config = {
        "etsy_api_key": "PASTE_YOUR_ETSY_API_KEY_HERE",
        "etsy_shop_name": "SmartSheetByRobert",
        "pinterest_app_id": "PASTE_YOUR_PINTEREST_APP_ID_HERE",
        "pinterest_app_secret": "PASTE_YOUR_PINTEREST_APP_SECRET_HERE",
        "redirect_uri": "http://localhost:8089/callback",
        "delay_seconds": 2,
        "utm_source": "pinterest",
        "utm_medium": "social",
        "utm_campaign": "auto_pin",
        "default_board": "Cybersecurity Study Planners",
        "board_mapping": {
            "CompTIA Study Planners": [
                "CompTIA", "Security+", "Network+", "CySA+", "PenTest+",
                "A+", "CASP+", "Cloud+", "Linux+", "Data+",
                "SY0-701", "N10-009", "CS0-003", "PT0-003",
                "220-1201", "220-1202", "CAS-005", "CV0-004", "XK0-006"
            ],
            "CISSP & ISC2 Study Planners": [
                "CISSP", "CCSP", "ISC2", "(ISC)2",
                "Certified in Cybersecurity", "CC Certified"
            ],
            "AWS Certification Planners": [
                "AWS", "Cloud Practitioner", "Solutions Architect",
                "CLF-C02", "SAA-C03", "SCS-C03", "DVA-C02", "SOA-C03"
            ],
            "Cisco Certification Planners": [
                "Cisco", "CCNA", "CCNP", "CyberOps",
                "200-301", "350-401", "200-201"
            ],
            "Microsoft Azure Study Planners": [
                "Microsoft", "Azure", "AZ-900", "AZ-104", "AZ-305",
                "AZ-500", "SC-900", "SC-200", "AI-900", "MS-900"
            ],
            "Google Cloud Study Planners": [
                "Google Cloud", "GCP",
                "Associate Cloud Engineer", "Professional Cloud Architect"
            ],
            "ISACA Certification Planners": [
                "ISACA", "CISA", "CISM", "CRISC", "CGEIT"
            ],
            "GIAC & SANS Study Planners": [
                "GIAC", "GSEC", "SANS", "GCIH", "GPEN"
            ]
        },
        "board_descriptions": {
            "CompTIA Study Planners": "Study planners and exam prep resources for CompTIA certifications including Security+, Network+, CySA+, PenTest+, A+, and more.",
            "CISSP & ISC2 Study Planners": "CISSP, CCSP, and ISC2 certification study planners with domain trackers and weekly schedules.",
            "AWS Certification Planners": "AWS certification study planners for Cloud Practitioner, Solutions Architect, Security Specialty, and more.",
            "Cisco Certification Planners": "Cisco CCNA, CCNP, and CyberOps certification study planners with structured weekly schedules.",
            "Microsoft Azure Study Planners": "Microsoft Azure and security certification study planners for AZ-900, AZ-104, AZ-305, SC-900, and more.",
            "Google Cloud Study Planners": "Google Cloud certification study planners for Associate Cloud Engineer and Professional Cloud Architect.",
            "ISACA Certification Planners": "ISACA certification study planners for CISA, CISM, and CRISC with domain-by-domain tracking.",
            "GIAC & SANS Study Planners": "GIAC and SANS certification study planners for GSEC, GCIH, and other advanced security certifications.",
            "Cybersecurity Study Planners": "Cybersecurity certification study planners for security professionals. CompTIA, ISC2, AWS, Cisco, Microsoft, and more."
        }
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print(f"Created: {CONFIG_PATH}")
    print(f"\nBoard mapping ({len(config['board_mapping'])} boards + 1 default):")
    for board in config["board_mapping"]:
        kw_count = len(config["board_mapping"][board])
        print(f"  - {board} ({kw_count} keywords)")
    print(f"  - {config['default_board']} (default/catch-all)")
    print("\nNext steps:")
    print("  1. Open pinner_config.json and paste your 3 API keys")
    print("  2. Run: python3 etsy_to_pinterest.py --auth")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"Config not found. Run: python3 {sys.argv[0]} --init")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    for key in ("etsy_api_key", "pinterest_app_id", "pinterest_app_secret"):
        val = config.get(key, "")
        if not val or "PASTE" in val.upper():
            print(f"ERROR: Fill in '{key}' in {CONFIG_PATH}")
            sys.exit(1)
    return config


# ── Pinterest OAuth ─────────────────────────────────────────────────────────

_auth_code = {"code": None, "error": None}


class _OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "code" in params:
            _auth_code["code"] = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body style='font-family:sans-serif;text-align:center;padding:3rem'>"
                b"<h1>Authorization successful!</h1>"
                b"<p>You can close this tab and return to the terminal.</p>"
                b"</body></html>"
            )
        else:
            _auth_code["error"] = params.get("error", ["unknown"])[0]
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"<html><body><h1>Error: {_auth_code['error']}</h1></body></html>".encode()
            )

    def log_message(self, format, *args):
        pass


def pinterest_auth(config):
    """Interactive Pinterest OAuth 2.0 flow."""
    app_id = config["pinterest_app_id"]
    app_secret = config["pinterest_app_secret"]
    redirect_uri = config.get("redirect_uri", "http://localhost:8089/callback")
    state = secrets.token_hex(16)

    # boards:write needed to auto-create boards
    auth_url = (
        f"{PINTEREST_AUTH_URL}?"
        f"response_type=code"
        f"&client_id={app_id}"
        f"&redirect_uri={urllib.parse.quote(redirect_uri, safe='')}"
        f"&scope=boards:read,boards:write,pins:read,pins:write"
        f"&state={state}"
    )

    parsed = urllib.parse.urlparse(redirect_uri)
    port = parsed.port or 8089

    server = HTTPServer(("localhost", port), _OAuthHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    print("\nOpening Pinterest authorization in your browser...")
    print(f"If it doesn't open, visit:\n\n  {auth_url}\n")
    webbrowser.open(auth_url)

    print("Waiting for authorization (timeout: 2 min)...")
    thread.join(timeout=120)
    server.server_close()

    if not _auth_code["code"]:
        print(f"ERROR: Authorization failed. {_auth_code.get('error', 'Timeout or denied.')}")
        sys.exit(1)

    print("Exchanging authorization code for access token...")
    creds = base64.b64encode(f"{app_id}:{app_secret}".encode()).decode()
    resp = requests.post(
        f"{PINTEREST_API_BASE}/oauth/token",
        headers={
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
            "code": _auth_code["code"],
            "redirect_uri": redirect_uri,
        },
    )

    if resp.status_code != 200:
        print(f"ERROR: Token exchange failed ({resp.status_code}):\n{resp.text}")
        sys.exit(1)

    tokens = resp.json()
    with open(TOKENS_PATH, "w") as f:
        json.dump(
            {
                "access_token": tokens["access_token"],
                "refresh_token": tokens.get("refresh_token", ""),
                "expires_in": tokens.get("expires_in", 0),
                "scope": tokens.get("scope", ""),
                "created_at": int(time.time()),
            },
            f,
            indent=4,
        )

    print(f"\nPinterest auth successful! Token saved to: {TOKENS_PATH}")
    print(f"Next: python3 {sys.argv[0]} --dry-run")


def load_pinterest_token():
    if not os.path.exists(TOKENS_PATH):
        print(f"Not authorized yet. Run: python3 {sys.argv[0]} --auth")
        sys.exit(1)
    with open(TOKENS_PATH) as f:
        data = json.load(f)
    return data["access_token"]


def refresh_pinterest_token(config):
    """Refresh expired Pinterest access token."""
    if not os.path.exists(TOKENS_PATH):
        return None
    with open(TOKENS_PATH) as f:
        data = json.load(f)
    refresh = data.get("refresh_token")
    if not refresh:
        return None

    creds = base64.b64encode(
        f"{config['pinterest_app_id']}:{config['pinterest_app_secret']}".encode()
    ).decode()
    resp = requests.post(
        f"{PINTEREST_API_BASE}/oauth/token",
        headers={
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "refresh_token", "refresh_token": refresh},
    )
    if resp.status_code != 200:
        return None

    new = resp.json()
    data["access_token"] = new["access_token"]
    if "refresh_token" in new:
        data["refresh_token"] = new["refresh_token"]
    data["created_at"] = int(time.time())
    with open(TOKENS_PATH, "w") as f:
        json.dump(data, f, indent=4)
    return new["access_token"]


# ── Etsy API ────────────────────────────────────────────────────────────────

def etsy_get(api_key, path, params=None):
    resp = requests.get(
        f"{ETSY_API_BASE}{path}",
        headers={"x-api-key": api_key},
        params=params or {},
    )
    resp.raise_for_status()
    return resp.json()


def resolve_shop_id(api_key, shop_name):
    """Resolve a shop name to its numeric ID."""
    try:
        data = etsy_get(api_key, f"/application/shops/{shop_name}")
        return data["shop_id"]
    except requests.HTTPError:
        pass
    try:
        data = etsy_get(api_key, "/application/shops", {"shop_name": shop_name})
        if data.get("results"):
            return data["results"][0]["shop_id"]
    except requests.HTTPError:
        pass
    print(f"ERROR: Could not resolve Etsy shop '{shop_name}'")
    sys.exit(1)


def fetch_all_listings(api_key, shop_id):
    """Fetch all active listings with images (paginated)."""
    all_listings = []
    limit = 100
    offset = 0

    while True:
        data = etsy_get(
            api_key,
            f"/application/shops/{shop_id}/listings/active",
            {"limit": limit, "offset": offset, "includes": "Images"},
        )
        results = data.get("results", [])
        all_listings.extend(results)
        total = data.get("count", len(all_listings))

        print(f"  Fetched {len(all_listings)}/{total} listings...")
        offset += limit
        if offset >= total or not results:
            break
        time.sleep(0.5)

    return all_listings


def fetch_listing_images(api_key, listing_id):
    """Fetch images for a single listing (fallback)."""
    try:
        data = etsy_get(api_key, f"/application/listings/{listing_id}/images")
        return data.get("results", [])
    except requests.HTTPError:
        return []


# ── Pinterest API ───────────────────────────────────────────────────────────

def pinterest_get(token, path, params=None):
    resp = requests.get(
        f"{PINTEREST_API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}"},
        params=params or {},
    )
    resp.raise_for_status()
    return resp.json()


def pinterest_post(token, path, payload):
    return requests.post(
        f"{PINTEREST_API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
    )


def fetch_all_boards(token):
    """Fetch all Pinterest boards as {lowercase_name: {id, name}}."""
    boards = {}
    bookmark = None
    while True:
        params = {"page_size": 25}
        if bookmark:
            params["bookmark"] = bookmark
        data = pinterest_get(token, "/boards", params)
        for board in data.get("items", []):
            boards[board["name"].strip().lower()] = {
                "id": board["id"],
                "name": board["name"],
            }
        bookmark = data.get("bookmark")
        if not bookmark:
            break
    return boards


def create_board(token, name, description=""):
    """Create a new Pinterest board. Returns board ID."""
    resp = pinterest_post(token, "/boards", {
        "name": name,
        "description": description,
        "privacy": "PUBLIC",
    })
    if resp.status_code in (200, 201):
        board = resp.json()
        return board["id"]
    else:
        print(f"  ERROR creating board '{name}': {resp.status_code} {resp.text[:200]}")
        return None


def resolve_all_boards(token, config):
    """
    Ensure every board in board_mapping + default_board exists on Pinterest.
    Creates missing boards automatically.
    Returns {board_name: board_id} mapping.
    """
    board_mapping = config.get("board_mapping", {})
    default_board = config.get("default_board", "Cybersecurity Study Planners")
    descriptions = config.get("board_descriptions", {})

    # All board names we need
    needed = set(board_mapping.keys())
    needed.add(default_board)

    # Fetch existing boards
    existing = fetch_all_boards(token)

    resolved = {}
    for name in needed:
        key = name.strip().lower()
        if key in existing:
            resolved[name] = existing[key]["id"]
            print(f"    Found: {name}")
        else:
            desc = descriptions.get(name, "")
            board_id = create_board(token, name, desc)
            if board_id:
                resolved[name] = board_id
                print(f"    Created: {name}")
            else:
                print(f"    FAILED to create: {name}")

    return resolved


def get_existing_pin_links(token, board_id):
    """Fetch all existing pin links from a board for dedup."""
    existing = set()
    bookmark = None
    while True:
        params = {"page_size": 25}
        if bookmark:
            params["bookmark"] = bookmark
        data = pinterest_get(token, f"/boards/{board_id}/pins", params)
        for pin in data.get("items", []):
            link = pin.get("link", "")
            if link:
                clean = link.split("?")[0].rstrip("/")
                existing.add(clean)
        bookmark = data.get("bookmark")
        if not bookmark:
            break
    return existing


def scan_all_boards_for_dedup(token, board_ids):
    """Scan all boards and return a combined set of existing pin links."""
    all_links = set()
    for name, bid in board_ids.items():
        links = get_existing_pin_links(token, bid)
        all_links.update(links)
        if links:
            print(f"    {name}: {len(links)} existing pins")
    return all_links


# ── Board Routing ───────────────────────────────────────────────────────────

def match_listing_to_board(title, board_mapping, default_board):
    """
    Match a listing title to the best board using keyword matching.
    Returns the board name. Falls back to default_board.
    """
    title_upper = title.upper()

    best_board = default_board
    best_score = 0

    for board_name, keywords in board_mapping.items():
        score = 0
        for kw in keywords:
            if kw.upper() in title_upper:
                # Longer keyword matches are more specific → higher score
                score += len(kw)
        if score > best_score:
            best_score = score
            best_board = board_name

    return best_board


# ── Pin Log ─────────────────────────────────────────────────────────────────

def load_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            return json.load(f)
    return {"pinned": {}}


def save_log(log):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)


# ── Helpers ─────────────────────────────────────────────────────────────────

def get_primary_image_url(listing, api_key=None):
    """Get the best-quality primary image URL."""
    images = listing.get("images", [])
    if not images and api_key:
        images = fetch_listing_images(api_key, listing["listing_id"])
    if not images:
        return None
    primary = sorted(images, key=lambda img: img.get("rank", 999))[0]
    return primary.get("url_fullxfull") or primary.get("url_570xN")


def get_listing_url(listing, config):
    """Build the full Etsy listing URL with optional UTM tracking."""
    url = listing.get("url", "")
    if url.startswith("/"):
        url = f"https://www.etsy.com{url}"
    elif not url:
        url = f"https://www.etsy.com/listing/{listing['listing_id']}"
    utm_source = config.get("utm_source")
    if utm_source:
        sep = "&" if "?" in url else "?"
        url += (
            f"{sep}utm_source={utm_source}"
            f"&utm_medium={config.get('utm_medium', 'social')}"
            f"&utm_campaign={config.get('utm_campaign', 'auto_pin')}"
        )
    return url


def truncate(text, max_len):
    if not text:
        return ""
    text = text.strip().replace("\n", " ").replace("\r", "")
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rsplit(" ", 1)[0] + "..."


# ── Main Logic ──────────────────────────────────────────────────────────────

def create_pin_with_retry(token, config, payload, title, i, total, log, lid):
    """Create a pin, handling 401 refresh and 429 rate limit. Returns (success, token)."""
    resp = pinterest_post(token, "/pins", payload)

    if resp.status_code in (200, 201):
        pin_data = resp.json()
        log["pinned"][lid] = {
            "pin_id": pin_data.get("id", ""),
            "board": payload["board_id"],
            "title": title,
            "pinned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        save_log(log)
        print(f"  [{i}/{total}] PINNED: {title[:55]}")
        return True, token

    if resp.status_code == 401:
        print("  Token expired, refreshing...")
        new_token = refresh_pinterest_token(config)
        if not new_token:
            print("  Refresh failed. Re-run: python3 etsy_to_pinterest.py --auth")
            sys.exit(1)
        token = new_token
        resp = pinterest_post(token, "/pins", payload)
        if resp.status_code in (200, 201):
            pin_data = resp.json()
            log["pinned"][lid] = {
                "pin_id": pin_data.get("id", ""),
                "board": payload["board_id"],
                "title": title,
                "pinned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            save_log(log)
            print(f"  [{i}/{total}] PINNED (refreshed): {title[:50]}")
            return True, token
        print(f"  [{i}/{total}] FAILED after refresh ({resp.status_code}): {title[:50]}")
        return False, token

    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 60))
        print(f"  Rate limited. Waiting {retry_after}s...")
        time.sleep(retry_after)
        resp = pinterest_post(token, "/pins", payload)
        if resp.status_code in (200, 201):
            pin_data = resp.json()
            log["pinned"][lid] = {
                "pin_id": pin_data.get("id", ""),
                "board": payload["board_id"],
                "title": title,
                "pinned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            save_log(log)
            print(f"  [{i}/{total}] PINNED (retry): {title[:50]}")
            return True, token
        print(f"  [{i}/{total}] FAILED after rate limit ({resp.status_code}): {title[:50]}")
        return False, token

    print(f"  [{i}/{total}] FAILED ({resp.status_code}): {title[:50]}")
    print(f"             {resp.text[:200]}")
    return False, token


def run_pinner(config, dry_run=False):
    board_mapping = config.get("board_mapping", {})
    default_board = config.get("default_board", "Cybersecurity Study Planners")
    all_board_names = list(board_mapping.keys()) + [default_board]

    print("=" * 60)
    print("  Etsy → Pinterest Auto-Pinner")
    print(f"  Boards: {len(set(all_board_names))} ({len(board_mapping)} mapped + 1 default)")
    if dry_run:
        print("  MODE: DRY RUN (no pins will be created)")
    print("=" * 60)

    api_key = config["etsy_api_key"]
    token = load_pinterest_token()

    # Step 1: Resolve Etsy shop
    shop_name = config.get("etsy_shop_name", "SmartSheetByRobert")
    print(f"\n[1/6] Resolving Etsy shop: {shop_name}")
    shop_id = resolve_shop_id(api_key, shop_name)
    print(f"  Shop ID: {shop_id}")

    # Step 2: Fetch all active listings
    print(f"\n[2/6] Fetching active listings...")
    listings = fetch_all_listings(api_key, shop_id)
    print(f"  Total: {len(listings)} active listings")

    # Step 3: Resolve/create Pinterest boards
    print(f"\n[3/6] Resolving Pinterest boards...")
    if dry_run:
        board_ids = {name: "DRY_RUN" for name in set(all_board_names)}
        print("  Skipped (dry run)")
    else:
        board_ids = resolve_all_boards(token, config)
        print(f"  Ready: {len(board_ids)} boards")

    # Step 4: Scan boards for existing pins (dedup)
    print(f"\n[4/6] Scanning boards for existing pins (dedup)...")
    if dry_run:
        existing_links = set()
        print("  Skipped (dry run)")
    else:
        existing_links = scan_all_boards_for_dedup(token, board_ids)
        print(f"  Total existing pins across all boards: {len(existing_links)}")

    # Step 5: Load local log
    print(f"\n[5/6] Loading pin log...")
    log = load_log()
    already_logged = set(log["pinned"].keys())
    print(f"  Previously pinned (log): {len(already_logged)}")

    # Step 6: Route and pin each listing
    delay = config.get("delay_seconds", 2)
    pinned = 0
    skipped_log = 0
    skipped_board = 0
    skipped_noimg = 0
    skipped_noboard = 0
    failed = 0
    board_counts = {}

    print(f"\n[6/6] {'Previewing' if dry_run else 'Pinning'} listings...\n")

    for i, listing in enumerate(listings, 1):
        lid = str(listing["listing_id"])
        title = truncate(listing.get("title", "Untitled"), 100)
        description = truncate(listing.get("description", ""), 500)
        image_url = get_primary_image_url(listing, api_key)
        listing_url = get_listing_url(listing, config)
        listing_url_clean = listing_url.split("?")[0].rstrip("/")

        # Skip: already in local log
        if lid in already_logged:
            skipped_log += 1
            continue

        # Skip: already pinned on any board
        if listing_url_clean in existing_links:
            skipped_board += 1
            log["pinned"][lid] = {
                "title": title,
                "skipped_reason": "already_on_board",
                "pinned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            save_log(log)
            continue

        # Skip: no image
        if not image_url:
            skipped_noimg += 1
            print(f"  [{i}/{len(listings)}] SKIP (no image): {title[:50]}")
            continue

        # Route to correct board
        target_board = match_listing_to_board(title, board_mapping, default_board)
        board_id = board_ids.get(target_board)

        if not board_id:
            skipped_noboard += 1
            print(f"  [{i}/{len(listings)}] SKIP (no board): {title[:50]}")
            continue

        board_counts[target_board] = board_counts.get(target_board, 0) + 1

        if dry_run:
            print(f"  [{i}/{len(listings)}] WOULD PIN: {title[:55]}")
            print(f"             Board: {target_board}")
            pinned += 1
            continue

        payload = {
            "board_id": board_id,
            "title": title,
            "description": description,
            "link": listing_url,
            "media_source": {
                "source_type": "image_url",
                "url": image_url,
            },
        }

        success, token = create_pin_with_retry(
            token, config, payload, title, i, len(listings), log, lid
        )
        if success:
            pinned += 1
        else:
            failed += 1

        if i < len(listings):
            time.sleep(delay)

    # Summary
    total_skipped = skipped_log + skipped_board + skipped_noimg + skipped_noboard
    print(f"\n{'─' * 55}")
    print(f"  {'PREVIEW' if dry_run else 'COMPLETE'}")
    print(f"  {'Would pin' if dry_run else 'Pinned'}:   {pinned}")
    print(f"  Skipped:  {total_skipped}")
    if skipped_log:
        print(f"    - already in log:    {skipped_log}")
    if skipped_board:
        print(f"    - already on board:  {skipped_board}")
    if skipped_noimg:
        print(f"    - no image:          {skipped_noimg}")
    if skipped_noboard:
        print(f"    - board not found:   {skipped_noboard}")
    if failed:
        print(f"  Failed:   {failed}")
    print(f"  Total listings: {len(listings)}")

    if board_counts:
        print(f"\n  {'Routing' if dry_run else 'Pins'} per board:")
        for board, count in sorted(board_counts.items(), key=lambda x: -x[1]):
            print(f"    {board}: {count}")

    print(f"{'─' * 55}")


def show_status():
    log = load_log()
    count = len(log.get("pinned", {}))
    print(f"\nPinning Status")
    print(f"  Listings pinned: {count}")
    print(f"  Log: {LOG_PATH}")
    if count:
        recent = list(log["pinned"].items())[-5:]
        print(f"\n  Last {len(recent)} pins:")
        for lid, info in recent:
            print(f"    #{lid}: {info.get('title', '?')[:50]}  ({info.get('pinned_at', '?')})")


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Pin Etsy listings to Pinterest boards with keyword routing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Steps:\n"
            "  1. python3 etsy_to_pinterest.py --init      # create config\n"
            "  2. Edit pinner_config.json with your keys\n"
            "  3. python3 etsy_to_pinterest.py --auth       # Pinterest login\n"
            "  4. python3 etsy_to_pinterest.py --dry-run    # preview routing\n"
            "  5. python3 etsy_to_pinterest.py              # pin everything\n"
        ),
    )
    parser.add_argument("--init", action="store_true", help="Create config template")
    parser.add_argument("--auth", action="store_true", help="Pinterest OAuth setup (one-time)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating pins")
    parser.add_argument("--status", action="store_true", help="Show pinning progress")
    args = parser.parse_args()

    if args.init:
        init_config()
        return

    if args.status:
        show_status()
        return

    config = load_config()

    if args.auth:
        pinterest_auth(config)
        return

    run_pinner(config, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
