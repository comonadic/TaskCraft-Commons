import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from pypdf import PdfReader
manifest=read_json(INPUT/'filings/manifest.json'); labels=read_json(INPUT/'schema.json'); allrows={}
for m in manifest:
    txt='\n'.join(p.extract_text() for p in PdfReader(INPUT/'filings'/m['file']).pages)
    r={'filing_id':m['id'],'company':m['company'],'year':m['year'],'currency':'CNY'}
    for key,label in labels.items():
        token=re.search(re.escape(label)+r'\s*\|\s*([^\n]+)',txt).group(1).strip().replace(',','')
        val=0 if token=='-' else -float(token[1:-1]) if token.startswith('(') else float(token)
        r[key]=val*(10000 if m['amount_unit']=='万元' and key not in ['eps','shares'] else 1)
    allrows[m['id']]=r; write_json(OUTPUT/'extractions'/f"{m['id']}.json",r)
    (OUTPUT/'raw_extractions').mkdir(exist_ok=True); (OUTPUT/'raw_extractions'/f"{m['id']}.txt").write_text(txt)
for fid in read_json(INPUT/'validation.json'): write_json(OUTPUT/'run2_extractions'/f'{fid}.json',allrows[fid])
current=[x for x in allrows.values() if x['year']==2024]
qa={'q1':max(current,key=lambda x:x['revenue'])['company'],'q2':sum(x['operating_cashflow'] for x in current),'q3':{}}
for x in current:
    old=next(y for y in allrows.values() if y['company']==x['company'] and y['year']==2022)
    qa['q3'][x['company']]=(x['revenue']/old['revenue'])**.5-1
write_json(OUTPUT/'qa_answers.json',qa)
