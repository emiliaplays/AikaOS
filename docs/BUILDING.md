# Build the live image

## Reference environment

The 11.1 beta was assembled on **Arch Linux x86_64 with Archiso 92**, then packaged with `grub-mkrescue`. The development host was Windows with a QEMU TCG Arch VM. Native Arch Linux or an Arch VM is the supported environment for this reference procedure.

Use a Linux filesystem for the checkout so symbolic links and executable modes are preserved. Do not build directly from an NTFS checkout with text placeholders in place of symbolic links.

Install the build tools on the Arch build machine:

```sh
sudo pacman -Syu --needed archiso grub xorriso squashfs-tools mtools dosfstools ttf-dejavu python
git clone https://github.com/emiliaplays/AikaOS.git
cd AikaOS
sudo bash scripts/build.sh
```

The build uses a fresh `build/` directory and writes the final image and checksums to `out/`. If `build/` already exists, the script stops; rename or remove your own previous build directory deliberately before starting again. Allow enough space for packages, the expanded root filesystem, and intermediate/final ISOs; the original build VM used an 80 GB virtual disk.

## What the recipe does

1. Runs Archiso using the checked-in profile to install packages and prepare a staged ISO tree.
2. Applies the live customization hook, locale generation, account ownership, and AikaOS identity.
3. Packs the root filesystem with Zstandard and updates its SHA-512 checksum.
4. Generates DejaVu GRUB fonts and replaces the intermediate boot arrangement with the Aika GRUB theme.
5. Creates a BIOS/UEFI hybrid ISO using `grub-mkrescue` and writes a SHA-256 file.

The intermediate Archiso ISO is not the final download. The final image is `out/aikaos-11.1-x86_64-grub.iso`.

## Release fidelity

The release ISO is the exact tested local 11.1 image, with SHA-256 recorded in `releases/11.1-beta.1/manifest.json`. The profile reflects its final desktop, branding and supplied Fastfetch configuration, including restoration of KDE's default splash behavior.

This is not a byte-reproducible build. Arch repositories roll forward, package versions can change, and filesystem/ISO timestamps differ. A full clean build of commit `a631d6040233b7c05e7c5e6f30b496e4c5f2c4d4` succeeded on 2026-11-01 with Archiso 92. Its new ISO booted through UEFI into KDE Plasma in QEMU, and the supplied Fastfetch configuration and branding aliases were checked. Compare behavior and package inventory, not the SHA-256, with the published beta.

That build also fixed package-owned artwork collisions and removed assumptions about rerunning Archiso's deleted customization hook or copying its emptied `/boot` directory. The published beta download is unchanged.

The published root filesystem was updated in its existing ISO allocation during development. Padding and checksums were validated, and all boot-image bytes were preserved. A fresh build from this repository creates a new image normally; it does not need that development-only patching process.

## Layout

| Path | Purpose |
| --- | --- |
| `profile/` | Archiso profile and live filesystem overlay |
| `assets/branding/` | Selected mascot, desktop and lock-screen artwork |
| `assets/grub/` | GRUB background, theme and configuration |
| `assets/fastfetch/` | Main, compact and full-character configurations |
| `scripts/apply-branding.py` | Regenerates branding overlay files from the assets |
| `scripts/build.sh` | Reference Archiso plus GRUB packaging procedure |
| `scripts/validate.py` | Static checks run locally and in CI |
| `releases/11.1-beta.1/` | Published binary metadata and package inventory |

The branding generator is optional: the generated overlay is already checked in. After asset changes, run `python3 scripts/apply-branding.py` before a new build and review the diff.

## Installer development image

The optional Calamares image is developed separately from the published live-only beta. See [installer development](INSTALLER.md) for the pinned package, build commands and VM acceptance criteria. Development artifacts are not stable releases.
