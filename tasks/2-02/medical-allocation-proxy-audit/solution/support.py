"""File contracts and explicit scoring helpers shared by TaskCraft verifiers."""
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
    with tempfile.TemporaryDirectory(prefix='taskcraft-replay-') as temp:
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
