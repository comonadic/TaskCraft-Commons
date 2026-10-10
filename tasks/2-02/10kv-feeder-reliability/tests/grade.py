import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

e=read_json(TESTS/'expected.json');g=Grade();g.check('负荷点路径累计',.4,lambda:record_score(read_csv(OUTPUT/'loadpoint_metrics.csv'),e['points'],['transformer_id']));g.check('等权指标',.25,lambda:tree_score(read_json(OUTPUT/'reliability_indices.json'),e['original']));g.check('用户加权及计划停电',.3,lambda:tree_score(read_json(OUTPUT/'cn_reliability_report.json'),e['cn']));g.check('方法说明',.05,lambda:len((OUTPUT/'method.md').read_text())>=60);g.finish()
