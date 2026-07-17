#!/usr/bin/env python3
"""Split a multi-[Desktop Entry] text file into individual .directory files.

The menu-categories file (novaos-directories.txt) contains many
[Desktop Entry] blocks concatenated. This script reads them and writes
one .directory file per block, named after the Name= field.
"""
import sys
import os
import re

def slugify(name: str) -> str:
    """Convert a menu name to a filesystem-safe slug."""
    s = name.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def split(input_path: str, output_dir: str) -> None:
    with open(input_path) as f:
        content = f.read()

    # Split on [Desktop Entry] blocks
    blocks = re.split(r'\n(?=\[Desktop Entry\])', content)
    written = 0
    for block in blocks:
        block = block.strip()
        if not block.startswith('[Desktop Entry]'):
            continue

        # Extract Name= line
        m = re.search(r'^Name=(.+)$', block, re.MULTILINE)
        if not m:
            continue
        name = m.group(1).strip()

        # Build filename
        slug = slugify(name)
        out_path = os.path.join(output_dir, f"novaos-{slug}.directory")

        # Inject Type=Directory if not present
        if 'Type=Directory' not in block:
            block = block.replace('[Desktop Entry]', '[Desktop Entry]\nType=Directory', 1)

        with open(out_path, 'w') as f:
            f.write(block + '\n')
        written += 1
        print(f"  wrote {out_path}")

    print(f"Split {written} directory entries into {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <input.txt> <output-dir>", file=sys.stderr)
        sys.exit(1)
    split(sys.argv[1], sys.argv[2])
