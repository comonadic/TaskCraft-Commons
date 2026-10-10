import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

expected=read_json(TESTS/'expected.json'); g=Grade()
def extracts():
    rows=expected['filings']; count=len(list((OUTPUT/'extractions').glob('*.json')))
    return sum(tree_score(read_json(OUTPUT/'extractions'/f'{k}.json'),v,atol=.01) for k,v in rows.items())/max(len(rows),count)
def evidence():
    scores=[]
    for fid,row in expected['filings'].items():
        t=(OUTPUT/'raw_extractions'/f'{fid}.txt').read_text()
        scores.append(all(x in t for x in [row['company'],str(row['year']),'合并利润','合并现金流量','营业收入']))
    return sum(scores)/len(scores)
g.check('18份完整字段抽取',.6,extracts)
g.check('证据覆盖',.1,evidence)
g.check('三项跨报告问答',.2,lambda:tree_score(read_json(OUTPUT/'qa_answers.json'),expected['qa'],atol=.01))
g.check('五份复跑内容正确且一致',.1,lambda:sum(tree_score(read_json(OUTPUT/'run2_extractions'/f'{k}.json'),expected['filings'][k],atol=.01) for k in expected['validation'])/5)
g.finish()
