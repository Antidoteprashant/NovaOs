#!/bin/bash
# ----------------------------------------------------------------------
# NovaOS branding installer
# ----------------------------------------------------------------------
# Runs on a BUILT Debian system to install all branding files
# into their correct system locations. Idempotent.
#
# Usage:
#   sudo ./install-branding.sh
#   sudo ./install-branding.sh --uninstall
#
# After running, package everything into a .deb with:
#   ./build-deb.sh
# ----------------------------------------------------------------------

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOVAOS_ROOT="$SCRIPT_DIR"  # this script lives in scripts/, root is one up

if [ "$(basename "$SCRIPT_DIR")" = "scripts" ]; then
    NOVAOS_ROOT="$(dirname "$SCRIPT_DIR")"
fi

ASSETS_DIR="/usr/share/novaos"
DESKTOP_DIRS="/usr/share/desktop-directories"
GRUB_DIR="/usr/share/grub/themes/novaos"
PLYMOUTH_DIR="/usr/share/plymouth/themes/novaos"
LIGHTDM_GREETER_DIR="/usr/share/lightdm-gtk-greeter"
LIGHTDM_ETC="/etc/lightdm"

ACTION="install"
if [ "${1:-}" = "--uninstall" ]; then
    ACTION="uninstall"
fi

log() { echo "[novaos-install] $*"; }
fail() { echo "[novaos-install] ERROR: $*" >&2; exit 1; }

[ "$(id -u)" -eq 0 ] || fail "must be run as root (sudo $0)"

# ----------------------------------------------------------------------
case "$ACTION" in
install)
    log "Installing NovaOS branding to $ASSETS_DIR"

    # Create ALL required system directories upfront
    mkdir -p "$ASSETS_DIR"/{config/lxqt,config/gtk-3.0,menus,desktop-directories,plymouth,grub,lightdm,wallpaper,icons,welcome,calamares}
    mkdir -p "$DESKTOP_DIRS"
    mkdir -p "$PLYMOUTH_DIR"
    mkdir -p "$GRUB_DIR"
    mkdir -p "$LIGHTDM_GREETER_DIR"
    mkdir -p "$LIGHTDM_ETC"
    mkdir -p /etc/calamares/{branding/novaos,scripts}

    # 1. LXQt config
    cp -r "$NOVAOS_ROOT/de-config/lxqt/"* "$ASSETS_DIR/config/lxqt/"

    # 2. GTK config
    cp -r "$NOVAOS_ROOT/de-config/gtk/"* "$ASSETS_DIR/config/gtk-3.0/"

    # NOTE: session.conf is included in de-config/lxqt/ — copied above with lxqt configs

    # 3. Menu
    cp "$NOVAOS_ROOT/menu-categories/lxqt-applications.menu" "$ASSETS_DIR/menus/"

    # 4. Menu directory headers (split the multi-desktop-entry file)
    log "  installing menu directories"
    python3 "$SCRIPT_DIR/split-directories.py" \
        "$NOVAOS_ROOT/menu-categories/novaos-directories.txt" \
        "$ASSETS_DIR/desktop-directories" 2>/dev/null || {
        log "  ⚠ split-directories.py failed — installing as single file"
        cp "$NOVAOS_ROOT/menu-categories/novaos-directories.txt" \
           "$DESKTOP_DIRS/novaos-directories.txt"
    }

    # 5. Plymouth theme
    cp -r "$NOVAOS_ROOT/plymouth-theme/novaos/"* "$PLYMOUTH_DIR/"
    log "  ✓ Plymouth theme files installed"

    # 6. GRUB theme (flatten into assets/grub — postinstall checks $NOVAOS_ASSETS/grub)
    mkdir -p "$ASSETS_DIR/grub"
    cp -r "$NOVAOS_ROOT/grub-theme/novaos/"* "$ASSETS_DIR/grub/"
    # Also install to GRUB system path
    cp -r "$NOVAOS_ROOT/grub-theme/novaos/"* "$GRUB_DIR/" 2>/dev/null || true
    log "  ✓ GRUB theme installed"

    # 7. LightDM
    cp "$NOVAOS_ROOT/lightdm-theme/greeter.css" "$LIGHTDM_GREETER_DIR/"
    cp "$NOVAOS_ROOT/lightdm-theme/lightdm-gtk-greeter.conf" "$LIGHTDM_ETC/"
    log "  ✓ LightDM config installed"

    # 8. Wallpaper + icons
    cp "$NOVAOS_ROOT/de-config/wallpaper/novaos-wallpaper.svg" "$ASSETS_DIR/wallpaper/"
    cp "$NOVAOS_ROOT/de-config/wallpaper"/novaos-wallpaper*.png "$ASSETS_DIR/wallpaper/" 2>/dev/null || true
    cp "$NOVAOS_ROOT/de-config/icons/novaos-logo.svg" "$ASSETS_DIR/icons/"
    cp "$NOVAOS_ROOT/de-config/icons"/novaos-logo*.png "$ASSETS_DIR/icons/" 2>/dev/null || true
    log "  ✓ Wallpaper + icons installed"

    # 9. Icon theme skeleton
    cp "$NOVAOS_ROOT/de-config/icons/index.theme" "$ASSETS_DIR/icons/"
    ICON_THEME_DIR="/usr/share/icons/NovaOS-Icon"
    mkdir -p "$ICON_THEME_DIR"
    cp "$NOVAOS_ROOT/de-config/icons/index.theme" "$ICON_THEME_DIR/"
    gtk-update-icon-cache -f -t "$ICON_THEME_DIR" 2>/dev/null || true
    log "  ✓ Icon theme installed"

    # 10. Calamares branding
    CALAMARES_BRANDING="/etc/calamares/branding/novaos"
    cp -r "$NOVAOS_ROOT/calamares-branding/novaos/"* "$CALAMARES_BRANDING/"
    log "  ✓ Calamares branding installed"

    # 11. Post-install script
    cp "$NOVAOS_ROOT/scripts/novaos-branding-postinstall.sh" \
       "/etc/calamares/scripts/novaos-branding-postinstall.sh"
    chmod 755 "/etc/calamares/scripts/novaos-branding-postinstall.sh"
    log "  ✓ Post-install hook installed"

    # 12. Welcome app
    cp "$NOVAOS_ROOT/welcome-app/novaos-welcome" "$ASSETS_DIR/welcome/"
    chmod 755 "$ASSETS_DIR/welcome/novaos-welcome"
    log "  ✓ Welcome app installed"

    log "Done."
    log "Next: configure Calamares settings.conf to call novaos-branding-postinstall.sh"
    log "      and select the 'novaos' branding via 'branding: novaos'"
    ;;

uninstall)
    log "Uninstalling NovaOS branding"
    rm -rf "$ASSETS_DIR"
    rm -rf "$ICON_THEME_DIR"
    rm -f /etc/calamares/scripts/novaos-branding-postinstall.sh
    plymouth-set-default-theme details || true
    rm -rf "$PLYMOUTH_DIR"
    rm -rf "$GRUB_DIR"
    log "Done. Restore /etc/lightdm/lightdm-gtk-greeter.conf from backup if needed."
    ;;
esac
