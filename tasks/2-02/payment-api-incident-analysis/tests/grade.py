import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

e=read_json(TESTS/'expected.json');g=Grade()
def roots():
 a=read_json(OUTPUT/'root_cause_analysis.json');rows=[]
 for r in a['roots']:
  d={k:r[k] for k in ['type','resource','evidence_file','evidence_quote']};rows.append(d)
 return record_score(rows,e['roots'],['type'])
g.check('根因与逐字证据',.5,roots)
g.check('受影响资源',.1,lambda:f1_set(read_json(OUTPUT/'root_cause_analysis.json')['affected_resources'],e['affected_resources']))
def params():
 a=read_json(OUTPUT/'root_cause_analysis.json');merged={}
 for r in a['remediation']:
  if not isinstance(r['priority'],int) or len(r['action'])<8:return 0
  merged.update(r['parameters'])
 return tree_score(merged,e['parameters'])
g.check('中文整改结构化参数',.25,params)
g.check('回滚版本与镜像',.1,lambda:tree_score({k:read_json(OUTPUT/'root_cause_analysis.json')['rollback'][k] for k in e['rollback']},e['rollback']))
g.check('诊断摘要与验证步骤',.05,lambda:len(read_json(OUTPUT/'root_cause_analysis.json')['summary'])>=20 and len(read_json(OUTPUT/'root_cause_analysis.json')['rollback']['verify'])>=10);g.finish()
