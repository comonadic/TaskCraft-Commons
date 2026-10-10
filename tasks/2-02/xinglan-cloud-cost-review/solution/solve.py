import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

rows=read_csv(INPUT/'usage.csv')+read_json(Path(__file__).parent/'image_transcription.json');prices={r['resource_type']:float(r['unit_price_cny']) for r in read_csv(INPUT/'pricing.csv')};out=[]
for r in rows:
 t=r['resource_type'];u=float(r['utilization_pct']);days=float(r['inactive_days']);ret=float(r['retention_days']);attached=str(r['attached']).lower()=='true';action=None;ratio=1
 if t=='CVM' and u<5 and days>=30:action,ratio='schedule_stop',.3
 elif t=='CDB' and u<10:action,ratio='downsize',.5
 elif t=='COS' and days>=30:action,ratio='archive',.25
 elif t=='NAT' and u==0 and days>=30:action,ratio='delete_idle',0
 elif t=='EIP' and not attached:action,ratio='release',0
 elif t=='LOG' and ret>30:action,ratio='shorten_retention',30/ret
 if action:
  cost=round(float(r['billable_units'])*prices[t],2);projected=round(cost*ratio,2);out.append({k:r[k] for k in ['resource_id','resource_type','name']}|{'action':action,'current_cost':cost,'projected_cost':projected,'monthly_savings':round(cost-projected,2)})
summary={k:round(sum(r[k] for r in out),2) for k in ['current_cost','projected_cost','monthly_savings']};summary['recommendation_count']=len(out)
write_json(OUTPUT/'optimization_report.json',{'executive_summary':summary,'recommendations':out});write_csv(OUTPUT/'savings_summary.csv',out)
