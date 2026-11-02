#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""The installation job must reject the host root before running any command."""
from pathlib import Path
from types import SimpleNamespace
import importlib.util
import sys

repo = Path(__file__).resolve().parent.parent
called = []
fake = SimpleNamespace(
    globalstorage=SimpleNamespace(value=lambda key: '/'),
    job=SimpleNamespace(configuration={'phase': 'prepare'}),
    utils=SimpleNamespace(target_env_call=lambda command: called.append(command)),
)
sys.modules['libcalamares'] = fake
spec = importlib.util.spec_from_file_location('aikaos_job', repo / 'installer/module/aikaos/main.py')
job = importlib.util.module_from_spec(spec)
spec.loader.exec_module(job)
for unsafe in ('/', '.', '', None):
    fake.globalstorage.value = lambda key, target=unsafe: target
    result = job.run()
    assert result and result[0] == 'Invalid installation target', (unsafe, result)
assert not called, 'An unsafe root reached target_env_call'
print('Unsafe installation targets are rejected before any target command runs.')
