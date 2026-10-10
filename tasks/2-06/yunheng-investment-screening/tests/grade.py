import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

g=Grade()
g.check('八项财务计算',.45,lambda:tree_score(read_json(OUTPUT/'analysis.json')['metrics'],read_json(TESTS/'expected.json')))
def evidence():
    a=read_json(OUTPUT/'analysis.json'); ok=0;total=0
    for item in a['thesis']+a['risks']+a['diligence']:
        total+=1
        refs=item.get('evidence',[])
        quotes=item.get('evidence_quotes',[]);valid=bool(refs) and len(quotes)==len(refs)
        pages=read_json(TESTS/'documents.json')
        for ref,quote in zip(refs,quotes):
            match=re.fullmatch(r'(D0[1-8]):p([1-3])',ref)
            if not match or int(match[2])>len(pages[match[1]]):valid=False;continue
            normalize=lambda s:re.sub(r'\s+','',s)
            valid=valid and len(quote)>=12 and normalize(quote) in normalize(''.join(pages[match[1]][int(match[2])-1]))
        ok+=valid and len(item.get('claim',item.get('description','')))>=8
    return ok/max(11,total) if len(a['thesis'])>=3 else 0
g.check('论点与证据结构',.15,evidence)
g.check('四类风险覆盖',.1,lambda:f1_set([x['id'] for x in read_json(OUTPUT/'analysis.json')['risks']],['R1','R2','R3','R4']))
g.check('四项待尽调',.1,lambda:f1_set([x['id'] for x in read_json(OUTPUT/'analysis.json')['diligence']],['Q1','Q2','Q3','Q4']))
def memo():
    t=(OUTPUT/'screening_memo.md').read_text(); a=read_json(OUTPUT/'analysis.json')
    return all('# '+s in t for s in ['投资建议','公司与产品','投资论点','财务分析','估值','风险','待尽调','证据附录']) and a['recommendation'] in ['Go','No-Go','Hold'] and a['recommendation'] in t and len(a['reason'])>=20
g.check('完整中文备忘录及明确建议',.2,memo);g.finish()
