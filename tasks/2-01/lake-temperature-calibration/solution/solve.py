import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import numpy as np,pandas as pd
from scipy.optimize import least_squares
from netCDF4 import Dataset
sys.path.insert(0,str(ROOT/'software'));from thermal import lake_column
f=pd.read_csv(INPUT/'forcing.csv');forcing=f[['air_c','solar_w_m2','wind_m_s']].to_numpy();o=pd.read_csv(INPUT/'observations.csv');day=o.day.to_numpy();z=o.depth_index.to_numpy();target=o.temperature_c.to_numpy()
fit=least_squares(lambda x:lake_column(forcing,x)[day,z]-target,[.07,.12,.4],bounds=([.02,.05,.08],[.5,.45,.6]),xtol=1e-8,ftol=1e-8);params=fit.x;sim=lake_column(forcing,params);rmse=float(np.sqrt(np.mean((sim[day,z]-target)**2)));OUTPUT.mkdir(exist_ok=True)
(OUTPUT/'calibrated.nml').write_text('&lake\n'+''.join(f' {k}={v:.12f}\n' for k,v in zip(['mixing','exchange','attenuation'],params))+'/\n')
with Dataset(OUTPUT/'output.nc','w') as nc:
 nc.createDimension('time',len(f));nc.createDimension('depth',16);tv=nc.createVariable('time','i4',('time',));tv.units='days since 2009-01-01';tv[:]=np.arange(len(f));dv=nc.createVariable('depth','f8',('depth',));dv.units='m';dv[:]=np.arange(16)+.5;v=nc.createVariable('temperature','f8',('time','depth'));v.units='degree_Celsius';v[:]=sim
write_json(OUTPUT/'calibration_report.json',{'rmse':rmse,'n_observations':len(o),'parameters':dict(zip(['mixing','exchange','attenuation'],map(float,params)))})
