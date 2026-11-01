#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
set -euo pipefail

repo="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
work="$repo/build"
out="$repo/out"
[[ $EUID -eq 0 ]] || { echo 'Run this script as root on Arch Linux.' >&2; exit 1; }
[[ $(uname -m) == x86_64 ]] || { echo 'An x86_64 build host is required.' >&2; exit 1; }
for tool in mkarchiso arch-chroot mksquashfs grub-mkrescue grub-mkfont grub-script-check xorriso python3; do
    command -v "$tool" >/dev/null || { echo "Missing build tool: $tool" >&2; exit 1; }
done
[[ ! -e "$work" ]] || { echo 'build/ already exists. Rename or remove your previous build deliberately.' >&2; exit 1; }
python3 "$repo/scripts/validate.py"
mkdir -p "$work/profile" "$work/intermediate" "$out"
cp -a "$repo/profile/." "$work/profile/"

# Archiso supplies the package installation, root filesystem and staged boot files.
mkarchiso -v -w "$work/staging" -o "$work/intermediate" "$work/profile"
root="$work/staging/x86_64/airootfs"
stage="$work/staging/iso"
[[ -d "$root/usr" && -d "$stage/arch" ]] || { echo 'Unexpected Archiso staging layout.' >&2; exit 1; }

# Apply the hook explicitly as well, so the recipe does not depend on legacy
# Archiso automatic customization-hook behavior.
mount --bind "$root" "$root"
trap 'umount "$root" 2>/dev/null || true' EXIT
arch-chroot "$root" /bin/bash /root/customize_airootfs.sh
chown -R 1000:1000 "$root/home/aika"
chmod 750 "$root/etc/sudoers.d"
chmod 440 "$root/etc/sudoers.d/10-aika-live"
arch-chroot "$root" pacman --config /dev/null -Q > "$stage/arch/pkglist.x86_64.txt"
arch-chroot "$root" fastfetch --config /etc/xdg/fastfetch/config.jsonc --pipe > "$out/fastfetch-build-check.txt"
grep -q 'AikaOS 11.1' "$out/fastfetch-build-check.txt"
cp "$root/boot/vmlinuz-linux" "$root/boot/initramfs-linux.img" "$stage/arch/boot/x86_64/"
umount "$root"
trap - EXIT

mksquashfs "$root" "$stage/arch/x86_64/airootfs.sfs" -noappend -comp zstd -Xcompression-level 4 -b 1M -processors "$(nproc)"
(cd "$stage/arch/x86_64" && sha512sum airootfs.sfs > airootfs.sha512)
printf '11.1\n' > "$stage/arch/version"

# Keep intermediate boot assets out of the final GRUB-only staging tree.
mkdir -p "$work/upstream-boot"
for item in EFI boot/syslinux loader efiboot.img; do
    if [[ -e "$stage/$item" ]]; then
        mv "$stage/$item" "$work/upstream-boot/${item//\//-}"
    fi
done
theme="$stage/boot/grub/themes/aikaos"
mkdir -p "$theme" "$stage/boot/grub/fonts"
cp "$repo/assets/grub/background.png" "$repo/assets/grub/theme.txt" "$theme/"
grub-mkfont -s 18 -o "$theme/aika18.pf2" /usr/share/fonts/TTF/DejaVuSans.ttf
grub-mkfont -s 24 -o "$theme/aika24.pf2" /usr/share/fonts/TTF/DejaVuSans.ttf
cp /usr/share/grub/unicode.pf2 "$stage/boot/grub/fonts/"
cp "$repo/assets/grub/grub.cfg" "$stage/boot/grub/grub.cfg"
grub-script-check "$stage/boot/grub/grub.cfg"

iso="$out/aikaos-11.1-x86_64-grub.iso"
grub-mkrescue -o "$iso" "$stage" -volid AIKAOS_11
(cd "$out" && sha256sum "$(basename "$iso")" > "$(basename "$iso").sha256")
xorriso -indev "$iso" -report_el_torito plain -report_system_area plain > "$out/boot-report.txt" 2>&1
printf 'Built %s\n' "$iso"
