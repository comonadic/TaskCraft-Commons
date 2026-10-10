import os,json,subprocess,time,yaml,base64
from pathlib import Path
ROOT=Path(os.environ.get('TASKCRAFT_ROOT','/app'));inp=ROOT/'input';out=ROOT/'output';out.mkdir(exist_ok=True)
def run(*cmd,**kw):return subprocess.run(cmd,text=True,capture_output=True,check=True,**kw).stdout
run('bash',str(ROOT/'software/start-cluster.sh'))
chart=out/'helm/webapp-chart';(chart/'templates').mkdir(parents=True,exist_ok=True)
(chart/'Chart.yaml').write_text('apiVersion: v2\nname: webapp-chart\nversion: 0.1.0\n')
(chart/'values.yaml').write_text('frontendReplicas: 2\nbackendReplicas: 2\nmarket: CN-SYNTHETIC\n')
def meta(name,tier=None):return {'name':name,'labels':{'app':'webapp',**({'tier':tier} if tier else {})}}
def sourcevol():return {'name':'source','configMap':{'name':'app-config'}}
objects=[]
data={'MARKET':'CN-SYNTHETIC','DB_HOST':'db-service','DB_NAME':'orders'}
for name,path in [('backend.py','backend/backend.py'),('index.html','frontend/index.html'),('react.js','frontend/react.js'),('react-dom.js','frontend/react-dom.js'),('init.sql','db/init.sql')]:data[name]=(inp/'app'/path).read_text()
objects.append({'apiVersion':'v1','kind':'ConfigMap','metadata':meta('app-config'),'data':data})
objects.append({'apiVersion':'v1','kind':'Secret','metadata':meta('db-secret'),'type':'Opaque','data':{'password':base64.b64encode(b'seedpass').decode()}})
for tier,port,mem,cpu,img in [('frontend',3000,'256Mi','500m','python:3.13-alpine'),('backend',5000,'512Mi','1000m','ale-cn-webapp:0.1.0')]:
    container={'name':tier,'image':img,'imagePullPolicy':'Never','ports':[{'containerPort':port}],'resources':{'requests':{'cpu':'100m','memory':'64Mi'},'limits':{'cpu':cpu,'memory':mem}},'volumeMounts':[{'name':'source','mountPath':'/app' if tier=='backend' else '/site','readOnly':True}],'command':['python','/app/backend.py'] if tier=='backend' else ['python','-m','http.server','3000','--directory','/site']}
    if tier=='backend':
        container.update(env=[{'name':k,'valueFrom':{'configMapKeyRef':{'name':'app-config','key':k}}} for k in ['MARKET','DB_HOST','DB_NAME']]+[{'name':'DB_USER','value':'seed'},{'name':'DB_PASSWORD','valueFrom':{'secretKeyRef':{'name':'db-secret','key':'password'}}}],readinessProbe={'httpGet':{'path':'/health','port':5000},'initialDelaySeconds':5,'periodSeconds':5},livenessProbe={'httpGet':{'path':'/health','port':5000},'initialDelaySeconds':20,'periodSeconds':10})
    objects.append({'apiVersion':'apps/v1','kind':'Deployment','metadata':meta(tier,tier),'spec':{'replicas':2,'selector':{'matchLabels':{'app':'webapp','tier':tier}},'template':{'metadata':{'labels':{'app':'webapp','tier':tier}},'spec':{'containers':[container],'volumes':[sourcevol()]}}}})
    objects.append({'apiVersion':'v1','kind':'Service','metadata':meta(tier+'-service',tier),'spec':{'type':'NodePort' if tier=='frontend' else 'ClusterIP','selector':{'app':'webapp','tier':tier},'ports':[{'port':port,'targetPort':port}]}})
objects.append({'apiVersion':'v1','kind':'Service','metadata':meta('db-service','db'),'spec':{'type':'ClusterIP','selector':{'app':'webapp','tier':'db'},'ports':[{'port':5432,'targetPort':5432}]}})
objects.append({'apiVersion':'apps/v1','kind':'StatefulSet','metadata':meta('db','db'),'spec':{'serviceName':'db-service','replicas':1,'selector':{'matchLabels':{'app':'webapp','tier':'db'}},'template':{'metadata':{'labels':{'app':'webapp','tier':'db'}},'spec':{'containers':[{'name':'db','image':'postgres:16.6','imagePullPolicy':'Never','ports':[{'containerPort':5432}],'env':[{'name':'POSTGRES_DB','value':'orders'},{'name':'POSTGRES_USER','value':'seed'},{'name':'POSTGRES_PASSWORD','valueFrom':{'secretKeyRef':{'name':'db-secret','key':'password'}}},{'name':'PGDATA','value':'/var/lib/postgresql/data/pgdata'}],'volumeMounts':[{'name':'data','mountPath':'/var/lib/postgresql/data'},{'name':'source','mountPath':'/docker-entrypoint-initdb.d/init.sql','subPath':'init.sql','readOnly':True}],'resources':{'requests':{'cpu':'100m','memory':'128Mi'},'limits':{'cpu':'1000m','memory':'512Mi'}}}],'volumes':[sourcevol()]}},'volumeClaimTemplates':[{'metadata':{'name':'data'},'spec':{'accessModes':['ReadWriteOnce'],'resources':{'requests':{'storage':'5Gi'}}}}]}})
objects.append({'apiVersion':'autoscaling/v2','kind':'HorizontalPodAutoscaler','metadata':meta('backend-hpa'),'spec':{'scaleTargetRef':{'apiVersion':'apps/v1','kind':'Deployment','name':'backend'},'minReplicas':2,'maxReplicas':5,'metrics':[{'type':'Resource','resource':{'name':'cpu','target':{'type':'Utilization','averageUtilization':70}}}]}})
objects.append({'apiVersion':'networking.k8s.io/v1','kind':'NetworkPolicy','metadata':meta('db-ingress'),'spec':{'podSelector':{'matchLabels':{'tier':'db'}},'policyTypes':['Ingress'],'ingress':[{'from':[{'podSelector':{'matchLabels':{'tier':'backend'}}}],'ports':[{'protocol':'TCP','port':5432}]}]}})
objects.append({'apiVersion':'networking.k8s.io/v1','kind':'Ingress','metadata':meta('webapp'),'spec':{'ingressClassName':'traefik','rules':[{'http':{'paths':[{'path':'/api','pathType':'Prefix','backend':{'service':{'name':'backend-service','port':{'number':5000}}}},{'path':'/','pathType':'Prefix','backend':{'service':{'name':'frontend-service','port':{'number':3000}}}}]}}]}})
for i,obj in enumerate(objects):
    content=yaml.safe_dump(obj,allow_unicode=True,sort_keys=False)
    if obj['kind']=='Deployment':content=content.replace('replicas: 2','replicas: {{ .Values.'+obj['metadata']['name']+'Replicas }}')
    (chart/'templates'/f'{i:02d}-{obj["kind"].lower()}.yaml').write_text(content)
(out/'terraform').mkdir(exist_ok=True)
(out/'terraform/main.tf').write_text('''terraform {
  required_providers {
    helm = { source = "hashicorp/helm", version = "2.17.0" }
  }
}
variable "kubeconfig" {
  type = string
  description = "本题隔离K3s集群的kubeconfig，不可指向生产集群"
  default = "/etc/rancher/k3s/k3s.yaml"
}
provider "helm" {
  kubernetes { config_path = var.kubeconfig }
}
resource "helm_release" "webapp" {
  name = "webapp"
  namespace = "alecn"
  create_namespace = true
  chart = "${path.module}/../helm/webapp-chart"
}
output "release_name" { value = helm_release.webapp.name }
''')
(out/'Jenkinsfile').write_text('''pipeline {
  agent any
  stages {
    stage('build') { steps { sh 'docker build -t ale-cn-webapp:0.1.0 app/backend; docker build -t ale-cn-frontend:0.1.0 app/frontend' } }
    stage('test') { steps { sh 'pytest app/backend/tests; cd app/frontend && npm test' } }
    stage('security') { steps { sh 'trivy image --exit-code 1 --severity CRITICAL ale-cn-webapp:0.1.0' } }
    stage('deploy') { steps { sh 'helm upgrade --install webapp helm/webapp-chart --namespace alecn --create-namespace' } }
    stage('verify') { steps { sh 'kubectl rollout status deployment/backend -n alecn; kubectl rollout status deployment/frontend -n alecn' } }
  }
}
''')
print(run('helm','upgrade','--install','webapp',str(chart),'-n','alecn','--create-namespace','--wait','--timeout','360s'),flush=True)
for i in range(90):
    h=json.loads(run('kubectl','get','hpa','backend-hpa','-n','alecn','-o','json'))
    if h.get('status',{}).get('currentMetrics'):break
    time.sleep(2)
v=out/'verification';v.mkdir(exist_ok=True)
for file,cmd in [('pods.txt',['kubectl','get','pods','-n','alecn','-o','wide']),('services.txt',['kubectl','get','services','-n','alecn']),('helm-status.txt',['helm','status','webapp','-n','alecn'])]:(v/file).write_text(run(*cmd))
pod=json.loads(run('kubectl','get','pods','-n','alecn','-l','tier=backend','-o','json'))['items'][0]['metadata']['name']
health=run('kubectl','exec','-n','alecn',pod,'--','python','-c',"import urllib.request; r=urllib.request.urlopen('http://localhost:5000/api/health');print(r.status,r.read().decode())")
(v/'health-check.txt').write_text(health)
(out/'migration_report.md').write_text('# 迁移报告\n\n使用题内ARM64 K3s，保持三层应用与合成订单；chart参数化副本，Secret提供密码，PVC持久化。后端探针真实访问数据库；HPA使用metrics-server，NetworkPolicy限制DB来源。Terraform和Jenkins为面向企业Runner的交付配置，本地未部署Jenkins也未terraform apply；实际部署通过Helm完成。镜像离线固定以避免国内获取路径不稳定，非对现行云平台的仿真。\n')
