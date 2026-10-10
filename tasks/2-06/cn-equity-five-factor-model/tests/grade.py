import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

g=Grade();g.check('134个月五因子数值与集合',.9,lambda:record_score(read_csv(OUTPUT/'ff5_factors_monthly_2015_onward.csv'),read_json(TESTS/'expected.json'),['date'],atol=1e-5,rtol=0))
g.check('时点筛选审计',.1,lambda:record_score(read_json(OUTPUT/'method_audit.json'),read_json(TESTS/'audit.json'),['date']));g.finish()
