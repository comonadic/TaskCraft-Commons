import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
"""File contracts and explicit scoring helpers shared by seed verifiers."""
import csv
import json
import math
import os
from pathlib import Path
import unicodedata
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager

ROOT=Path(os.environ.get('TASKCRAFT_ROOT','/app'))
INPUT=ROOT/'input'
OUTPUT=ROOT/'output'
if not OUTPUT.exists() and Path('/logs/artifacts').exists():
    for candidate in ['/logs/artifacts/app/output','/logs/artifacts/output']:
        if Path(candidate).is_dir():
            OUTPUT=Path(candidate)
            break
TESTS=Path(__file__).resolve().parent


@contextmanager
def replay(code, inputs, arguments=None, software=None, timeout=120):
    """Run submitted code without access to hidden gold in the Docker verifier.

    Local authoring checks run at the current UID; production verification runs
    as nobody in a fresh directory, while /tests is root-only. No network is
    available in the verifier container. This is not an adversarial OS sandbox.
    """
    with tempfile.TemporaryDirectory(prefix='ale-replay-') as temp:
        root=Path(temp);root.chmod(0o755)
        shutil.copytree(inputs,root/'input');(root/'output').mkdir()
        if software:shutil.copytree(software,root/'software')
        shutil.copyfile(code,root/'candidate.py')
        for p in root.rglob('*'):
            if p.is_symlink():raise ValueError('symlink in replay input')
            p.chmod(0o755 if p.is_dir() else 0o644)
        env={'PATH':os.environ.get('PATH','/usr/local/bin:/usr/bin:/bin'),'TASKCRAFT_ROOT':str(root),'HOME':str(root/'output'),'MPLCONFIGDIR':str(root/'output/mpl'),'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONNOUSERSITE':'1'}
        kwargs={}
        if os.geteuid()==0:
            (root/'output').chmod(0o777)
            kwargs={'user':65534,'group':65534,'extra_groups':[]}
        args=[sys.executable,str(root/'candidate.py')]+(arguments(root) if arguments else [])
        r=subprocess.run(args,cwd=root,env=env,capture_output=True,text=True,timeout=timeout,**kwargs)
        if r.returncode:raise ValueError('submitted program failed: '+r.stderr[-400:])
        yield root/'output'


def read_json(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def write_json(p,obj):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')


def read_csv(p,delimiter=','):
    with Path(p).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f,delimiter=delimiter))


def write_csv(p,rows,fields=None,delimiter=','):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    with Path(p).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),delimiter=delimiter)
        w.writeheader(); w.writerows(rows)


def equal(a,b,atol=1e-6,rtol=1e-5):
    if isinstance(b,bool):
        return a is b or (isinstance(a,str) and a.lower()==str(b).lower())
    if isinstance(b,(float,int)):
        try:
            x=float(a)
            return math.isfinite(x) and abs(x-b)<=atol+rtol*abs(b)
        except (ValueError,TypeError):
            return False
    return unicodedata.normalize('NFKC',str(a)).strip()==unicodedata.normalize('NFKC',str(b)).strip()


def tree_score(got,expected,atol=1e-6,rtol=1e-5):
    if isinstance(expected,dict):
        if not isinstance(got,dict): return 0.
        keys=set(got)|set(expected)
        return sum(tree_score(got.get(k),expected[k],atol,rtol) for k in expected)/max(1,len(keys))
    if isinstance(expected,list):
        if not isinstance(got,list): return 0.
        return sum(tree_score(a,b,atol,rtol) for a,b in zip(got,expected))/max(1,len(got),len(expected))
    return float(equal(got,expected,atol,rtol))


def record_score(got,expected,keys,atol=1e-6,rtol=1e-5):
    if not isinstance(got,list) or not isinstance(expected,list): return 0.
    def index(rows):
        result={}
        for r in rows:
            k=tuple(str(r.get(x,'')) for x in keys)
            if k in result: raise ValueError('duplicate record key')
            result[k]=r
        return result
    g,e=index(got),index(expected)
    return sum(tree_score(g.get(k),v,atol,rtol) for k,v in e.items())/max(1,len(set(g)|set(e)))


def f1_set(got,expected):
    a,b=set(got),set(expected)
    return 2*len(a&b)/max(1,len(a)+len(b))


class Grade:
    def __init__(self): self.items=[]
    def check(self,name,weight,fn):
        try:
            if OUTPUT.is_symlink() or any(p.is_symlink() for p in OUTPUT.rglob('*')):
                raise ValueError('symlinks are not accepted as submitted artifacts')
            v=fn()
            score=float(v)
            if not math.isfinite(score): raise ValueError('nonfinite score')
            self.items.append({'name':name,'weight':weight,'score':max(0.,min(1.,score))})
        except Exception as exc:
            self.items.append({'name':name,'weight':weight,'score':0.,'error':type(exc).__name__+': '+str(exc)[:300]})
    def finish(self):
        value=sum(x['score']*x['weight'] for x in self.items)/sum(x['weight'] for x in self.items)
        log=Path(os.environ.get('TASKCRAFT_LOG','/logs/verifier'))
        log.mkdir(parents=True,exist_ok=True)
        write_json(log/'score.json',{'reward':value,'checks':self.items})
        (log/'reward.txt').write_text(f'{value:.10f}\n')
        print(json.dumps({'reward':value,'checks':self.items},ensure_ascii=False))
        return value


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
