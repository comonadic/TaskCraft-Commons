# 目标架构（合成订单数据）
命名空间alecn，release webapp；所有chart资源label app=webapp，工作负载/Pod额外tier=frontend/backend/db。
Deployment/frontend：2副本，limits cpu=500m,memory=256Mi，requests cpu=100m,memory=64Mi，3000端口。
Deployment/backend：2副本，limits cpu=1000m,memory=512Mi，requests cpu=100m,memory=64Mi，5000端口；readiness和liveness均GET /health。
StatefulSet/db：1副本，PVC5Gi，5432端口；POSTGRES_DB=orders，POSTGRES_USER=seed。密码通过Secret keyRef设置；数据库初始化附件init.sql，后端也只能从Secret读取密码。练习密码seedpass不是真实凭据。
ConfigMap存储MARKET=CN-SYNTHETIC、DB_HOST=db-service、DB_NAME=orders以及应用与SQL源文件；保留原源码业务行为。
Secret只用data base64，不能stringData或把密码明文放入Pod env。
Service frontend-service为NodePort，backend-service和db-service为ClusterIP。
HPA autoscaling/v2指向backend，min2/max5，CPU利用率70%；必须能取得当前指标，不能仅创建空HPA。
NetworkPolicy选择tier=db，仅允许同namespace tier=backend访问TCP5432；实际证明frontend不通、backend通。
Ingress使用traefik，host可留空，/api到backend-service:5000，/到frontend-service:3000。
Terraform声明hashicorp/helm provider、kubeconfig变量（description）、helm_release资源和output；对接已提供K3s，不要写不存在的Minikube资源。本题只检查配置结构。
Jenkinsfile五阶段build/test/security/deploy/verify，分别docker build、pytest+前端测试、trivy、helm upgrade、kubectl rollout status。用于可联网的企业Runner，题内静态验证，不假定Jenkins已部署。
快照必须来自当前集群。/api/health应healthy、orders=3、market=CN-SYNTHETIC；/api/orders合计1048.30元。镜像使用docker.io/library/python:3.13-alpine、docker.io/library/postgres:16.6、docker.io/library/ale-cn-webapp:0.1.0，imagePullPolicy: Never。离线镜像与二进制是第三方软件，不属于合成材料。
