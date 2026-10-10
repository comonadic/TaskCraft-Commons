import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from xlsx_runtime import read_xlsx,fill_xlsx
cells,_=read_xlsx(INPUT/'posts.xlsx');d=read_json(INPUT/'column_dictionary.json');values={}
def column(n):
 s=''
 while n:n,r=divmod(n-1,26);s=chr(65+r)+s
 return s
for row in range(2,97):
 txt=cells['E'+str(row)];own=re.sub(r'我没有出现“[^”]+”的情况。','',txt);own=re.sub(r'朋友说他有过“[^”]+”的经历，这不是我的经历。','',own)
 for i,label in enumerate(d['focus'],6):values[column(i)+str(row)]='主诉是'+label in own
 for item in d['themes']:values[column(item['column'])+str(row)]=item['positive_statement'] in own
OUTPUT.mkdir(exist_ok=True);fill_xlsx(INPUT/'posts.xlsx',OUTPUT/'ai_addiction_annotations_output.xlsx',values)
