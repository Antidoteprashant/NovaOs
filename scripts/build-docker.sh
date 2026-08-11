#!/bin/bash
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "========================================"
echo "  Preparing Docker environment for NovaOS"
echo "========================================"
docker build -t novaos-builder -f "$REPO_ROOT/Dockerfile" "$REPO_ROOT"

echo ""
echo "========================================"
echo "  Running lb build inside Docker..."
echo "  (Using a native Linux container to bypass macOS file system restrictions)"
echo "========================================"
docker run --rm -it --privileged -v "$REPO_ROOT:/workspace" novaos-builder bash -c '
  set -e
  echo ">> Copying repository to native Linux filesystem (/build)..."
  cp -a /workspace /build
  cd /build
  
  echo ">> Starting scripts/build.sh..."
  # Clean up any partial state from Mac before running
  rm -rf .build chroot cache || true
  bash scripts/build.sh
  
  echo ">> Build completed. Copying artifacts back to host..."
  cp *.iso /workspace/ 2>/dev/null || true
  cp build.log /workspace/ 2>/dev/null || true
  echo ">> Done!"
'
