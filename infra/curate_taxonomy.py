#!/usr/bin/env python3
"""Rebuild the knowledge-work catalog after editing scope-policy.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
folder = ROOT / 'taxonomy'
full = json.loads((folder / 'china_occupations.full.json').read_text())
policy = json.loads((folder / 'scope-policy.json').read_text())
codes = {o['code'] for o in full['occupations']}
unknown = set(policy['includeCodes'] + policy['excludeCodes']) - codes
if unknown:
    raise ValueError(f'Unknown occupation codes: {sorted(unknown)}')
def allowed(code):
    if code in policy['excludeCodes'] or any(code.startswith(p) for p in policy['excludePrefixes']):
        return False
    return code in policy['includeCodes'] or any(code.startswith(p) for p in policy['includePrefixes'])
selected = [o for o in full['occupations'] if allowed(o['code'])]
categories = [{**c, 'classificationName': c['name'], 'name': policy['categoryNames'].get(c['code'], c['name'])} for c in full['categories'] if any(o['category'] == c['code'] for o in selected)]
catalog = {**full, 'scope': 'knowledge-work', 'scopeVersion': policy['version'], 'label': '中国知识工作职业目录', 'selectionPolicy': 'scope-policy.json', 'majors': {m:policy['majorNames'].get(m,n) for m,n in full['majors'].items() if any(c['major'] == m for c in categories)}, 'categories': categories, 'occupations': selected}
(folder / 'china_occupations.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
print(f'{len(categories)} categories / {len(selected)} occupations')
