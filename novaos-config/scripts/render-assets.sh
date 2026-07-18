#!/bin/bash
# ----------------------------------------------------------------------
# render-assets.sh
# ----------------------------------------------------------------------
# Convert SVG source files into the PNGs the Plymouth / GRUB /
# Calamares / LightDM stack needs. Run once on a Linux box with
# rsvg-convert (librsvg2-bin) or inkscape installed.
# ----------------------------------------------------------------------

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

WALLPAPER_DIR="$ROOT/de-config/wallpaper"
LOGO_DIR="$ROOT/de-config/icons"
PLYMOUTH_DIR="$ROOT/plymouth-theme/novaos"
CALAMARES_DIR="$ROOT/calamares-branding/novaos"
LIGHTDM_DIR="$ROOT/lightdm-theme"

# Pick a renderer
if command -v rsvg-convert >/dev/null 2>&1; then
    RENDER="rsvg-convert -w WIDTH -h HEIGHT -o OUTPUT INPUT"
    ENGINE=rsvg
elif command -v inkscape >/dev/null 2>&1; then
    RENDER='inkscape INPUT --export-type=png -o OUTPUT -w WIDTH -h HEIGHT'
    ENGINE=inkscape
else
    echo "ERROR: install librsvg2-bin or inkscape first:" >&2
    echo "  sudo apt install librsvg2-bin" >&2
    exit 1
fi

render() {
    local input="$1" width="$2" height="$3" output="$4"
    echo "  render $output ($width×$height)"
    if [ "$ENGINE" = "rsvg" ]; then
        rsvg-convert -w "$width" -h "$height" -o "$output" "$input"
    else
        inkscape "$input" --export-type=png -o "$output" -w "$width" -h "$height"
    fi
}

echo "[render] wallpaper (1920×1080, 1366×768, 1280×720)"
render "$WALLPAPER_DIR/novaos-wallpaper.svg" 1920 1080 "$WALLPAPER_DIR/novaos-wallpaper.png"
render "$WALLPAPER_DIR/novaos-wallpaper.svg" 1366 768  "$WALLPAPER_DIR/novaos-wallpaper-1366.png"
render "$WALLPAPER_DIR/novaos-wallpaper.svg" 1280 720  "$WALLPAPER_DIR/novaos-wallpaper-1280.png"

echo "[render] logo (256×256 for Plymouth)"
render "$LOGO_DIR/novaos-logo.svg" 256 256 "$LOGO_DIR/novaos-logo.png"

# Plymouth wants logo.png inside its theme dir
cp "$LOGO_DIR/novaos-logo.png" "$PLYMOUTH_DIR/logo.png"

echo "[render] GRUB background (1920×1080)"
render "$WALLPAPER_DIR/novaos-wallpaper.svg" 1920 1080 \
       "$ROOT/grub-theme/novaos/background.png"

echo "[render] Calamares sidebar (260×800)"
render "$WALLPAPER_DIR/novaos-wallpaper.svg" 260 800 \
       "$CALAMARES_DIR/sidebar.png"
# background.png is the same wallpaper (full bleed)
cp "$WALLPAPER_DIR/novaos-wallpaper.png" "$CALAMARES_DIR/background.png"

echo "[render] Calamares per-step images (480×320 each)"
# Simple solid background with logo — re-render for each step is overkill;
# the user can later replace these with proper illustrations.
render "$LOGO_DIR/novaos-logo.svg" 480 320 "$CALAMARES_DIR/images/welcome.png"
render "$LOGO_DIR/novaos-logo.svg" 480 320 "$CALAMARES_DIR/images/partitioning.png"
render "$LOGO_DIR/novaos-logo.svg" 480 320 "$CALAMARES_DIR/images/install.png"
render "$LOGO_DIR/novaos-logo.svg" 480 320 "$CALAMARES_DIR/images/finished.png"

echo "[render] LightDM login background (1920×1080)"
render "$WALLPAPER_DIR/novaos-wallpaper.svg" 1920 1080 \
       "$LIGHTDM_DIR/login-background.png"

# Plymouth progress bar — drawn with ImageMagick (most build hosts have it)
if command -v convert >/dev/null 2>&1; then
    echo "[render] Plymouth progress box"
    # 600×8px rounded teal bar background
    convert -size 600x8 xc:none \
        -fill "#1FB8C1" -draw "roundrectangle 0,0 600,8 4,4" \
        -fill "#0E1620"  -draw "roundrectangle 1,1 599,7 3,3" \
        "$PLYMOUTH_DIR/progress_box.png"

    # 600×8px filled bar (the progress thumb)
    convert -size 600x8 xc:none \
        -fill "#1FB8C1" -draw "roundrectangle 0,0 600,8 4,4" \
        "$PLYMOUTH_DIR/progress_box_thumb.png"

    # Plymouth lock/unlock arrows (16×16, white on transparent)
    convert -size 16x16 xc:none \
        -fill "#E6EDF3" -font "DejaVu-Sans" -pointsize 14 -gravity center \
        -annotate +0+0 "🔒" "$PLYMOUTH_DIR/lock.png" 2>/dev/null || \
    convert -size 16x16 xc:none \
        -fill "#E6EDF3" -draw "rectangle 4,7 12,15" \
        -draw "arc 4,4 12,12 0,180" \
        "$PLYMOUTH_DIR/lock.png"

    convert -size 16x16 xc:none \
        -fill "#E6EDF3" -draw "rectangle 4,7 12,15" \
        -draw "arc 4,4 12,12 0,180" \
        "$PLYMOUTH_DIR/unlock.png"

    # Spinner (32×32 with a partial ring)
    convert -size 32x32 xc:none \
        -fill none -stroke "#1FB8C1" -strokewidth 3 -draw "arc 4,4 28,28 0,90" \
        "$PLYMOUTH_DIR/spinner.png"
else
    echo "WARN: ImageMagick not found. Plymouth progress images skipped." >&2
    echo "      Install imagemagick or manually create the following in $PLYMOUTH_DIR:" >&2
    echo "        progress_box.png (600x8 rounded rectangle, dark teal background)" >&2
    echo "        progress_box_thumb.png (600x8 rounded rectangle, teal fill)" >&2
    echo "        lock.png / unlock.png (16x16, white)" >&2
    echo "        spinner.png (32x32, partial teal ring)" >&2
fi

echo "[render] Done."
