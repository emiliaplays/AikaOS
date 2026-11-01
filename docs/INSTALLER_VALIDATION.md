# Installer development validation

Development checks on 2026-11-01. This report is separate from the [published beta validation](VALIDATION.md). It is not stable-release approval.

## Clean baseline rebuild

The first clean build of the published repository failed because four prepopulated Arch artwork paths collided with the `filesystem` package. Commit `a631d6040233b7c05e7c5e6f30b496e4c5f2c4d4` moves these overrides into AikaOS-owned paths and applies them after package installation. It also fixes the wrapper's handling of Archiso 92's already-removed customization hook and emptied root `/boot`.

The complete fresh rebuild then passed, including package installation, initramfs generation, root filesystem compression, SHA-512 verification and GRUB hybrid packaging.

| Image | Bytes | SHA-256 |
| --- | ---: | --- |
| Clean baseline rebuild | 2,315,489,280 | `b1033593bf618a4d4e46ae459cf18c0429a2f193ff0b24986c10917312168e27` |
| First installer development build (`071b04a`) | 2,313,517,056 | `68d9bba0329954dc6f8eb745d7809f817c2cb128470d83e050bd001e5d43a0a4` |

The baseline ISO booted through its own UEFI/GRUB path into KDE Plasma Wayland without graphics overrides. Fastfetch's supplied configuration hash matched the source, the Arch-logo PNG alias matched the Aika logo, HTTPS connectivity worked, and no system services failed. The initial run had no coredumps, but KRunner and KSplash exceeded their startup timeouts under TCG emulation. KRunner subsequently started successfully with its unchanged timeout.

A second boot reproduced the KSplash timeout. Switching away from the graphical VT during Plasma startup caused repeated `plasmashell` crashes while it reported no available output. Returning to the graphical VT and restarting Plasma restored the desktop. This recovery does not erase the failure. That console-switch case remains a known issue requiring further investigation, including hardware-accelerated VM or physical-hardware comparison.

## Installer build and configuration

- Calamares 3.4.3 was built from the pinned official source archive.
- Fourteen module configurations passed the upstream release's JSON schemas.
- Job ordering, installation confirmation and installed-account defaults passed semantic checks.
- Invalid/root installation targets were rejected before any target command ran.
- The complete installer ISO build passed on a disposable Arch Linux CI container; the downloaded ISO matched its SHA-256 sidecar.
- [Build run](https://github.com/emiliaplays/AikaOS/actions/runs/41315690259). The large temporary artifact was removed after a verified local download.

## End-to-end VM installation

In progress. No successful installed-disk boot or stable-release readiness is claimed yet.

The local test uses QEMU TCG, four virtual CPUs, 6 GiB RAM, a blank 64 GiB virtual disk and a separate UEFI variable store. Host physical disks and USB devices are not attached. The image's normal KDE graphics defaults are retained. Slow startup and TCG-specific failures must be distinguished from successful installation results.
