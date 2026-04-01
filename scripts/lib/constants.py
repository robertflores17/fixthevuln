"""
FixTheVuln — Shared Constants

Single source of truth for CSS versions, site config, and hardcoded values.
Bump CSS versions here — all generators pick them up automatically.
"""

# ---------------------------------------------------------------------------
# CSS Cache-Bust Versions (bump here after editing CSS files)
# ---------------------------------------------------------------------------

STYLE_CSS_VERSION = 8
QUIZ_CSS_VERSION = 3
COMPARISON_CSS_VERSION = 3
STORE_CSS_VERSION = 6
PRACTICE_TESTS_CSS_VERSION = 1

# ---------------------------------------------------------------------------
# Site Config
# ---------------------------------------------------------------------------

SITE_NAME = "FixTheVuln"
SITE_URL = "https://fixthevuln.com"
OG_IMAGE = f"{SITE_URL}/og-image.png"
CYBERFOLIO_URL = "https://cyberfolio.io"

# ---------------------------------------------------------------------------
# Cloudflare Analytics
# ---------------------------------------------------------------------------

CF_ANALYTICS_TOKEN = "8304415b01684a00adedcbf6975458d7"

# ---------------------------------------------------------------------------
# Favicon (inline SVG data URI — identical across all pages)
# ---------------------------------------------------------------------------

FAVICON_SVG = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' "
    "fill='%23667eea'/%3E%3Ctext x='50' y='68' font-family='Arial,sans-serif' "
    "font-size='60' font-weight='bold' fill='white' text-anchor='middle'%3E"
    "F%3C/text%3E%3C/svg%3E"
)
