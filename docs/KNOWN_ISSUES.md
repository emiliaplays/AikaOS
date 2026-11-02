# AikaOS 11.1 scope and known observations

The validated installation path is x86_64 **UEFI, a dedicated target disk and ext4**, with no swap or the installer's swap-file option. KDE Plasma Wayland is the default session. Validation is a set of recorded tests, not certification of every device.

## Untested release paths

- Secure Boot is unsupported; use UEFI with Secure Boot disabled.
- Legacy-BIOS installation, Windows dual boot, custom/manual layouts, encryption, hibernation and recovery procedures have not passed release acceptance tests.
- Wi-Fi, Bluetooth and proprietary NVIDIA configurations are not covered by the current hardware test matrix.
- Tests used 8 GiB VM RAM and physical systems with approximately 24/32 GiB. Lower-memory configurations have not received equivalent end-to-end coverage.

## Graphics and virtual machines

Early QEMU **TCG** runs had KSplash timeouts, graphics stalls and unreliable visual unlock transitions. A later **KVM** installation passed startup, normal password lock/unlock, all 29 installed/swap checks and 11 extended checks without guest desktop graphics overrides. TCG is not an accepted first-release desktop test configuration.

The older development kernel logged RA24 messages during startup on the RX 580 test PC, despite a functioning accelerated desktop. After a full installed update to kernel 7.2.14, the observed boot and resume logged none. This does not establish a universal fix. The maintainer also reported pre-existing GPU faults and a monitor-reconnect incident; its cause was not independently diagnosed.

## Power and boot messages

One timed physical S3 suspend/resume succeeded, including password unlock and post-resume file/network checks. The same resume logged ACPI `_GTF.DSSP` / `AE_NOT_FOUND` messages on the older Intel platform. These messages remain recorded even though the tested functions worked.

Initramfs generation can warn about an unconfigured console font and firmware for additional fallback drivers. Both generated images and installed boot passed the recorded tests.

The final-image live VM shutdown delayed at a Plasma/user-manager stop timeout while the diagnostic daemon belonged to that session. With diagnostics moved to a separate transient system unit, the installed VM shut down promptly. The fixture difference prevents assigning a definite cause; the observed live delay remains recorded. See [final-image acceptance](RELEASE_VALIDATION.md).

## Desktop integrations and package management

Use `sudo pacman -Syu` for supported Arch package updates. Discover's PackageKit backend is not configured in this image; its notifier logged a missing `libpackagekitqt6.so.2`. Graphical Arch package installation/updates through Discover are not a validated release feature.

The VM journal also included optional-service/virtual-hardware warnings and a transient D-Bus-activated KSplash exit-code result. The main splash service succeeded, the desktop and lock/unlock worked, and no failed units or guest coredumps remained at the acceptance audit. These results do not mean the journal is warning-free.

## Evidence

- [Installer and earlier VM results](INSTALLER_VALIDATION.md)
- [Physical installation and microcode correction](HARDWARE_VALIDATION.md)
- [Full installed update, reboot and timed suspend](UPDATE_VALIDATION.md)
- [Actual Calamares swap-file installation](SWAP_VALIDATION.md)
- [Final stable-image acceptance](RELEASE_VALIDATION.md)

Report additional reproducible issues at [GitHub](https://github.com/emiliaplays/AikaOS/issues).
