# Beta validation

## Published image

- Version: **11.1 Beta 1**, x86_64.
- ISO size: **2,325,436,416 bytes**.
- SHA-256: `67e9a02edabc58ee082d68838499a51f7f62ecb57fc9cd4b00be749b993d405e`.
- SourceForge's server-reported SHA-256 after upload matched the local ISO exactly.
- A raw image write was checked by reading the complete written ISO range back from the USB and matching its SHA-256.
- Maintainer reported a successful physical USB live boot on **2026-11-01**, and confirmed using **Rufus ISO Image mode** to prepare the bootable USB.

These are separate checks. Rufus ISO Image mode extracts the ISO contents and can change the USB layout; the raw-write read-back checksum does not describe that extracted layout.

The physical test is a maintainer report, not an independently executed hardware test by the build assistant. It represents one successful machine, not a compatibility matrix.

## Emulator checks

KDE Plasma Wayland, the desktop wallpaper, selected Aika icons, mascot launcher, lock-screen artwork, and the supplied Fastfetch portrait were visually checked. The final test run reported no failed system services, no failed user services, and no fresh coredumps. Main, compact and full Fastfetch configurations were also run with Linux Fastfetch 2.70.0.

The TCG emulator used test-only software graphics, disabled animations, and a masked splash service in its RAM overlay. These overrides are **not in the distributed ISO**. An earlier software-rendered run suffered a KWin/Breeze crash and recovered. The final source profile restores KDE's normal splash defaults; hardware graphics behavior still needs wider community testing.

The matching kernel/initramfs from the ISO were used with the ISO attached as read-only USB storage for serial diagnostics. The hybrid boot structures and GRUB configuration were verified separately, with earlier BIOS/UEFI emulator boot checks. The maintainer subsequently confirmed physical live boot of the final image.

## Known beta limitations

- Unsigned bootloader: Secure Boot must be disabled.
- Automatic live login with an empty password and passwordless `sudo`.
- Changes are not persistent after reboot.
- German locale/keyboard and Europe/Berlin timezone are the current defaults.
- No graphical AikaOS installer; upstream `archinstall` does not preserve the live customization automatically.
- Wallpapers are natively **1672 × 941**, not native 4K. The transparent mascot logo is **1319 × 1193**.
- Hardware testing is limited; additional GPU, Wi-Fi, laptop and firmware reports are welcome.
- SHA-256 checksums are supplied; no separate GPG signature is provided in this first beta.

See [GETTING_STARTED.md](GETTING_STARTED.md) for Rufus instructions and [BUILDING.md](BUILDING.md) for build limitations.
