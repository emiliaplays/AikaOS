# Changelog

## Unreleased — installer development

- Fixed clean Archiso builds, package-owned artwork collisions and handling of Archiso's staged boot files.
- Added a pinned Calamares 3.4.3 package recipe and native Arch CI package build.
- Added an optional Aika-themed offline installer, guarded target configuration and installed-user defaults.
- Added upstream configuration-schema checks and invalid-target regression checks.
- Added a separate development ISO workflow; the published beta image is unchanged.
- Completed an offline UEFI VM installation, password login and signed-package update/branding checks; recorded remaining TCG graphics failures separately.
- Added German keyboard previews, readable dark partition labels, installer sleep inhibition and removal of the live login hint from installed systems.

## 11.1 Beta 1 — 2026-11-01

First public beta of the tested AikaOS 11.1 live image.

### Included

- Arch-based x86_64 live system with KDE Plasma Wayland and SDDM automatic login.
- Aika mascot for system branding, launcher and live-user avatar.
- Selected Aika-themed icons with Breeze inheritance.
- New desktop and lock-screen artwork based on the supplied Aika design.
- Custom Aika GRUB theme and hybrid BIOS/UEFI boot configuration.
- Fastfetch 2.70.0 with the supplied color portrait configuration as the default; compact and full variants included.
- NetworkManager, Firefox, Dolphin, Konsole, Kate and desktop utilities.

### Final image adjustments

- Live writable overlay limit set to 50% of RAM.
- Interactive systemd first-boot setup disabled for the live image.
- KDE splash override removed to restore valid upstream defaults.
- Full USB image read-back verified against the release ISO's SHA-256.

See [validation and limitations](docs/VALIDATION.md). The live defaults are German; repository documentation is English.
