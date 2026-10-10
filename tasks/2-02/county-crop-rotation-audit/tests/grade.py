import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import geopandas as gpd
e=read_json(TESTS/'expected.json');g=Grade()
def audit():
 d=gpd.read_file(OUTPUT/'eligible_units.gpkg',layer='eligible_units');rows=d[[*e[0]]].to_dict('records');return record_score(rows,e,['id_lcp'])
def geometry():
 original=gpd.read_file(TESTS/'source.gpkg').set_index('id_lcp');d=gpd.read_file(OUTPUT/'eligible_units.gpkg',layer='eligible_units').set_index('id_lcp')
 if d.crs.to_epsg()!=4547 or set(d.index)!={r['id_lcp'] for r in e}:return 0
 cols=[c for c in original.columns if c!='geometry']
 return all(row.geometry.equals_exact(original.loc[pid].geometry,0) and all(str(row[c])==str(original.loc[pid,c]) for c in cols) for pid,row in d.iterrows())
def flagged():
 d=gpd.read_file(OUTPUT/'flagged_units.gpkg',layer='flagged_units');expected=[r for r in e if r['risk_flag']];return record_score(d[[*e[0]]].to_dict('records'),expected,['id_lcp'])
g.check('八字段与资格',.6,audit);g.check('原字段几何CRS保真',.2,geometry);g.check('风险精确子集',.2,flagged);g.finish()
