import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

import shutil,subprocess
dest=OUTPUT/'submission/scripts';dest.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(__file__).parent/'remediate_catalog.py',dest/'remediate_catalog.py')
subprocess.run([sys.executable,str(dest/'remediate_catalog.py'),'--case-dir',str(INPUT/'case'),'--output-dir',str(OUTPUT/'submission/outputs/public_case')],check=True)
