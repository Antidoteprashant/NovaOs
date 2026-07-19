#!/bin/bash
# ============================================================
# scripts/build.sh — NovaOS local build helper
# Owned by: Person 1 (Base System & Build Engineer)
# ============================================================
# Run this from the repo root on a Debian/Ubuntu build machine.
# DO NOT run on macOS — live-build requires a Debian/Ubuntu host.
#
# Usage:
#   sudo bash scripts/build.sh
#
# One-time pre-requisites (run manually before first build):
#   sudo apt update
#   sudo apt install -y --reinstall \
#       live-build live-config live-boot \
#       isolinux syslinux-common syslinux-utils \
#       grub-common grub-efi-amd64-bin grub-pc-bin \
#       xorriso squashfs-tools

set -e
set -o pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# -----------------------------------------------------------------------
# Sanity checks
# -----------------------------------------------------------------------
if ! command -v lb > /dev/null 2>&1; then
  echo "ERROR: live-build not found. Install it first:"
  echo "  sudo apt update && sudo apt install -y live-build live-config live-boot"
  exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR: This script must be run as root (use: sudo bash scripts/build.sh)"
  exit 1
fi

echo "========================================"
echo "  NovaOS Build — $(date)"
echo "  Repo: $REPO_ROOT"
echo "========================================"

# -----------------------------------------------------------------------
# Step 1: Clean previous build artifacts
# -----------------------------------------------------------------------
echo ""
echo "== [1/5] Cleaning previous build =="
lb clean --purge
rm -f wget-log*

# -----------------------------------------------------------------------
# Step 2: Configure live-build
# -----------------------------------------------------------------------
echo ""
echo "== [2/5] Configuring live-build =="
lb config \
  --distribution bookworm \
  --architecture amd64 \
  --archive-areas "main contrib non-free-firmware" \
  --security false \
  --linux-flavours amd64

# -----------------------------------------------------------------------
# Step 3: Stage NovaOS branding assets into the chroot tree
# -----------------------------------------------------------------------
echo ""
echo "== [3/5] Staging NovaOS branding for chroot =="
mkdir -p config/includes.chroot/opt/
cp -r "$REPO_ROOT/novaos-config" config/includes.chroot/opt/novaos-config
echo "   ✓ Branding assets staged → config/includes.chroot/opt/novaos-config"

# -----------------------------------------------------------------------
# Step 4: Build the ISO
# -----------------------------------------------------------------------
echo ""
echo "== [4/5] Building ISO (this takes 15-40 minutes) =="
lb build 2>&1 | tee build.log

# -----------------------------------------------------------------------
# Step 5: Results
# -----------------------------------------------------------------------
echo ""
echo "== [5/5] Build complete =="
if ls live-image-*.iso 2>/dev/null | head -1 | grep -q .; then
  ls -lh live-image-*.iso
  du -h live-image-*.iso
  echo ""
  echo "ISO size check (flag if >2.5GB before AI is added):"
  du -sh live-image-*.iso
  echo ""
  echo "RAM-tier test commands:"
  echo "  qemu-system-x86_64 -m 1024 -cdrom live-image-amd64.hybrid.iso -boot d  # 1GB tier"
  echo "  qemu-system-x86_64 -m 2048 -cdrom live-image-amd64.hybrid.iso -boot d  # 2GB tier"
  echo "  qemu-system-x86_64 -m 4096 -cdrom live-image-amd64.hybrid.iso -boot d  # 4GB tier"
  echo ""
  echo "Inside the booted VM, check RAM:"
  echo "  free -h"
else
  echo "ERROR: No ISO found. Check build.log for errors."
  echo "  tail -50 build.log"
  exit 1
fi
