import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from xlsx_runtime import read_xlsx
e=read_json(TESTS/'expected.json');g=Grade()
def col(n):
 s=''
 while n:n,r=divmod(n-1,26);s=chr(65+r)+s
 return s
def score():
 d,_=read_xlsx(OUTPUT/'ai_addiction_annotations_output.xlsx');correct=0
 for row,meta in e['metadata'].items():
  if any(d.get(col(i+1)+row)!=v for i,v in enumerate(meta)):return 0
  got=[d.get(col(j)+row) for j in range(6,45)]
  if not all(isinstance(x,bool) for x in got) or sum(got[:3])!=1:return 0
  correct+=sum(a==b for a,b in zip(got,e['booleans'][row]))
 return correct/3705
g.check('元数据保真、焦点唯一与3705格编码',1,score);g.finish()
