# Verify an AikaOS download

Use the checksum and provenance files from the official [AikaOS GitHub releases](https://github.com/emiliaplays/AikaOS/releases). The 11.1 stable image has the distinct filename `aikaos-11.1-stable-x86_64.iso`.

## SHA-256

On Windows PowerShell:

```powershell
Get-FileHash .\aikaos-11.1-stable-x86_64.iso -Algorithm SHA256
Get-Content .\aikaos-11.1-stable-x86_64.iso.sha256
```

The two 64-character hashes must match; letter case does not matter.

On Linux, with the ISO and sidecar in the same directory:

```sh
sha256sum -c aikaos-11.1-stable-x86_64.iso.sha256
```

Expect `OK`. If verification fails, download the image again before writing a USB.

## Build provenance

The release workflow generates a GitHub/Sigstore build-provenance attestation linking the image digest to the source revision and workflow. With a current GitHub CLI:

```sh
gh attestation verify aikaos-11.1-stable-x86_64.iso --repo emiliaplays/AikaOS
```

The published `aikaos-11.1.intoto.jsonl` bundle can also be supplied explicitly:

```sh
gh attestation verify aikaos-11.1-stable-x86_64.iso --bundle aikaos-11.1.intoto.jsonl --repo emiliaplays/AikaOS
```

Check that verification succeeds for `emiliaplays/AikaOS` and the release-image workflow. See the [official GitHub CLI verification reference](https://cli.github.com/manual/gh_attestation_verify).

The build manifest records the exact image size, SHA-256, source commit and build time. `packages.x86_64.txt` records the packages and versions in the live image. Secure Boot remains unsupported; the bootloader is unsigned.
