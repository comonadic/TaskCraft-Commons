import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

e=read_json(TESTS/'expected.json');g=Grade();g.check('全部共同cell的评分',.75,lambda:record_score(read_csv(OUTPUT/'per_cell_scores.csv'),e['cells'],['model','location','target_date','horizon'],atol=1e-6));g.check('模型汇总和相对WIS',.25,lambda:record_score(read_csv(OUTPUT/'submission.csv'),e['summary'],['model'],atol=1e-6));g.finish()
