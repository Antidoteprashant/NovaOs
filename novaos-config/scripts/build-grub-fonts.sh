#!/bin/bash
# ----------------------------------------------------------------------
# build-grub-fonts.sh
# ----------------------------------------------------------------------
# Converts DejaVu TTF fonts into GRUB's .pf2 format and places them
# in grub-theme/novaos/fonts/.
#
# Run ONCE on a Debian/Ubuntu build machine before packaging the .deb.
# Requires: grub-common, fonts-dejavu-core, fonts-dejavu-extra
#
# Usage:
#   sudo apt install grub-common fonts-dejavu-core fonts-dejavu-extra
#   bash scripts/build-grub-fonts.sh
# ----------------------------------------------------------------------

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
FONTS_OUT="$ROOT/grub-theme/novaos/fonts"

DEJAVU_DIR="/usr/share/fonts/truetype/dejavu"

log() { echo "[build-grub-fonts] $*"; }
fail() { echo "[build-grub-fonts] ERROR: $*" >&2; exit 1; }

# Check dependencies
command -v grub-mkfont >/dev/null 2>&1 || \
    fail "grub-mkfont not found. Run: sudo apt install grub-common"

[ -f "$DEJAVU_DIR/DejaVuSans.ttf" ] || \
    fail "DejaVu fonts not found. Run: sudo apt install fonts-dejavu-core fonts-dejavu-extra"

mkdir -p "$FONTS_OUT"

log "Generating GRUB .pf2 fonts into $FONTS_OUT"

# Title font: DejaVu Sans Bold 28pt
grub-mkfont -s 28 -o "$FONTS_OUT/DejaVuSans-Bold-28.pf2" \
    "$DEJAVU_DIR/DejaVuSans-Bold.ttf"
log "  ✓ DejaVuSans-Bold-28.pf2"

# Menu item font: DejaVu Sans 16pt
grub-mkfont -s 16 -o "$FONTS_OUT/DejaVuSans-16.pf2" \
    "$DEJAVU_DIR/DejaVuSans.ttf"
log "  ✓ DejaVuSans-16.pf2"

# Tagline font: DejaVu Sans 12pt
grub-mkfont -s 12 -o "$FONTS_OUT/DejaVuSans-12.pf2" \
    "$DEJAVU_DIR/DejaVuSans.ttf"
log "  ✓ DejaVuSans-12.pf2"

# Bottom bar font: DejaVu Sans 11pt
grub-mkfont -s 11 -o "$FONTS_OUT/DejaVuSans-11.pf2" \
    "$DEJAVU_DIR/DejaVuSans.ttf"
log "  ✓ DejaVuSans-11.pf2"

# Progress bar font: DejaVu Sans 10pt
grub-mkfont -s 10 -o "$FONTS_OUT/DejaVuSans-10.pf2" \
    "$DEJAVU_DIR/DejaVuSans.ttf"
log "  ✓ DejaVuSans-10.pf2"

# --- Generate GRUB boot menu icons ---
ICONS_OUT="$ROOT/grub-theme/novaos/icons"
mkdir -p "$ICONS_OUT"

if command -v convert >/dev/null 2>&1; then
    log "Generating GRUB boot entry icons (32×32) ..."

    # Linux icon — teal penguin-ish shape
    convert -size 32x32 xc:none \
        -fill "#1FB8C1" \
        -draw "circle 16,13 16,5" \
        -draw "roundrectangle 8,18 24,28 4,4" \
        "$ICONS_OUT/linux.png" 2>/dev/null
    log "  ✓ linux.png"

    # Windows icon — blue 4-square grid
    convert -size 32x32 xc:none \
        -fill "#0078D4" \
        -draw "rectangle 4,4  14,14" \
        -draw "rectangle 17,4  28,14" \
        -draw "rectangle 4,17 14,28" \
        -draw "rectangle 17,17 28,28" \
        "$ICONS_OUT/windows.png" 2>/dev/null
    log "  ✓ windows.png"

    # UEFI icon — grey gear shape (simple)
    convert -size 32x32 xc:none \
        -fill "#8B9BB0" \
        -draw "circle 16,16 16,6" \
        -fill "#0E1620" \
        -draw "circle 16,16 16,10" \
        "$ICONS_OUT/uefi.png" 2>/dev/null
    log "  ✓ uefi.png"

    # Memtest icon — orange memory shape
    convert -size 32x32 xc:none \
        -fill "#E07040" \
        -draw "roundrectangle 4,10 28,22 3,3" \
        -fill "#0E1620" \
        -draw "rectangle 7,13 10,19" \
        -draw "rectangle 13,13 16,19" \
        -draw "rectangle 19,13 22,19" \
        "$ICONS_OUT/memtest.png" 2>/dev/null
    log "  ✓ memtest.png"
else
    log "WARN: ImageMagick not found. Icons skipped."
    log "      Install: sudo apt install imagemagick"
    log "      Then re-run this script, OR manually place 32×32 PNGs in $ICONS_OUT"
fi

log "Done. All GRUB theme assets ready in grub-theme/novaos/"
log "Next: run render-assets.sh to generate background.png, then build-deb.sh"
