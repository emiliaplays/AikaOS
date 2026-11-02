# AikaOS 11.1

**Prepared for publication.** The exact final image has passed acceptance; the public ISO upload and release publication are still pending.

AikaOS 11.1 is the first installable AikaOS release: an Arch-based x86_64 desktop with KDE Plasma, Aika artwork and an offline Calamares installer.

## Included

- KDE Plasma Wayland and the Aika desktop, lock-screen, launcher, selected icons and GRUB theme.
- Calamares 3.4.3 with Aika branding, German keyboard preview and explicit target-disk confirmation.
- Offline installation to ext4, with either no swap or a 512 MiB swap file.
- Password-protected user login and sudo, locked root account and disabled SSH autostart after installation.
- Kernel/initramfs, package-provided Intel/AMD microcode images, UEFI GRUB and a fallback EFI loader.
- Firefox, Dolphin, Konsole, Kate, NetworkManager and Fastfetch with the supplied Aika portrait.

## Download and install

The release filename is **`aikaos-11.1-stable-x86_64.iso`**. Its single-file download will be hosted on SourceForge, with the checksum, build manifest, package inventory and provenance bundle attached to the GitHub release.

- Size: **2,334,775,296 bytes**.
- SHA-256: `c14421479741e7ea8de9fda50af7ea617ca451ac38f869bf36078e4710f00116`.
- Build source: `f07245344426639dab65dd5087df73ed202a208c`; Linux 7.2.14 and KDE Plasma 6.8.2.

Verify the image, then use **Rufus → ISO Image mode** to write an 8 GB or larger USB drive. Boot its **UEFI** entry with Secure Boot disabled. See the [installation guide](../../docs/INSTALLING.md) and [verification instructions](../../docs/VERIFYING.md).

The live session uses German language/keyboard and Europe/Berlin time by default. Calamares allows these choices to be changed. The live account is `aika`, with automatic login and passwordless sudo; those live settings are removed from the installed system.

## Supported scope for this release

The supported installation path is a **fresh x86_64 UEFI installation to a dedicated target disk, using ext4**. Erase-disk installation deletes the contents of the selected disk. Select the target carefully and back up files first.

8 GB RAM is recommended. Installer checks require at least 4 GiB RAM and 20 GiB storage; the complete VM installation tests used 8 GiB RAM and a 64 GiB disk. Secure Boot, legacy-BIOS installation, dual boot, encryption, hibernation and recovery procedures are not validated release paths.

## Validation and known limitations

The corrected installer profile passed a physical installation, a full 25-package update and reboot, and timed S3 suspend/resume. The exact final stable ISO passed a separate fresh KVM swap-file installation: all **33 jobs**, **29 installed checks** and **11 extended checks**, including Firefox HTTPS, password lock/unlock and installed shutdown. See [final-image acceptance](../../docs/RELEASE_VALIDATION.md) and the separate [earlier swap test](../../docs/SWAP_VALIDATION.md).

Earlier QEMU TCG tests had startup timeouts and unreliable graphics transitions. Later KVM tests passed the visible desktop/unlock flow. A live shutdown delay, optional desktop/backend warnings, old-hardware ACPI messages and earlier RA24 graphics warnings remain recorded. Discover's graphical Arch package backend is not configured; use full pacman upgrades. Read [known issues and scope](../../docs/KNOWN_ISSUES.md).

## Updates and support

Installed Arch packages use the official Arch repositories and complete `sudo pacman -Syu` upgrades. AikaOS-specific configuration changes are announced separately; see [maintenance](../../docs/MAINTENANCE.md). Report reproducible issues on [GitHub](https://github.com/emiliaplays/AikaOS/issues).

The project scripts use GPL-3.0-or-later. Bundled packages retain their licenses; artwork has separate provenance and terms. See [third-party notices](../../THIRD_PARTY.md) and [artwork information](../../ARTWORK.md).
