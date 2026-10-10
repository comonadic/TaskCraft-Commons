import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import xml.etree.ElementTree as E
edges={int(x.attrib['to_node']):x.attrib for x in E.parse(INPUT/'feeder_cim.xml').getroot()};loads=read_csv(INPUT/'transformers.csv');rows=[];planned={}
for t in loads:
 node=int(t['node']);freq=hours=plan=0
 while node:
  e=edges[node];rate=float(e['lambda']);freq+=rate;hours+=rate*(float(e['transfer_hours']) or float(e['repair_hours']));plan+=float(e['planned_hours']);node=int(e['from_node'])
 rows.append({'transformer_id':t['transformer_id'],'lambda_per_year':freq,'outage_hours':hours,'customers':int(t['customers']),'kw':float(t['kw'])});planned[t['transformer_id']]=plan
write_csv(OUTPUT/'loadpoint_metrics.csv',rows)
for cn in [False,True]:
 den=sum(x['customers'] if cn else 1 for x in rows);fi=sum(x['lambda_per_year']*(x['customers'] if cn else 1) for x in rows)/den;di=sum((x['outage_hours']+(planned[x['transformer_id']] if cn else 0))*(x['customers'] if cn else 1) for x in rows)/den;ens=sum(x['kw']*.6*(x['outage_hours']+(planned[x['transformer_id']] if cn else 0)) for x in rows);a={'SAIFI':fi,'SAIDI':di,'CAIDI':di/fi,'ASAI':1-di/8760,'ENS_kWh':ens}
 if cn:a['total_customers']=den
 write_json(OUTPUT/('cn_reliability_report.json' if cn else 'reliability_indices.json'),a)
(OUTPUT/'method.md').write_text('沿根到负荷点路径累计故障频率及转供或修复时长；原口径变压器等权且排除计划停电，企业合成口径按用户加权并纳入计划小时。ENS使用0.6负荷系数，单位kWh；不声称现行国家标准认证。')
