import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

from features import features
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
labels=read_json(INPUT/'labels.json');train=read_csv(INPUT/'train_labels.csv');test=read_csv(INPUT/'record_ids.csv')
X=np.array([features(INPUT/'train'/r['ecg_id']) for r in train]);Y=np.array([[int(r[k]) for k in labels] for r in train]);Z=np.array([features(INPUT/'records'/r['ecg_id']) for r in test]);model=ExtraTreesClassifier(n_estimators=160,min_samples_leaf=1,max_features=.8,random_state=42,n_jobs=2);model.fit(X,Y);pred=model.predict(Z)
write_csv(OUTPUT/'predictions.csv',[{'ecg_id':r['ecg_id'],**dict(zip(labels,map(int,y)))} for r,y in zip(test,pred)])
(OUTPUT/'model_report.md').write_text('按每导联幅度分位数、方差、一阶差分幅度和六个频带能量提取特征；ExtraTrees多输出分类，固定随机种子，训练与测试分离。仅适用于题设合成形态，未经真实临床验证。')
