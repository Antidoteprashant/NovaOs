#!/bin/bash
# NovaOS build helper — owned by Person 1.
# Run this from the repo root on a Debian/Ubuntu build machine.
#
# Usage: ./scripts/build.sh
#
# Pre-requisites (one-time setup, run manually before first build):
#   sudo apt install grub-common fonts-dejavu-core fonts-dejavu-extra \
#                    librsvg2-bin imagemagick live-build live-config live-boot \
#                    calamares calamares-settings-debian lightdm lightdm-gtk-greeter
#   bash novaos-config/scripts/build-grub-fonts.sh
#   bash novaos-config/scripts/render-assets.sh

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v lb >/dev/null 2>&1; then
  echo "live-build not found. Install it first:"
  echo "  sudo apt update && sudo apt install -y live-build live-config live-boot"
  exit 1
fi

# -----------------------------------------------------------------------
# Step 1: Install NovaOS branding into the chroot tree
# -----------------------------------------------------------------------
echo "== Installing NovaOS branding into chroot =="
if [ -f "$REPO_ROOT/novaos-config/scripts/install-branding.sh" ]; then
  sudo bash "$REPO_ROOT/novaos-config/scripts/install-branding.sh"
  echo "   ✓ Branding installed"
else
  echo "   WARN: novaos-config/scripts/install-branding.sh not found — skipping branding step"
fi

# -----------------------------------------------------------------------
# Step 2: Configure and run live-build
# -----------------------------------------------------------------------
echo "== Cleaning previous build and caches =="
sudo lb clean --purge
sudo rm -rf auto/
sudo rm -f wget-log*

echo "== Configuring build =="
lb config \
  --distribution bookworm \
  --architecture amd64 \
  --debian-installer none \
  --archive-areas "main contrib non-free-firmware" \
  --security false

echo "== Building ISO =="
sudo lb build 2>&1 | tee build.log

echo "== Build complete =="
ls -lh live-image-*.iso 2>/dev/null || echo "No ISO found — check build.log for errors."
du -h live-image-*.iso 2>/dev/null || true
echo ""
echo "RAM test commands:"
echo "  qemu-system-x86_64 -m 1024 -cdrom live-image-amd64.hybrid.iso -boot d"
echo "  qemu-system-x86_64 -m 2048 -cdrom live-image-amd64.hybrid.iso -boot d"
echo "  qemu-system-x86_64 -m 4096 -cdrom live-image-amd64.hybrid.iso -boot d"
