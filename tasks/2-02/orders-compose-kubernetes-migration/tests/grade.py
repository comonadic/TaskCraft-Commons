import sys,os,json,re,subprocess,base64,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from support import *
import yaml
g=Grade();chart=OUTPUT/'helm/webapp-chart'
def run(*args,timeout=30):return subprocess.run(args,capture_output=True,text=True,check=True,timeout=timeout).stdout
def kub(*args):return json.loads(run('kubectl',*args,'-n','alecn','-o','json'))
try:
    card=yaml.safe_load((chart/'Chart.yaml').read_text());assert card.get('name') and (chart/'values.yaml').is_file()
    docs=[x for x in yaml.safe_load_all(run('helm','template','webapp',str(chart),'-n','alecn')) if x]
    for obj in docs:
        if obj['kind']=='Secret':
            assert not obj.get('stringData') and obj.get('data')
            for value in obj['data'].values():assert base64.b64decode(value,validate=True)
except Exception as exc:
    g.check('Helm与Secret硬门槛',1,lambda:0);g.finish();sys.exit(0)
index={(x['kind'],x['metadata']['name']):x for x in docs}
def get(kind,name):return index[(kind,name)]
def podspec(kind,name):return get(kind,name)['spec']['template']['spec']
required=[('Deployment','frontend'),('Deployment','backend'),('StatefulSet','db'),('ConfigMap','app-config'),('Secret','db-secret'),('HorizontalPodAutoscaler','backend-hpa'),('NetworkPolicy','db-ingress'),('Ingress','webapp')]
g.check('8项Helm资源覆盖',.2,lambda:sum(x in index for x in required)/8)
def config():
    front=podspec('Deployment','frontend')['containers'][0];back=podspec('Deployment','backend')['containers'][0];db=podspec('StatefulSet','db')['containers'][0];h=get('HorizontalPodAutoscaler','backend-hpa')['spec'];network=get('NetworkPolicy','db-ingress')['spec'];ing=get('Ingress','webapp')['spec'];checks=[]
    checks += [front['resources']['limits']=={'cpu':'500m','memory':'256Mi'},back['resources']['limits']=={'cpu':'1000m','memory':'512Mi'}]
    checks += [back[x]['httpGet']=={'path':'/health','port':5000} for x in ['readinessProbe','livenessProbe']]
    checks += [h['minReplicas']==2 and h['maxReplicas']==5 and h['metrics'][0]['resource']['target']['averageUtilization']==70]
    checks += [network['podSelector'].get('matchLabels',{}).get('tier')=='db']
    checks += [all(any(e.get('valueFrom',{}).get('secretKeyRef') for e in c['env']) and not any('PASSWORD' in e['name'] and 'value' in e for e in c['env']) for c in [back,db])]
    checks += [get('StatefulSet','db')['spec']['volumeClaimTemplates'][0]['spec']['resources']['requests']['storage']=='5Gi']
    checks += [get('Deployment','frontend')['spec']['replicas']==2 and get('Deployment','backend')['spec']['replicas']==2 and get('StatefulSet','db')['spec']['replicas']==1]
    paths=[p for r in ing['rules'] for p in r['http']['paths']];checks += [any(x['path']=='/api' and x['backend']['service']['name']=='backend-service' for x in paths)]
    checks += [get('Service','frontend-service')['spec']['type']=='NodePort' and all(get('Service',x)['spec'].get('type','ClusterIP')=='ClusterIP' for x in ['backend-service','db-service'])]
    checks += [all(x['metadata'].get('labels',{}).get('app')=='webapp' for x in docs)]
    return sum(checks)/len(checks)
g.check('结构与资源配置',.25,config)
def terraform():
    t=(OUTPUT/'terraform/main.tf').read_text();blocks=re.findall(r'variable\s+"[^"]+"\s*\{([^}]+)\}',t,re.S)
    return sum([bool(re.search(r'required_providers\s*\{',t)),bool(blocks) and all('description' in x for x in blocks),bool(re.search(r'output\s+"',t)),bool(re.search(r'resource\s+"helm_release"',t)) and 'kubeconfig' in t])/4
g.check('Terraform静态合同',.1,terraform)
def ci():
    t=(OUTPUT/'Jenkinsfile').read_text();pairs=[('build',['docker build']),('test',['pytest','npm test']),('security',['trivy']),('deploy',['helm upgrade']),('verify',['rollout status'])]
    return sum(bool(re.search(r"stage\(['\"]"+name+r"['\"]\)",t)) and all(cmd in t for cmd in commands) for name,commands in pairs)/5
g.check('Jenkins五阶段静态合同',.1,ci)
g.check('快照与中文报告',.05,lambda:all((OUTPUT/'verification'/f).stat().st_size>20 for f in ['pods.txt','services.txt','helm-status.txt','health-check.txt']) and len((OUTPUT/'migration_report.md').read_text())>60)
def pods():
    items=kub('get','pods','-l','app=webapp')['items'];counts={k:0 for k in ['frontend','backend','db']}
    for p in items:
        if p['metadata']['labels'].get('tier') in counts and p['status'].get('phase')=='Running' and all(c.get('ready') for c in p['status'].get('containerStatuses',[])):counts[p['metadata']['labels']['tier']]+=1
    return counts['frontend']==2 and 2<=counts['backend']<=5 and counts['db']==1
g.check('实时Pod可用性',.12,pods)
g.check('实时Service',.045,lambda:all(kub('get','service',x)['spec'].get('clusterIP') not in [None,'','None'] for x in ['frontend-service','backend-service','db-service']))
def pod(tier):return kub('get','pods','-l','tier='+tier)['items'][0]['metadata']['name']
def health():
    s=run('kubectl','exec','-n','alecn',pod('backend'),'--','python','-c',"import urllib.request,json; h=json.load(urllib.request.urlopen('http://localhost:5000/api/health'));o=json.load(urllib.request.urlopen('http://localhost:5000/api/orders'));print(json.dumps([h,o]))")
    h,o=json.loads(s);return h['status']=='healthy' and h['orders']==3 and h['market']=='CN-SYNTHETIC' and abs(sum(x['amount_cny'] for x in o['orders'])-1048.30)<.001
g.check('实时Flask与数据库结果',.045,health)
def hpa():
    for _ in range(30):
        h=kub('get','hpa','backend-hpa');metrics=h.get('status',{}).get('currentMetrics',[])
        if any(x.get('resource',{}).get('current',{}).get('averageUtilization') is not None for x in metrics):return 1
        time.sleep(2)
    return 0
g.check('HPA真实CPU指标',.045,hpa)
def isolation():
    code="import socket; s=socket.socket();s.settimeout(3); print(s.connect_ex(('db-service',5432)))"
    yes=int(run('kubectl','exec','-n','alecn',pod('backend'),'--','python','-c',code).strip());no=int(run('kubectl','exec','-n','alecn',pod('frontend'),'--','python','-c',code).strip())
    return yes==0 and no!=0
g.check('实际网络策略正反向连接',.045,isolation);g.finish()
