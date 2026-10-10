import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

rows=read_csv(INPUT/'patients.csv');need={x['patient_id']:2*int(x['chronic_count'])+3*int(x['acute_events'])+int(x['functional_limitations']) for x in rows};b=sorted(rows,key=lambda x:(-float(x['baseline_score']),x['patient_id']))[:1200];r=sorted(rows,key=lambda x:(-need[x['patient_id']],x['patient_id']))[:1200];bi={x['patient_id'] for x in b};ri={x['patient_id'] for x in r}
write_csv(OUTPUT/'full_predictions.csv',[{'patient_id':x['patient_id'],'baseline_score':x['baseline_score'],'revised_score':need[x['patient_id']],'baseline_selected':x['patient_id'] in bi,'revised_selected':x['patient_id'] in ri} for x in rows])
for name,sel in [('baseline',b),('revised',r)]:
 a=sum(x['group']=='A' for x in sel);total=sum(need[x['patient_id']] for x in sel);write_json(OUTPUT/f'{name}_report.json',{'selected_count':len(sel),'group_a_share':a/len(sel),'group_b_share':1-a/len(sel),'mean_need':total/len(sel),'total_need_captured':total})
(OUTPUT/'analysis.md').write_text('该合成机制中，费用同时受健康需要和获取服务机会影响。按费用排序低估了B组的需要，改用题设临床需要指数可增加疾病负担覆盖。实验群体不对应任何现实人群，不能外推因果结论。')
