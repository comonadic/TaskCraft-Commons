import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import numpy as np
sys.path.insert(0,str(ROOT/'software'));from g1_runner import rollout
reports=[]
for c in read_json(INPUT/'cases.json'):
 m,frames=rollout(INPUT/'g1',c,OUTPUT/'visual_demos'/c['case_id']);fallen=m['fall_time'] is not None;verdict='failed' if fallen or m['tracking_rmse']>.35 else 'successful' if m['tracking_rmse']<=.15 else 'nearly_successful'
 observation=(f"在{m['fall_time']:.2f}秒首次跌倒，基座高度降到阈值以下。" if fallen else '六秒回放保持站立，没有触发跌倒阈值。')+f"关节跟踪误差为{m['tracking_rmse']:.4f}弧度，最小基座高度{m['min_base_height']:.4f}米。"
 reports.append({'case_id':c['case_id'],'verdict':verdict,'observation':observation,'evidence':{k:m[k] for k in ['min_base_height','tracking_rmse','fall_time']}})
write_json(OUTPUT/'policy_evaluation_report.json',reports)
