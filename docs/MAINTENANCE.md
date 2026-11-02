# Updates and maintenance

AikaOS 11.1 is an installation-image release on an Arch rolling base. The installed kernel and applications continue to change through official Arch package updates; the ISO is a fixed snapshot.

## System updates

Read [Arch Linux news](https://archlinux.org/news/) before upgrading, then run:

```sh
sudo pacman -Syu
```

Complete the full transaction. Arch does not support partial upgrades such as synchronizing databases and selectively installing packages without completing the system upgrade. See [Arch's system-maintenance guidance](https://wiki.archlinux.org/title/System_maintenance).

Reboot after kernel updates. Keep backups of personal files. The tested kernel/microcode upgrade preserved Aika assets and generated boot images; see the [update and suspend report](UPDATE_VALIDATION.md).

## AikaOS changes

The initial release does not provide a separate AikaOS package repository or automatic configuration-migration service. Arch updates maintain the upstream packages. AikaOS artwork/default changes and any required manual migration steps will be documented in project release notes.

The installed artwork hook reapplies the Aika aliases when Arch's `filesystem` package changes. User desktop preferences remain ordinary KDE configuration files. Reinstalling from each new ISO is not the routine Arch package-update method.

## Project support

Support is community/best effort, focused on the documented x86_64 UEFI/ext4 installation path. Use [GitHub issues](https://github.com/emiliaplays/AikaOS/issues) for AikaOS build, installer and branding problems. Include the ISO checksum and a reproducible description; remove secrets from logs.

Upstream kernel, KDE and application issues may need to be reported to their maintainers. Known observations and untested modes are listed in [KNOWN_ISSUES.md](KNOWN_ISSUES.md). See [SECURITY.md](../SECURITY.md) for sensitive reports.
