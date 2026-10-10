import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

g=Grade();truth=read_json(TESTS/'truth.json');base=read_json(TESTS/'baseline.json')
def loss(rows):
 indexed={(r['location'],int(r['horizon'])):r for r in rows}
 if len(rows)!=212 or len(indexed)!=212:raise ValueError('expected exactly 212 unique rows')
 wis=[];mae=[]
 for t in truth:
  r=indexed[(t['location'],t['horizon'])];pt,l,u=[float(r[k]) for k in ['point','lower95','upper95']];y=t['truth']
  if not all(math.isfinite(x) for x in [pt,l,u]) or not 0<=l<=pt<=u:raise ValueError('invalid interval')
  err=abs(y-pt);wis.append((.5*err+.025*(u-l+40*max(l-y,0)+40*max(y-u,0)))/1.5);mae.append(err)
 return sum(wis)/212,sum(mae)/212
def skill():
 w,m=loss(read_csv(OUTPUT/'submission.csv'));bw,bm=loss(base)
 return .7*min(1,max(0,(1-w/bw)/.35))+.3*min(1,max(0,(1-m/bm)/.35))
g.check('相对naive预测技能',.9,skill)
def rerun():
 if len((OUTPUT/'method.md').read_text())<30:return 0
 with replay(OUTPUT/'forecast.py',TESTS/'replay_input') as generated:
  return record_score(read_csv(generated/'submission.csv'),read_csv(OUTPUT/'submission.csv'),['location','horizon'])
g.check('预测代码隔离复跑',.1,rerun);g.finish()
