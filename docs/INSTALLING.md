# Install AikaOS 11.1

This guide covers a fresh **x86_64 UEFI/ext4 installation to a dedicated target disk**. Manual partitioning, Windows dual boot, encryption and legacy-BIOS installation are outside the validated release scope.

## Prepare the USB

1. Download `aikaos-11.1-stable-x86_64.iso` from the official GitHub release's SourceForge link.
2. Follow [VERIFYING.md](VERIFYING.md) to check its SHA-256 and optional build-provenance attestation.
3. Open [Rufus](https://rufus.ie/en/) on Windows. Select the intended **8 GB or larger USB drive** and the exact stable ISO filename.
4. Start writing. If Rufus asks, choose **ISO Image mode**. Writing erases the selected USB drive.
5. In the computer's boot menu, choose the USB's **UEFI** entry. Secure Boot must be disabled for this image.

## Run the installer

1. Reach the Aika live desktop. The live account is `aika`, with no password and passwordless sudo. Live changes are temporary.
2. Open **Install AikaOS**. The terminal command `install-aikaos` opens the same installer wrapper.
3. Choose language, timezone and keyboard. The initial defaults are German and Europe/Berlin.
4. Select the intended target disk. For the validated path, choose **Erase disk**. This removes that disk's existing data; back it up first.
5. Choose **No swap** or **Use a swap file**. The swap-file option creates a private 512 MiB `/swapfile` that is enabled at boot. Hibernation is not a validated feature.
6. Create your normal user and password. Review the complete disk summary and final confirmation before starting.
7. Wait for completion. Shut down, remove the installer USB and start from the internal disk.
8. Log in with the password you created. The live account, live automatic login, passwordless sudo and installer are removed from the installed system. SSH is disabled by default.

8 GB RAM is recommended. The installer checks for at least 4 GiB RAM and 20 GiB storage; tested VM installations used 8 GiB RAM and a 64 GiB disk.

## First installed boot

Connect to the Internet and perform a full update:

```sh
sudo pacman -Syu
```

Reboot after a kernel update. Updates can replace the kernel, firmware and libraries independently of the ISO's release number. Read [MAINTENANCE.md](MAINTENANCE.md) and the [known issues](KNOWN_ISSUES.md).

For an issue report, include the AikaOS version, ISO checksum, CPU/GPU, UEFI boot mode and steps to reproduce. Omit passwords, private keys and personal files.
