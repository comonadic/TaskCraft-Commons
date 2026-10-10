import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from sklearn.metrics import f1_score
e=read_json(TESTS/'labels.json');labels=['NORM', 'MI', 'STTC', 'CD', 'HYP'];g=Grade()
def score():
 rows=read_csv(OUTPUT/'predictions.csv');ids=[r['ecg_id'] for r in rows]
 if len(ids)!=len(e) or len(set(ids))!=len(e) or set(ids)!={r['ecg_id'] for r in e}:return 0
 d={r['ecg_id']:r for r in rows};pred=[];truth=[]
 for r in e:
  q=d[r['ecg_id']]
  if set(q)!={'ecg_id',*labels} or any(q[k] not in ['0','1'] for k in labels):return 0
  pred.append([int(q[k]) for k in labels]);truth.append([r[k] for k in labels])
 f=float(f1_score(truth,pred,average='macro',zero_division=0));write_json(Path(os.environ.get('TASKCRAFT_LOG','/logs/verifier'))/'classification_metrics.json',{'macro_f1':f,'threshold':0.75})
 return min(1,f/.75)
g.check('独立测试macro-F1',.98,score);g.check('方法与限制说明',.02,lambda:len((OUTPUT/'model_report.md').read_text())>60);g.finish()
