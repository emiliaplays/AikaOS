#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
set -euo pipefail
[[ $EUID -ne 0 ]] || { echo 'Run package compilation as an ordinary build user.' >&2; exit 1; }
repo="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
work="$repo/out/package-build/calamares"
mkdir -p "$work" "$repo/out/localrepo"
cp "$repo/packages/calamares/PKGBUILD" "$work/PKGBUILD"
(cd "$work"; makepkg --cleanbuild --force --noconfirm)
packages=("$work/"calamares-*-x86_64.pkg.tar.zst)
[[ -f ${packages[0]} && ${#packages[@]} == 1 ]] || { echo 'Expected one Calamares package.' >&2; exit 1; }
cp "${packages[@]}" "$repo/out/localrepo/"
(cd "$repo/out/localrepo"; sha256sum calamares-*-x86_64.pkg.tar.zst > SHA256SUMS)
