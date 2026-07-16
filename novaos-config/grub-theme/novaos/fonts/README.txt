# GRUB Theme Fonts
# ----------------
# GRUB cannot use system fonts directly — it needs fonts in its own .pf2 format.
# Generate them with grub-mkfont from the DejaVu TTF packages.
#
# Run this ONCE on a Debian/Ubuntu build machine (needs grub-common + fonts-dejavu):
#
#   sudo apt install grub-common fonts-dejavu-core fonts-dejavu-extra
#
#   grub-mkfont -s 28 -o /boot/grub/themes/novaos/fonts/DejaVuSans-Bold-28.pf2 \
#       /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
#
#   grub-mkfont -s 16 -o /boot/grub/themes/novaos/fonts/DejaVuSans-16.pf2 \
#       /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
#
#   grub-mkfont -s 12 -o /boot/grub/themes/novaos/fonts/DejaVuSans-12.pf2 \
#       /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
#
#   grub-mkfont -s 11 -o /boot/grub/themes/novaos/fonts/DejaVuSans-11.pf2 \
#       /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
#
#   grub-mkfont -s 10 -o /boot/grub/themes/novaos/fonts/DejaVuSans-10.pf2 \
#       /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
#
# The install-branding.sh script calls render-assets.sh which handles wallpaper.
# Fonts must be pre-built and bundled here before the .deb is packaged.
# The build-deb.sh script will include everything in grub-theme/novaos/.
#
# Expected files in this directory after generation:
#   DejaVuSans-Bold-28.pf2   (title font)
#   DejaVuSans-16.pf2        (menu item font)
#   DejaVuSans-12.pf2        (tagline font)
#   DejaVuSans-11.pf2        (bottom bar font)
#   DejaVuSans-10.pf2        (progress bar font)
