# Changelog

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
