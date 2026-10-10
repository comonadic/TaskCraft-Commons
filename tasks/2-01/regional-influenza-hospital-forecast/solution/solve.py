import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import numpy as np
import pandas as pd
def forecast(input_dir,output_dir):
 d=pd.read_csv(input_dir/'history.csv');rows=[]
 for loc,z in d.groupby('location'):
  z=z.dropna();w=z.week.to_numpy();y=z.admissions.to_numpy();X=np.column_stack([np.ones(len(w)),w,np.sin(2*np.pi*w/52),np.cos(2*np.pi*w/52)]);coef=np.linalg.lstsq(X,y,rcond=None)[0];res=y-X@coef;sd=max(6,float(np.std(res,ddof=4)))
  for h in range(1,5):
   t=103+h;point=max(0,float(np.array([1,t,np.sin(2*np.pi*t/52),np.cos(2*np.pi*t/52)])@coef));spread=1.96*sd*(1+h/104)**.5;rows.append({'location':loc,'horizon':h,'point':point,'lower95':max(0,point-spread),'upper95':point+spread})
 write_csv(output_dir/'submission.csv',rows)
forecast(INPUT,OUTPUT)
(OUTPUT/'method.md').write_text('拟合线性趋势与52周正余弦季节项，缺报删除；残差标准差估计95%区间并随预测期扩张。所有数据来自可见历史。')
(OUTPUT/'forecast.py').write_text(Path(__file__).read_text().replace('from support import *', (Path(__file__).parent/'support.py').read_text(),1) if (Path(__file__).parent/'support.py').exists() else Path(__file__).read_text())
