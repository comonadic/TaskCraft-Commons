import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import pandas as pd
d=pd.read_parquet(INPUT/'unified_profiles.parquet');d=d[(d.transaction_count_90d>=8)&(d.spend_90d>=3000)&d.email_opens_30d.eq(0)&~d.active_support].copy()
d['sms_eligible']=d.sms_opt_in.eq(True)&~d.sms_opt_out&d.phone_present;d['push_eligible']=d.push_opt_in.eq(True)&~d.push_opt_out&d.push_token_present;d['any_channel_eligible']=d.sms_eligible|d.push_eligible
cols=['customer_id','transaction_count_90d','spend_90d','email_opens_30d','sms_eligible','push_eligible','any_channel_eligible'];OUTPUT.mkdir(exist_ok=True);d[cols].to_csv(OUTPUT/'audience_roster.csv',index=False)
write_json(OUTPUT/'segment_definition.json',{'as_of':'2025-03-31','audience_count':len(d),'sms_count':int(d.sms_eligible.sum()),'push_count':int(d.push_eligible.sum()),'any_channel_count':int(d.any_channel_eligible.sum())})
segments=pd.read_csv(INPUT/'existing_segments.csv');ids=set(d.customer_id);over=[]
for sid,s in segments.groupby('segment_id'):
 n=len(ids&set(s.customer_id));over.append({'segment_id':sid,'overlap_count':n,'overlap_pct':round(n/len(ids)*100,6)})
write_csv(OUTPUT/'overlap_report.tsv',over,delimiter='\t')
