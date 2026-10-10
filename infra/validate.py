#!/usr/bin/env python3
"""Validate cards, manifests, file references, Python syntax and task structure."""
import ast
import json
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parent.parent
cards = json.loads((ROOT / 'index.json').read_text())
catalog = json.loads((ROOT / 'taxonomy/china_occupations.json').read_text())
codes = {o['code'] for o in catalog['occupations']}
seen = set()
for card in cards:
    identity = card['taskId']
    assert identity not in seen, f'Duplicate task: {identity}'
    seen.add(identity)
    assert card['occupation']['code'] in codes, f'Occupation out of scope: {identity}'
    assert not any(k in card for k in ['source', 'source_task_id', 'provenance', 'synthetic', 'priority'])
    task = ROOT / 'tasks' / identity
    assert json.loads((task / 'task_card.json').read_text()) == card, f'Index mismatch: {identity}'
    assert json.loads((task / 'evaluation.json').read_text()) == card['evaluation']
    config = tomllib.loads((task / 'task.toml').read_text())
    assert config['task']['version'] == card['version']
    assert config['verifier']['environment_mode'] == card['runtime']['verifierMode']
    for f in card['inputFiles'] + card['referenceFiles'] + card['filePreviews']:
        path = (task / f['path']).resolve()
        assert path.is_relative_to(task.resolve()) and path.exists(), f'Missing file: {identity}/{f["path"]}'
    for path in task.rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))
    subprocess.run([sys.executable, str(task / 'run.py'), 'check'], check=True)
try:
    from jsonschema import Draft202012Validator
except ImportError:
    pass
else:
    schema = json.loads((ROOT / 'task-card.schema.json').read_text())
    validator = Draft202012Validator(schema)
    for card in cards:
        validator.validate(card)
print(f'Validated {len(cards)} self-contained task packages, {len(codes)} occupations.')
