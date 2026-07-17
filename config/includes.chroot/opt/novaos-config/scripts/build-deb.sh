#!/bin/bash
# ----------------------------------------------------------------------
# build-deb.sh
# ----------------------------------------------------------------------
# Build a .deb package containing the entire NovaOS branding layer.
# Result: novaos-branding_VERSION_all.deb
#
# Your base-ISO teammate adds this to their live-build config:
#   config/packages.chroot/  (just drop the .deb here)
# Or hooks it in chroot_local-hooks:
#   dpkg -i /path/to/novaos-branding_*.deb
# ----------------------------------------------------------------------
# Requires: devscripts, build-essential, debhelper
# ----------------------------------------------------------------------

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

VERSION="1.0.0"
PACKAGE_NAME="novaos-branding"
BUILD_DIR="$SCRIPT_DIR/build"
PKG_DIR="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}"

# Clean
rm -rf "$BUILD_DIR"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/usr/share/novaos"
mkdir -p "$PKG_DIR/usr/share/icons/NovaOS-Icon"
mkdir -p "$PKG_DIR/usr/share/grub/themes/novaos"
mkdir -p "$PKG_DIR/usr/share/plymouth/themes/novaos"
mkdir -p "$PKG_DIR/usr/share/lightdm-gtk-greeter"
mkdir -p "$PKG_DIR/usr/share/desktop-directories"
mkdir -p "$PKG_DIR/usr/share/calamares/branding/novaos"
mkdir -p "$PKG_DIR/usr/share/calamares/branding/novaos/images"
mkdir -p "$PKG_DIR/etc/calamares/scripts"
mkdir -p "$PKG_DIR/etc/skel/.config/lxqt"
mkdir -p "$PKG_DIR/etc/skel/.config/gtk-3.0"
mkdir -p "$PKG_DIR/etc/skel/.config/menus"
mkdir -p "$PKG_DIR/etc/skel/.config/autostart"
mkdir -p "$PKG_DIR/etc/xdg/lxqt"
mkdir -p "$PKG_DIR/etc/lightdm"
mkdir -p "$PKG_DIR/usr/bin"

# --- Control file ---
cat > "$PKG_DIR/DEBIAN/control" <<EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: metapackages
Priority: optional
Architecture: all
Depends: lxqt, lxqt-panel, lxqt-config, lxqt-globalkeyshcuts,
         qterminal, pcmanfm-qt, lightdm, lightdm-gtk-greeter,
         plymouth, plymouth-themes, calamares, python3, python3-pyqt5,
         adwaita-qt, papirus-icon-theme, fonts-inter,
         fonts-dejavu-core, fonts-noto-core
Suggests: zeal, libreoffice-core, code, vim, neovim
Maintainer: NovaOS Team <team@novaos.local>
Description: NovaOS branding layer (Desktop Experience)
 Provides the LXQt session config, Plymouth boot theme, GRUB theme,
 LightDM greeter styling, Calamares installer branding, custom
 application menu, and the NovaOS Welcome app for first login.
 Designed to be layered on top of a stock Debian system without
 requiring other components of NovaOS.
EOF

# --- Conffiles (preserve user changes on upgrade) ---
cat > "$PKG_DIR/DEBIAN/conffiles" <<EOF
/etc/lightdm/lightdm-gtk-greeter.conf
EOF

# --- Postinst: run the branding installer at install time ---
cat > "$PKG_DIR/DEBIAN/postinst" <<'EOF'
#!/bin/bash
set -e
# Run the branding post-install against the live root (we ARE the live root)
# This is what the Calamares post-install script does for a fresh install.
echo "[novaos-branding] post-install: applying branding to live system"
/usr/share/novaos/scripts/novaos-branding-postinstall.sh / || true

# Rebuild Plymouth initramfs if this is an installed system (not live)
if [ -d /boot ] && [ -x /usr/sbin/update-initramfs ]; then
    update-initramfs -u 2>/dev/null || true
fi

# Run ldconfig
ldconfig 2>/dev/null || true

echo "[novaos-branding] post-install complete"
exit 0
EOF
chmod 755 "$PKG_DIR/DEBIAN/postinst"

# --- Prerm: backup user conf on removal ---
cat > "$PKG_DIR/DEBIAN/prerm" <<'EOF'
#!/bin/bash
set -e
echo "[novaos-branding] removing branding layer"
# Restore Plymouth default
plymouth-set-default-theme details 2>/dev/null || true
exit 0
EOF
chmod 755 "$PKG_DIR/DEBIAN/prerm"

# --- Copy files ---

# /usr/share/novaos/
cp -r "$ROOT/de-config/lxqt"     "$PKG_DIR/usr/share/novaos/config/"
cp -r "$ROOT/de-config/gtk"      "$PKG_DIR/usr/share/novaos/config/gtk-3.0/"
cp "$ROOT/menu-categories/lxqt-applications.menu" "$PKG_DIR/usr/share/novaos/menus/"

# Menu directory headers
python3 "$SCRIPT_DIR/split-directories.py" \
    "$ROOT/menu-categories/novaos-directories.txt" \
    "$PKG_DIR/usr/share/desktop-directories/" 2>/dev/null || {
    cp "$ROOT/menu-categories/novaos-directories.txt" \
       "$PKG_DIR/usr/share/desktop-directories/"
}

# Plymouth
cp "$ROOT/plymouth-theme/novaos/"* "$PKG_DIR/usr/share/plymouth/themes/novaos/"

# GRUB
cp -r "$ROOT/grub-theme/novaos/"* "$PKG_DIR/usr/share/grub/themes/novaos/"

# LightDM
cp "$ROOT/lightdm-theme/lightdm-gtk-greeter.conf" "$PKG_DIR/etc/lightdm/"
cp "$ROOT/lightdm-theme/greeter.css" "$PKG_DIR/usr/share/lightdm-gtk-greeter/"

# Wallpaper + icons
mkdir -p "$PKG_DIR/usr/share/novaos/wallpaper"
mkdir -p "$PKG_DIR/usr/share/novaos/icons"
cp "$ROOT/de-config/wallpaper/novaos-wallpaper.svg" "$PKG_DIR/usr/share/novaos/wallpaper/"
cp "$ROOT/de-config/wallpaper/"*.png "$PKG_DIR/usr/share/novaos/wallpaper/" 2>/dev/null || true
cp "$ROOT/de-config/icons/novaos-logo.svg" "$PKG_DIR/usr/share/novaos/icons/"
cp "$ROOT/de-config/icons/novaos-logo.png" "$PKG_DIR/usr/share/novaos/icons/" 2>/dev/null || true
cp "$ROOT/de-config/icons/index.theme" "$PKG_DIR/usr/share/icons/NovaOS-Icon/"

# Calamares
cp -r "$ROOT/calamares-branding/novaos/"* "$PKG_DIR/usr/share/calamares/branding/novaos/"

# Post-install script (used by Calamares on real installs)
cp "$ROOT/scripts/novaos-branding-postinstall.sh" "$PKG_DIR/etc/calamares/scripts/"
chmod 755 "$PKG_DIR/etc/calamares/scripts/novaos-branding-postinstall.sh"
# Also keep a copy in /usr/share/novaos/scripts/ for the .deb postinst to use
mkdir -p "$PKG_DIR/usr/share/novaos/scripts"
cp "$ROOT/scripts/novaos-branding-postinstall.sh" "$PKG_DIR/usr/share/novaos/scripts/"
chmod 755 "$PKG_DIR/usr/share/novaos/scripts/novaos-branding-postinstall.sh"

# Welcome app
mkdir -p "$PKG_DIR/usr/share/novaos/welcome"
cp "$ROOT/welcome-app/welcome.py" "$PKG_DIR/usr/share/novaos/welcome/"
cp "$ROOT/welcome-app/novaos-welcome" "$PKG_DIR/usr/bin/"
chmod 755 "$PKG_DIR/usr/bin/novaos-welcome"

# /etc/skel defaults
cp "$ROOT/de-config/lxqt/lxqt.conf"                  "$PKG_DIR/etc/skel/.config/lxqt/"
cp "$ROOT/de-config/lxqt/panel.conf"                 "$PKG_DIR/etc/skel/.config/lxqt/"
cp "$ROOT/de-config/lxqt/globalkeyshortcuts.conf"    "$PKG_DIR/etc/skel/.config/lxqt/"
cp "$ROOT/de-config/gtk/settings.ini"                "$PKG_DIR/etc/skel/.config/gtk-3.0/"
cp "$ROOT/menu-categories/lxqt-applications.menu"    "$PKG_DIR/etc/skel/.config/menus/"

# Autostart welcome
cat > "$PKG_DIR/etc/skel/.config/autostart/novaos-welcome.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=NovaOS Welcome
Comment=First-time setup and tour for NovaOS
Exec=/usr/bin/novaos-welcome
Icon=/usr/share/novaos/icons/novaos-logo.svg
Terminal=false
Categories=System;Education;
StartupNotify=true
X-GNOME-Autostart-enabled=true
EOF

# System-wide default LXQt config
cp "$ROOT/de-config/lxqt/lxqt.conf" "$PKG_DIR/etc/xdg/lxqt/"

# Build
cd "$BUILD_DIR"
dpkg-deb --build --root-owner-group "$PKG_DIR"

# Rename to a cleaner filename
DEB_FILE="$PKG_DIR.deb"
FINAL_NAME="$SCRIPT_DIR/${PACKAGE_NAME}_${VERSION}_all.deb"
mv "$DEB_FILE" "$FINAL_NAME"

echo
echo "Built: $FINAL_NAME"
ls -lh "$FINAL_NAME"
