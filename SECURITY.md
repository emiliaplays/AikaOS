# Security

AikaOS 11.1 has separate live and installed defaults. In the live installer session, `aika` logs in automatically, has an empty password and can run sudo without a password. Live automatic locking is disabled and changes are held in a non-persistent RAM overlay.

Calamares creates a password-protected normal user, locks root, removes live automatic login/passwordless sudo, enables the user's automatic-lock default and leaves SSH autostart disabled. Installation requires explicit disk selection and confirmation. The bootloader is unsigned and Secure Boot is unsupported.

For sensitive vulnerability reports, use the repository's private vulnerability reporting option when available: https://github.com/emiliaplays/AikaOS/security/advisories/new. Avoid posting exploit credentials or private user data in a public issue.

Project support is best effort without a formal response-time guarantee. Keep the installed system current through full Arch package upgrades and review [maintenance guidance](docs/MAINTENANCE.md). Bundled third-party packages follow their upstream security policies; the ISO remains a fixed snapshot. AikaOS configuration migrations are documented separately from upstream package updates.
