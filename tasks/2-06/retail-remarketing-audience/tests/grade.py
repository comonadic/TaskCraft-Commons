import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

e=read_json(TESTS/'expected.json');g=Grade()
g.check('精确受众与渠道资格',.65,lambda:record_score(read_csv(OUTPUT/'audience_roster.csv'),e['roster'],['customer_id']))
g.check('分群摘要',.15,lambda:tree_score(read_json(OUTPUT/'segment_definition.json'),e['definition']))
g.check('正确分母重叠率',.2,lambda:record_score(read_csv(OUTPUT/'overlap_report.tsv','\t'),e['overlap'],['segment_id'],atol=1e-6));g.finish()
