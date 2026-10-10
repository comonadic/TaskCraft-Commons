import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from xlsx_runtime import fill_xlsx
from html import unescape
contract=read_json(INPUT/'output_contract.json');values={}
for file in ['quote.html','statistics.html','annual_report.html']:
 txt=unescape(re.sub('<[^>]+>','\n',(INPUT/file).read_text()))
 for name,row in contract['cells'].items():
  m=re.search(re.escape(name)+r'\s*\|\s*([\d.]+)',txt)
  if m:values['B'+str(row)]=float(m.group(1))
formulas=read_json(Path(__file__).parent/'formula_plan.json')
for cell,formula in formulas.items():
 expr=re.sub(r'B\d+',lambda m:str(values[m.group(0)]),formula.lstrip('='));values[cell]=eval(expr,{'__builtins__':{}})
OUTPUT.mkdir(exist_ok=True);fill_xlsx(INPUT/'template.xlsx',OUTPUT/'CN_Financial_Summary.xlsx',values,formulas);write_json(OUTPUT/'sources.json',contract['sources'])
