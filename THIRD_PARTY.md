# Third-party components

AikaOS builds on Arch Linux, Archiso, KDE Plasma, GNU GRUB, Fastfetch and the other packages listed in `releases/11.1-beta.1/packages.x86_64.txt`.

The live profile originated from Archiso's `releng` profile. Archiso is GPL-3.0-or-later; its upstream license and author list are included under `third_party/archiso/`. Existing upstream notices in profile files are retained. AikaOS-specific changes add desktop packages, live-session defaults, branding and GRUB packaging.

Bundled programs, firmware, fonts, and libraries retain their individual licenses. Relevant notices are included in the installed packages, commonly under `/usr/share/licenses`. The repository's top-level software license does not relicense all contents of the ISO or the project's artwork.

Upstream source references:

- Archiso: https://gitlab.archlinux.org/archlinux/archiso
- Arch package build sources: https://gitlab.archlinux.org/archlinux/packaging/packages
- Arch source archive: https://sources.archlinux.org/
- KDE: https://invent.kde.org/
- GNU GRUB: https://www.gnu.org/software/grub/
- Fastfetch: https://github.com/fastfetch-cli/fastfetch

The exact package inventory is supplied for locating the corresponding upstream versions. This repository contains the AikaOS profile and project sources; it is not a complete mirror of every bundled package's upstream source tree.
