import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

e=read_json(TESTS/'expected.json');g=Grade()
def ids():
 r=read_csv(OUTPUT/'sa_aki_patients.csv');a=[x['subject_id'] for x in r]
 return f1_set(a,e['patients']) if len(a)==len(set(a)) and all(set(x)=={'subject_id'} for x in r) else 0
g.check('患者精确集合F1',.65,ids);g.check('720次住院起始与边界证据',.35,lambda:record_score(read_csv(OUTPUT/'phenotype_audit.csv'),e['audit'],['stay_id']));g.finish()
