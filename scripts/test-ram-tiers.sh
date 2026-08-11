#!/bin/bash
# NovaOS RAM-Tier Testing Script
# This script automates testing the ISO across different RAM configurations using QEMU.

ISO_PATH="live-image-amd64.hybrid.iso"

if [ ! -f "$ISO_PATH" ]; then
    echo "Error: $ISO_PATH not found in the current directory."
    echo "Please run this script from the root of the novaos-build directory."
    exit 1
fi

echo "======================================"
echo "    NovaOS RAM-Tier Test Suite"
echo "======================================"
echo "Select the RAM tier to test:"
echo "1) 1024 MB (1GB)"
echo "2) 2048 MB (2GB)"
echo "3) 4096 MB (4GB)"
echo "4) Run all sequentially"
echo "q) Quit"
echo "======================================"
read -p "Choice: " choice

run_qemu() {
    local ram_size=$1
    echo "Starting VM with ${ram_size}MB RAM..."
    echo "(Inside the VM, open terminal and run 'free -h' to log RAM usage)"
    qemu-system-x86_64 -m $ram_size -cdrom $ISO_PATH -boot d
    echo "VM with ${ram_size}MB closed."
}

case $choice in
    1)
        run_qemu 1024
        ;;
    2)
        run_qemu 2048
        ;;
    3)
        run_qemu 4096
        ;;
    4)
        run_qemu 1024
        read -p "Press Enter to start 2GB test..."
        run_qemu 2048
        read -p "Press Enter to start 4GB test..."
        run_qemu 4096
        ;;
    q|Q)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac
