import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from pypdf import PdfReader
texts={f.stem:'\n'.join(x.extract_text() for x in PdfReader(f).pages) for f in INPUT.glob('D*.pdf')}
def val(pattern,doc): return float(re.search(pattern,texts[doc]).group(1))
rev=val(r'2024年收入：(\d+)', 'D02'); prior=val(r'2023年收入：(\d+)', 'D02'); cost=val(r'营业成本：([\d.]+)','D02');cash=val(r'年末现金：(\d+)','D02');debt=val(r'有息债务：(\d+)','D02')
burn=abs(val(r'经营现金流：(-?\d+)','D02'))+val(r'资本性支出：(\d+)','D02')
metrics={'revenue_growth':rev/prior-1,'gross_margin':1-cost/rev,'nrr':103.5/90,'top5_share':50/rev,'net_debt':debt-cash,'ev_revenue':(240+debt-cash)/rev,'annual_burn':burn,'runway_months':cash/burn*12}
thesis=[{'claim':'收入增长25%，需与每年翻倍的销售口径区分。','evidence':['D02:p1','D01:p2']},{'claim':'同一客户队列NRR为115%，有扩张能力。','evidence':['D03:p1']},{'claim':'集成能力得到部分受访客户认可，但访谈有选择偏差。','evidence':['D06:p1']}]
risks=[{'id':f'R{i}','description':d,'evidence':[f'D07:p{1 if i<4 else 2}']} for i,d in enumerate(['客户集中与续约风险','应收回款及现金消耗风险','访谈样本和市场估计偏差','奖励稀释与交易价格不完整'],1)]
questions=[{'id':f'Q{i}','description':d,'evidence':[f'D08:p{1 if i<3 else 2}']} for i,d in enumerate(['索取续约合同与回款流水','核查逾期账款回收','独立访谈与原始市场研究','补全期权奖励与费用'],1)]
a={'metrics':metrics,'thesis':thesis,'risks':risks,'diligence':questions,'recommendation':'Hold','reason':'增长与留存有吸引力，但大客户续约、回款及稀释未核实，应待尽调后决策。'}
for item in a['thesis']+a['risks']+a['diligence']:
 item['evidence_quotes']=[PdfReader(INPUT/(ref.split(':')[0]+'.pdf')).pages[int(ref.split(':p')[1])-1].extract_text().split('合成材料 / ALE-CN seed / 不对应真实主体')[-1].rsplit('第 ',1)[0].strip() for ref in item['evidence']]
write_json(OUTPUT/'analysis.json',a)
sections={'投资建议':a['recommendation']+'：'+a['reason'],'公司与产品':'云衡软件是合成制造业SaaS标的。[D01:p1]','投资论点':'\n'.join(t['claim']+' '+str(t['evidence']) for t in thesis),'财务分析':json.dumps(metrics,ensure_ascii=False)+' [D02:p1] [D02:p2] [D03:p1]','估值':'EV=240+18-30=228百万元，EV/收入=1.824倍。[D04:p1]','风险':json.dumps(risks,ensure_ascii=False),'待尽调':json.dumps(questions,ensure_ascii=False),'证据附录':'材料编号D01至D08，金额以百万元，年度2024。'}
(OUTPUT/'screening_memo.md').write_text('\n\n'.join('# '+k+'\n'+v for k,v in sections.items()))
