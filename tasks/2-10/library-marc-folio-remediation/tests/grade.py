import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import xml.etree.ElementTree as E
g=Grade();e=read_json(TESTS/'expected.json');out=OUTPUT/'submission/outputs/public_case'
def records():
 root=E.parse(out/'remediated_records.xml').getroot();rows=[]
 for r in root.findall('record'):
  def f(t,c):return r.find(f"datafield[@tag='{t}']/subfield[@code='{c}']").text
  rows.append({'id':r.find("controlfield[@tag='001']").text,'isbn':f('020','a'),'author':f('100','a'),'title':f('245','a'),'lang':f('041','a'),'url':f('856','u'),'branch':f('949','a')})
 return record_score(rows,e['records'],['id'])
g.check('400条字段修复',.3,records)
g.check('覆盖/创建/隔离决策',.2,lambda:record_score(read_csv(out/'overlay_decisions.csv'),e['decisions'],['record_id']))
def plans():
 p=read_json(out/'folio_import_plan.json');expected=[{'record_id':r['record_id'],'action':r['decision'],'instance_id':r['target_instance'],'branch':e['records'][i]['branch']} for i,r in enumerate(e['decisions'])];return record_score(p,expected,['record_id'])
g.check('导入计划',.1,plans)
def qa():
 a=read_json(out/'qa_report.json');counts={k:sum(x['decision']==k for x in e['decisions']) for k in ['quarantine','review','create','skip_protected','overlay']}
 return tree_score(a['decision_counts'],counts)*int(a['records']==400 and len(a['changes'])==400 and len((out/'remediation_summary.md').read_text())>40 and (OUTPUT/'submission/scripts/remediate_catalog.py').is_file())
g.check('QA与CLI材料',.1,qa)
def hidden():
 global out,e
 saved_out,saved_e=out,e
 try:
  with replay(OUTPUT/'submission/scripts/remediate_catalog.py',TESTS/'hidden_case',lambda root:['--case-dir',str(root/'input'),'--output-dir',str(root/'output')]) as generated:
   out=generated;e=read_json(TESTS/'hidden_expected.json')
   return .4*records()+.4*record_score(read_csv(out/'overlay_decisions.csv'),e['decisions'],['record_id'])+.2*plans()
 finally:out,e=saved_out,saved_e
g.check('80条隐藏案例CLI复跑',.3,hidden);g.finish()
