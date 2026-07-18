#!/bin/bash
# ----------------------------------------------------------------------
# NovaOS Calamares post-install hook
# ----------------------------------------------------------------------
# Called by Calamares after the user clicks "Install" and the system
# is on the target disk. Receives the new system root in $1.
#
# This is the SINGLE seam where NovaOS branding layer meets the base ISO.
# Your base-ISO teammate doesn't need to know about anything in
# /etc/skel/.config/ — they just include this script in their
# settings.conf and it applies everything for them.
#
# Idempotent: safe to run multiple times (skips if already applied).
# ----------------------------------------------------------------------

set -e

TARGET="$1"

if [ -z "$TARGET" ]; then
    echo "[novaos-branding] FATAL: no target root given"
    exit 1
fi

if [ ! -d "$TARGET" ]; then
    echo "[novaos-branding] FATAL: target $TARGET is not a directory"
    exit 1
fi

NOVAOS_ASSETS="/usr/share/novaos"
SKEL_DIR="$TARGET/etc/skel"
LOG="/var/log/novaos-branding.log"

mkdir -p "$TARGET/var/log"

log() {
    echo "[novaos-branding] $*" | tee -a "$TARGET$LOG" 2>/dev/null || echo "[novaos-branding] $*"
}

log "Applying NovaOS branding to $TARGET"

# ----------------------------------------------------------------------
# 1. Copy user-level config files to /etc/skel so new users inherit them
# ----------------------------------------------------------------------
mkdir -p "$SKEL_DIR/.config"

# LXQt config
if [ -d "$NOVAOS_ASSETS/config/lxqt" ]; then
    mkdir -p "$SKEL_DIR/.config/lxqt"
    cp -r "$NOVAOS_ASSETS/config/lxqt/"* "$SKEL_DIR/.config/lxqt/"
    log "  ✓ LXQt config"
fi

# GTK config
if [ -d "$NOVAOS_ASSETS/config/gtk-3.0" ]; then
    mkdir -p "$SKEL_DIR/.config/gtk-3.0"
    cp -r "$NOVAOS_ASSETS/config/gtk-3.0/"* "$SKEL_DIR/.config/gtk-3.0/"
    log "  ✓ GTK 3 config"
fi

# Menu definitions
if [ -d "$NOVAOS_ASSETS/menus" ]; then
    mkdir -p "$SKEL_DIR/.config/menus"
    cp -r "$NOVAOS_ASSETS/menus/"* "$SKEL_DIR/.config/menus/"
    log "  ✓ Menu definitions"
fi

# Menu directory headers
if [ -d "$NOVAOS_ASSETS/desktop-directories" ]; then
    mkdir -p "$TARGET/usr/share/desktop-directories"
    cp -r "$NOVAOS_ASSETS/desktop-directories/"* "$TARGET/usr/share/desktop-directories/"
    log "  ✓ Menu directory headers"
fi

# ----------------------------------------------------------------------
# 2. System-wide defaults (already installed by .deb; this just re-asserts)
# ----------------------------------------------------------------------

# Default LXQt config for all users (e.g. fresh login) — we just copy our
# config over the default location so even non-skel users get it.
if [ -f "$NOVAOS_ASSETS/config/lxqt/lxqt.conf" ]; then
    mkdir -p "$TARGET/etc/xdg/lxqt"
    cp "$NOVAOS_ASSETS/config/lxqt/lxqt.conf" "$TARGET/etc/xdg/lxqt/"
fi

# ----------------------------------------------------------------------
# 3. Enable the Plymouth theme
# ----------------------------------------------------------------------
# NOTE (fixed): install-branding.sh copies the Plymouth theme straight to
# the REAL system path /usr/share/plymouth/themes/novaos/ — NOT under
# /usr/share/novaos/plymouth/ (that staging path is never populated).
# On the live ISO, the theme already lives at the real path, so we copy
# FROM there INTO the newly-installed target disk.
PLYMOUTH_SRC="/usr/share/plymouth/themes/novaos"

if [ -d "$PLYMOUTH_SRC" ]; then
    mkdir -p "$TARGET/usr/share/plymouth/themes/novaos"
    cp -r "$PLYMOUTH_SRC/"* "$TARGET/usr/share/plymouth/themes/novaos/"
    chroot "$TARGET" plymouth-set-default-theme novaos 2>>"$TARGET$LOG" || {
        log "  ⚠ plymouth-set-default-theme failed — continuing"
    }
    log "  ✓ Plymouth theme copied and selected"
else
    log "  ⚠ Plymouth theme not found at $PLYMOUTH_SRC — skipped"
fi

# ----------------------------------------------------------------------
# 4. Enable the GRUB theme
# ----------------------------------------------------------------------
# NOTE (fixed): same issue as Plymouth — real source is
# /usr/share/grub/themes/novaos/, not /usr/share/novaos/grub/.
GRUB_SRC="/usr/share/grub/themes/novaos"

if [ -d "$GRUB_SRC" ]; then
    mkdir -p "$TARGET/usr/share/grub/themes/novaos"
    cp -r "$GRUB_SRC/"* "$TARGET/usr/share/grub/themes/novaos/"

    # Update /etc/default/grub to reference our theme
    GRUB_THEME_LINE='GRUB_THEME=/usr/share/grub/themes/novaos/theme.txt'
    mkdir -p "$TARGET/etc/default"
    if [ -f "$TARGET/etc/default/grub" ]; then
        if ! grep -q "^GRUB_THEME=" "$TARGET/etc/default/grub"; then
            echo "$GRUB_THEME_LINE" >> "$TARGET/etc/default/grub"
        else
            sed -i "s|^GRUB_THEME=.*|$GRUB_THEME_LINE|" "$TARGET/etc/default/grub"
        fi
    else
        echo "$GRUB_THEME_LINE" > "$TARGET/etc/default/grub"
    fi

    # Set a sensible default resolution
    if ! grep -q "^GRUB_GFXMODE=" "$TARGET/etc/default/grub"; then
        echo "GRUB_GFXMODE=auto" >> "$TARGET/etc/default/grub"
    fi
    log "  ✓ GRUB theme configured (run update-grub on first boot)"
fi

# ----------------------------------------------------------------------
# 5. Configure LightDM greeter
# ----------------------------------------------------------------------
# NOTE (fixed): install-branding.sh puts these at the real system paths
# /etc/lightdm/lightdm-gtk-greeter.conf and
# /usr/share/lightdm-gtk-greeter/greeter.css — not under /usr/share/novaos/.

if [ -f "/etc/lightdm/lightdm-gtk-greeter.conf" ]; then
    mkdir -p "$TARGET/etc/lightdm"
    cp "/etc/lightdm/lightdm-gtk-greeter.conf" \
       "$TARGET/etc/lightdm/lightdm-gtk-greeter.conf"
    log "  ✓ LightDM greeter config copied"
else
    log "  ⚠ LightDM greeter config not found on live system — skipped"
fi

# Ensure the greeter can find its custom CSS
if [ -f "/usr/share/lightdm-gtk-greeter/greeter.css" ]; then
    mkdir -p "$TARGET/usr/share/lightdm-gtk-greeter"
    cp "/usr/share/lightdm-gtk-greeter/greeter.css" \
       "$TARGET/usr/share/lightdm-gtk-greeter/greeter.css" 2>/dev/null || {
        log "  ⚠ could not install greeter.css — package lightdm-gtk-greeter may not be installed yet"
    }
    log "  ✓ LightDM greeter.css copied"
fi

# ----------------------------------------------------------------------
# 6. Autostart the Welcome app on first login
# ----------------------------------------------------------------------

WELCOME_DESKTOP="[Desktop Entry]
Type=Application
Name=NovaOS Welcome
Comment=First-time setup and tour for NovaOS
Exec=/usr/bin/novaos-welcome --first-run
Icon=/usr/share/novaos/icons/novaos-logo.svg
Terminal=false
Categories=System;Education;
StartupNotify=true
X-GNOME-Autostart-enabled=true
"

# NOTE (fixed): this was checking `-d` (directory) but novaos-welcome is a
# FILE (a launcher script) — the check always failed silently and the
# welcome app was never installed. Changed to `-f`.
if [ -f "$NOVAOS_ASSETS/welcome/novaos-welcome" ]; then
    # Install both the launcher AND the Python app it execs
    # (the launcher alone is useless without welcome.py next to it)
    mkdir -p "$TARGET/usr/bin" "$TARGET/usr/share/novaos/welcome"
    cp "$NOVAOS_ASSETS/welcome/novaos-welcome" "$TARGET/usr/bin/novaos-welcome"
    chmod 755 "$TARGET/usr/bin/novaos-welcome"
    if [ -f "$NOVAOS_ASSETS/welcome/welcome.py" ]; then
        cp "$NOVAOS_ASSETS/welcome/welcome.py" "$TARGET/usr/share/novaos/welcome/welcome.py"
    else
        log "  ⚠ welcome.py not found — launcher will fail at runtime"
    fi
    log "  ✓ Welcome app installed"

    # Set up autostart for new users
    mkdir -p "$SKEL_DIR/.config/autostart"
    echo "$WELCOME_DESKTOP" > "$SKEL_DIR/.config/autostart/novaos-welcome.desktop"
    log "  ✓ Welcome autostart configured"
else
    log "  ⚠ novaos-welcome launcher not found at $NOVAOS_ASSETS/welcome/ — skipped"
fi

# ----------------------------------------------------------------------
# 7. Set the default wallpaper (xfce and LXQt both honor this)
# ----------------------------------------------------------------------

if [ -f "$NOVAOS_ASSETS/wallpaper/novaos-wallpaper.png" ]; then
    # pcmanfm-qt (LXQt default) uses ~/.config/pcmanfm-qt/lxqt/settings.conf
    # NOTE (fixed): this used to check `if [ -d ".../pcmanfm-qt" ]` first —
    # but that directory never exists yet on a fresh system (pcmanfm-qt
    # hasn't run to create its own default config), so the write was
    # always silently skipped. Now creates the directory unconditionally.
    mkdir -p "$SKEL_DIR/.config/pcmanfm-qt/lxqt"
    cat > "$SKEL_DIR/.config/pcmanfm-qt/lxqt/settings.conf" <<EOF
[Desktop]
Wallpaper=$NOVAOS_ASSETS/wallpaper/novaos-wallpaper.png
WallpaperMode=stretch
EOF
    log "  ✓ Wallpaper set"
else
    log "  ⚠ wallpaper PNG not found at $NOVAOS_ASSETS/wallpaper/ — skipped"
fi

# ----------------------------------------------------------------------
# 8. Run ldconfig (in case any of the above touched libs)
# ----------------------------------------------------------------------
chroot "$TARGET" ldconfig 2>/dev/null || true

log "NovaOS branding applied successfully"
exit 0
