#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Static release-profile checks; this does not claim to perform a live boot."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET

repo=Path(__file__).resolve().parent.parent
profile=repo/'profile/airootfs'
manifest=json.loads((repo/'releases/11.1-beta.1/manifest.json').read_text())
assert manifest['version']=='11.1'
assert manifest['bytes']==2325436416
assert manifest['sha256']=='67e9a02edabc58ee082d68838499a51f7f62ecb57fc9cd4b00be749b993d405e'
assert (repo/'releases/11.1-beta.1/SHA256SUMS').read_text().split()[0]==manifest['sha256']
packages=set((repo/'profile/packages.x86_64').read_text().split())
assert {'linux','plasma-meta','sddm','fastfetch','networkmanager','grub'}<=packages
assert 'fastfetch 2.70.0-1' in (repo/'releases/11.1-beta.1/packages.x86_64.txt').read_text()

links={
 'etc/systemd/system/default.target':'/usr/lib/systemd/system/graphical.target',
 'etc/systemd/system/display-manager.service':'/usr/lib/systemd/system/sddm.service',
 'etc/systemd/system/multi-user.target.wants/NetworkManager.service':'/usr/lib/systemd/system/NetworkManager.service',
}
for name,target in links.items():
    path=profile/name
    actual=str(path.readlink()) if path.is_symlink() else path.read_text()
    assert actual==target,(name,actual)
assert not (profile/'home/aika/.config/ksplashrc').exists()
assert not (profile/'etc/skel/.config/ksplashrc').exists()
assert not (profile/'etc/environment.d/90-qemu-test.conf').exists()
assert not (profile/'etc/systemd/user/plasma-ksplash.service').is_symlink()
desktop=(profile/'home/aika/.config/kdeglobals').read_text()
assert 'Theme=Aika' in desktop and 'AnimationDurationFactor=0' not in desktop
assert 'LOGO=aikaos-logo' in (profile/'etc/os-release').read_text()
assert 'lockscreen.png' in (profile/'home/aika/.config/kscreenlockerrc').read_text()
grub=(repo/'assets/grub/grub.cfg').read_text()
assert 'cow_spacesize=50%' in grub and 'systemd.condition_first_boot=no' in grub
assert 'debug_shell' not in grub and 'systemd.unit=' not in grub
source=(repo/'assets/fastfetch/config.jsonc').read_bytes()
assert hashlib.sha256(source).hexdigest()==manifest['fastfetch_config_sha256']
for name in ('config.jsonc','config-compact.jsonc','config-full.jsonc'):
    supplied=(repo/'assets/fastfetch'/name).read_bytes()
    cfg=json.loads(supplied)
    assert cfg['logo']['type']=='data-raw'
    assert all(isinstance(m,str) and m.lower()!='command' for m in cfg['modules'])
    for dest in ('home/aika/.config/fastfetch','etc/skel/.config/fastfetch','etc/xdg/fastfetch','usr/share/aikaos/fastfetch'):
        assert (profile/dest/name).read_bytes()==supplied
icons=list((profile/'usr/share/icons/Aika/scalable').rglob('*.svg'))
assert len(icons)>=20
for icon in icons: ET.parse(icon)
for file in ('usr/share/backgrounds/aikaos/desktop.png','usr/share/backgrounds/aikaos/lockscreen.png','usr/share/pixmaps/aikaos-logo.png'):
    assert (profile/file).stat().st_size>10000
for name in ('archlinux-logo.svg','archlinux-logo-text.svg','archlinux-logo-text-dark.svg','archlinux-logo.png'):
    assert not (profile/'usr/share/pixmaps'/name).exists(), 'Package-owned artwork must be applied after pacstrap'
    assert (profile/'usr/share/aikaos/branding/arch-aliases'/name).is_file()
assert 'Target = filesystem' in (profile/'etc/pacman.d/hooks/95-aika-branding.hook').read_text()

# Scan tracked files when available, otherwise the prepared checkout. Never
# traverse ignored build outputs or Git's internal storage.
if (repo/'.git').exists():
    names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=repo,text=True).splitlines()
    paths=[repo/p for p in names if (repo/p).exists() or (repo/p).is_symlink()]
else:
    paths=[p for p in repo.rglob('*') if p.is_file() and not ({'.git','build','out'} & set(p.relative_to(repo).parts))]
for path in paths:
    if path.is_symlink():continue
    assert path.suffix.lower() not in {'.iso','.qcow2','.vdi','.vmdk','.pem','.key'},path
    assert path.name not in {'id_ed25519','id_rsa','.env'},path
    data=path.read_bytes()
    if b'\0' in data:continue
    text=data.decode('utf-8')
    assert not re.search(r'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----',text),path
    assert ('C:'+'\\Users\\Familie') not in text,path
    assert ('C:'+'/Users/Familie') not in text,path
    assert ('100522'+'11001471') not in text,path
    supplied_fastfetch='fastfetch' in path.parts and path.suffix in {'.jsonc','.txt'}
    assert supplied_fastfetch or b'\r\n' not in data,path
print(f'Validated live profile, {len(icons)} icons, supplied Fastfetch layouts and public-file hygiene.')
