#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
set -eu
for artwork in /usr/share/aikaos/branding/arch-aliases/archlinux-logo*; do
    [ -f "$artwork" ] || continue
    install -m 0644 "$artwork" "/usr/share/pixmaps/${artwork##*/}"
done
