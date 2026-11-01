# Installer development

The `feature/calamares-installer` branch adds an optional offline Calamares installer. The existing 11.1 Beta 1 release remains a live-only image. Do not use development images on a disk containing data you need.

## Design and installation behavior

- Aika mascot, wallpaper, navy/cyan styling and English/German slideshow.
- Explicit partition selection and a final installation confirmation.
- The compressed root filesystem is read from the attached installation medium; an Internet connection is not required to unpack it.
- A new normal user, password-based `sudo`, locked root account and SDDM login. Live automatic login and passwordless `sudo` are removed.
- Installed kernel, regenerated initramfs, Aika GRUB theme, fresh machine identity and per-installation package keyring.
- The installer and live-only setup tools are removed from the installed system.

The Aika setup module checks that Calamares has a mounted block-device target and runs its setup script inside that target's chroot. It refuses `/` and invalid targets. This guard complements Calamares' partition confirmation; it is not a substitute for backups or disk selection.

## Pinned upstream source

Calamares **3.4.3** is built from its official Codeberg source archive, pinned by SHA-256 in [`packages/calamares/PKGBUILD`](../packages/calamares/PKGBUILD). This is an AikaOS-maintained build recipe, not an official Arch repository package. Its source license and notices remain included. Only the required installer modules are compiled.

The package also includes the standalone `ckbcomp` keyboard-preview helper from Debian console-setup **1.249**, pinned to the official Debian source archive and its SHA-256. Its GPL-2.0-or-later copyright notice is included separately. Debian's console configuration is not installed. The ISO build checks that the helper generates a German keymap.

A small tracked patch makes the partition labels follow the Qt text palette instead of using black on the dark Aika background. The patch is included alongside the package recipe and checked by SHA-256.

## Build on Arch Linux

Use a Linux checkout with symbolic links and executable modes preserved. Install the normal ISO build dependencies described in [BUILDING.md](BUILDING.md), plus the package's `depends` and `makedepends` from its PKGBUILD. `python-yaml` and `python-jsonschema` are required for configuration validation.

Build the package as a regular user:

```sh
bash scripts/build-packages.sh
python3 tests/test-installer-guard.py
python3 scripts/validate-installer.py --upstream out/package-build/calamares/src/calamares
```

Then build a new ISO as root:

```sh
sudo env AIKAOS_INSTALLER=1 bash scripts/build.sh
```

The result is `out/aikaos-11.1-installer-dev-x86_64.iso`, with a SHA-256 sidecar and boot report. The script refuses to reuse `build/`; deliberately rename or remove your previous build first. The locally built package repository is used only during image construction and is not added to the running or installed system.

The `Build installer development ISO` workflow performs the same steps on a disposable Arch Linux container. Downloadable workflow artifacts expire after one day. A successful build is not an installation test.

## VM acceptance criteria

Use a new disposable virtual disk and separate UEFI variable store. Never pass physical host disks through to this test VM.

1. Boot the complete ISO through its own GRUB/UEFI path.
2. Check the installer launcher, Aika UI, keyboard, locale and disk summary.
3. Install onto the blank virtual disk and inspect all job results.
4. Shut down, detach the ISO, and boot the installed disk.
5. Log in through SDDM; verify KDE, Fastfetch, wallpaper, lock screen and network access.
6. Verify the root lock, normal user/sudo setup, enabled services, regenerated initramfs, unique machine identity and removal of live defaults.
7. Check failed services and coredumps, then perform an update/reboot test.

Physical hardware, dual boot, encryption, BIOS installation and recovery paths require separate tests before they can be advertised as supported. Secure Boot remains unsupported.
