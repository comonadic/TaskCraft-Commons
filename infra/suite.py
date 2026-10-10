#!/usr/bin/env python3
"""Check or run a selection of TaskCraft folders through Harbor."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['check', 'oracle', 'nop'])
    p.add_argument('--task', action='append', help='Task ID; repeat to select multiple tasks')
    p.add_argument('--exclude', action='append', default=[])
    p.add_argument('--jobs-dir', default='runs')
    p.add_argument('--job-name', default=None)
    p.add_argument('--concurrency', type=int, default=1)
    args = p.parse_args()
    tasks = [ROOT / 'tasks' / c['taskId'] for c in json.loads((ROOT / 'index.json').read_text()) if (not args.task or c['taskId'] in args.task) and c['taskId'] not in args.exclude]
    if not tasks:
        p.error('No tasks selected')
    for task in tasks:
        subprocess.run([sys.executable, str(task / 'run.py'), 'check'], check=True)
        if args.action != 'check':
            subprocess.run([sys.executable, str(task / 'run.py'), 'prepare'], check=True)
    if args.action == 'check':
        return
    executable = os.environ.get('HARBOR_BIN') or shutil.which('harbor')
    if not executable:
        p.error('Install Harbor: pip install harbor==0.22.0')
    config = {'jobs_dir': str(Path(args.jobs_dir).resolve()), 'n_concurrent_trials': args.concurrency,
              'agents': [{'name': args.action}], 'tasks': [{'path': str(t)} for t in tasks],
              'environment': {'type': 'docker'}}
    if args.job_name:
        config['job_name'] = args.job_name
    with tempfile.TemporaryDirectory(prefix='taskcraft-suite-') as temp:
        path = Path(temp) / 'job.json'
        path.write_text(json.dumps(config, indent=2))
        raise SystemExit(subprocess.call([executable, 'run', '-c', str(path)]))

if __name__ == '__main__':
    main()
