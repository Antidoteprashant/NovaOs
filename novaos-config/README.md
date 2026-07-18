# NovaOS — Desktop Experience & Installer
**Owner:** [you] · **Status:** Week 1-2 work-in-progress · **Last updated:** 2026-07-16

This directory contains everything related to the NovaOS desktop layer
(LXQt theming, Plymouth, GRUB, LightDM, Calamares branding, Welcome app)
and is **modular** — designed to be dropped onto a base Debian ISO built
by another teammate.

## Quick Start

```bash
# On a freshly built Debian system (for testing):
cd novaos-config
sudo scripts/install-branding.sh

# Reverse (uninstall):
sudo scripts/install-branding.sh --uninstall
```

## Directory layout

```
novaos-config/
├── docs/                       Documentation (design tokens, decisions, handoff)
├── design-tokens.txt           The single source of truth for colors
├── de-config/                  Desktop environment config files
│   ├── lxqt/                   LXQt panel, keybindings, session config
│   ├── gtk/                    GTK 3 settings (for non-Qt apps)
│   ├── icons/                  Icon theme skeleton + NovaOS logo
│   └── wallpaper/              Default wallpaper (SVG)
├── plymouth-theme/novaos/      Plymouth boot splash (script theme)
├── grub-theme/novaos/          GRUB boot menu theme
├── lightdm-theme/              LightDM login screen config + CSS
├── calamares-branding/         Installer branding (branding.desc + QSS)
│   ├── novaos/                 branding.desc (YAML!), stylesheet.qss, images
│   ├── modules/                shellprocess instance config (post-install hook)
│   └── settings.conf.snippet   Exact settings.conf wiring instructions
├── calamares-modules/          (reserved for future custom modules)
├── welcome-app/                First-login PyQt5 app
├── menu-categories/            Custom app menu XML + directory headers
├── scripts/                    Installer/uninstaller + helpers
├── package-lists/              Debian packages for live-build
└── install-branding.sh         Master installer
```

## Handoff to teammates

### To: Base-OS teammate (builds the Debian ISO)

You don't need to know about any of the LXQt/Plymouth/Calamares specifics.
You only need to:

1. Add `package-lists/novaos-desktop.list.chroot` to your `live-build`
   `config/package-lists/` directory.
2. Hook the post-install script — read `calamares-branding/settings.conf.snippet`
   carefully, it needs THREE things (not just one snippet):
   a. `branding: novaos` + a named `shellprocess` instance in `settings.conf`
   b. Copy `calamares-branding/modules/shellprocess-novaosbranding.conf`
      into `/etc/calamares/modules/`
   c. Add `shellprocess@novaosbranding` as the LAST entry in the `exec:` sequence
3. Include the welcome app as a chroot-install hook:
   ```bash
   cp -r novaos-config/welcome-app/welcome.py \
       config/chroot_local-includes/usr/share/novaos/welcome/welcome.py
   cp novaos-config/welcome-app/novaos-welcome \
       config/chroot_local-includes/usr/bin/novaos-welcome
   chmod +x config/chroot_local-includes/usr/bin/novaos-welcome
   ```

That's it. Your Calamares config can stay generic; the branding layer
self-activates via the post-install script.

### To: AI-assistant teammate

None of the AI-assistant work conflicts with this layer. The Welcome app
already includes a "Quick Links" section; if you build an in-house tutor
or chatbot, you can register it via a single `.desktop` file dropped into
`/usr/share/applications/` — no other change needed.

## Design decisions

| Decision | Choice | Why |
|----------|--------|-----|
| DE | **LXQt** | ~150 MB idle vs XFCE ~300 MB; cleaner config files; better theming |
| Compositor | None | 2GB RAM target; compositing costs ~50 MB + GPU dependency |
| Color scheme | Dark + teal `#1FB8C1` | Reduces eye strain during long coding sessions |
| Font | Inter (UI), JetBrains Mono (code) | Free, ships in Debian; no licensing concerns |
| Plymouth | Script theme (not pixel) | Smooth on any hardware; no frame tearing |
| LightDM | lightdm-gtk-greeter | ~10 MB vs webkit-greeter's ~200 MB |
| Welcome app | Python + PyQt5 | ~30 MB RAM; native feel; QSS for theming |

## Files I haven't yet created (and what to do about them)

These are binary assets — you'll need real PNGs. The SVGs and the
generator scripts are here; the PNGs you'll need to render separately:

| File | Source | Notes |
|------|--------|-------|
| `de-config/wallpaper/novaos-wallpaper.png` | Render `novaos-wallpaper.svg` at 1920x1080 | Inkscape CLI: `inkscape ... --export-png` |
| `plymouth-theme/novaos/logo.png` | Render `de-config/icons/novaos-logo.svg` at 256x256 | |
| `plymouth-theme/novaos/progress_box.png` | Custom draw (one-time) | Use ImageMagick or Inkscape |
| `plymouth-theme/novaos/progress_box_thumb.png` | Custom draw | |
| `calamares-branding/novaos/sidebar.png` | TBD | Render at 260×800 px |
| `calamares-branding/novaos/background.png` | Use `de-config/wallpaper/novaos-wallpaper.png` | Same image works |

## Reproducibility checklist (before each rebuild)

- [ ] `scripts/install-branding.sh` runs cleanly on a fresh Debian install
- [ ] Plymouth theme rebuilds initramfs without errors
- [ ] GRUB theme renders correctly at 1920×1080 and 1366×768
- [ ] LightDM greeter shows logo + custom CSS
- [ ] Welcome app appears on first login
- [ ] `novaos-welcome` launches from menu
- [ ] Calamares branding shows on every install step
- [ ] `docs/design-tokens.txt` is in sync with all the .qss / .css files
- [ ] `package-lists/novaos-desktop.list.chroot` installs cleanly via apt
