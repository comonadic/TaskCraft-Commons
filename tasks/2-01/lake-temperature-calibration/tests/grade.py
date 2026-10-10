import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import numpy as np,pandas as pd
from netCDF4 import Dataset
from thermal import lake_column
g=Grade()
def evaluate():
 t=(OUTPUT/'calibrated.nml').read_text();keys=['mixing','exchange','attenuation'];par=[float(re.search(k+r'\s*=\s*([0-9.eE+-]+)',t).group(1)) for k in keys]
 if not all(lo<=v<=hi for v,lo,hi in zip(par,[.02,.05,.08],[.5,.45,.6])):return 0
 forcing=pd.read_csv(TESTS/'forcing.csv')[['air_c','solar_w_m2','wind_m_s']].to_numpy();truth=lake_column(forcing,par)
 with Dataset(OUTPUT/'output.nc') as nc:
  s=np.asarray(nc['temperature'][:]);times=np.asarray(nc['time'][:]);depth=np.asarray(nc['depth'][:])
 if s.shape!=truth.shape or not np.isfinite(s).all() or not np.allclose(s,truth,atol=1e-6) or not np.array_equal(times,np.arange(len(forcing))) or not np.array_equal(depth,np.arange(16)+.5):return 0
 obs=pd.read_csv(TESTS/'observations.csv');rmse=float(np.sqrt(np.mean((s[obs.day.to_numpy(),obs.depth_index.to_numpy()]-obs.temperature_c.to_numpy())**2)));report=read_json(OUTPUT/'calibration_report.json')
 correctness=tree_score(report,{'rmse':rmse,'n_observations':len(obs),'parameters':dict(zip(keys,par))},atol=1e-6)
 return correctness*min(1,.08/max(rmse,1e-12))
g.check('参数约束、独立模型回放、完整NetCDF与观测RMSE',1,evaluate);g.finish()
