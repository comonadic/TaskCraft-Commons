import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from model_writer import build
parts=[]
def add(name,x,y,z,a,b,c):parts.append({'id':name,'box':[x,y,z,a,b,c]})
for x in range(7):
 for y in range(5):add(f'H_COL_{x}_{y}',6000*x,5000*y,0,400,400,12000)
for l in range(3):
 z=l*6000;add(f'H_SLAB_{l}',0,0,z,36400,20400,250)
 for x in range(6):
  for y in range(5):add(f'H_BEAMX_{l}_{x}_{y}',6000*x+400,5000*y,z+250,5600,400,500)
 for x in range(7):
  for y in range(4):add(f'H_BEAMY_{l}_{x}_{y}',6000*x,5000*y+400,z+250,400,4600,500)
add('H_NORTH_WALL',0,20400,0,36400,250,12500)
for x in range(12):add(f'H_GLASS_{x}',3000*x,0,500,2950,80,5500)
for l in range(7):
 add(f'T_SLAB_{l}',42000,0,4000*l,12400,10400,250)
 if l<6:
  for x in range(3):
   for y in range(3):add(f'T_COL_{l}_{x}_{y}',42000+6000*x,5000*y,4000*l+250,400,400,3750)
  add(f'T_CORE_{l}',46200,4000,4000*l+250,4000,3000,3750)
build(parts,OUTPUT)
