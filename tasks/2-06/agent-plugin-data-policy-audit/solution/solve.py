import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

fields=read_json(INPUT/'action_data_entities.json');actions=read_json(INPUT/'action_metadata.json');tax={r['data_type']:r for r in read_csv(INPUT/'taxonomy.csv')};meta={a['action_id']:a for a in actions};v=[]
for f in fields:
 t=f['type'].strip().lower();rule=tax[t];a=meta[f['action_id']]
 if rule['severity']!='ALLOWED': v.append({'action_id':a['action_id'],'severity':rule['severity'],'policy_clause':rule['policy_clause'],'action_domain':a['domain'],'api_name':a['api_name'],'data_field_name':f['field'],'data_type':t})
write_json(OUTPUT/'policy_violations.json',{'total_violations':len(v),'severity_breakdown':{s:sum(x['severity']==s for x in v) for s in ['CRITICAL','HIGH']},'violations':v})
out=[]
for domain in sorted(set(a['domain'] for a in actions)):
 aa=[a for a in actions if a['domain']==domain];n=len({g for a in aa for g in a['agent_ids']});ds=[{f['type'].strip().lower() for f in fields if f['action_id']==a['action_id']} for a in aa]
 if n>=3:
  un=len(set().union(*ds));avg=sum(len(s) for s in ds)/len(ds);out.append({'domain':domain,'agent_count':n,'union_datatypes_count':un,'avg_datatypes_per_action':avg,'amplification':f'{un/avg:.3f}x'})
write_csv(OUTPUT/'cross_domain_exposure_report.csv',out)
