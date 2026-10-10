import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import numpy as np,rhino3dm as rh
g=Grade();expected={x['id']:x['box'] for x in read_json(TESTS/'geometry.json')}
def bounds(vertices):
 a=np.array(vertices);lo=a.min(axis=0);return np.r_[lo,a.max(axis=0)-lo]
def native():
 m=rh.File3dm.Read(str(OUTPUT/'model.3dm'))
 if m.Settings.ModelUnitSystem!=rh.UnitSystem.Millimeters:return 0
 d={}
 for obj in m.Objects:
  mesh=obj.Geometry
  if not isinstance(mesh,rh.Mesh) or len(mesh.Faces)<6 or not mesh.IsClosed:return 0
  d[obj.Attributes.Name]=bounds([(v.X,v.Y,v.Z) for v in mesh.Vertices])
 return sum(k in d and np.allclose(d[k],v,atol=1,rtol=0) for k,v in expected.items())/max(len(d),len(expected))
def obj():
 verts=[];objects={};name=None
 for line in (OUTPUT/'model.obj').read_text().splitlines():
  s=line.split()
  if not s:continue
  if s[0]=='o':name=' '.join(s[1:]);objects[name]={'indices':set(),'faces':0,'edges':{}}
  elif s[0]=='v':verts.append(list(map(float,s[1:4])))
  elif s[0]=='f':
   if name is None:return 0
   ix=[int(v.split('/')[0])-1 for v in s[1:]]
   if len(ix)<3 or min(ix)<0 or max(ix)>=len(verts):return 0
   objects[name]['indices'].update(ix);objects[name]['faces']+=1
   for a,b in zip(ix,ix[1:]+ix[:1]):
    edge=tuple(sorted((a,b)));objects[name]['edges'][edge]=objects[name]['edges'].get(edge,0)+1
 if len(verts)<1000:return 0
 hits=0
 for k,v in expected.items():
  if k in objects:
   o=objects[k];a=[verts[i] for i in o['indices']];hits+=o['faces']>=6 and len(a)>=8 and all(n==2 for n in o['edges'].values()) and np.allclose(bounds(a),v,atol=1,rtol=0)
 return hits/max(len(objects),len(expected))
g.check('原生模型毫米坐标与全部实体',.5,native);g.check('OBJ实体与几何一致',.5,obj);g.finish()
