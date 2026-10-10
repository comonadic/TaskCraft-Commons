import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import pandas as pd
stays=pd.read_csv(INPUT/'his_icu_stays.csv'); labs=pd.read_csv(INPUT/'lis_labs.csv'); urine=pd.read_csv(INPUT/'nursing_urine.csv'); inf=pd.read_csv(INPUT/'infection_orders.csv');sofa=pd.read_csv(INPUT/'sofa_assessments.csv');rows=[];patients=set()
for s in stays.itertuples():
 a=inf[(inf.icu_id==s.icu_id)&inf.suspected_infection.eq(1)].merge(sofa[sofa.icu_id==s.icu_id],on=['icu_id','hour']);a=a[a.current_sofa-a.baseline_sofa>=2];sh=None if a.empty else float(a.hour.min())
 l=labs[(labs.icu_id==s.icu_id)&(labs.specimen_hour<=s.discharge_hour)].copy();l['v']=l.result_value/l.unit.map({'umol/L':88.4,'mg/dL':1.})
 hits=[]
 if pd.notna(s.baseline_creatinine_mg_dl):
  b=s.baseline_creatinine_mg_dl;hits=list(l[(l.v-b>=.3-1e-6)|(l.v>=1.5*b-1e-6)].specimen_hour)
 u=urine[urine.icu_id==s.icu_id].sort_values('hour_ending');mean=u.urine_ml.rolling(6).mean()/s.weight_kg;hits+=list(u[(mean<.5)&(u.hour_ending<=s.discharge_hour)].hour_ending)
 ah=min(hits) if hits else None;eligible=sh is not None and ah is not None and 0<=ah-sh<=168
 reason='eligible' if eligible else 'no_sepsis' if sh is None else 'no_aki' if ah is None else 'aki_before_sepsis' if ah<sh else 'outside_7d'
 rows.append({'stay_id':s.icu_id,'sepsis_hour':'' if sh is None else sh,'aki_hour':'' if ah is None else ah,'eligible':eligible,'reason':reason})
 if eligible:patients.add(s.patient_id)
write_csv(OUTPUT/'sa_aki_patients.csv',[{'subject_id':x} for x in sorted(patients)]);write_csv(OUTPUT/'phenotype_audit.csv',rows)
