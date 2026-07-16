# Calamares Custom Modules
# ========================
# This directory is RESERVED for future NovaOS-specific Calamares modules.
#
# Currently NovaOS uses only Calamares built-in modules (welcome, locale,
# keyboard, partition, install, bootloader, etc.) plus the post-install
# script hook in scripts/novaos-branding-postinstall.sh.
#
# ## When to add a module here
#
# Add a custom module if you need to:
# - Run Python code inside the Calamares install flow
# - Add a custom UI page (e.g., "Choose student tools")
# - Integrate with NovaOS-specific services post-install
#
# ## Module structure (Python example)
#
#   calamares-modules/
#   └── novaos-student-setup/
#       ├── module.desc        ← module descriptor
#       └── main.py            ← Python job script
#
# ## module.desc format
#
#   ---
#   type:      job
#   name:      novaos-student-setup
#   interface: python
#   script:    main.py
#
# ## Registering a module
#
# Once created, add the module name to your Calamares settings.conf:
#
#   exec:
#     - novaos-student-setup
#
# And symlink or copy this directory into:
#   /usr/lib/calamares/modules/novaos-student-setup/
#
# The install-branding.sh script will need to be updated to copy modules.
#
# ## References
# - https://github.com/calamares/calamares/wiki/Develop-Module
# - https://api.kde.org/calamares/
