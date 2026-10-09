"""
FixTheVuln — Shared Constants

Single source of truth for CSS versions, site config, and hardcoded values.
Bump CSS versions here — all generators pick them up automatically.
"""

# ---------------------------------------------------------------------------
# CSS Cache-Bust Versions (bump here after editing CSS files)
# ---------------------------------------------------------------------------

STYLE_CSS_VERSION = 13
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
# Favicon (shared SVG file — identical across all pages)
# ---------------------------------------------------------------------------

FAVICON_SVG = "/favicon.svg"
