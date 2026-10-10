import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from pypdf import PdfReader
pages={f.stem:[p.extract_text() for p in PdfReader(f).pages] for f in INPUT.glob('?.pdf')}
findings=[{'subject': '云汐设备股权转让', 'field': 'amount', 'values': ['24000万元', '2.6亿元'], 'evidence': [{'document': 'A.pdf', 'page': 1, 'quote': '本次交易对价为人民币24000万元。'}, {'document': 'B.pdf', 'page': 1, 'quote': '本次交易对价为人民币2.6亿元。'}]}, {'subject': '云汐设备股权转让', 'field': 'ownership', 'values': ['30%', '35%'], 'evidence': [{'document': 'A.pdf', 'page': 1, 'quote': '受让方拟取得标的公司30%股权。'}, {'document': 'C.pdf', 'page': 1, 'quote': '权益变动完成后青岚产业持股比例为35%。'}]}, {'subject': '云汐设备股权转让', 'field': 'share_count', 'values': ['3000万股', '3200万股'], 'evidence': [{'document': 'A.pdf', 'page': 2, 'quote': '转让股数为3000万股，每股价格8元。'}, {'document': 'D.pdf', 'page': 1, 'quote': '受让股数为3200万股。'}]}, {'subject': '云汐设备股权转让', 'field': 'approval_date', 'values': ['2024年11月18日', '2024年11月19日'], 'evidence': [{'document': 'A.pdf', 'page': 2, 'quote': '董事会审议日期为2024年11月18日。'}, {'document': 'D.pdf', 'page': 2, 'quote': '董事会审议日期为2024年11月19日。'}]}]
for f in findings:
    for e in f['evidence']:
        if e['quote'] not in pages[e['document'][0]][e['page']-1]: raise ValueError('source evidence changed')
write_json(OUTPUT/'findings.json',findings)
report='# 股权转让一致性审计\n\n四份合成公告交叉核对。\n'
for i,f in enumerate(findings,1):
    report+=f"\n## 发现{i}：{f['field']}\n同一交易存在互不相容的陈述：{' 与 '.join(f['values'])}。\n"
    for e in f['evidence']: report+=f"- [{e['document']}:p{e['page']}] {e['quote']}\n"
report+='\n## 核对说明\n员工数截止日不同且新增人数可调节；净资产显示为四舍五入；30日付款描述一致，均不作为错误发现。\n'
(OUTPUT/'audit_report.md').write_text(report)
