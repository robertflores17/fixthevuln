#!/usr/bin/env python3
"""Generate a 2000x2000 cybersecurity tips infographic (Reddit-safe, no branding)."""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = HEIGHT = 2000
OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "hero-image.png")


# --- colours ---
def gradient_color(y, h):
    """Dark gradient: deep navy (#0f172a) to dark slate (#1e293b)."""
    t = y / h
    r = int(15 + (30 - 15) * t)
    g = int(23 + (41 - 23) * t)
    b = int(42 + (59 - 42) * t)
    return (r, g, b)


ACCENT = (99, 102, 241)       # indigo-500
ACCENT_LIGHT = (165, 180, 252)  # indigo-300
GREEN = (34, 197, 94)          # green-500
WHITE = (248, 250, 252)
MUTED = (148, 163, 184)       # slate-400
CARD_BG = (30, 41, 59)        # slate-800
CARD_BORDER = (51, 65, 85)    # slate-700

img = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# Draw gradient background
for y in range(HEIGHT):
    color = gradient_color(y, HEIGHT)
    draw.line([(0, y), (WIDTH, y)], fill=color)


# --- Load fonts ---
def load_font(size, bold=False):
    font_paths = [
        "/System/Library/Fonts/SFCompact-Bold.otf" if bold else "/System/Library/Fonts/SFCompact-Regular.otf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


font_title = load_font(88, bold=True)
font_subtitle = load_font(42)
font_tip_num = load_font(38, bold=True)
font_tip_title = load_font(40, bold=True)
font_tip_desc = load_font(32)
font_footer = load_font(30)
font_section = load_font(36, bold=True)


def draw_centered(text, y, font, fill=WHITE):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((WIDTH - w) // 2, y), text, fill=fill, font=font)


def draw_shield_icon(cx, cy, size=60):
    """Draw a small shield icon."""
    pts = [
        (cx, cy - size),
        (cx + size * 0.7, cy - size * 0.5),
        (cx + size * 0.65, cy + size * 0.25),
        (cx, cy + size * 0.6),
        (cx - size * 0.65, cy + size * 0.25),
        (cx - size * 0.7, cy - size * 0.5),
    ]
    draw.polygon(pts, outline=ACCENT, width=3)
    # Checkmark inside
    check_pts = [
        (cx - size * 0.2, cy - size * 0.05),
        (cx - size * 0.02, cy + size * 0.15),
        (cx + size * 0.25, cy - size * 0.2),
    ]
    draw.line(check_pts, fill=GREEN, width=4)


# ============================================================
# HEADER
# ============================================================

# Shield icon at top
draw_shield_icon(WIDTH // 2, 130, size=70)

# Title
draw_centered("10 Security Habits", 230, font_title)
draw_centered("That Actually Matter", 330, font_title)

# Subtitle
draw_centered("A quick-reference guide for everyday users", 445, font_subtitle, fill=MUTED)

# Divider line
div_w = 200
draw.line(
    [(WIDTH // 2 - div_w // 2, 510), (WIDTH // 2 + div_w // 2, 510)],
    fill=ACCENT, width=3
)

# ============================================================
# TIPS — 2 columns, 5 rows
# ============================================================

tips = [
    ("Use a password manager",
     "One master password, unique\ncredentials everywhere."),
    ("Enable MFA everywhere",
     "SMS is okay, authenticator\napps or hardware keys are better."),
    ("Keep software updated",
     "Most breaches exploit known\nvulns with patches available."),
    ("Verify before you click",
     "Hover over links. Check sender\naddresses. When in doubt, don't."),
    ("Lock down your router",
     "Change default creds, use WPA3,\ndisable WPS and UPnP."),
    ("Back up with 3-2-1 rule",
     "3 copies, 2 media types,\n1 offsite or cloud backup."),
    ("Review app permissions",
     "Audit what apps can access.\nRevoke what they don't need."),
    ("Use HTTPS everywhere",
     "Browser extensions help. Never\nenter passwords on HTTP sites."),
    ("Separate work & personal",
     "Different browsers or profiles.\nDon't reuse passwords across."),
    ("Check haveibeenpwned.com",
     "Free breach monitoring. Change\nany compromised passwords ASAP."),
]

col_left_x = 100
col_right_x = 1040
card_w = 860
card_h = 175
row_gap = 20
start_y = 560

for i, (title, desc) in enumerate(tips):
    col = i % 2
    row = i // 2
    x = col_left_x if col == 0 else col_right_x
    y = start_y + row * (card_h + row_gap)

    # Card background
    draw.rounded_rectangle(
        [x, y, x + card_w, y + card_h],
        radius=16,
        fill=CARD_BG,
        outline=CARD_BORDER,
        width=2,
    )

    # Number circle
    num_cx = x + 45
    num_cy = y + card_h // 2
    num_r = 28
    draw.ellipse(
        [num_cx - num_r, num_cy - num_r, num_cx + num_r, num_cy + num_r],
        fill=ACCENT,
    )
    num_text = str(i + 1)
    nb = draw.textbbox((0, 0), num_text, font=font_tip_num)
    nw = nb[2] - nb[0]
    nh = nb[3] - nb[1]
    draw.text(
        (num_cx - nw // 2, num_cy - nh // 2 - nb[1]),
        num_text,
        fill=WHITE,
        font=font_tip_num,
    )

    # Tip title
    text_x = x + 90
    draw.text((text_x, y + 22), title, fill=WHITE, font=font_tip_title)

    # Tip description (multi-line)
    draw.text((text_x, y + 75), desc, fill=MUTED, font=font_tip_desc)

# ============================================================
# FOOTER
# ============================================================

footer_y = start_y + 5 * (card_h + row_gap) + 40

# Divider
draw.line(
    [(WIDTH // 2 - div_w // 2, footer_y), (WIDTH // 2 + div_w // 2, footer_y)],
    fill=ACCENT, width=3
)

draw_centered(
    "Save this. Share it. Stay safe out there.",
    footer_y + 30,
    font_footer,
    fill=MUTED,
)

# Save
img.save(OUT, "PNG", optimize=True)
print(f"Hero image saved to: {OUT}")
print(f"Size: {os.path.getsize(OUT) / 1024:.0f} KB")
