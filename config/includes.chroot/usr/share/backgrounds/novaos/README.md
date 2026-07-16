Owned by Person 2.

This directory is baked into the live ISO at:
  /usr/share/backgrounds/novaos/

## How the wallpaper gets here

The wallpaper PNG is NOT committed to git (binary file, 80KB+).
It is generated from the SVG source and installed by the build hook.

## Build-time flow

  novaos-config/de-config/wallpaper/novaos-wallpaper.svg   ← source of truth
       │
       ▼  (scripts/render-assets.sh)
  novaos-config/de-config/wallpaper/novaos-wallpaper.png   ← rendered PNG
       │
       ▼  (scripts/install-branding.sh → copies to /usr/share/novaos/wallpaper/)
  /usr/share/novaos/wallpaper/novaos-wallpaper.png          ← in chroot
       │
       ▼  (config/hooks/live/005-novaos-branding.hook.chroot)
  /usr/share/backgrounds/novaos/novaos-wallpaper.png        ← final location in ISO

## For Person 1 (build engineer)

Before running `lb build`, make sure install-branding.sh was run inside
the chroot OR add the novaos .deb to config/package-lists/.

The hook (005-novaos-branding.hook.chroot) handles the copy automatically.

## LXQt wallpaper config

LXQt's file manager (pcmanfm-qt) reads wallpaper from:
  ~/.config/pcmanfm-qt/lxqt/settings.conf → Wallpaper=...

The novaos-branding-postinstall.sh hook writes this to /etc/skel/
so every new user gets it automatically on first login.
