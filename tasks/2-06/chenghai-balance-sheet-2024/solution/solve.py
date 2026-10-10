import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from pypdf import PdfReader
schema=read_json(INPUT/'schema.json'); pages=[p.extract_text() for p in PdfReader(INPUT/'chenghai_2024.pdf').pages]
answer={k:schema[k] for k in ['company','date','currency','unit']}; evidence={}
for field,label in schema['fields'].items():
    for page,txt in enumerate(pages[:2],1):
        match=re.search(r'(?m)^'+re.escape(label)+r'\s*\|\s*([-\d,.]+)\s*\|\s*([-\d,.]+)',txt)
        if match:
            answer[field]=float(match.group(1).replace(',',''))*10000
            evidence[field]={'page':page,'quote':match.group(0),'source':'chenghai_2024.pdf'}
            break
write_json(OUTPUT/'balance_sheet.json',answer); write_json(OUTPUT/'evidence.json',evidence)
