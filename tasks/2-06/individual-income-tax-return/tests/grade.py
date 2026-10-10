import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from PIL import Image
e=read_json(TESTS/'expected.json');g=Grade()
g.check('三人申报字段与税额',.95,lambda:sum(tree_score(read_json(OUTPUT/'returns'/f"{r['taxpayer_id']}.json"),r,atol=.01,rtol=0) for r in e)/3)
def images():
 for r in e:
  im=Image.open(OUTPUT/'screenshots'/f"{r['taxpayer_id']}.png");im.verify()
  if im.width<800 or im.height<500:return 0
 return 1
g.check('提交截图可读取',.05,images);g.finish()
