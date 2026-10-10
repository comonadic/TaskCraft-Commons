import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

expected=read_json(TESTS/'expected.json'); docs=read_json(TESTS/'documents.json');g=Grade()
def audit():
    got=read_json(OUTPUT/'findings.json'); target={x['field']:x for x in expected}; matched=set(); valid=0
    report=(OUTPUT/'audit_report.md').read_text()
    report_count=len(re.findall(r'^##\s+发现\s*\d+',report,re.M))
    for f in got:
        ev=f.get('evidence',[]); field=f.get('field'); vals=f.get('values',[])
        correct=field in target and field not in matched and len(ev)>=2 and len({e.get('document') for e in ev})>=2
        for e in ev:
            d=e['document'].split('.')[0];pg=int(e['page']);q=e['quote']
            correct=correct and q in docs.get(d,[[]]*4)[pg-1] and q in report and f"{e['document']}:p{pg}" in report
        if field in target:
            correct=correct and all(any(v in e.get('quote','') for e in ev) for v in target[field]['values'])
        if correct: matched.add(field);valid+=1
    return max(0,valid/4-.2*(len(got)-valid)-.2*abs(report_count-len(got)))
g.check('四项证据化发现及额外发现惩罚',1,audit);g.finish()
