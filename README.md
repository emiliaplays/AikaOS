<p align="center"><img src="assets/branding/aika-logo-v2.png" width="150" alt="AikaOS mascot"></p>

<h1 align="center">AikaOS</h1>
<p align="center"><strong>An Arch-based KDE Plasma live system with an Aika identity.</strong></p>
<p align="center">11.1 Beta 1 · x86_64 · KDE Plasma · Custom GRUB · Fastfetch</p>
<p align="center"><a href="https://sourceforge.net/projects/aikaos/files/11.1-beta.1/aikaos-11.1-x86_64-grub.iso/download">Download ISO</a> · <a href="https://github.com/emiliaplays/AikaOS/releases/tag/v11.1-beta.1">Release notes</a> · <a href="docs/GETTING_STARTED.md">Create a USB with Rufus</a> · <a href="docs/BUILDING.md">Build from source</a> · <a href="https://github.com/emiliaplays/AikaOS/issues">Report a bug</a></p>

![AikaOS desktop](docs/screenshots/desktop.png)

## Meet the beta

AikaOS combines an Arch Linux base with KDE Plasma, a midnight-blue desktop, and a consistent Aika mascot. This first public beta packages the working 11.1 live image for community testing.

- **KDE Plasma on Wayland** with a dark desktop and selected Aika-themed icons.
- **Aika branding** for the launcher, system logo, avatar, desktop wallpaper, and lock screen.
- **Custom GRUB artwork** with BIOS and UEFI boot support.
- **Fastfetch 2.70.0** preinstalled with a color ASCII portrait, plus compact and full-character variants.
- **Everyday tools** including Firefox, Dolphin, Konsole, Kate, and NetworkManager.

## Download and boot

Get the single ISO from the SourceForge link in the [11.1 Beta 1 release](https://github.com/emiliaplays/AikaOS/releases/tag/v11.1-beta.1), verify its SHA-256, and write it to an **8 GB or larger USB drive using [Rufus](https://rufus.ie/en/)**. Choose **ISO Image mode** if Rufus offers an ISO/DD choice; the maintainer confirmed a successful live boot using this mode. DD Image mode is an alternative if ISO mode fails on your hardware. USB writing erases the selected drive.

Disable Secure Boot for this unsigned beta, then select the UEFI USB entry in your computer's boot menu. See the [step-by-step Rufus guide](docs/GETTING_STARTED.md).

| Release detail | Value |
| --- | --- |
| Image | `aikaos-11.1-x86_64-grub.iso` |
| Status | **Beta / prerelease** |
| Architecture | x86_64 |
| Live account | `aika` — automatic login, no password, passwordless `sudo` |
| Session defaults | German (`de_DE.UTF-8`), German keyboard, Europe/Berlin timezone |
| Persistence | Live changes are held in RAM and reset after reboot |
| Installer | `archinstall` CLI is included; no AikaOS graphical installer |

The published ISO is the existing tested 11.1 image. English documentation does not change its German session defaults. The live image's artwork and settings are not automatically transferred by a stock Arch installation.

## A closer look

| Fastfetch | Lock screen |
| --- | --- |
| ![Aika ASCII portrait in Fastfetch](docs/screenshots/fastfetch.png) | ![Aika lock screen](docs/screenshots/lockscreen.png) |

![Custom Aika GRUB menu](docs/screenshots/grub.png)

## Testing and beta scope

The image was checked in QEMU, its complete written USB image was read back and matched by SHA-256, and the maintainer reported a successful physical live boot on 1 November 2026. Hardware coverage is still limited. Review [validation details and known limitations](docs/VALIDATION.md) before reporting an issue.

This is a live beta with an intentionally open live account. It is intended for evaluation and development, rather than a hardened production deployment. It does not install to an internal drive automatically.

## Source and contributions

The repository contains the live profile, artwork, selected icons, Fastfetch configurations, and a [reference build procedure](docs/BUILDING.md). Build in an Arch Linux environment; the ISO is a release download, not a Git blob.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for useful bug reports and changes. For security concerns, see [SECURITY.md](SECURITY.md).

## Credits and licensing

Built with [Arch Linux](https://archlinux.org/), [Archiso](https://gitlab.archlinux.org/archlinux/archiso), [KDE Plasma](https://kde.org/plasma-desktop/), [GNU GRUB](https://www.gnu.org/software/grub/), and [Fastfetch](https://github.com/fastfetch-cli/fastfetch).

Build scripts and profile modifications use **GPL-3.0-or-later**. Upstream files and bundled packages retain their own licenses. Artwork and mascot branding have separate provenance and are not covered by the software license: see [ARTWORK.md](ARTWORK.md) and [THIRD_PARTY.md](THIRD_PARTY.md).
