import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import pandas as pd,numpy as np
import statsmodels.api as sm
d=pd.read_csv(INPUT/'demographics.csv').merge(pd.read_csv(INPUT/'questionnaire.csv'),on='id').merge(pd.read_csv(INPUT/'labs.csv'),on='id');med=pd.read_csv(INPUT/'medications.csv');flags={}
for pid,z in med.groupby('id'):flags[pid]=int(((z.drug_class=='NSAID')&z.current_use.eq(1)).any()) if z.ascertained.eq(1).all() else np.nan
d['nsaid']=d.id.map(flags);d=d[(d.age>=18)&d.weight.gt(0)];sub=d.dropna();out=[]
for m,z,cols in [('M1',d,['multimorbidity','age','sex','bmi']),('M2',sub,['multimorbidity','age','sex','bmi']),('M3',sub,['multimorbidity','age','sex','bmi','hpyl','nsaid'])]:
 fit=sm.GLM(z.ulcer,sm.add_constant(z[cols]),family=sm.families.Binomial(),freq_weights=z.weight).fit();b=fit.params['multimorbidity'];se=fit.bse['multimorbidity'];o=float(np.exp(b));out.append({'model':m,'n':len(z),'odds_ratio':o,'ci_low':float(np.exp(b-1.959963984540054*se)),'ci_high':float(np.exp(b+1.959963984540054*se)),'p_value':float(fit.pvalues['multimorbidity']),'or_change_pct':0 if not out else (o/out[0]['odds_ratio']-1)*100})
OUTPUT.mkdir(exist_ok=True);sub[['id','ulcer','multimorbidity','age','sex','bmi','weight','hpyl','nsaid']].to_csv(OUTPUT/'hpyl_nsaid_subset.csv',index=False);write_csv(OUTPUT/'sensitivity_summary.csv',out)
