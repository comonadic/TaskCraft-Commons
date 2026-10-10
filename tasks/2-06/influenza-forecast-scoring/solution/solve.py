import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import pandas as pd
f=pd.read_parquet(INPUT/'forecast_archive.parquet');t=pd.read_csv(INPUT/'truth.csv');t=t[t.release_date<='2024-06-30'].sort_values('release_date').drop_duplicates(['location','target_date'],keep='last').set_index(['location','target_date']);q=read_json(INPUT/'quantiles.json');rows=[]
keys=['location','target_date','horizon'];good=[]
for key,z in f.groupby(keys):
 if z.groupby('model').size().eq(23).all() and z.model.nunique()==5:good.append(key)
allowed=set(good)
for (model,loc,date,h),z in f.groupby(['model']+keys):
 if (loc,date,h) not in allowed:continue
 pred=dict(zip(z['quantile'],z.prediction));y=float(t.loc[(loc,date),'value']);mae=abs(y-pred[.5]);total=.5*mae
 for lo in q[:11]:
  a=2*lo;l,u=pred[lo],pred[round(1-lo,3)];total+=a/2*(u-l+2/a*max(l-y,0)+2/a*max(y-u,0))
 rows.append({'model':model,'location':loc,'target_date':date,'horizon':h,'wis':total/11.5,'mae':mae,'coverage50':int(pred[.25]<=y<=pred[.75]),'coverage95':int(pred[.025]<=y<=pred[.975])})
d=pd.DataFrame(rows);summary=d.groupby('model').agg(n_cells=('wis','size'),mean_wis=('wis','mean'),mean_mae=('mae','mean'),coverage50=('coverage50','mean'),coverage95=('coverage95','mean')).reset_index();summary['rel_wis']=summary.mean_wis/float(summary.loc[summary.model=='naive','mean_wis'].iloc[0]);OUTPUT.mkdir(exist_ok=True);d.to_csv(OUTPUT/'per_cell_scores.csv',index=False);summary.to_csv(OUTPUT/'submission.csv',index=False)
