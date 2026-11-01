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
installer=${AIKAOS_INSTALLER:-0}
[[ $installer == 0 || $installer == 1 ]] || { echo 'AIKAOS_INSTALLER must be 0 or 1.' >&2; exit 1; }
if [[ $installer == 1 ]]; then
    command -v repo-add >/dev/null
    shopt -s nullglob
    local_packages=("$out/localrepo/"calamares-*.pkg.tar.zst)
    ((${#local_packages[@]} == 1)) || { echo 'Build or download one Calamares package into out/localrepo/ first.' >&2; exit 1; }
    [[ $(pacman -Qp "${local_packages[0]}" | cut -d ' ' -f 1) == calamares ]] || { echo 'Unexpected local package.' >&2; exit 1; }
    repo-add -q "$out/localrepo/aikaos-build.db.tar.gz" "${local_packages[@]}"
    python3 "$repo/scripts/prepare-installer-profile.py" --profile "$work/profile"
    # This repository contains only our locally built installer package. The
    # normal Arch repository signature policy remains unchanged.
    printf '\n[aikaos-build]\nSigLevel = Optional TrustedOnly\nServer = file://%s\n' "$out/localrepo" >> "$work/profile/pacman.conf"
fi

# Archiso supplies the package installation, root filesystem and staged boot files.
mkarchiso -v -w "$work/staging" -o "$work/intermediate" "$work/profile"
root="$work/staging/x86_64/airootfs"
stage="$work/staging/iso"
[[ -d "$root/usr" && -d "$stage/arch" ]] || { echo 'Unexpected Archiso staging layout.' >&2; exit 1; }

# Archiso 92 runs and removes the customization hook, then preserves the boot
# files in the ISO staging tree before clearing the root filesystem's /boot.
[[ ! -e "$root/root/customize_airootfs.sh" ]] || { echo 'Archiso did not finish the customization hook.' >&2; exit 1; }
for artifact in arch/x86_64/airootfs.sfs arch/x86_64/airootfs.sha512 arch/boot/x86_64/vmlinuz-linux arch/boot/x86_64/initramfs-linux.img; do
    [[ -s "$stage/$artifact" ]] || { echo "Missing staged artifact: $artifact" >&2; exit 1; }
done
[[ $(stat -c %u:%g "$root/home/aika") == 1000:1000 ]] || { echo 'Incorrect live home ownership.' >&2; exit 1; }
if [[ -d "$root/etc/pacman.d/gnupg/private-keys-v1.d" ]] &&
    find "$root/etc/pacman.d/gnupg/private-keys-v1.d" -type f -print -quit | grep -q .; then
    echo 'A private package-signing key must not be included in the live image.' >&2
    exit 1
fi
mount --bind "$root" "$root"
trap 'umount "$root" 2>/dev/null || true' EXIT
arch-chroot "$root" fastfetch --config /etc/xdg/fastfetch/config.jsonc --pipe > "$out/fastfetch-build-check.txt"
grep -q 'AikaOS 11.1' "$out/fastfetch-build-check.txt"
umount "$root"
trap - EXIT

(cd "$stage/arch/x86_64" && sha512sum -c airootfs.sha512)

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
if [[ $installer == 1 ]]; then
    sed -i 's/archisobasedir=arch/archisobasedir=arch copytoram=n/' "$stage/boot/grub/grub.cfg"
fi
grub-script-check "$stage/boot/grub/grub.cfg"

iso="$out/aikaos-11.1-x86_64-grub.iso"
[[ $installer == 0 ]] || iso="$out/aikaos-11.1-installer-dev-x86_64.iso"
grub-mkrescue -o "$iso" "$stage" -volid AIKAOS_11
(cd "$out" && sha256sum "$(basename "$iso")" > "$(basename "$iso").sha256")
xorriso -indev "$iso" -report_el_torito plain -report_system_area plain > "$out/boot-report.txt" 2>&1
printf 'Built %s\n' "$iso"
