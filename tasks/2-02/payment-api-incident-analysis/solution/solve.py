import sys, os, json, csv, math, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from support import *

logs=(INPUT/'failing_pod.txt').read_text();cluster=(INPUT/'cluster_state.txt').read_text();roots=[]
for typ,needle,resource,desc in [('memory_limit','OOMKilled','deployment/payment-api','容器内存限制低于启动工作集，导致OOM终止。'),('premature_liveness','Liveness probe failed','deployment/payment-api','启动需要24秒，过早存活探针触发重启。'),('metrics_port_mismatch','ServiceMonitor targetPort','ServiceMonitor/payment-api','指标监听端口与采集目标不一致。')]:
 q=next(s for s in logs.splitlines() if needle in s);roots.append({'type':typ,'resource':resource,'evidence_file':'failing_pod.txt','evidence_quote':q,'description':desc})
mem=re.search(r'approved memory limit=(\w+)',logs).group(1);delay=int(re.search(r'minimum probe delay=(\d+)',logs).group(1));port=int(re.search(r'listener bound to port (\d+)',logs).group(1))
a={'roots':roots,'affected_resources':['deployment/payment-api','svc/payment-api','ServiceMonitor/payment-api'],'remediation':[{'priority':1,'resource':'deployment/payment-api','action':'先回滚恢复服务，再调整内存及探针并灰度发布；采集端口对齐。','parameters':{'memory_limit':mem,'initialDelaySeconds':delay,'metrics_target_port':port}}],'rollback':{'revision':int(re.search(r'previous_revision=(\d+)',cluster).group(1)),'image':re.search(r'old revision16 image=(\S+)',cluster).group(1),'verify':'检查双副本就绪、503恢复、无OOM及指标采集成功'},'summary':'发布后资源与探针配置导致重启，指标端口另有配置错误。数据库和DNS证据正常，不应当作根因。'}
write_json(OUTPUT/'root_cause_analysis.json',a)
