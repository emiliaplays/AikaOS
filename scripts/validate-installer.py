#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate distribution configuration against the pinned upstream schemas."""
from pathlib import Path
import argparse
import jsonschema
import yaml

repo = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--upstream', type=Path, required=True)
args = parser.parse_args()
configuration = repo / 'installer/calamares'
count = 0
for path in (configuration / 'modules').glob('*.conf'):
    schema = args.upstream / 'src/modules' / path.stem / (path.stem + '.schema.yaml')
    value = yaml.safe_load(path.read_text(encoding='utf-8'))
    if schema.exists():
        jsonschema.validate(value, yaml.safe_load(schema.read_text(encoding='utf-8')))
        count += 1
settings = yaml.safe_load((configuration / 'settings.conf').read_text(encoding='utf-8'))
assert settings['prompt-install'] is True
assert settings['dont-chroot'] is False
jobs = next(item['exec'] for item in settings['sequence'] if 'exec' in item)
critical_order = ['partition', 'mount', 'unpackfs', 'aikaos@prepare', 'removeuser', 'users', 'bootloader', 'aikaos@finalize', 'umount']
assert [jobs.index(name) for name in critical_order] == sorted(jobs.index(name) for name in critical_order)
users = yaml.safe_load((configuration / 'modules/users.conf').read_text(encoding='utf-8'))
assert users['doAutologin'] is False
assert users['setRootPassword'] is False
assert users['passwordRequirements']['minLength'] > 0
print(f'Validated {count} upstream module schemas, job ordering and installed-account defaults.')
