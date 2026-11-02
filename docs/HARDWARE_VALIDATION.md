# Installed-system hardware validation

Physical tests performed by the maintainer and audited over SSH on 2026-11-01 and 2026-11-02. This is separate from the [VM installation report](INSTALLER_VALIDATION.md). Raw diagnostic logs, account names, network addresses and credentials are not published.

## Test system

| Component | Observed configuration |
| --- | --- |
| CPU | Intel Core i7-2600K, 4 cores / 8 threads |
| GPU | AMD Radeon RX 580 / Polaris, amdgpu + radeonsi |
| RAM | Approximately 32 GiB |
| Storage | 111.8 GiB SATA SSD; 512 MiB FAT32 EFI partition and ext4 root |
| Boot/session | UEFI, installed root on `/dev/sda2`, KDE Plasma Wayland |
| Software | AikaOS 11.1 Development, Linux 7.2.11-arch1-1, Plasma 6.8.2, Mesa 26.2.6 |

The installed disk and firmware boot entries were inspected without changing partitions. No installation medium was mounted. The exact original ISO checksum was not recorded on the test PC.

## Initial results

All **24 original installed-system acceptance checks passed**, including password-protected sudo, locked root, removal of live defaults, boot files, Aika branding, the exact supplied Fastfetch configuration, private user home, enabled desktop/network services and disabled SSH autostart. SSH was running manually for this audit.

There were no failed system/user services or coredumps at the initial checkpoint. KSplash returned `Result=success` and exit status 0. KWin reported active hardware-accelerated OpenGL ES rendering on the Radeon GPU, with no VM-specific graphics overrides.

Ten of eleven additional checks passed: fstab validation, desktop package presence, Fastfetch execution, KWin and audio graph responses, Aika assets, DNS, HTTPS, package database consistency and a disposable user-home write/read/fsync test. The remaining package-file check exposed the microcode-image issue described below.

The maintainer separately confirmed that Firefox/web browsing, audio playback and screen locking/unlocking all worked. These are human-observed functional results, not claims inferred from an active process.

## Microcode package-file correction

`pacman -Qk` found exactly two missing package-owned files: `/boot/amd-ucode.img` and `/boot/intel-ucode.img`. Archiso clears `/boot` in its compressed root, and the installer previously restored the kernel but not these two images.

This did **not** mean early CPU microcode was absent: `lsinitcpio --early` found `GenuineIntel.bin` inside the installed initramfs, and the kernel reported a successful early microcode update. Arch's [mkinitcpio microcode hook](https://archlinux.org/news/mkinitcpio-hook-migration-and-early-microcode/) embeds that firmware in the combined initramfs.

A full repository synchronization/upgrade transaction found no pending version upgrades and reinstalled both signed microcode packages. Both default and fallback initramfs images were regenerated successfully. GRUB configuration was backed up, regenerated and checked with `grub-script-check`; its default and fallback entries now include both package-provided images. No partition or firmware boot entry was changed.

Source commit `da8120f` preserves the original package-provided images in the installer filesystem before Archiso cleanup, verifies their checksums and restores them to the installed `/boot`. It also adds a 25th acceptance check and a build-time payload check. The [complete clean ISO build passed](https://github.com/emiliaplays/AikaOS/actions/runs/41336768728), including its microcode payload check. The large temporary CI artifact was deleted after its verified local download.

| Corrected development image | Value |
| --- | --- |
| Source | `da8120f6ed49978433aaf4533ddfcac39ed28c1a` |
| Filename | `aikaos-11.1-installer-dev-x86_64.iso` |
| Bytes | 2,328,059,904 |
| SHA-256 | `d2f0abcf3396ebc8e6ce8d3817f703b1e0c30dac1f036622a50fd6abb5effe3b` |

The downloaded ISO was copied to the test PC and its complete SHA-256 was verified again. Its ISO and compressed root were mounted read-only. Both preserved microcode payloads passed their manifest checks, matched the repaired official package files and survived the exact offline `install -m 0644` copy operation into a disposable directory. Both mounts were removed afterwards. This is targeted payload/copy validation, **not another full installation from this corrected image**.

## Repair and controlled-reboot results

Before the controlled reboot, all eleven extended checks passed, including the complete `pacman -Qk` file check. The expanded installation check passed **24 of 25** checks. The remaining raw result was `sshd_disabled=false`: the maintainer intentionally enabled SSH autostart for remote testing after the initial audit. That user-selected setting was preserved; it is not evidence that the installer enables SSH by default. No system/user service failures or coredumps were present, and KSplash completed successfully.

One controlled reboot then returned to SSH automatically with the same host key and a new boot ID. The root filesystem was still the installed ext4 disk with no Archiso boot parameters. Early Intel microcode updated from revision `0x28` to `0x2f`. Boot files, GRUB theme, account policy, Aika assets and the exact supplied Fastfetch configuration remained intact.

After reboot the installation check again passed **24 of 25**, with only the intentional SSH-autostart difference. Ten of eleven extended checks passed. `kwin_responds` was false because the physical seat remained at the SDDM greeter without a logged-in Plasma session. This checkpoint does not claim a successful post-reboot physical desktop login. There were no failed system/user services or coredumps; package database and file checks, DNS, HTTPS, audio graph response and a disposable user-home write/read/fsync test passed.

The maintainer subsequently clarified that the physical desktop also works on this GPU. The monitor had been disconnected, and reconnecting it temporarily failed to restore the display; the maintainer attributes that behavior to the GPU's known hardware problems. Desktop operation is therefore **maintainer-confirmed**, while the earlier SSH checkpoint remains unchanged. The reconnect incident does not establish a general AikaOS desktop failure, and its hardware cause was not independently diagnosed.

## Remote application smoke tests

After the reboot, the maintainer reported that this GPU no longer produced a physical picture and already had known core problems. The tests therefore used a **separate CPU-rendered X11/Openbox session**, accessed through password-protected, loopback-only TigerVNC and an SSH tunnel. This was not the normal Plasma Wayland session and did not validate the GPU, physical display, screen locking or the complete Plasma desktop.

Actual GUI interactions verified:

- Konsole opened and accepted keyboard input.
- Kate created and saved a two-line test document. An independent filesystem read confirmed the exact saved bytes.
- Dolphin renamed the file, created a folder and moved the file through its graphical interface. The new path and unchanged contents were independently verified.
- Opening that moved document in Dolphin launched Kate through the normal file association and displayed the saved text.
- Firefox loaded `https://archlinux.org/` without a certificate warning. Its `about:support` page reported **WebRender (Software)** and Mesa llvmpipe.

![Kate reopened the document moved in Dolphin, in the separate software-rendered VNC session](screenshots/hardware-kate-software-vnc.jpg)

The isolated session logged missing accessibility-registry and KDE job-server services. File operations and application opening still succeeded; those warnings are retained as test-fixture limitations. Firefox used a disposable profile, and software-rendering variables applied only to this temporary session. No global graphics override was installed.

The VNC session, SSH forward, local proxy, temporary credentials/profile and uploaded ISO were removed afterwards. Only the eight packages added for this test were uninstalled; a final package-file check passed and no system services were failed. The temporary sleep inhibitor was released. The GRUB backup and private diagnostic reports were retained locally. SSH autostart remained enabled at the maintainer's request.

## Graphics messages retained for investigation

The initial boot logged 463 amdgpu `Unsupported screen format RA24` messages in a three-second burst during graphical startup. The desktop subsequently used accelerated rendering, and the maintainer reported no visible failure during the functional checks. Plasma also logged screen-geometry warnings during the session.

The next audited graphical boot had zero RA24 messages, and the controlled-reboot checkpoint also had zero. The latter remained at the greeter, so these counts do not establish a repeatable graphics fix. The only kernel error at those later checkpoints was the old Intel platform's unsupported TDX capability message.

Similar RA24 errors are tracked in the [upstream KDE report](https://bugs.kde.org/show_bug.cgi?id=524476), where developers attribute the reported problem to amdgpu. That report involves different hardware; it does not establish that this test has the identical root cause. The maintainer's report of defective GPU hardware limits conclusions about the reconnect incident. A healthy-GPU comparison would help isolate the warnings; no claim is made that every earlier graphics warning was caused by that defect.

## Remaining checks

Installed-disk reboot, package integrity, core services and the separate remote application tests are verified. Physical desktop operation, browsing, audio and lock/unlock are maintainer-confirmed. Physical monitor reconnect behavior and repeat lock/unlock after the controlled reboot have not been independently retested. The temporary loss of physical output is recorded as a monitor-reconnect incident on reportedly defective hardware, rather than a demonstrated AikaOS desktop failure.

Automatic standby occurred during the initial SSH audit. The subsequent recovery had a different boot ID and therefore does **not** prove successful suspend/resume. Suspend/resume remains unverified. Accelerated virtualization, BIOS installation, dual boot, encryption and recovery also remain untested. The earlier TCG VM graphics failures remain recorded in the [VM report](INSTALLER_VALIDATION.md). This remains a development build, not stable-release approval.

## Fresh physical installation follow-up — 2026-11-02

The maintainer completed another USB installation, enabled SSH and reported working GPU output. The audit confirmed a new machine identity, completed installer state and an installed ext4 root on the internal SATA disk. No USB device was attached at this installed-system checkpoint. The physical session was active, unlocked **Plasma Wayland**, and KWin reported accelerated OpenGL ES rendering on the RX 580 with no global software-rendering override.

The initial audit passed **23 of 25** installation checks and **10 of 11** extended checks. The exceptions were the intentionally enabled SSH service and the same two missing package-owned microcode images, which also made the package-file check fail. There were no failed system/user services or coredumps; KSplash completed successfully. DNS, HTTPS, audio graph response, fstab, Aika desktop/lock artwork, exact Fastfetch configuration and the disposable user-file round trip passed. Early Intel CPU microcode still loaded successfully from the combined initramfs.

The preserved `/usr/share/aikaos/boot` directory was also absent. The used USB stick was then inspected read-only on Windows. A complete SHA-512 read of its 2,207,404,032-byte `airootfs.sfs` matched both its manifest and the compressed root inside the **older `bba059b` installer image**; it differed from the microcode-corrected `da8120f` image. This identifies the older installation medium, rather than a failed restoration in the corrected installer. Both local ISO files had shared the same basename in different directories. The corrected ISO now additionally has the unambiguous local filename `AikaOS-11.1-dev-da8120f-microcode-fixed.iso`, with unchanged SHA-256 `d2f0abcf3396ebc8e6ce8d3817f703b1e0c30dac1f036622a50fd6abb5effe3b`.

The boot logged 491 RA24 messages during a six-second graphical-startup burst. The desktop was subsequently accelerated and the maintainer reported working output. This preserves the recurring warning as an unresolved observation without treating it as a visible desktop failure or proving a hardware cause.

No package update, microcode repair or GRUB rewrite was performed during this follow-up. Its initial evidence was retained; the temporary sleep inhibitor was released and uploaded temporary helpers were removed. At this checkpoint, a full installation from the corrected image was still outstanding; the subsequent test below completes that installation check.

## Corrected-image physical installation — 2026-11-02

The maintainer then performed a fresh physical installation using the clearly named microcode-corrected image and enabled SSH for validation. The subsequent audit confirmed another new machine identity, completed installation state and an installed boot from `/dev/sda2` (ext4), with the FAT32 EFI partition on the same SATA SSD. No USB installation medium was attached. No package update, manual microcode repair or GRUB regeneration was performed before or during this audit.

**The installer microcode correction passed its fresh-installation test.** All seven targeted checks passed:

- Both `/boot/amd-ucode.img` and `/boot/intel-ucode.img` exactly matched the original payloads verified in the `da8120f` ISO and the preserved `/usr/share/aikaos/boot` copies; owner and mode were root and `0644`.
- The preserved checksum manifest verified successfully.
- GRUB configuration passed `grub-script-check`, and all generated default/fallback initrd entries included both microcode images.
- The combined initramfs also contained Intel early microcode, and the boot journal reported the early CPU revision update from `0x28` to `0x2f`.

The installation acceptance check passed **24 of 25** checks, with only `sshd_disabled=false` because the maintainer intentionally enabled SSH. All **11 of 11** extended checks passed, including package database consistency and the complete package-owned file check. No package-owned files were missing. The package tool warned that online `core`/`extra` sync databases had not yet been downloaded; this read-only audit did not refresh repositories or upgrade packages.

The active, unlocked physical session was Plasma Wayland. KWin reported accelerated OpenGL ES on the RX 580 with radeonsi and no global software-rendering overrides. KSplash completed successfully. No system/user services were failed and no coredumps were present. DNS, HTTPS, audio graph response, fstab, the exact supplied Fastfetch configuration, Aika icons and desktop/lock wallpapers, automatic-lock configuration and the disposable user-file round trip all passed. These SSH checks do not replace a visual application or lock/unlock test on this particular fresh installation.

The kernel again logged 463 RA24 messages, this time from 18:57:00 to 18:57:04 local time during graphical startup. Accelerated desktop rendering was subsequently active. The repeated warning remains an unresolved observation; this successful installation does not establish its cause or resolve the earlier VM graphics failures.

Temporary uploaded helpers were removed and the sleep inhibitor was released after the reports were saved. The existing SSH setting was preserved. This verifies the corrected offline installer path and installed-disk boot on this physical UEFI system; BIOS, dual boot, encryption, suspend/resume and recovery remain outside the tested coverage.
