import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from xlsx_runtime import read_xlsx
from formula_check import equivalence
g=Grade();e=read_json(TESTS/'expected.json');f=read_json(TESTS/'formulas.json')
g.check('全部输入与派生数值',.65,lambda:tree_score({k:read_xlsx(OUTPUT/'CN_Financial_Summary.xlsx')[0].get(k) for k in e},e))
g.check('动态公式四组扰动等价',.25,lambda:equivalence(read_xlsx(OUTPUT/'CN_Financial_Summary.xlsx')[1],f,e))
g.check('来源与时点',.1,lambda:tree_score(read_json(OUTPUT/'sources.json'),{'quote_time':'2025-03-31 15:00','company':'澄海精密','currency':'CNY','pages':['quote.html','statistics.html','annual_report.html']}));g.finish()
