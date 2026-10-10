import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import numpy as np
import imageio.v2 as imageio
from g1_runner import rollout
g=Grade()
def evaluate():
 reports=read_json(OUTPUT/'policy_evaluation_report.json');d={x['case_id']:x for x in reports};cases=read_json(TESTS/'cases.json')
 if len(d)!=8 or len(reports)!=8:return 0
 total=0
 for c in cases:
  m,frames=rollout(TESTS/'g1',c);r=d[c['case_id']];fall=m['fall_time'] is not None;label='failed' if fall or m['tracking_rmse']>.35 else 'successful' if m['tracking_rmse']<=.15 else 'nearly_successful'
  ev=tree_score(r['evidence'],{k:m[k] for k in ['min_base_height','tracking_rmse','fall_time']},atol=1e-4)
  trajectory=read_csv(OUTPUT/'visual_demos'/c['case_id']/'trajectory.csv')
  if len(trajectory)!=m['frames']:continue
  stable=[x for x in trajectory if float(x['time'])>=1]
  calculated={'min_base_height':min(float(x['base_height']) for x in stable),'tracking_rmse':float(np.sqrt(np.mean([float(x['joint_rmse'])**2 for x in stable]))),'fall_time':next((float(x['time']) for x in stable if float(x['base_height'])<.45),None)}
  if tree_score(calculated,{k:m[k] for k in calculated},atol=1e-4)<.999999:continue
  video=imageio.get_reader(OUTPUT/'visual_demos'/c['case_id']/'rollout.mp4');meta=video.get_meta_data()
  valid=meta.get('duration',0)>5.7
  for idx in [30,90,150]:
   f=video.get_data(idx);valid=valid and f.shape==frames[idx].shape and float(np.mean((f.astype(float)-frames[idx].astype(float))**2))<250
  video.close()
  if valid:total+=.7*int(r['verdict']==label)+.3*ev*int(len(r['observation'])>=20)
 return total/8
g.check('独立MuJoCo回放、视频内容、中文证据与分类',1,evaluate);g.finish()
