#!/bin/bash
set -e
locale-gen
ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime
chmod 750 /etc/sudoers.d
chmod 440 /etc/sudoers.d/10-aika-live
mkinitcpio -P
cat > /usr/lib/os-release <<'EOF'
NAME="AikaOS"
PRETTY_NAME="AikaOS 11.1"
ID=aikaos
ID_LIKE=arch
VERSION_ID=11.1
BUILD_ID=live
ANSI_COLOR="38;2;0;180;255"
LOGO=aikaos-logo
EOF
ln -sf ../usr/lib/os-release /etc/os-release
test -f /usr/share/wayland-sessions/plasma.desktop
test -f /usr/share/backgrounds/aikaos/default.webp
test -x /usr/bin/sddm
test -x /usr/bin/NetworkManager
