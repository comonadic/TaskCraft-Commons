import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import numpy as np,pandas as pd
from scipy.optimize import linprog
sys.path.insert(0,str(ROOT/'software'));from thermal import building_step
cal=pd.read_csv(INPUT/'calibration.csv');features=['air','wall','outside','solar','occupied','cooling'];X=cal[features].to_numpy();coef=np.linalg.lstsq(X,cal[['next_air','next_wall']].to_numpy(),rcond=None)[0];write_json(OUTPUT/'identified_model.json',{'air_coefficients':coef[:,0].tolist(),'wall_coefficients':coef[:,1].tolist()});write_json(OUTPUT/'rc_diagnostics.json',{'train_rmse':float(np.sqrt(np.mean((X@coef-cal[['next_air','next_wall']].to_numpy())**2)))})
w=pd.read_csv(INPUT/'eval_weather.csv');A=coef[:2,:].T;B=coef[5,:];allrows={};metrics={}
for mode in ['baseline','cost','peak']:
 state=np.array([26.,27.]);rows=[];cost=peak=viol=0
 for i in range(len(w)):
  ww=w.iloc[i];dist=ww[['outside','solar','occupied']].to_numpy(dtype=float)
  if mode=='baseline':u=float(np.clip((building_step(state,dist,0)[0]-26)/.28,0,8))
  else:
   h=min(24,len(w)-i);T=np.zeros((2,h));free=state.copy();constraints=[];bounds=[];c=np.zeros(h+1)
   for k in range(h):
    step=w.iloc[i+k];d=step[['outside','solar','occupied']].to_numpy(dtype=float);free=A@free+coef[2:5,:].T@d;T=A@T;T[:,k]+=B;lo,hi=(24,26) if step.occupied else (23,28)
    constraints.append(np.r_[T[0],0]);bounds.append(hi-free[0]);constraints.append(np.r_[-T[0],0]);bounds.append(free[0]-lo)
    peakrow=np.zeros(h+1);peakrow[k]=1;peakrow[-1]=-1;constraints.append(peakrow);bounds.append(0)
    c[k]=float(step.price_cny_kwh)*.25*(1 if mode=='cost' else .001)
   c[-1]=.00001 if mode=='cost' else 1
   res=linprog(c,A_ub=np.array(constraints),b_ub=np.array(bounds),bounds=[(0,8)]*(h+1),method='highs')
   if not res.success:raise RuntimeError(res.message)
   u=float(res.x[0])
  state=building_step(state,dist,u);rows.append({'step':i,'air':state[0],'wall':state[1],'cooling':u});cost+=u*.25*ww.price_cny_kwh;peak=max(peak,u);lo,hi=(24,26) if ww.occupied else (23,28);viol+=(max(lo-state[0],0)+max(state[0]-hi,0))*.25
 allrows[mode]=rows;metrics[mode]={'cost_cny':cost,'peak_kw':peak,'comfort_violation_degree_hours':viol};write_csv(OUTPUT/f'{mode}_timeseries.csv',rows)
 if mode!='baseline':write_csv(OUTPUT/f'{mode}_actions.csv',[{'step':r['step'],'cooling':r['cooling']} for r in rows])
write_json(OUTPUT/'metrics.json',metrics)
(OUTPUT/'controller.py').write_text(Path(__file__).read_text().replace('from support import *',(Path(__file__).parent/'support.py').read_text(),1) if (Path(__file__).parent/'support.py').exists() else Path(__file__).read_text())
