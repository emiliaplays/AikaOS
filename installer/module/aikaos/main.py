# SPDX-License-Identifier: GPL-3.0-or-later
"""Apply AikaOS target configuration only inside Calamares' mounted target."""
from pathlib import Path
import os
import subprocess
import libcalamares


def run():
    target = Path(libcalamares.globalstorage.value('rootMountPoint') or '/')
    phase = libcalamares.job.configuration.get('phase')
    if phase not in ('prepare', 'finalize'):
        return ('Invalid AikaOS installer phase', 'Expected prepare or finalize.')
    if not target.is_absolute() or target.resolve() == Path('/') or not os.path.ismount(target):
        return ('Invalid installation target', 'A mounted target filesystem is required.')
    mounted = subprocess.run(
        ['findmnt', '-n', '-o', 'SOURCE', '--target', str(target)],
        text=True, capture_output=True, check=False,
    )
    if mounted.returncode or not mounted.stdout.strip().startswith('/dev/'):
        return ('Invalid installation target', 'The target must be a mounted block-device filesystem.')
    rc = libcalamares.utils.target_env_call([
        '/bin/bash', '/usr/local/lib/aikaos/configure-installed.sh', phase,
    ])
    if rc:
        return ('AikaOS configuration failed', f'The {phase} step exited with status {rc}.')
    return None
