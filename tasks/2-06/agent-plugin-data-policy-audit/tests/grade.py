import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

e=read_json(TESTS/'expected.json');g=Grade()
g.check('字段级违规与条款',.65,lambda:record_score(read_json(OUTPUT/'policy_violations.json')['violations'],e['violations'],['action_id','data_field_name']))
g.check('严重性汇总',.1,lambda:tree_score({k:v for k,v in read_json(OUTPUT/'policy_violations.json').items() if k!='violations'},{'total_violations':len(e['violations']),'severity_breakdown':e['severity']}))
g.check('跨域放大率',.25,lambda:record_score(read_csv(OUTPUT/'cross_domain_exposure_report.csv'),e['exposure'],['domain']));g.finish()
