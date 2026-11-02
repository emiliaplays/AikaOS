# Installed-system update and suspend validation

Tests on 2026-11-02 used the freshly installed, microcode-corrected `da8120f` image on the Intel Core i7-2600K / Radeon RX 580 UEFI test system described in [hardware validation](HARDWARE_VALIDATION.md). The audit was performed over SSH. Raw logs, machine identities, account details and network addresses remain private.

## Full system upgrade and reboot

A complete `pacman -Syu` transaction upgraded **25 packages**, including the kernel, AMD microcode, Linux firmware and Qt declarative libraries. Package signature/integrity and conflict checks passed. The transaction and both default/fallback initramfs builds completed successfully with exit status 0.

The initial Fastly download was slow and was interrupted while still retrieving packages, before package changes began. The full upgrade was resumed using a temporary pacman configuration pointing to the [official Berlin Arch mirror](https://archlinux.org/mirrors/geo.mirror.pkgbuild.com/2228/). The normal pacman configuration, mirror list and signature policy were preserved. The temporary configuration was removed after testing.

| Component | Result |
| --- | --- |
| Kernel | Upgraded from `7.2.11-arch1-1` to `7.2.14-arch1-1`; the new version was verified running after reboot |
| AMD microcode | Upgraded to `20261019-1`; installed image matched the corresponding cached package payload |
| Intel microcode | `20260925-1`; early revision update from `0x28` to `0x2f` remained present |
| Linux firmware | Upgraded to `20261019-1` |
| Qt declarative | Upgraded to `6.12.0-4` |
| Boot configuration | Valid GRUB syntax, both microcode images included in default/fallback entries, installed kernel matching `/boot/vmlinuz-linux` |
| Branding | Every recorded artwork and user-configuration hash unchanged, including the exact supplied Fastfetch configuration |

Before reboot, the running old kernel no longer had its old on-disk modules after the kernel package replacement. This was recorded as a pending-reboot condition. After reboot the running kernel and its modules matched, and all six boot/package checks passed.

The reboot changed the boot ID while preserving the machine identity. The system again booted from the internal ext4 disk without an installation medium. SSH returned, the maintainer logged into KDE, and the audit confirmed an active Plasma Wayland session with accelerated Radeon OpenGL ES rendering and no global software-rendering override.

| Checkpoint | Installation checks | Extended system checks |
| --- | ---: | ---: |
| Before upgrade | 24/25 | 11/11 |
| After upgrade, before reboot | 24/25 | 11/11 |
| After reboot and desktop login | 24/25 | 11/11 |
| After suspend/resume | 24/25 | 11/11 |

The sole installation-check difference was the maintainer's intentionally enabled SSH service. At every checkpoint there were no failed system/user services or coredumps. Package database/file checks, DNS, HTTPS, the audio graph, fstab, Fastfetch, Aika assets and the disposable user-file round trip passed. KSplash completed successfully after the new-kernel boot.

## Timed suspend and resume

An otherwise unused RTC alarm was set for 35 seconds, the temporary sleep inhibitor was stopped, and normal `systemctl suspend` was requested. The kernel recorded **deep suspend / ACPI S3 entry and exit**. The suspend service returned `Result=success` and exit status 0.

After recovery, the boot ID was unchanged. The difference between boot-time and monotonic clocks increased by approximately **35.874 seconds**, independently confirming a real suspension rather than a reboot. A new SSH connection worked after the original connection was lost. The Wayland session, accelerated renderer, network, package integrity and user-file write/read/fsync check remained functional.

The maintainer confirmed seeing the Aika lock screen and personally unlocking it with the account password after the test. This supplies the visual/authentication evidence that an SSH state query alone cannot provide.

## Additional smoke tests

- A disposable **256 MiB swap file** was allocated on ext4, initialized and successfully activated. It appeared in the active swap inventory, was deactivated and removed. No persistent swap or fstab entry was created. This verifies runtime swap support, **not Calamares' offered swap-file installation path**.
- After the upgrade, Firefox ran as the normal user in its documented [headless screenshot mode](https://firefox-source-docs.mozilla.org/browser/CommandLineParameters.html), with a separate disposable profile. It loaded `https://archlinux.org/`, returned exit status 0 and produced a 1280 × 800 image showing the expected page. This is a browser startup/network/render smoke test, not a visual test of Firefox's normal Wayland window or GPU acceleration.

## Messages retained and coverage limits

The initramfs builds warned about the unconfigured console font and missing firmware for additional fallback modules. Both images nevertheless completed and the resulting kernel boot was verified.

The updated boot and subsequent resume had **zero RA24 messages**, compared with the earlier startup bursts. This is one observed updated boot; it does not prove a general fix or establish the cause of the earlier warnings. The old Intel platform's unsupported TDX capability message remained.

Resume also logged four ACPI error lines concerning the SATA `_GTF.DSSP` symbol and `AE_NOT_FOUND`. The suspend service and post-resume I/O checks passed. These firmware-method errors are retained as an unresolved observation rather than treating the log as error-free. The earlier TCG VM graphics failures remain outside this hardware test.

The RTC alarm, test swap, disposable Firefox profile, uploaded temporary helper and temporary package configuration were removed. The temporary sleep inhibitor was released, and the maintainer's SSH setting was preserved. Private reports and ordinary package-cache files were retained.

These results cover this physical system's installed upgrade, reboot and one S3 cycle. They do not validate hibernation, other hardware, BIOS installation, dual boot, encryption or recovery. The installer's swap option was subsequently verified in a [separate complete KVM installation](SWAP_VALIDATION.md). The downloaded ISO itself was not rebuilt or modified by this test; its kernel snapshot remains separate from the subsequently updated installation.
