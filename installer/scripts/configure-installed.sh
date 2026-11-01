#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Called in the mounted target chroot by the guarded AikaOS Calamares module.
set -euo pipefail
[[ -f /usr/share/aikaos/os-release ]] || { echo 'AikaOS target identity is missing.' >&2; exit 1; }

case ${1:-} in
prepare)
    # Remove the live session's empty-password login and transient keyring units.
    for unit in pacman-init.service choose-mirror.service livecd-alsa-unmuter.service livecd-talk.service etc-pacman.d-gnupg.mount; do
        systemctl disable "$unit" 2>/dev/null || true
        rm -f -- "/etc/systemd/system/$unit" "/etc/systemd/system/multi-user.target.wants/$unit"
    done
    rm -f -- /etc/sudoers.d/10-aika-live /etc/sddm.conf.d/10-aikaos.conf \
        /etc/systemd/system/getty@tty1.service.d/autologin.conf \
        /etc/systemd/system-generators/systemd-gpt-auto-generator \
        /etc/systemd/logind.conf.d/do-not-suspend.conf \
        /etc/systemd/journald.conf.d/volatile-storage.conf \
        /etc/ssh/sshd_config.d/10-archiso.conf \
        /etc/mkinitcpio.conf.d/archiso.conf /root/.automated_script.sh /root/.zlogin
    usermod --lock root

    # These tools belong to the live image. All removal is offline.
    remove_packages=()
    for package in calamares mkinitcpio-archiso archinstall; do
        pacman -Q "$package" >/dev/null 2>&1 && remove_packages+=("$package")
    done
    if ((${#remove_packages[@]})); then pacman -R --noconfirm "${remove_packages[@]}"; fi

    # Archiso deliberately strips /boot from its root image. Restore the kernel
    # before Calamares generates an installed-system initramfs and GRUB menu.
    mapfile -t kernels < <(find /usr/lib/modules -mindepth 2 -maxdepth 2 -name vmlinuz -type f)
    ((${#kernels[@]} == 1)) || { echo 'Expected exactly one installed Linux kernel.' >&2; exit 1; }
    install -m 0644 "${kernels[0]}" /boot/vmlinuz-linux
    install -d /etc/mkinitcpio.d
    cat > /etc/mkinitcpio.d/linux.preset <<'EOF'
ALL_kver="/boot/vmlinuz-linux"
PRESETS=('default' 'fallback')
default_image="/boot/initramfs-linux.img"
fallback_image="/boot/initramfs-linux-fallback.img"
fallback_options="-S autodetect"
EOF
    # A regular /etc/os-release survives updates of Arch's filesystem package.
    rm -f -- /etc/os-release
    install -m 0644 /usr/share/aikaos/os-release /etc/os-release
    if [[ -f /etc/skel/.config/kscreenlockerrc ]]; then
        sed -i 's/^Autolock=false$/Autolock=true/' /etc/skel/.config/kscreenlockerrc
    fi
    install -m 0644 /usr/share/pixmaps/aikaos-logo.png /etc/skel/.face.icon
    cat > /etc/default/grub <<'EOF'
GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="AikaOS"
GRUB_CMDLINE_LINUX_DEFAULT="quiet"
GRUB_CMDLINE_LINUX=""
GRUB_GFXMODE=auto
GRUB_GFXPAYLOAD_LINUX=keep
GRUB_THEME="/usr/share/grub/themes/aikaos/theme.txt"
GRUB_DISABLE_OS_PROBER=true
EOF
    install -d -m 0755 /var/lib/aikaos
    printf 'prepared\n' > /var/lib/aikaos/installation-state
    ;;
finalize)
    [[ $(cat /var/lib/aikaos/installation-state) == prepared ]]
    usermod --lock root
    ! test -e /etc/sudoers.d/10-aika-live
    ! test -e /etc/sddm.conf.d/10-aikaos.conf
    test -s /boot/vmlinuz-linux
    test -s /boot/initramfs-linux.img
    test -s /boot/grub/grub.cfg
    # SDDM cannot read an avatar inside a private (0700) home directory.
    install -d -m 0755 /usr/share/sddm/faces
    while IFS=: read -r account _ uid _; do
        if ((uid >= 1000 && uid < 65534)); then
            install -m 0644 /usr/share/pixmaps/aikaos-logo.png "/usr/share/sddm/faces/$account.face.icon"
        fi
    done < /etc/passwd
    # Initialize a distinct package trust database for this installation.
    pacman-key --init
    pacman-key --populate archlinux
    systemctl set-default graphical.target
    rm -f -- /usr/share/applications/aikaos-installer.desktop /usr/local/bin/install-aikaos
    rm -rf -- /etc/calamares /usr/lib/calamares/modules/aikaos
    printf 'complete\n' > /var/lib/aikaos/installation-state
    rm -f -- /usr/local/lib/aikaos/configure-installed.sh
    ;;
*) echo 'Expected prepare or finalize.' >&2; exit 2 ;;
esac
