#!/usr/bin/env python3
"""Standalone task-folder entry point. Python 3.11+, Docker and Harbor required."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import urllib.request

TASK = Path(__file__).resolve().parent

def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def check():
    for name in ['instruction.md', 'task_card.json', 'task.toml', 'environment/Dockerfile', 'solution/solve.sh', 'tests/test.sh', 'tests/grade.py', 'evaluation.json', 'materials.json']:
        if not (TASK / name).is_file():
            raise ValueError(f'Missing {name}')
    config = tomllib.loads((TASK / 'task.toml').read_text())
    card = json.loads((TASK / 'task_card.json').read_text())
    weights = sum(c['weight'] for c in card['evaluation']['checks'])
    if abs(weights - 100) > 1e-6:
        raise ValueError('Evaluation weights must sum to 100')
    for item in json.loads((TASK / 'materials.json').read_text()):
        path = (TASK / item['path']).resolve()
        if not path.is_relative_to(TASK) or not path.is_file() or sha256(path) != item['sha256']:
            raise ValueError(f"Input checksum mismatch: {item['path']}")
    print(json.dumps({'task': card['taskId'], 'version': card['version'], 'inputs': card['inputFileCount'], 'verifier': config['verifier']['environment_mode'], 'status': 'valid'}, ensure_ascii=False))

def prepare():
    lockpath = TASK / 'assets.lock.json'
    if not lockpath.exists():
        return
    lock = json.loads(lockpath.read_text())
    def complete():
        return all((TASK / f['path']).is_file() and sha256(TASK / f['path']) == f['sha256'] for f in lock['files'])
    if complete():
        print('Runtime assets ready.')
        return
    with tempfile.TemporaryDirectory(prefix='taskcraft-assets-') as temp:
        archive = Path(temp) / 'assets.tar.gz'
        print(f"Downloading {lock['archive']['url']}", flush=True)
        with urllib.request.urlopen(lock['archive']['url'], timeout=120) as response, archive.open('wb') as output:
            shutil.copyfileobj(response, output)
        if sha256(archive) != lock['archive']['sha256']:
            raise ValueError('Runtime archive checksum mismatch')
        with tarfile.open(archive) as bundle:
            for member in bundle.getmembers():
                target = (TASK / member.name).resolve()
                if not target.is_relative_to(TASK / 'environment/assets') or not (member.isfile() or member.isdir()):
                    raise ValueError('Unexpected path in runtime archive')
            bundle.extractall(TASK)
    if not complete():
        raise ValueError('Runtime assets checksum mismatch')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'prepare', 'oracle', 'nop', 'run'])
    args, extra = parser.parse_known_args()
    if args.action == 'check':
        check()
        return
    prepare()
    if args.action == 'prepare':
        return
    check()
    executable = os.environ.get('HARBOR_BIN') or shutil.which('harbor')
    if not executable:
        raise ValueError('Install Harbor first: pip install harbor==0.22.0')
    command = [executable, 'run', '-p', str(TASK), '-e', 'docker']
    if args.action != 'run':
        command += ['-a', args.action]
    command += extra
    raise SystemExit(subprocess.call(command))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
