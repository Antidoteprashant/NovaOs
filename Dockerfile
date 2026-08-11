FROM --platform=linux/amd64 debian:bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    live-build \
    live-config \
    live-boot \
    isolinux \
    syslinux-common \
    syslinux-utils \
    grub-common \
    grub-efi-amd64-bin \
    grub-pc-bin \
    xorriso \
    squashfs-tools \
    sudo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
CMD ["/bin/bash"]
