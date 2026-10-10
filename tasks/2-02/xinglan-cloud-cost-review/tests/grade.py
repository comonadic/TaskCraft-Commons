import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

e=read_json(TESTS/'expected.json');g=Grade()
g.check('浪费资源覆盖F1',.3,lambda:f1_set([r['resource_id'] for r in read_csv(OUTPUT/'savings_summary.csv')],[r['resource_id'] for r in e]))
def subset(cols):return record_score([{k:r[k] for k in cols} for r in read_csv(OUTPUT/'savings_summary.csv')],[{k:r[k] for k in cols} for r in e],['resource_id'],atol=.01,rtol=0)
g.check('动作',.3,lambda:subset(['resource_id','action']))
g.check('逐资源费用与节约',.25,lambda:subset(['resource_id','current_cost','projected_cost','monthly_savings']))
def report():
 a=read_json(OUTPUT/'optimization_report.json');summary={k:round(sum(r[k] for r in e),2) for k in ['current_cost','projected_cost','monthly_savings']};summary['recommendation_count']=len(e)
 return .5*tree_score(a['executive_summary'],summary,atol=.01)+.5*record_score(a['recommendations'],e,['resource_id'],atol=.01)
g.check('摘要与双产物完整性',.15,report);g.finish()
