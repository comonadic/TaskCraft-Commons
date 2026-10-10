import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from pypdf import PdfReader
from playwright.sync_api import sync_playwright
import shutil
OUTPUT.mkdir(exist_ok=True);(OUTPUT/'returns').mkdir(exist_ok=True);(OUTPUT/'screenshots').mkdir(exist_ok=True)
with sync_playwright() as pw:
 executable=shutil.which('chromium') or shutil.which('chromium-browser')
 if not executable and Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome').exists():executable='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
 browser=pw.chromium.launch(headless=True,**({'executable_path':executable} if executable else {}),args=['--no-sandbox']);page=browser.new_page(viewport={'width':1100,'height':950})
 page.goto((INPUT/'tax_form.html').as_uri())
 for tid in ['T001','T002','T003']:
  rows=read_csv(INPUT/f'{tid}_payroll.csv');income=round(sum(float(x['salary']) for x in rows),2);special=round(sum(float(x['social_insurance_housing']) for x in rows),2);prepaid=round(sum(float(x['withheld_tax']) for x in rows),2)
  txt=''.join(p.extract_text() for p in PdfReader(INPUT/f'{tid}_deductions.pdf').pages);extra=float(re.search(r'专项附加扣除：(\d+)',txt).group(1));taxable=max(0,income-60000-special-extra)
  rate,quick=next((r,q) for top,r,q in [(36000,.03,0),(144000,.1,2520),(300000,.2,16920),(420000,.25,31920),(660000,.3,52920),(960000,.35,85920),(float('inf'),.45,181920)] if taxable<=top);due=round(taxable*rate-quick,2)
  vals={'income':income,'special_deduction':special,'additional_deduction':extra,'taxable_income':taxable,'tax_due':due,'prepaid':prepaid,'balance':round(due-prepaid,2)}
  page.select_option('#taxpayer_id',tid)
  for k,v in vals.items():page.fill('#'+k,str(v))
  page.screenshot(path=str(OUTPUT/'screenshots'/f'{tid}.png'),full_page=True)
  with page.expect_download() as info:page.get_by_text('保存结果',exact=True).click()
  info.value.save_as(OUTPUT/'returns'/f'{tid}.json')
 browser.close()
