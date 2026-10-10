import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import geopandas as gpd
d=gpd.read_file(INPUT/'seq1524_cn.gpkg',layer='seq1524_cn');d=d[d.stable & (d.area_ha>=.5)].copy();codes={'rice','wheat','maize','soy','fallow'};audit=[]
for _,row in d.iterrows():
 c=[row[f'crop_{y}'] for y in range(2015,2025)];valid=[v for v in c if v in codes];run=best=0;last=None
 for v in c:
  run=run+1 if v==last and v in codes-{'fallow'} else 1 if v in codes-{'fallow'} else 0;best=max(best,run);last=v
 reasons=[];leg=c.count('soy');fal=c.count('fallow')
 if len(valid)<10:reasons.append('missing_or_unknown')
 if best>=4:reasons.append('monoculture')
 if leg==0:reasons.append('no_legume')
 if fal>=3:reasons.append('too_much_fallow')
 audit.append({'valid_years':len(valid),'distinct_crops':len(set(valid)-{'fallow'}),'max_consecutive':best,'rotation_changes':sum(a in codes and b in codes and a!=b for a,b in zip(c,c[1:])),'legume_years':leg,'fallow_years':fal,'risk_flag':bool(reasons),'risk_reasons':'|'.join(sorted(reasons))})
for k in audit[0]:d[k]=[a[k] for a in audit]
OUTPUT.mkdir(exist_ok=True);d.to_file(OUTPUT/'eligible_units.gpkg',layer='eligible_units',driver='GPKG');d[d.risk_flag].to_file(OUTPUT/'flagged_units.gpkg',layer='flagged_units',driver='GPKG')
