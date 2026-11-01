# Security

AikaOS 11.1 is a live beta for evaluation. The account `aika` logs in automatically, has an empty password and can run `sudo` without a password. Automatic screen locking is disabled. The bootloader is unsigned, and the live writable overlay is not persistent.

Do not treat the live environment as a hardened or access-controlled installation. The release does not automatically install to an internal drive.

For sensitive vulnerability reports, use the repository's private vulnerability reporting option when available: https://github.com/emiliaplays/AikaOS/security/advisories/new. Avoid posting exploit credentials or private user data in a public issue.

This first beta has no established security-support lifetime or response-time guarantee. Bundled third-party packages follow their upstream security policies; the live ISO is a fixed snapshot, not a promise of automatic image updates.
