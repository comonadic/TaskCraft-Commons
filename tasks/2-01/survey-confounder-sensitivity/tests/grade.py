import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

e=read_json(TESTS/'expected.json');g=Grade();g.check('完整病例与字段',.4,lambda:record_score(read_csv(OUTPUT/'hpyl_nsaid_subset.csv'),e['subset'],['id']));g.check('三模型估计与变化',.6,lambda:record_score(read_csv(OUTPUT/'sensitivity_summary.csv'),e['models'],['model'],atol=1e-5));g.finish()
