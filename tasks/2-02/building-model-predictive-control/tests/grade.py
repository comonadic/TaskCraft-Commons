import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import numpy as np
from thermal import building_step
w=read_csv(TESTS/'weather.csv');g=Grade()
def dynamics():
 total=0
 for mode in ['baseline','cost','peak']:
  rows=read_csv(OUTPUT/f'{mode}_timeseries.csv')
  if len(rows)!=672:return 0
  state=np.array([26.,27.]);cost=peak=viol=0
  for i,(r,ww) in enumerate(zip(rows,w)):
   if int(r['step'])!=i:return 0
   u=float(r['cooling']);weather=[float(ww[k]) for k in ['outside','solar','occupied']]
   if not math.isfinite(u) or not -1e-6<=u<=8.000001:return 0
   if mode=='baseline' and not equal(u,float(np.clip((building_step(state,weather,0)[0]-26)/.28,0,8)),atol=1e-5):return 0
   state=building_step(state,weather,u)
   if not np.allclose(state,[float(r['air']),float(r['wall'])],atol=1e-5):return 0
   cost+=u*.25*float(ww['price_cny_kwh']);peak=max(peak,u);lo,hi=(24,26) if int(ww['occupied']) else (23,28);viol+=(max(lo-state[0],0)+max(state[0]-hi,0))*.25
  metric=read_json(OUTPUT/'metrics.json')[mode]
  total+=tree_score(metric,{'cost_cny':cost,'peak_kw':peak,'comfort_violation_degree_hours':viol},atol=1e-5)
  if mode!='baseline':
   if viol>1e-3:return 0
   actions=read_csv(OUTPUT/f'{mode}_actions.csv')
   if record_score(actions,[{'step':i,'cooling':float(r['cooling'])} for i,r in enumerate(rows)],['step'])<.99999:return 0
 return total/3
g.check('独立动力学回放与指标重算',.6,dynamics)
def performance():
 if dynamics()<1-1e-6:return 0
 a=read_json(OUTPUT/'metrics.json');b=a['baseline'];return .5*min(1,max(0,(1-a['cost']['cost_cny']/b['cost_cny'])/.01))+.5*min(1,max(0,(1-a['peak']['peak_kw']/b['peak_kw'])/.01))
g.check('节费与削峰',.25,performance)
g.check('RC模型识别',.1,lambda:tree_score(read_json(OUTPUT/'identified_model.json'),{'air_coefficients':[.9,.05,.05,.0012,.12,-.28],'wall_coefficients':[.02,.97,.01,0,0,0]},atol=1e-6))
def rerun():
 if float(read_json(OUTPUT/'rc_diagnostics.json')['train_rmse'])>=1e-5:return 0
 with replay(OUTPUT/'controller.py',TESTS/'replay_input',software=TESTS/'replay_software',timeout=300) as generated:
  return tree_score(read_json(generated/'metrics.json'),read_json(OUTPUT/'metrics.json'),atol=1e-5)
g.check('控制器隔离复跑与诊断',.05,rerun);g.finish()
