"""Synthetic G1 position-control experiments executed by MuJoCo."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import mujoco
from PIL import Image,ImageDraw
import imageio.v2 as imageio


def render_frame(model,data,time,case_id):
    im=Image.new('RGB',(640,480),'#e9eff3');d=ImageDraw.Draw(im)
    d.line((0,430,640,430),fill='#536b78',width=3)
    def point(v):return (int(310+v[0]*230+v[1]*60),int(430-v[2]*260))
    for i in range(1,model.nbody):
        parent=model.body_parentid[i]
        if parent>0:d.line((point(data.xpos[parent]),point(data.xpos[i])),fill='#16496a',width=7)
        x,y=point(data.xpos[i]);d.ellipse((x-4,y-4,x+4,y+4),fill='#b45b34')
    d.text((15,12),f'{case_id} | MuJoCo G1 | t={time:.2f}s | SYNTHETIC POLICY',fill='#152b38')
    return np.asarray(im)


def rollout(model_dir,case,output=None):
    m=mujoco.MjModel.from_xml_path(str(model_dir/'scene.xml'));d=mujoco.MjData(m)
    mujoco.mj_resetDataKeyframe(m,d,0)
    m.actuator_gainprm[:,0]*=case['gain_scale'];m.actuator_biasprm[:,1]*=case['gain_scale']
    default=m.key_ctrl[0].copy();ids=[m.actuator(i).name for i in range(m.nu)]
    chosen=[i for i,n in enumerate(ids) if 'shoulder_pitch' in n or 'elbow' in n]
    qpos_indices=[m.jnt_qposadr[m.actuator_trnid[i,0]] for i in range(m.nu)]
    base_id=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_BODY,'pelvis');rows=[];frames=[];dt=m.opt.timestep;stride=max(1,round(1/30/dt))
    for step in range(int(6/dt)):
        t=step*dt;target=default.copy();command=default.copy()
        for idx in chosen:
            target[idx]+=case['amplitude']*np.sin(2*np.pi*case['frequency']*t)
            command[idx]+=case['amplitude']*np.sin(2*np.pi*case['frequency']*max(0,t-case['delay']))
        d.ctrl[:]=command;d.xfrc_applied[:]=0
        if 2<=t<2.5:d.xfrc_applied[base_id,0]=case['push_newton']
        mujoco.mj_step(m,d)
        if step%stride==0:
            rmse=float(np.sqrt(np.mean((d.qpos[qpos_indices]-target)**2)));rows.append({'time':float(d.time),'base_height':float(d.xpos[base_id,2]),'joint_rmse':rmse,'base_x':float(d.xpos[base_id,0])});frames.append(render_frame(m,d,float(d.time),case['case_id']))
    stable=[r for r in rows if r['time']>=1];minimum=min(r['base_height'] for r in stable);rms=float(np.sqrt(np.mean([r['joint_rmse']**2 for r in stable])));fall=next((r['time'] for r in stable if r['base_height']<.45),None)
    metrics={'min_base_height':minimum,'tracking_rmse':rms,'fall_time':fall,'duration':rows[-1]['time'],'frames':len(frames)}
    if output is not None:
        output.mkdir(parents=True,exist_ok=True)
        with (output/'trajectory.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        imageio.mimwrite(output/'rollout.mp4',frames,fps=30,codec='libx264',quality=7,macro_block_size=1)
        for i in [30,90,150]:Image.fromarray(frames[min(i,len(frames)-1)]).save(output/f'frame_{i}.png')
    return metrics,frames


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--model-dir',type=Path,required=True);ap.add_argument('--cases',type=Path,required=True);ap.add_argument('--case-id',required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();c=next(x for x in json.loads(a.cases.read_text()) if x['case_id']==a.case_id);metrics,_=rollout(a.model_dir,c,a.output_dir);print(json.dumps({'run_complete':a.case_id,'frames':metrics['frames']}))
