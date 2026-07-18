#!/usr/bin/env python3
"""
NovaOS — Pillow-based PNG asset generator
=========================================
Generates ALL PNG branding assets directly with Pillow's drawing primitives.
No SVG parsing, no external converters.

Run:
    python generate_assets.py

Outputs:
    de-config/wallpaper/novaos-wallpaper.png           1920x1080
    de-config/wallpaper/novaos-wallpaper-1366.png      1366x768
    de-config/wallpaper/novaos-wallpaper-1280.png      1280x720
    de-config/icons/novaos-logo.png                    256x256
    de-config/icons/novaos-logo-64.png                 64x64
    plymouth-theme/novaos/logo.png                     256x256
    plymouth-theme/novaos/progress_box.png             600x10
    plymouth-theme/novaos/progress_box_thumb.png       600x10
    plymouth-theme/novaos/lock.png                     32x32
    plymouth-theme/novaos/unlock.png                   32x32
    plymouth-theme/novaos/spinner.png                  32x32
    calamares-branding/novaos/logo.png                 128x128
    calamares-branding/novaos/sidebar.png              260x800
    calamares-branding/novaos/background.png           1920x1080  (copy of wallpaper)
    calamares-branding/novaos/images/welcome.png       480x320
    calamares-branding/novaos/images/partitioning.png  480x320
    calamares-branding/novaos/images/install.png       480x320
    calamares-branding/novaos/images/finished.png      480x320
    lightdm-theme/login-background.png                 1920x1080  (cropped wallpaper)
    contact-sheet.png                                  1200x1500
"""
from __future__ import annotations

import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ------------------------------------------------------------------------
# Design tokens — mirror docs/design-tokens.txt exactly
# ------------------------------------------------------------------------
BG_DEEP     = (0x0E, 0x16, 0x20)
BG_SURFACE  = (0x16, 0x1E, 0x2A)
BG_ELEVATED = (0x1E, 0x2A, 0x3A)
BORDER      = (0x2A, 0x3A, 0x50)
ACCENT      = (0x1F, 0xB8, 0xC1)
ACCENT_HOV  = (0x2B, 0xD4, 0xDE)
ACCENT_SOFT = (0x14, 0x30, 0x36)
FG          = (0xE6, 0xED, 0xF3)
FG_MUTED    = (0x8B, 0x9B, 0xB0)
FG_DIM      = (0x5C, 0x6B, 0x80)
SUCCESS     = (0x4A, 0xDE, 0x80)
WARNING     = (0xF4, 0xB7, 0x40)
ERROR       = (0xF8, 0x71, 0x71)

# ------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
WALLPAPER_DIR    = ROOT / "de-config" / "wallpaper"
ICONS_DIR        = ROOT / "de-config" / "icons"
PLYMOUTH_DIR     = ROOT / "plymouth-theme" / "novaos"
CALAMARES_DIR    = ROOT / "calamares-branding" / "novaos"
CALAMARES_IMAGES = CALAMARES_DIR / "images"
LIGHTDM_DIR      = ROOT / "lightdm-theme"
CONTACT_SHEET    = ROOT / "contact-sheet.png"

# ------------------------------------------------------------------------
# Font loader — picks the first available system font
# ------------------------------------------------------------------------
def _load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Find a usable TTF/OTF font on the system. Falls back to default."""
    candidates = []
    if bold:
        candidates += [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
    else:
        candidates += [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]
    # Linux fallbacks (for teammates who run this on Linux)
    candidates += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

# ------------------------------------------------------------------------
# Drawing helpers
# ------------------------------------------------------------------------
def vertical_gradient(width: int, height: int,
                      top: tuple[int,int,int],
                      bottom: tuple[int,int,int]) -> Image.Image:
    """Create a vertical gradient image."""
    img = Image.new("RGB", (width, height), top)
    px = img.load()
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(width):
            px[x, y] = (r, g, b)
    return img

def radial_gradient(width: int, height: int,
                     center: tuple[float,float],
                     inner: tuple[int,int,int],
                     outer: tuple[int,int,int],
                     inner_r: float = 0.0,
                     outer_r: float = 1.5) -> Image.Image:
    """Create a radial gradient. center is (0..1, 0..1) normalized."""
    img = Image.new("RGB", (width, height), outer)
    px = img.load()
    cx, cy = center[0] * width, center[1] * height
    max_dist = math.hypot(max(cx, width - cx), max(cy, height - cy))
    inner_radius = inner_r * max_dist
    outer_radius = outer_r * max_dist
    for y in range(height):
        for x in range(width):
            d = math.hypot(x - cx, y - cy)
            if d <= inner_radius:
                color = inner
            elif d >= outer_radius:
                color = outer
            else:
                t = (d - inner_radius) / (outer_radius - inner_radius)
                r = int(inner[0] + (outer[0] - inner[0]) * t)
                g = int(inner[1] + (outer[1] - inner[1]) * t)
                b = int(inner[2] + (outer[2] - inner[2]) * t)
                color = (r, g, b)
            px[x, y] = color
    return img

def rounded_rectangle(draw: ImageDraw.ImageDraw, xy: tuple, radius: int,
                      fill=None, outline=None, width: int = 1) -> None:
    """Pillow's rounded_rectangle exists in newer versions, but polyfill for older."""
    if hasattr(draw, "rounded_rectangle"):
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
    else:
        # Fallback: draw the rectangle in pieces
        x0, y0, x1, y1 = xy
        draw.rectangle((x0 + radius, y0, x1 - radius, y1), fill=fill)
        draw.rectangle((x0, y0 + radius, x1, y1 - radius), fill=fill)
        draw.ellipse((x0, y0, x0 + 2*radius, y0 + 2*radius), fill=fill)
        draw.ellipse((x1 - 2*radius, y0, x1, y0 + 2*radius), fill=fill)
        draw.ellipse((x0, y1 - 2*radius, x0 + 2*radius, y1), fill=fill)
        draw.ellipse((x1 - 2*radius, y1 - 2*radius, x1, y1), fill=fill)
        if outline:
            # Approximate outline with line segments
            draw.arc((x0, y0, x0 + 2*radius, y0 + 2*radius), 180, 270, fill=outline, width=width)
            draw.arc((x1 - 2*radius, y0, x1, y0 + 2*radius), 270, 360, fill=outline, width=width)
            draw.arc((x0, y1 - 2*radius, x0 + 2*radius, y1), 90, 180, fill=outline, width=width)
            draw.arc((x1 - 2*radius, y1 - 2*radius, x1, y1), 0, 90, fill=outline, width=width)
            draw.line((x0 + radius, y0, x1 - radius, y0), fill=outline, width=width)
            draw.line((x0 + radius, y1, x1 - radius, y1), fill=outline, width=width)
            draw.line((x0, y0 + radius, x0, y1 - radius), fill=outline, width=width)
            draw.line((x1, y0 + radius, x1, y1 - radius), fill=outline, width=width)

# ------------------------------------------------------------------------
# 1. Wallpaper — radial gradient + teal starburst rays
# ------------------------------------------------------------------------
def make_wallpaper(width: int, height: int, path: Path) -> None:
    """Dark radial background with 6 teal rays emanating from the top-left."""
    # Layer 1: radial gradient
    img = radial_gradient(width, height, (0.0, 0.0),
                          inner=BG_ELEVATED, outer=BG_DEEP,
                          inner_r=0.0, outer_r=1.2)
    draw = ImageDraw.Draw(img, "RGBA")

    # Layer 2: 6 rays at -90, -60, -30, 0, 30, 60 degrees from top-left.
    # Each ray is a wedge with strong alpha near the corner that fades
    # along its length (so the burst looks like it's EMANATING outward).
    cx, cy = 0, 0
    # Render each ray as a series of overlapping polygons with
    # decreasing alpha — cheaper than a true gradient and looks the same.
    rays = [
        # (angle_degrees, half_width_degrees, max_alpha, length_factor)
        (5,   5, 200, 1.8),    # main rightward ray
        (25,  4, 150, 1.6),
        (45,  6, 110, 1.5),
        (62,  8, 75,  1.3),
        (78,  10, 50, 1.1),
    ]
    for angle, half_w, max_alpha, length_f in rays:
        length = int(math.hypot(width, height) * length_f)
        a_rad = math.radians(angle)
        ex = cx + math.cos(a_rad) * length
        ey = cy + math.sin(a_rad) * length
        perp = a_rad + math.pi / 2
        dx = math.cos(perp)
        dy = math.sin(perp)
        edge_thickness = length * math.tan(math.radians(half_w))

        # Build the ray as 8 stacked polygons from corner outward,
        # each progressively more transparent to simulate a gradient.
        steps = 8
        for s in range(steps, 0, -1):
            t0 = (s - 1) / steps
            t1 = s / steps
            # start of this sub-segment
            sx = cx + math.cos(a_rad) * length * t0
            sy = cy + math.sin(a_rad) * length * t0
            # end of this sub-segment
            ex_s = cx + math.cos(a_rad) * length * t1
            ey_s = cy + math.sin(a_rad) * length * t1
            # half-thickness tapers as we go outward
            taper = 1.0 - (s / steps) * 0.3
            et = edge_thickness * taper
            p1 = (sx - dx * et, sy - dy * et)
            p2 = (sx + dx * et, sy + dy * et)
            p3 = (ex_s + dx * et, ey_s + dy * et)
            p4 = (ex_s - dx * et, ey_s - dy * et)
            # Alpha fades with distance from origin
            alpha = int(max_alpha * (1.0 - (s / steps) * 0.85))
            draw.polygon([p1, p2, p3, p4], fill=ACCENT + (alpha,))

    # Layer 3: Nova core glow at top-left (two soft circles)
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((-200, -200, 400, 400), fill=ACCENT + (40,))
    glow_draw.ellipse((-100, -100, 240, 240), fill=ACCENT + (60,))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=80))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

    # Layer 4: very subtle vignette
    vignette = Image.new("L", (width, height), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-width*0.2, -height*0.2, width*1.2, height*1.2), fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=200))
    dark = Image.new("RGB", (width, height), (0, 0, 0))
    img = Image.composite(img, dark, vignette)

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    print(f"  wrote {path.name}  {width}x{height}")

# ------------------------------------------------------------------------
# 2. Logo — stylized N with corner star core
# ------------------------------------------------------------------------
def make_logo(size: int, path: Path) -> None:
    """N made of 4 elements + a glowing core star at bottom-right."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Scale based on size
    s = size / 256.0

    # Vertical left bar
    bx = 48 * s
    by = 48 * s
    bw = 22 * s
    bh = 160 * s
    bar_color = ACCENT_HOV
    # Subtle gradient on the bar
    bar = Image.new("RGBA", (int(bw), int(bh)), (0,0,0,0))
    bd = ImageDraw.Draw(bar)
    for y in range(int(bh)):
        t = y / max(1, bh - 1)
        r = int(ACCENT_HOV[0] + (ACCENT[0] - ACCENT_HOV[0]) * t)
        g = int(ACCENT_HOV[1] + (ACCENT[1] - ACCENT_HOV[1]) * t)
        b = int(ACCENT_HOV[2] + (ACCENT[2] - ACCENT_HOV[2]) * t)
        bd.line((0, y, bw, y), fill=(r, g, b, 255))
    # Round the corners by masking
    mask = Image.new("L", (int(bw), int(bh)), 0)
    md = ImageDraw.Draw(mask)
    radius = int(4 * s)
    rounded_rectangle(md, (0, 0, int(bw)-1, int(bh)-1), radius, fill=255)
    bar.putalpha(mask)
    img.paste(bar, (int(bx), int(by)), bar)

    # Vertical right bar
    rx = 186 * s
    bar2 = Image.new("RGBA", (int(bw), int(bh)), (0,0,0,0))
    bd2 = ImageDraw.Draw(bar2)
    for y in range(int(bh)):
        t = y / max(1, bh - 1)
        r = int(ACCENT_HOV[0] + (ACCENT[0] - ACCENT_HOV[0]) * t)
        g = int(ACCENT_HOV[1] + (ACCENT[1] - ACCENT_HOV[1]) * t)
        b = int(ACCENT_HOV[2] + (ACCENT[2] - ACCENT_HOV[2]) * t)
        bd2.line((0, y, bw, y), fill=(r, g, b, 255))
    mask2 = Image.new("L", (int(bw), int(bh)), 0)
    md2 = ImageDraw.Draw(mask2)
    rounded_rectangle(md2, (0, 0, int(bw)-1, int(bh)-1), radius, fill=255)
    bar2.putalpha(mask2)
    img.paste(bar2, (int(rx), int(by)), bar2)

    # Diagonal connector — single solid polygon, filled cleanly.
    # The diagonal goes from the inner-top of the left bar to the
    # inner-bottom of the right bar (the "N" stroke).
    # Vertices: top-left, bottom-left, bottom-right, top-right.
    diag_pts = [
        (int(70 * s),  int(80 * s)),    # top-left of diag (inner edge of left bar)
        (int(70 * s),  int(128 * s)),   # bottom-left of diag
        (int(186 * s), int(176 * s)),   # bottom-right (inner edge of right bar)
        (int(186 * s), int(128 * s)),   # top-right (inner edge of right bar)
    ]
    draw.polygon(diag_pts, fill=ACCENT_HOV)

    # Glow around the bars — soft blur of the whole shape
    glow_layer = img.copy()
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=int(8 * s)))
    img = Image.alpha_composite(glow_layer, img)

    draw = ImageDraw.Draw(img)

    # Core star (the "nova") — at bottom-right corner
    sx, sy = 196 * s, 196 * s
    sr_outer = 20 * s
    sr_inner = 10 * s
    # Soft halo
    halo = Image.new("RGBA", (size, size), (0,0,0,0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse((sx - sr_outer*2.5, sy - sr_outer*2.5,
                sx + sr_outer*2.5, sy + sr_outer*2.5),
               fill=ACCENT + (60,))
    halo = halo.filter(ImageFilter.GaussianBlur(radius=int(6 * s)))
    img = Image.alpha_composite(img, halo)
    draw = ImageDraw.Draw(img)
    # Bright core
    draw.ellipse((sx - sr_outer, sy - sr_outer,
                  sx + sr_outer, sy + sr_outer),
                 fill=ACCENT)
    # White hot center
    draw.ellipse((sx - sr_inner, sy - sr_inner,
                  sx + sr_inner, sy + sr_inner),
                 fill=(255, 255, 255))

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    print(f"  wrote {path.name}  {size}x{size}")

# ------------------------------------------------------------------------
# 3. Plymouth assets
# ------------------------------------------------------------------------
def make_plymouth_assets() -> None:
    PLYMOUTH_DIR.mkdir(parents=True, exist_ok=True)

    # progress_box.png — 600x10, dark teal rounded bar (the "track")
    w, h = 600, 10
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Outer rounded rect (slightly lighter teal)
    rounded_rectangle(d, (0, 0, w-1, h-1), 4, fill=ACCENT_SOFT, outline=ACCENT)
    # Inner darker rect (the "track")
    d.rectangle((2, 2, w-3, h-3), fill=BG_DEEP)
    img.save(PLYMOUTH_DIR / "progress_box.png", "PNG")
    print(f"  wrote progress_box.png  {w}x{h}")

    # progress_box_thumb.png — 600x10, solid teal filled (the "fill")
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rounded_rectangle(d, (0, 0, w-1, h-1), 4, fill=ACCENT)
    img.save(PLYMOUTH_DIR / "progress_box_thumb.png", "PNG")
    print(f"  wrote progress_box_thumb.png  {w}x{h}")

    # lock.png — 32x32, white padlock
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Padlock body
    rounded_rectangle(d, (8, 14, 23, 27), 2, fill=(255, 255, 255, 255))
    # Shackle (the U on top) — drawn as an arc
    d.arc((11, 5, 20, 17), 180, 360, fill=(255, 255, 255, 255), width=2)
    # Keyhole
    d.ellipse((14, 18, 17, 21), fill=BG_DEEP)
    d.rectangle((15, 20, 16, 23), fill=BG_DEEP)
    img.save(PLYMOUTH_DIR / "lock.png", "PNG")
    print(f"  wrote lock.png  32x32")

    # unlock.png — 32x32, same as lock but shackle open
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rounded_rectangle(d, (8, 14, 23, 27), 2, fill=(255, 255, 255, 255))
    d.arc((11, 5, 20, 17), 180, 360, fill=(255, 255, 255, 255), width=2)
    # Rotate the open half by redrawing
    d.arc((11, 5, 20, 17), 270, 360, fill=(255, 255, 255, 255), width=2)
    # Cover the closed half to make it look open
    d.line((15, 5, 15, 14), fill=(0, 0, 0, 0), width=2)
    d.ellipse((14, 18, 17, 21), fill=BG_DEEP)
    d.rectangle((15, 20, 16, 23), fill=BG_DEEP)
    img.save(PLYMOUTH_DIR / "unlock.png", "PNG")
    print(f"  wrote unlock.png  32x32")

    # spinner.png — 32x32, partial teal arc (90° wedge)
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Draw a circle outline (background)
    d.ellipse((3, 3, 28, 28), outline=BG_ELEVATED, width=3)
    # Draw a 90° arc in accent (starting at top, going clockwise)
    d.arc((3, 3, 28, 28), start=270, end=0, fill=ACCENT, width=3)
    img.save(PLYMOUTH_DIR / "spinner.png", "PNG")
    print(f"  wrote spinner.png  32x32")

# ------------------------------------------------------------------------
# 4. Calamares branding
# ------------------------------------------------------------------------
def make_calamares_logo() -> None:
    """128x128 logo for the Calamares branding directory."""
    CALAMARES_DIR.mkdir(parents=True, exist_ok=True)
    # Generate at 256, downscale to 128 for sharpness
    tmp = ROOT / "contact-sheet.png"  # safe tmp location
    make_logo(256, tmp)
    img = Image.open(tmp).convert("RGBA")
    img = img.resize((128, 128), Image.LANCZOS)
    img.save(CALAMARES_DIR / "logo.png", "PNG", optimize=True)
    print(f"  wrote calamares/logo.png  128x128")
    tmp.unlink(missing_ok=True)

def make_calamares_sidebar() -> None:
    """260x800 — the tall sidebar shown on the left during install."""
    w, h = 260, 800
    # Vertical gradient from BG_SURFACE to BG_DEEP
    img = vertical_gradient(w, h, BG_SURFACE, BG_DEEP).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    # Subtle accent line on the right edge (2px, low alpha)
    draw.rectangle((w-2, 0, w-1, h-1), fill=ACCENT + (90,))

    # Subtle starburst rays from top-left, very faint
    for angle, half_w, alpha in [(20, 6, 18), (40, 8, 12), (60, 10, 8)]:
        a_rad = math.radians(angle)
        length = int(math.hypot(w, h) * 1.2)
        ex = math.cos(a_rad) * length
        ey = math.sin(a_rad) * length
        perp = a_rad + math.pi / 2
        dx = math.cos(perp)
        dy = math.sin(perp)
        thick = length * math.tan(math.radians(half_w))
        p1 = (ex - dx * thick, ey - dy * thick)
        p2 = (ex + dx * thick, ey + dy * thick)
        draw.polygon([(0, 0), p1, p2], fill=ACCENT + (alpha,))

    # Logo at top
    logo = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    # Render directly at small size
    _render_logo_small(logo, 96)
    img.paste(logo, ((w - 96)//2, 60), logo)

    # "NovaOS" title
    font_title = _load_font(28, bold=True)
    font_sub = _load_font(11)
    text = "NovaOS"
    bbox = draw.textbbox((0, 0), text, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw)//2, 170), text, font=font_title, fill=ACCENT)

    # Subtitle
    sub = "Custom Linux for CS/IT"
    bbox = draw.textbbox((0, 0), sub, font=font_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw)//2, 210), sub, font=font_sub, fill=FG_MUTED)

    # Step list placeholder (we don't know which step is active,
    # so just show generic step rows that the QSS will theme)
    font_step = _load_font(10)
    steps = ["Welcome", "Language", "Keyboard", "Partition",
             "User", "Summary", "Install"]
    y = 290
    for i, step in enumerate(steps):
        # Circle for step number
        cx = 30
        cy = y + 8
        draw.ellipse((cx-7, cy-7, cx+7, cy+7), outline=FG_DIM, width=1)
        # Step number
        num = str(i + 1)
        nb = draw.textbbox((0, 0), num, font=font_step)
        nw = nb[2] - nb[0]
        nh = nb[3] - nb[1]
        draw.text((cx - nw//2, cy - nh//2 - 1), num,
                  font=font_step, fill=FG_DIM)
        # Step name
        draw.text((50, y), step, font=font_step, fill=FG_MUTED)
        y += 36

    # Bottom: version
    font_ver = _load_font(8)
    ver = "v1.0 (2026-07)"
    bbox = draw.textbbox((0, 0), ver, font=font_ver)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw)//2, h - 20), ver, font=font_ver, fill=FG_DIM)

    img.save(CALAMARES_DIR / "sidebar.png", "PNG", optimize=True)
    print(f"  wrote calamares/sidebar.png  {w}x{h}")

def _render_logo_small(target: Image.Image, size: int) -> None:
    """Render a simplified version of the logo at small size for sidebar use."""
    s = size / 256.0
    draw = ImageDraw.Draw(target)
    bx = int(48 * s)
    by = int(48 * s)
    bw = int(22 * s)
    bh = int(160 * s)
    radius = max(2, int(4 * s))

    # Left bar
    rounded_rectangle(draw, (bx, by, bx + bw - 1, by + bh - 1), radius, fill=ACCENT_HOV)
    # Right bar
    rx = int(186 * s)
    rounded_rectangle(draw, (rx, by, rx + bw - 1, by + bh - 1), radius, fill=ACCENT_HOV)
    # Diagonal
    draw.polygon([
        (int(70 * s), int(80 * s)),
        (int(70 * s), int(128 * s)),
        (int(186 * s), int(176 * s)),
        (int(186 * s), int(128 * s)),
    ], fill=ACCENT_HOV)
    # Core
    sx, sy = int(196 * s), int(196 * s)
    sr = int(20 * s)
    draw.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=ACCENT)
    draw.ellipse((sx - sr//2, sy - sr//2, sx + sr//2, sy + sr//2), fill=(255, 255, 255))

def make_calamares_step_illustrations() -> None:
    """480x320 illustrations for the 4 main install steps.
    Each is a card with the dark background, an icon, and a label."""
    CALAMARES_IMAGES.mkdir(parents=True, exist_ok=True)

    steps = [
        ("welcome.png",      "Welcome",     "👋", ACCENT),
        ("partitioning.png", "Partition",   "🗂", ACCENT),
        ("install.png",      "Install",     "⚙", ACCENT),
        ("finished.png",     "Complete",    "✓", SUCCESS),
    ]

    font_label = _load_font(28, bold=True)
    font_sub = _load_font(12)

    for filename, label, glyph, color in steps:
        w, h = 480, 320
        # Background — dark gradient
        img = vertical_gradient(w, h, BG_ELEVATED, BG_DEEP).convert("RGBA")
        draw = ImageDraw.Draw(img, "RGBA")

        # Rounded card border
        rounded_rectangle(draw, (8, 8, w-9, h-9), 12,
                          outline=BORDER, width=2)

        # Subtle radial accent in top-left
        for angle, half_w, alpha in [(0, 5, 30), (30, 6, 20)]:
            a_rad = math.radians(angle)
            length = int(math.hypot(w, h) * 0.8)
            ex = math.cos(a_rad) * length
            ey = math.sin(a_rad) * length
            perp = a_rad + math.pi / 2
            dx = math.cos(perp)
            dy = math.sin(perp)
            thick = length * math.tan(math.radians(half_w))
            p1 = (ex - dx * thick, ey - dy * thick)
            p2 = (ex + dx * thick, ey + dy * thick)
            draw.polygon([(0, 0), p1, p2], fill=ACCENT + (alpha,))

        # Central icon — a large rounded square with the glyph
        icon_size = 120
        ix = (w - icon_size) // 2
        iy = 70
        rounded_rectangle(draw, (ix, iy, ix + icon_size, iy + icon_size),
                          16, fill=BG_SURFACE, outline=color, width=2)

        # Glyph — use the actual character (best effort)
        # Most Pillow builds don't have color emoji fonts on Windows,
        # so we fall back to drawing a stylized shape
        cx = ix + icon_size // 2
        cy = iy + icon_size // 2
        if glyph == "✓":
            # Checkmark
            draw.line([(cx - 30, cy), (cx - 8, cy + 22), (cx + 30, cy - 22)],
                      fill=color, width=8)
        elif label == "Welcome":
            # Open hand-ish: a circle with 5 short lines (rays)
            draw.ellipse((cx - 25, cy - 25, cx + 25, cy + 25),
                         outline=color, width=4)
            for ang in range(0, 360, 45):
                a = math.radians(ang)
                x1 = cx + math.cos(a) * 30
                y1 = cy + math.sin(a) * 30
                x2 = cx + math.cos(a) * 40
                y2 = cy + math.sin(a) * 40
                draw.line((x1, y1, x2, y2), fill=color, width=3)
        elif label == "Partition":
            # Disk icon: cylinder (top oval + sides)
            draw.ellipse((cx - 35, cy - 30, cx + 35, cy - 5),
                         outline=color, width=3)
            draw.line((cx - 35, cy - 5, cx - 35, cy + 25), fill=color, width=3)
            draw.line((cx + 35, cy - 5, cx + 35, cy + 25), fill=color, width=3)
            draw.ellipse((cx - 35, cy + 25, cx + 35, cy + 50),
                         outline=color, width=3)
        elif label == "Install":
            # Gear: rough approximation
            for ang in range(0, 360, 30):
                a = math.radians(ang)
                x1 = cx + math.cos(a) * 28
                y1 = cy + math.sin(a) * 28
                x2 = cx + math.cos(a) * 40
                y2 = cy + math.sin(a) * 40
                draw.line((x1, y1, x2, y2), fill=color, width=5)
            draw.ellipse((cx - 28, cy - 28, cx + 28, cy + 28),
                         outline=color, width=3)
            draw.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=color)

        # Label below the icon
        text = label
        bbox = draw.textbbox((0, 0), text, font=font_label)
        tw = bbox[2] - bbox[0]
        draw.text(((w - tw)//2, iy + icon_size + 24), text,
                  font=font_label, fill=FG)

        # Subtitle
        subs = {
            "Welcome":   "Get started with NovaOS",
            "Partition": "Choose where to install",
            "Install":   "Copying files...",
            "Complete":  "Installation finished",
        }
        sub = subs.get(label, "")
        bbox = draw.textbbox((0, 0), sub, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((w - tw)//2, iy + icon_size + 70), sub,
                  font=font_sub, fill=FG_MUTED)

        img.save(CALAMARES_IMAGES / filename, "PNG", optimize=True)
        print(f"  wrote calamares/images/{filename}  {w}x{h}")

# ------------------------------------------------------------------------
# 5. LightDM login background — wallpaper, lightly darken + crop
# ------------------------------------------------------------------------
def make_lightdm_background() -> None:
    """Reuse the wallpaper PNG; apply a darker overlay for login readability."""
    LIGHTDM_DIR.mkdir(parents=True, exist_ok=True)
    src = WALLPAPER_DIR / "novaos-wallpaper.png"
    if not src.exists():
        print(f"  WARN: {src} not found, skipping login background")
        return
    img = Image.open(src).convert("RGBA")
    # Darken by 25% — multiply with a semi-transparent black
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 80))
    img = Image.alpha_composite(img, overlay).convert("RGB")
    img.save(LIGHTDM_DIR / "login-background.png", "PNG", optimize=True)
    print(f"  wrote login-background.png  {img.size[0]}x{img.size[1]}")

# ------------------------------------------------------------------------
# 6. Contact sheet
# ------------------------------------------------------------------------
def make_contact_sheet() -> None:
    """Single image showing all generated assets at thumbnail size.

    Layout: sections stacked vertically. Each item is rendered as a
    card (thumbnail + filename label). Cards flow left-to-right and
    wrap to the next row when they would exceed the sheet width.
    """
    # Compute sheet height dynamically based on content
    sections = [
        ("Wallpapers", [
            ("de-config/wallpaper/novaos-wallpaper.png",          360, 202),
            ("de-config/wallpaper/novaos-wallpaper-1366.png",     260, 146),
            ("de-config/wallpaper/novaos-wallpaper-1280.png",     240, 135),
        ]),
        ("Logo", [
            ("de-config/icons/novaos-logo.png",    128, 128),
            ("de-config/icons/novaos-logo-64.png", 64,  64),
            ("plymouth-theme/novaos/logo.png",     128, 128),
            ("calamares-branding/novaos/logo.png", 128, 128),
        ]),
        ("Calamares", [
            ("calamares-branding/novaos/sidebar.png",     130, 400),
            ("calamares-branding/novaos/background.png",  260, 146),
        ]),
        ("Calamares Step Illustrations", [
            ("calamares-branding/novaos/images/welcome.png",      200, 133),
            ("calamares-branding/novaos/images/partitioning.png", 200, 133),
            ("calamares-branding/novaos/images/install.png",      200, 133),
            ("calamares-branding/novaos/images/finished.png",     200, 133),
        ]),
        ("Plymouth", [
            ("plymouth-theme/novaos/progress_box.png",       300, 12),
            ("plymouth-theme/novaos/progress_box_thumb.png", 300, 12),
            ("plymouth-theme/novaos/lock.png",   32, 32),
            ("plymouth-theme/novaos/unlock.png", 32, 32),
            ("plymouth-theme/novaos/spinner.png", 32, 32),
        ]),
        ("LightDM", [
            ("lightdm-theme/login-background.png", 360, 202),
        ]),
    ]

    SHEET_W = 1200
    MARGIN = 30
    GAP = 12
    LABEL_H = 18
    PAD = 8
    SECTION_HEADER_H = 28
    SECTION_GAP = 18

    font_title = _load_font(28, bold=True)
    font_section = _load_font(14, bold=True)
    font_label = _load_font(9)

    # Pre-measure to find total height
    total_h = 90  # top padding for title
    section_heights = []
    for _, items in sections:
        # Compute layout: how many rows? How tall?
        available_w = SHEET_W - 2 * MARGIN
        row_w = 0
        rows = 1
        max_h_in_row = 0
        max_section_h = 0
        for rel_path, tw, th in items:
            if not (ROOT / rel_path).exists():
                continue
            card_w = tw + 2 * PAD
            card_h = th + 2 * PAD + LABEL_H
            if row_w + card_w > available_w and row_w > 0:
                rows += 1
                max_section_h += max_h_in_row + GAP
                row_w = 0
                max_h_in_row = 0
            row_w += card_w + GAP
            max_h_in_row = max(max_h_in_row, card_h)
        max_section_h += max_h_in_row
        section_heights.append((rows, max_section_h))
        total_h += SECTION_HEADER_H + max_section_h + SECTION_GAP

    sheet = Image.new("RGB", (SHEET_W, total_h), BG_DEEP)
    draw = ImageDraw.Draw(sheet)

    # Title
    draw.text((30, 20), "NovaOS Asset Contact Sheet", font=font_title, fill=ACCENT)
    draw.text((30, 60), "Generated by scripts/generate_assets.py",
              font=font_label, fill=FG_MUTED)

    y = 90
    for (section_name, items), (_rows, _sh) in zip(sections, section_heights):
        # Section header
        draw.text((30, y), section_name, font=font_section, fill=FG)
        y += SECTION_HEADER_H

        x = MARGIN
        row_max_h = 0
        for rel_path, tw, th in items:
            full_path = ROOT / rel_path
            if not full_path.exists():
                continue
            try:
                thumb = Image.open(full_path).convert("RGBA")
                thumb.thumbnail((tw, th), Image.LANCZOS)

                card_w = tw + 2 * PAD
                card_h = th + 2 * PAD + LABEL_H
                card = Image.new("RGBA", (card_w, card_h), BG_SURFACE + (255,))
                cd = ImageDraw.Draw(card)
                rounded_rectangle(cd, (0, 0, card_w-1, card_h-1), 6,
                                  fill=BG_SURFACE, outline=BORDER, width=1)
                # Center thumbnail horizontally, place near top
                tx = (card_w - thumb.size[0]) // 2
                ty = PAD
                if thumb.mode == "RGBA":
                    card.paste(thumb, (tx, ty), thumb)
                else:
                    card.paste(thumb, (tx, ty))
                # Filename label
                label = Path(rel_path).name
                cd.text((PAD, th + 2 * PAD + 2), label,
                        font=font_label, fill=FG_MUTED)

                # Wrap if needed
                if x + card_w > SHEET_W - MARGIN:
                    y += row_max_h + GAP
                    x = MARGIN
                    row_max_h = 0

                sheet.paste(card, (x, y), card)
                x += card_w + GAP
                row_max_h = max(row_max_h, card_h)
            except Exception as e:
                print(f"  WARN: couldn't read {full_path}: {e}")

        # Advance past the last row of this section
        y += row_max_h + SECTION_GAP

    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET, "PNG", optimize=True)
    print(f"  wrote {CONTACT_SHEET.name}  {SHEET_W}x{total_h}")

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------
def main() -> None:
    print("\n[1/6] Wallpaper")
    make_wallpaper(1920, 1080, WALLPAPER_DIR / "novaos-wallpaper.png")
    make_wallpaper(1366, 768,  WALLPAPER_DIR / "novaos-wallpaper-1366.png")
    make_wallpaper(1280, 720,  WALLPAPER_DIR / "novaos-wallpaper-1280.png")

    print("\n[2/6] Logo")
    make_logo(256, ICONS_DIR / "novaos-logo.png")
    make_logo(64,  ICONS_DIR / "novaos-logo-64.png")
    # Also create the plymouth copy
    make_logo(256, PLYMOUTH_DIR / "logo.png")

    print("\n[3/6] Plymouth assets")
    make_plymouth_assets()

    print("\n[4/6] Calamares branding")
    make_calamares_logo()
    make_calamares_sidebar()
    # Calamares background.png = same as wallpaper
    bg = WALLPAPER_DIR / "novaos-wallpaper.png"
    if bg.exists():
        Image.open(bg).save(CALAMARES_DIR / "background.png", "PNG", optimize=True)
        print(f"  wrote calamares/background.png  (copy of wallpaper)")
    make_calamares_step_illustrations()

    print("\n[5/6] LightDM login background")
    make_lightdm_background()

    print("\n[6/6] Contact sheet")
    make_contact_sheet()
    print(f"\n[OK] Done. Open {CONTACT_SHEET.relative_to(ROOT)} to review.")

if __name__ == "__main__":
    main()
