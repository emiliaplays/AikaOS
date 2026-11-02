# Prepare and publish AikaOS 11.1

The stable channel produces `aikaos-11.1-stable-x86_64.iso`. It is a candidate until the downloaded artifact passes acceptance; a successful workflow is not by itself release approval.

## Build and verify

1. Review the release branch and run the **Build AikaOS 11.1 release image** workflow. It builds the pinned Calamares recipe and a clean Archiso profile, verifies stable identity, exports the package inventory/manifest and generates build provenance.
2. Download the `aikaos-11.1-release-candidate` artifact. Verify the ISO against its sidecar and verify its attestation for `emiliaplays/AikaOS`.
3. Preserve the exact ISO and verification files locally. Record its source commit, SHA-256 and byte count. Remove large temporary CI artifacts only after a verified local copy is available.
4. Boot that exact image, perform the documented installation into a new virtual disk and boot without the installer ISO. Run the installed acceptance check, including `--expect-swap-file` for that choice. Record any fixture modifications and limitations separately.
5. Copy the exact build manifest and package inventory into `releases/11.1/`, and complete the final-image validation report and release notes. Documentation-only follow-ups must preserve the recorded build-source revision.

## Prepare publication

- Prepare a GitHub draft release for `v11.1`, with English notes and the small verification/metadata assets. Do not attach or split the multi-gigabyte ISO for GitHub's individual-file limit.
- Host the single ISO at SourceForge under `11.1/aikaos-11.1-stable-x86_64.iso`. Upload its checksum alongside it.
- After upload, check the public single-file download and verify the downloaded bytes against the same SHA-256. Use that verified SourceForge link in the GitHub release and README.
- Publish only the exact tested artifact. If image content changes, produce a new checksum/provenance record and repeat acceptance.
- Complete the release-branch review/merge, final publication status and `v11.1` release. Preserve Beta 1 as historical evidence and retain its original checksum/files.

Publication and changing the default public download are separate from candidate preparation. No credentials or private test logs belong in release assets.
