# GRUB Theme Icons
# ----------------
# These icons appear next to boot menu entries (the icon_height/icon_width
# defined in theme.txt). They must be PNG files.
#
# Required icons:
#   linux.png    — shown for Linux boot entries  (32×32 or 24×24 px)
#   windows.png  — shown for Windows entries     (32×32 or 24×24 px)
#   uefi.png     — shown for UEFI shell entries   (32×32)
#   memtest.png  — shown for Memtest86+ entry     (32×32)
#
# Generation (on a Linux box with ImageMagick):
#   # Linux penguin icon (teal #1FB8C1 on transparent bg)
#   convert -size 32x32 xc:none \
#       -fill "#1FB8C1" -font "DejaVu-Sans-Bold" -pointsize 22 \
#       -gravity center -annotate +0+0 "🐧" linux.png
#
#   # Windows icon (blue #0078D4 on transparent bg)
#   convert -size 32x32 xc:none \
#       -fill "#0078D4" -draw "rectangle 4,4 14,14" \
#       -draw "rectangle 17,4 28,14" \
#       -draw "rectangle 4,17 14,28" \
#       -draw "rectangle 17,17 28,28" windows.png
#
# OR just copy matching icons from /usr/share/grub/themes/starfield/icons/
# and recolor them to match #1FB8C1 (nova-accent).
#
# The render-assets.sh script does NOT generate these; they are one-time assets.
# Pre-generate on a dev box and commit the PNGs to git.
