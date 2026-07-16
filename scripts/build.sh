#!/bin/bash
# NovaOS build helper \u2014 owned by Person 1.
# Run this from the repo root on a Debian/Ubuntu build machine.
#
# Usage: ./scripts/build.sh

set -e

if ! command -v lb >/dev/null 2>&1; then
  echo "live-build not found. Install it first:"
  echo "  sudo apt update && sudo apt install -y live-build live-config live-boot"
  exit 1
fi

echo "== Cleaning previous build =="
sudo lb clean

echo "== Building ISO =="
sudo lb build 2>&1 | tee build.log

echo "== Build complete =="
ls -lh live-image-*.iso 2>/dev/null || echo "No ISO found \u2014 check build.log for errors."
du -h live-image-*.iso 2>/dev/null || true
