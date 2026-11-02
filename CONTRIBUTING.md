# Contributing

Thank you for testing AikaOS. Small, focused reports and changes help keep this young project maintainable.

For a bug report, include the release version, ISO checksum, CPU/GPU, boot mode, Rufus write mode, and steps to reproduce. Describe expected and actual behavior. Redact credentials, personal paths, serial numbers and private information from logs or screenshots.

For a change, explain the problem and the resulting behavior, keep the diff focused, and run `python3 scripts/validate.py`, `python3 tests/test-installer-guard.py` and `bash -n scripts/build.sh`. Installer changes also require `scripts/validate-installer.py` against the pinned Calamares source as described in [the installer guide](docs/INSTALLER.md). If you rebuild or boot an ISO, record the exact checksum, environment and what you tested. Static checks do not substitute for a live boot.

Use English for issues, pull requests and documentation. Be respectful and constructive. New artwork needs clear provenance and permission to distribute; do not replace upstream license notices.
