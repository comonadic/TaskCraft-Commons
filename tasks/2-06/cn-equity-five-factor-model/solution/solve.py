import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import pandas as pd
df=pd.read_csv(INPUT/'monthly_stock_panel.csv'); rf=pd.read_csv(INPUT/'risk_free.csv').set_index('date').rf_decimal; out=[]; audits=[]
for date,full in df.groupby('date',sort=True):
    d=full[(full.financials_visible==1)&(full.tradable==1)].copy(); d['size']=(d.begin_market_cap>d.begin_market_cap.median()).map({False:'S',True:'B'})
    factors={}; sizes=[]
    for key,name in [('book_to_market','HML'),('operating_profitability','RMW'),('asset_growth','CMA')]:
        low,high=d[key].quantile([.3,.7]); d['group']=d[key].apply(lambda x:'L' if x<=low else 'H' if x>high else 'M')
        cells={}
        for (sz,gr),z in d.groupby(['size','group']): cells[sz+gr]=(z.begin_market_cap*z.return_decimal).sum()/z.begin_market_cap.sum()
        factors[name]=(cells['SH']+cells['BH']-cells['SL']-cells['BL'])/2*(1 if name!='CMA' else -1)*100
        sizes.append(sum(cells['S'+g]-cells['B'+g] for g in 'LMH')/3)
    out.append({'date':date,'MKT_RF':((d.begin_market_cap*d.return_decimal).sum()/d.begin_market_cap.sum()-rf[date])*100,'SMB':sum(sizes)/3*100,**factors})
    audits.append({'date':date,'eligible_count':len(d),'late_filing_excluded_count':int((full.financials_visible==0).sum())})
write_csv(OUTPUT/'ff5_factors_monthly_2015_onward.csv',out,['date','MKT_RF','SMB','HML','RMW','CMA']);write_json(OUTPUT/'method_audit.json',audits)
