import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

g=Grade()
g.check('期间口径与22个金额',.8,lambda:tree_score(read_json(OUTPUT/'balance_sheet.json'),read_json(TESTS/'expected.json'),atol=.01))
g.check('逐字段可定位证据',.2,lambda:tree_score(read_json(OUTPUT/'evidence.json'),read_json(TESTS/'quotes.json')))
g.finish()
