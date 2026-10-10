import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

e=read_json(TESTS/'expected.json');g=Grade()
def predictions():
 r=read_csv(OUTPUT/'full_predictions.csv');ids=[x['patient_id'] for x in r]
 if len(r)!=6000 or len(set(ids))!=6000:return 0
 original=sum(equal(x['baseline_score'],e['scores'].get(x['patient_id'])) for x in r)/6000
 b=[x['patient_id'] for x in r if x['baseline_selected'].lower()=='true'];s=[x['patient_id'] for x in r if x['revised_selected'].lower()=='true']
 ranked=[x['patient_id'] for x in sorted(r,key=lambda x:(-float(x['revised_score']),x['patient_id']))[:1200]]
 return .3*original+.2*f1_set(b,e['baseline'])+.3*f1_set(s,e['revised'])+.2*f1_set(ranked,e['revised'])
g.check('原分数与两种排序',.65,predictions)
for name in ['baseline','revised']:g.check(name+'人群需要与构成',.15,lambda name=name:tree_score(read_json(OUTPUT/f'{name}_report.json'),e[name+'_report']))
g.check('机制及外推限制说明',.05,lambda:len((OUTPUT/'analysis.md').read_text())>=60);g.finish()
