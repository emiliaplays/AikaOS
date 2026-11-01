# Create an AikaOS USB with Rufus

## 1. Download the ISO

Open the [11.1 Beta 1 release](https://github.com/emiliaplays/AikaOS/releases/tag/v11.1-beta.1) and follow its **Download ISO on SourceForge** link. Download the complete `aikaos-11.1-x86_64-grub.iso` file. It is a single ISO; no joining or extraction is required.

The release also provides a SHA-256 file. In PowerShell, run:

```powershell
Get-FileHash .\aikaos-11.1-x86_64-grub.iso -Algorithm SHA256
```

Expected SHA-256:

```text
67e9a02edabc58ee082d68838499a51f7f62ecb57fc9cd4b00be749b993d405e
```

The ISO is **2,325,436,416 bytes**. A checksum confirms file integrity; this beta does not include a separate GPG signature.

## 2. Write it using Rufus

1. Download Rufus from its official website: **https://rufus.ie/en/**.
2. Insert an **8 GB or larger USB drive** and back up anything you need from it.
3. Open Rufus and select that USB under **Device**. Writing will erase the selected drive.
4. Under **Boot selection**, choose **Disk or ISO image**, click **SELECT**, and open the AikaOS ISO.
5. Click **START**. If prompted to choose between ISO and DD mode, select **Write in ISO Image mode (Recommended)**. The maintainer confirmed a successful physical live boot with Rufus ISO Image mode.
6. Wait until Rufus reports **READY**, then safely eject the USB.

Do not select a split file, a source archive, or a checksum file in Rufus. The boot image is the `.iso` file. Windows may not recognize the Linux/hybrid partitions after writing; do not format the stick again when Windows offers to do so.

If the USB does not boot on your hardware, verify the downloaded ISO's checksum and the selected firmware boot entry first. You can then rewrite the USB using **DD Image mode** as an alternative; this copies the hybrid image directly and erases the USB again.

References: [Rufus FAQ](https://github.com/pbatard/rufus/wiki/FAQ), [ArchWiki USB installation media](https://wiki.archlinux.org/title/USB_flash_installation_medium).

## 3. Boot the live session

1. Disable **Secure Boot** in firmware settings; the beta's GRUB loader is unsigned.
2. Restart and open your computer's boot-device menu.
3. Choose the **UEFI USB** entry. The image also includes legacy BIOS boot support.
4. Select the AikaOS live entry in GRUB.

The account `aika` logs in automatically. It has no password and can use `sudo` without a password. The default language and keyboard are German; change them in KDE System Settings if needed.

## Fastfetch

Open Konsole, enlarge the window for the portrait, and run:

```sh
fastfetch
```

Alternative layouts:

```sh
fastfetch --config /etc/xdg/fastfetch/config-compact.jsonc
fastfetch --config /etc/xdg/fastfetch/config-full.jsonc
```

## Live-system behavior

Changes are stored in RAM and disappear after reboot. The live image does not automatically install AikaOS to an internal disk. The included `archinstall` command is the upstream Arch CLI; it is not an AikaOS-branded installation wizard and does not copy this live desktop's customizations automatically.

For a boot failure, report the selected boot mode, whether Secure Boot is disabled, Rufus's write mode, the ISO checksum, and the exact error message in a [bug report](https://github.com/emiliaplays/AikaOS/issues/new?template=bug_report.yml).
