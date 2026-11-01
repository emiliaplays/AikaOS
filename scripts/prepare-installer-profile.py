#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Stage the optional installer into a disposable Archiso profile copy."""
from pathlib import Path
import argparse
import shutil
import subprocess

repo = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--profile', required=True, type=Path)
args = parser.parse_args()
profile = args.profile.resolve()
profile.relative_to((repo / 'build').resolve())
assert profile.is_dir() and profile != (repo / 'build').resolve()
root = profile / 'airootfs'
source = repo / 'installer'

shutil.copytree(source / 'calamares', root / 'etc/calamares', dirs_exist_ok=True)
shutil.copytree(source / 'module/aikaos', root / 'usr/lib/calamares/modules/aikaos', dirs_exist_ok=True)
branding = root / 'etc/calamares/branding/aikaos'
shutil.copy2(repo / 'assets/branding/aika-logo-v2.png', branding / 'aika-logo.png')
shutil.copy2(repo / 'assets/branding/aika-desktop.png', branding / 'wallpaper.png')
copies = {
    'scripts/install-aikaos': 'usr/local/bin/install-aikaos',
    'scripts/configure-installed.sh': 'usr/local/lib/aikaos/configure-installed.sh',
    'aikaos-installer.desktop': 'usr/share/applications/aikaos-installer.desktop',
}
for original, destination in copies.items():
    path = root / destination
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / original, path)
desktop = root / 'home/aika/Desktop/Install-AikaOS.desktop'
desktop.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(source / 'aikaos-installer.desktop', desktop)
user_dirs = root / 'home/aika/.config/user-dirs.dirs'
user_dirs.write_text('XDG_DESKTOP_DIR="$HOME/Desktop"\n', encoding='utf-8')

identity = '''NAME="AikaOS"
PRETTY_NAME="AikaOS 11.1 Development"
ID=aikaos
ID_LIKE=arch
VERSION_ID=11.1
BUILD_ID=installer-dev
ANSI_COLOR="38;2;0;180;255"
LOGO=aikaos-logo
HOME_URL="https://github.com/emiliaplays/AikaOS"
SUPPORT_URL="https://github.com/emiliaplays/AikaOS/issues"
'''
(root / 'usr/share/aikaos/os-release').write_text(identity, encoding='utf-8')
# Keep the build-only local package repository out of the running system.
shutil.copy2(repo / 'profile/pacman.conf', root / 'etc/pacman.conf')
os_release = root / 'etc/os-release'
if os_release.is_symlink():
    os_release.unlink()
os_release.write_text(identity, encoding='utf-8')

# Use a one-time ALPM hook instead of Archiso's deprecated root shell hook.
customize = root / 'root/customize_airootfs.sh'
if customize.exists():
    customize.unlink()
customizer = root / 'usr/local/lib/aikaos/customize-live.sh'
customizer.write_text('''#!/bin/bash
set -euo pipefail
locale-gen
ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime
chmod 750 /etc/sudoers.d
chmod 440 /etc/sudoers.d/10-aika-live
install -m 0644 /usr/share/aikaos/os-release /etc/os-release
test -f /usr/share/wayland-sessions/plasma.desktop
test -x /usr/bin/sddm
test -x /usr/bin/calamares
rm -f /usr/local/lib/aikaos/customize-live.sh
''', encoding='utf-8')
(root / 'etc/pacman.d/hooks/99-aika-live.hook').write_text('''# remove from airootfs
[Trigger]
Operation = Install
Type = Package
Target = filesystem
[Action]
Description = Configuring the AikaOS live session...
When = PostTransaction
Depends = bash
Depends = glibc
Exec = /bin/bash /usr/local/lib/aikaos/customize-live.sh
''', encoding='utf-8')

theme = root / 'usr/share/grub/themes/aikaos'
theme.mkdir(parents=True, exist_ok=True)
for name in ('background.png', 'theme.txt'):
    shutil.copy2(repo / 'assets/grub' / name, theme / name)
(theme / 'theme.txt').write_text(
    (theme / 'theme.txt').read_text().replace('KDE PLASMA  /  LIVE SYSTEM', 'KDE PLASMA  /  AIKAOS'),
    encoding='utf-8',
)
for size in (18, 24):
    subprocess.run(['grub-mkfont', '-s', str(size), '-o', str(theme / f'aika{size}.pf2'), '/usr/share/fonts/TTF/DejaVuSans.ttf'], check=True)

skel_lock = root / 'etc/skel/.config/kscreenlockerrc'
skel_lock.write_text(skel_lock.read_text().replace('Autolock=false', 'Autolock=true'), encoding='utf-8')
shutil.copy2(repo / 'assets/branding/aika-logo-v2.png', root / 'etc/skel/.face.icon')
packages = profile / 'packages.x86_64'
packages.write_text('\n'.join(sorted(set(packages.read_text().split()) | {'calamares'})) + '\n', encoding='utf-8')
definition = profile / 'profiledef.sh'
definition.write_text(definition.read_text().replace('iso_version="11.1"', 'iso_version="11.1-installer-dev"') + '''
file_permissions+=(
  ["/usr/local/bin/install-aikaos"]="0:0:755"
  ["/usr/local/lib/aikaos/configure-installed.sh"]="0:0:755"
  ["/home/aika/Desktop/Install-AikaOS.desktop"]="1000:1000:755"
)
''', encoding='utf-8')
print('Staged AikaOS installer, branding, offline installation jobs and installed-user defaults.')
