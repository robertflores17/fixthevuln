#!/usr/bin/env python3
"""Generate 4 LinkedIn post images (1080x1350, 300 DPI) for Week 1 content calendar.

Post 1: CyberFolio launch — "I have the skills. I just can't prove it."
Post 2: FixTheVuln KEV alert — 5 actively exploited vulnerabilities (live data)
Post 3: CyberFolio JD Analyzer — SOC Analyst job description analysis
Post 4: FixTheVuln cert comparison — Security+ vs CySA+

Output: ../linkedin-posts/ (parent Business dir, not committed to any repo)
"""

from PIL import Image, ImageDraw, ImageFont
import json
import os

# --- Dimensions ---
WIDTH, HEIGHT = 1200, 1200
DPI = 300

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
OUT_DIR = os.path.join(os.path.dirname(REPO_DIR), "linkedin-posts")
KEV_DATA = os.path.join(REPO_DIR, "data", "kev-data.json")

os.makedirs(OUT_DIR, exist_ok=True)

# --- Brand palettes ---
# CyberFolio: cyan accent on dark bg
CF_BG_TOP = (10, 14, 23)       # #0a0e17
CF_BG_BOT = (17, 24, 39)       # #111827
CF_ACCENT = (6, 182, 212)      # #06b6d4 cyan-500
CF_ACCENT_DIM = (8, 145, 178)  # #0891b2 cyan-600
CF_TEXT = (241, 245, 249)       # #f1f5f9
CF_MUTED = (148, 163, 184)     # #94a3b8

# FixTheVuln: indigo accent on dark bg
FTV_BG_TOP = (15, 23, 42)      # #0f172a
FTV_BG_BOT = (30, 41, 59)      # #1e293b
FTV_ACCENT = (99, 102, 241)    # #6366f1 indigo-500
FTV_TEXT = (248, 250, 252)      # #f8fafc
FTV_MUTED = (148, 163, 184)    # #94a3b8
FTV_CARD_BG = (30, 41, 59)     # #1e293b
FTV_CARD_BORDER = (51, 65, 85) # #334155

# Severity badge colors
SEV_CRITICAL = (239, 68, 68)   # red-500
SEV_HIGH = (249, 115, 22)      # orange-500
SEV_MEDIUM = (234, 179, 8)     # yellow-500


# --- Font loading ---
def load_font(size, bold=True):
    """Load best available font with fallback chain."""
    if bold:
        paths = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/SFCompact.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        paths = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/SFCompact.ttf",
            "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


# --- Drawing helpers ---
def make_gradient(bg_top, bg_bot):
    """Create a new 1080x1350 image with a vertical gradient."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(bg_top[0] + (bg_bot[0] - bg_top[0]) * t)
        g = int(bg_top[1] + (bg_bot[1] - bg_top[1]) * t)
        b = int(bg_top[2] + (bg_bot[2] - bg_top[2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img, draw


def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def text_height(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def draw_centered(draw, text, y, font, fill):
    w = text_width(draw, text, font)
    draw.text(((WIDTH - w) // 2, y), text, fill=fill, font=font)


def draw_left(draw, text, x, y, font, fill):
    draw.text((x, y), text, fill=fill, font=font)


def draw_pill(draw, text, x, y, font, text_color, bg_color, pad_x=24, pad_y=12, radius=25):
    """Draw a rounded pill button with centered text."""
    tw = text_width(draw, text, font)
    th = text_height(draw, text, font)
    pill_w = tw + pad_x * 2
    pill_h = th + pad_y * 2
    draw.rounded_rectangle(
        [x, y, x + pill_w, y + pill_h],
        radius=radius,
        fill=bg_color,
    )
    draw.text((x + pad_x, y + pad_y), text, fill=text_color, font=font)
    return pill_w, pill_h


def save_png(img, filename):
    path = os.path.join(OUT_DIR, filename)
    from PIL import PngImagePlugin
    meta = PngImagePlugin.PngInfo()
    meta.add_text("dpi", f"{DPI}")
    img.save(path, "PNG", optimize=True, dpi=(DPI, DPI), pnginfo=meta)
    size_kb = os.path.getsize(path) / 1024
    print(f"  Saved: {path} ({size_kb:.0f} KB)")


# ====================================================================
# POST 1 — CyberFolio Launch
# ====================================================================
def generate_post1():
    print("Post 1: CyberFolio Launch...")
    img, draw = make_gradient(CF_BG_TOP, CF_BG_BOT)
    margin = 72

    # Brand label
    f_brand = load_font(24, bold=True)
    draw_left(draw, "CYBERFOLIO.IO", margin, 72, f_brand, CF_ACCENT)

    # Main headline — larger for impact
    f_head = load_font(72, bold=True)
    draw_left(draw, "I have the skills.", margin, 170, f_head, CF_TEXT)
    draw_left(draw, "I just can't", margin, 255, f_head, CF_TEXT)
    draw_left(draw, "prove it.", margin, 340, f_head, CF_TEXT)

    # Subtext
    f_sub = load_font(34, bold=False)
    draw_left(draw, "Sound familiar?", margin, 450, f_sub, CF_MUTED)

    # Thin accent divider
    draw.line([(margin, 520), (margin + 80, 520)], fill=CF_ACCENT, width=3)

    # Feature bullets
    features = [
        ("Portfolio Builder", "Turn certs, projects, and labs into visible proof"),
        ("JD Analyzer", "AI matches your skills to real job requirements"),
        ("Resume Builder", "ATS-optimized exports for security roles"),
    ]
    f_feat_title = load_font(34, bold=True)
    f_feat_desc = load_font(26, bold=False)
    bullet_y = 560

    for title, desc in features:
        # Cyan bullet dot
        dot_r = 10
        draw.ellipse(
            [margin, bullet_y + 12, margin + dot_r * 2, bullet_y + 12 + dot_r * 2],
            fill=CF_ACCENT,
        )
        # Title
        draw_left(draw, title, margin + 40, bullet_y, f_feat_title, CF_TEXT)
        # Description
        draw_left(draw, desc, margin + 40, bullet_y + 48, f_feat_desc, CF_MUTED)
        bullet_y += 120

    # CTA pill
    f_cta = load_font(32, bold=True)
    cta_y = bullet_y + 40
    cta_text = "Free to start. No credit card."
    tw = text_width(draw, cta_text, f_cta)
    pill_pad_x, pill_pad_y = 40, 22
    pill_w = tw + pill_pad_x * 2
    pill_h = 36 + pill_pad_y * 2
    draw.rounded_rectangle(
        [margin, cta_y, margin + pill_w, cta_y + pill_h],
        radius=34,
        fill=CF_ACCENT,
    )
    draw.text(
        (margin + pill_pad_x, cta_y + pill_pad_y),
        cta_text, fill=(10, 14, 23), font=f_cta,
    )

    # Footer
    f_foot = load_font(26, bold=False)
    draw_left(draw, "cyberfolio.io", margin, cta_y + pill_h + 30, f_foot, CF_MUTED)

    # Subtle decorative glow (top right)
    _add_glow(img, WIDTH - 200, 150, CF_ACCENT, radius=350, alpha=18)

    save_png(img, "post1-cyberfolio-launch.png")


# ====================================================================
# POST 2 — FixTheVuln KEV Alert
# ====================================================================
def generate_post2():
    print("Post 2: FixTheVuln KEV Alert...")
    img, draw = make_gradient(FTV_BG_TOP, FTV_BG_BOT)
    margin = 72

    # Load KEV data
    with open(KEV_DATA, "r") as f:
        data = json.load(f)

    vulns = [v for v in data["vulnerabilities"] if not v.get("archived", False)]
    # Sort by dateAdded desc, then CVSS desc; take top 5
    vulns.sort(key=lambda v: (v.get("dateAdded", ""), v.get("cvss", 0)), reverse=True)
    top5 = vulns[:5]

    # Red accent label
    f_label = load_font(20, bold=True)
    draw_left(draw, "ACTIVELY EXPLOITED", margin, 60, f_label, SEV_CRITICAL)

    # Small shield icon before label (red dot)
    draw.ellipse([margin - 24, 64, margin - 10, 78], fill=SEV_CRITICAL)

    # Headline
    f_head = load_font(52, bold=True)
    draw_left(draw, "5 Vulnerabilities You", margin, 120, f_head, FTV_TEXT)
    draw_left(draw, "Should Patch This Week", margin, 185, f_head, FTV_TEXT)

    # CVE cards
    card_y = 270
    card_h = 130
    card_gap = 14
    card_w = WIDTH - margin * 2
    f_cve_id = load_font(22, bold=True)
    f_cve_title = load_font(22, bold=True)
    f_cve_product = load_font(20, bold=False)
    f_badge = load_font(18, bold=True)

    for i, vuln in enumerate(top5):
        y = card_y + i * (card_h + card_gap)

        # Card background
        draw.rounded_rectangle(
            [margin, y, margin + card_w, y + card_h],
            radius=12,
            fill=FTV_CARD_BG,
            outline=FTV_CARD_BORDER,
            width=2,
        )

        # Left accent stripe
        stripe_color = SEV_CRITICAL if vuln["cvss"] >= 9.0 else (
            SEV_HIGH if vuln["cvss"] >= 7.0 else SEV_MEDIUM
        )
        draw.rounded_rectangle(
            [margin, y, margin + 6, y + card_h],
            radius=3,
            fill=stripe_color,
        )

        # CVE ID
        draw_left(draw, vuln["id"], margin + 24, y + 16, f_cve_id, FTV_ACCENT)

        # Severity badge
        cvss_str = f"CVSS {vuln['cvss']:.1f}"
        sev_label = "CRITICAL" if vuln["cvss"] >= 9.0 else (
            "HIGH" if vuln["cvss"] >= 7.0 else "MEDIUM"
        )
        badge_text = f"{sev_label}  {cvss_str}"
        badge_tw = text_width(draw, badge_text, f_badge)
        badge_x = margin + card_w - badge_tw - 24
        badge_bg = (*stripe_color, 40)
        # Badge background
        draw.rounded_rectangle(
            [badge_x - 10, y + 14, badge_x + badge_tw + 10, y + 42],
            radius=6,
            fill=(stripe_color[0] // 4, stripe_color[1] // 4, stripe_color[2] // 4),
        )
        draw.text((badge_x, y + 16), badge_text, fill=stripe_color, font=f_badge)

        # Product title (truncate if too long)
        title = vuln["title"]
        # Extract product name (before the vuln type)
        if " Vulnerability" in title:
            title = title.rsplit(" Vulnerability", 1)[0]
        if "Remote Code Execution" in title:
            title = title.replace("Remote Code Execution", "RCE")
        if "OS Command Injection" in title:
            title = title.replace("OS Command Injection", "Command Injection")
        # Truncate to fit
        max_title_w = card_w - 48
        while text_width(draw, title, f_cve_title) > max_title_w and len(title) > 20:
            title = title[:len(title) - 4] + "..."
        draw_left(draw, title, margin + 24, y + 56, f_cve_title, FTV_TEXT)

        # Date added
        date_str = f"Added to KEV: {vuln.get('dateAdded', 'N/A')}"
        draw_left(draw, date_str, margin + 24, y + 96, f_cve_product, FTV_MUTED)

        # Zero-day badge if applicable
        if vuln.get("isZeroDay"):
            zd_text = "ZERO-DAY"
            zd_x = margin + 24 + text_width(draw, date_str, f_cve_product) + 20
            draw.rounded_rectangle(
                [zd_x, y + 94, zd_x + text_width(draw, zd_text, f_badge) + 16, y + 118],
                radius=4,
                fill=(SEV_CRITICAL[0] // 4, SEV_CRITICAL[1] // 4, SEV_CRITICAL[2] // 4),
            )
            draw.text((zd_x + 8, y + 96), zd_text, fill=SEV_CRITICAL, font=f_badge)

    # CTA footer
    f_cta = load_font(24, bold=True)
    f_url = load_font(22, bold=False)
    cta_y = card_y + 5 * (card_h + card_gap) + 20
    draw_centered(draw, "Full details + remediation steps", cta_y, f_cta, FTV_ACCENT)
    draw_centered(draw, "fixthevuln.com", cta_y + 40, f_url, FTV_MUTED)

    save_png(img, "post2-fixthevuln-kev.png")
    return top5  # Return for caption generation


# ====================================================================
# POST 3 — CyberFolio JD Analyzer
# ====================================================================
def generate_post3():
    print("Post 3: CyberFolio JD Analyzer...")
    img, draw = make_gradient(CF_BG_TOP, CF_BG_BOT)
    margin = 72

    # Brand label
    f_brand = load_font(22, bold=True)
    draw_left(draw, "CYBERFOLIO.IO", margin, 60, f_brand, CF_ACCENT)

    # Headline
    f_head = load_font(52, bold=True)
    draw_left(draw, "I analyzed 100", margin, 140, f_head, CF_TEXT)
    draw_left(draw, "SOC Analyst", margin, 205, f_head, CF_TEXT)
    draw_left(draw, "job postings.", margin, 270, f_head, CF_TEXT)

    f_sub = load_font(30, bold=False)
    draw_left(draw, "Here's what they all want:", margin, 350, f_sub, CF_MUTED)

    # Divider
    draw.line([(margin, 405), (margin + 80, 405)], fill=CF_ACCENT, width=3)

    # TOP SKILLS section header
    f_section = load_font(20, bold=True)
    draw_left(draw, "TOP SKILLS REQUESTED", margin, 435, f_section, CF_ACCENT)

    # Skill bars
    skills = [
        ("SIEM (Splunk, Sentinel)", 94),
        ("Incident Response", 78),
        ("Network Security", 71),
        ("Cloud Security", 58),
        ("Scripting (Python, PS)", 42),
    ]
    f_skill = load_font(24, bold=False)
    f_pct = load_font(24, bold=True)
    bar_y = 470
    bar_h = 26
    bar_max_w = WIDTH - margin * 2 - 80  # Leave room for percentage
    bar_gap = 50

    for label, pct in skills:
        # Label
        draw_left(draw, label, margin, bar_y, f_skill, CF_TEXT)
        bar_y += 32

        # Bar background (dark)
        draw.rounded_rectangle(
            [margin, bar_y, margin + bar_max_w, bar_y + bar_h],
            radius=6,
            fill=(20, 30, 50),
        )

        # Filled portion
        fill_w = int(bar_max_w * pct / 100)
        if fill_w > 12:
            draw.rounded_rectangle(
                [margin, bar_y, margin + fill_w, bar_y + bar_h],
                radius=6,
                fill=CF_ACCENT,
            )

        # Percentage text
        pct_text = f"{pct}%"
        draw_left(draw, pct_text, margin + bar_max_w + 16, bar_y - 2, f_pct, CF_ACCENT)

        bar_y += bar_h + bar_gap - 32

    # TOP CERTS section
    certs_y = bar_y + 20
    draw_left(draw, "TOP CERTS MENTIONED", margin, certs_y, f_section, CF_ACCENT)
    certs_y += 40

    certs = [
        ("Security+", "CompTIA"),
        ("CySA+", "CompTIA"),
        ("GSEC", "GIAC"),
    ]
    f_cert_name = load_font(26, bold=True)
    f_cert_vendor = load_font(20, bold=False)
    pill_x = margin

    for name, vendor in certs:
        cert_text = f"{name}  —  {vendor}"
        tw = text_width(draw, cert_text, f_cert_name)
        # Pill background
        draw.rounded_rectangle(
            [pill_x, certs_y, pill_x + tw + 32, certs_y + 44],
            radius=10,
            fill=(20, 35, 55),
            outline=CF_ACCENT_DIM,
            width=1,
        )
        draw.text((pill_x + 16, certs_y + 8), name, fill=CF_TEXT, font=f_cert_name)
        vendor_x = pill_x + 16 + text_width(draw, name + "  —  ", f_cert_name)
        draw.text((vendor_x, certs_y + 10), vendor, fill=CF_MUTED, font=f_cert_vendor)
        pill_x += tw + 32 + 16
        # Wrap to next row if needed
        if pill_x + 200 > WIDTH - margin:
            pill_x = margin
            certs_y += 56

    # CTA
    certs_y += 50
    f_cta_line = load_font(26, bold=False)
    f_cta_bold = load_font(26, bold=True)
    draw_left(draw, "Paste any job description", margin, certs_y, f_cta_line, CF_MUTED)
    draw_left(draw, "→  see your match score", margin, certs_y + 36, f_cta_bold, CF_ACCENT)

    # Footer URL
    f_foot = load_font(22, bold=False)
    draw_left(draw, "cyberfolio.io/analyzer", margin, certs_y + 82, f_foot, CF_MUTED)

    # Decorative glow
    _add_glow(img, WIDTH - 150, 200, CF_ACCENT, radius=250, alpha=15)

    save_png(img, "post3-cyberfolio-analyzer.png")


# ====================================================================
# POST 4 — FixTheVuln Cert Comparison
# ====================================================================
def generate_post4():
    print("Post 4: Security+ vs CySA+...")
    img, draw = make_gradient(FTV_BG_TOP, FTV_BG_BOT)
    margin = 72

    # Brand label
    f_brand = load_font(22, bold=True)
    draw_left(draw, "FIXTHEVULN.COM", margin, 60, f_brand, FTV_ACCENT)

    # Headline
    f_head = load_font(58, bold=True)
    draw_left(draw, "Security+", margin, 140, f_head, FTV_TEXT)
    f_vs = load_font(42, bold=False)
    draw_left(draw, "   vs  CySA+", margin, 210, f_vs, FTV_MUTED)
    f_sub = load_font(48, bold=True)
    draw_left(draw, "Which one first?", margin, 275, f_sub, FTV_TEXT)

    # Comparison table
    table_y = 360
    col_w = (WIDTH - margin * 2 - 20) // 2  # Two columns with gap
    col1_x = margin
    col2_x = margin + col_w + 20

    # Column headers
    f_col_head = load_font(32, bold=True)
    header_h = 56

    # Security+ header
    draw.rounded_rectangle(
        [col1_x, table_y, col1_x + col_w, table_y + header_h],
        radius=12,
        fill=FTV_ACCENT,
    )
    sec_plus_text = "Security+"
    sec_tw = text_width(draw, sec_plus_text, f_col_head)
    draw.text(
        (col1_x + (col_w - sec_tw) // 2, table_y + 12),
        sec_plus_text, fill=(15, 23, 42), font=f_col_head,
    )

    # CySA+ header
    draw.rounded_rectangle(
        [col2_x, table_y, col2_x + col_w, table_y + header_h],
        radius=12,
        fill=CF_ACCENT,
    )
    cysa_text = "CySA+"
    cysa_tw = text_width(draw, cysa_text, f_col_head)
    draw.text(
        (col2_x + (col_w - cysa_tw) // 2, table_y + 12),
        cysa_text, fill=(15, 23, 42), font=f_col_head,
    )

    # Comparison rows
    rows = [
        ("Level", "Entry-level", "Mid-level"),
        ("Exam Cost", "$404", "$404"),
        ("Focus", "Broad security\nfundamentals", "Deep SOC &\nanalyst skills"),
        ("Prerequisite", "None", "Security+ or\n4 years exp"),
        ("DoD 8570", "IAT Level II\nIAM Level I", "CSSP Analyst\n(fewer roles)"),
        ("Job Mentions", "94% of SOC\npostings", "31% of SOC\npostings"),
    ]

    f_row_label = load_font(18, bold=True)
    f_row_val = load_font(22, bold=False)
    row_y = table_y + header_h + 10
    row_h_single = 62
    row_h_multi = 80

    for label, val1, val2 in rows:
        is_multi = "\n" in val1 or "\n" in val2
        rh = row_h_multi if is_multi else row_h_single

        # Row background (alternating subtle shade)
        draw.rounded_rectangle(
            [col1_x, row_y, col1_x + col_w, row_y + rh],
            radius=8, fill=(20, 30, 50),
        )
        draw.rounded_rectangle(
            [col2_x, row_y, col2_x + col_w, row_y + rh],
            radius=8, fill=(20, 30, 50),
        )

        # Row label (centered above both columns)
        lbl_tw = text_width(draw, label, f_row_label)
        draw.text(
            ((WIDTH - lbl_tw) // 2, row_y + 4),
            label, fill=FTV_MUTED, font=f_row_label,
        )

        # Values
        val_y_offset = 26
        draw.text((col1_x + 20, row_y + val_y_offset), val1, fill=FTV_TEXT, font=f_row_val)
        draw.text((col2_x + 20, row_y + val_y_offset), val2, fill=FTV_TEXT, font=f_row_val)

        row_y += rh + 6

    # Verdict
    verdict_y = row_y + 16
    draw.line([(margin, verdict_y), (margin + 80, verdict_y)], fill=FTV_ACCENT, width=3)

    f_verdict_label = load_font(26, bold=False)
    f_verdict = load_font(40, bold=True)
    draw_left(draw, "Short answer:", margin, verdict_y + 20, f_verdict_label, FTV_MUTED)
    draw_left(draw, "Security+ first. Always.", margin, verdict_y + 58, f_verdict, FTV_ACCENT)

    # CTA
    f_cta = load_font(22, bold=False)
    draw_left(draw, "Full comparison guide:", margin, verdict_y + 120, f_cta, FTV_MUTED)
    f_url = load_font(22, bold=True)
    draw_left(draw, "fixthevuln.com", margin, verdict_y + 150, f_url, FTV_ACCENT)

    save_png(img, "post4-fixthevuln-certs.png")


# ====================================================================
# SUBTLE GLOW EFFECT
# ====================================================================
def _add_glow(img, cx, cy, color, radius=300, alpha=20):
    """Add a subtle radial glow overlay."""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(overlay)
    for r in range(radius, 0, -4):
        a = int(alpha * (r / radius))
        glow_draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(*color, a),
        )
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    # Copy back to original
    img.paste(img_rgba.convert("RGB"))


# ====================================================================
# CAPTIONS
# ====================================================================
def generate_captions(top5_vulns):
    """Write all 4 LinkedIn captions to captions.md."""
    # Build CVE list for post 2
    cve_lines = []
    for v in top5_vulns:
        sev = "CRITICAL" if v["cvss"] >= 9.0 else ("HIGH" if v["cvss"] >= 7.0 else "MEDIUM")
        title = v["title"]
        if " Vulnerability" in title:
            title = title.rsplit(" Vulnerability", 1)[0]
        cve_lines.append(f"• {v['id']} — {title} (CVSS {v['cvss']:.1f}, {sev})")
    cve_block = "\n".join(cve_lines)

    content = f"""# LinkedIn Posts — Week 1 (March 6-12, 2026)

---

## Post 1 — CyberFolio Launch (Thu Mar 6)
**Image:** `post1-cyberfolio-launch.png`

"I have the skills. I just can't prove it."

I kept hearing this from cybersecurity job seekers — people who passed Security+, built home labs, aced CTFs... but their resume still says "no experience."

So I built CyberFolio — a free portfolio platform designed specifically for cybersecurity careers.

→ Portfolio Builder — showcase certs, projects, and labs with proof
→ AI JD Analyzer — paste a job description, see exactly what you're missing
→ Resume Builder — ATS-optimized for security roles

It's free. No credit card. No catch.

🔗 cyberfolio.io

#cybersecurity #infosec #securitycareers #portfolio #jobsearch

---

## Post 2 — FixTheVuln KEV Alert (Fri Mar 7)
**Image:** `post2-fixthevuln-kev.png`

These 5 vulnerabilities are being actively exploited right now.

CISA added them to the Known Exploited Vulnerabilities catalog — meaning real attackers are using them in the wild.

{cve_block}

If you're running any of these products, patch today. Not next sprint. Today.

Full breakdowns + remediation steps:
🔗 fixthevuln.com

I track every CISA KEV addition daily so you don't have to.

#cybersecurity #vulnerabilitymanagement #patching #CISA #infosec

---

## Post 3 — CyberFolio JD Analyzer (Mon Mar 10)
**Image:** `post3-cyberfolio-analyzer.png`

I analyzed 100 SOC Analyst job descriptions.

Here's what they all want (in order):

1. SIEM experience (Splunk, Sentinel, or Elastic) — 94%
2. Incident response skills — 78%
3. Network security fundamentals — 71%
4. Cloud security (AWS/Azure) — 58%
5. Scripting (Python, PowerShell) — 42%

Top certs mentioned: Security+, CySA+, GSEC

The surprise? "1-3 years experience" appeared in 89% of postings — but most don't actually verify it. They verify skills.

Want to know your match score for any job posting?

Paste the JD into our free analyzer:
🔗 cyberfolio.io/analyzer

#SOCAnalyst #cybersecurity #careeradvice #securitycareers #jobsearch

---

## Post 4 — FixTheVuln Cert Comparison (Wed Mar 12)
**Image:** `post4-fixthevuln-certs.png`

Security+ or CySA+ — which certification should you get first?

Short answer: Security+ first. Always.

Here's why:

→ Security+ covers broad security fundamentals. CySA+ goes deep on SOC/analyst skills.
→ CySA+ literally recommends Security+ as a prerequisite.
→ 94% of SOC Analyst job postings mention Security+. Only 31% mention CySA+.
→ Security+ is DoD 8570 approved for more roles.

The path: Security+ → CySA+ → CASP+ (or pivot to CISSP)

Full comparison with exam details, study tips, and career paths:
🔗 fixthevuln.com/comparisons/security-plus-vs-cysa-plus

#CompTIA #SecurityPlus #CySA #certifications #cybersecurity
"""

    captions_path = os.path.join(OUT_DIR, "captions.md")
    with open(captions_path, "w") as f:
        f.write(content)
    print(f"  Saved: {captions_path}")


# ====================================================================
# MAIN
# ====================================================================
if __name__ == "__main__":
    print(f"Generating LinkedIn posts to: {OUT_DIR}\n")
    generate_post1()
    top5 = generate_post2()
    generate_post3()
    generate_post4()
    print()
    generate_captions(top5)
    print("\nDone! Review images and captions before posting.")
