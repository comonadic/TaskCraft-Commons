# 订单应用 Compose 到 Kubernetes 迁移

你是云平台工程师，需要迁移包含 React 前端、Flask 后端和 PostgreSQL 数据库的订单应用。

1. 把 Compose 服务整理为 Helm Chart 和配置参数
2. 准备 Terraform、Jenkins 流水线及持久化和扩缩容设置
3. 部署应用，检查接口、数据库、网络策略并提交运行记录

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/helm/webapp-chart/`：可渲染的 Helm Chart、values 与资源模板。
- `/app/output/terraform/main.tf`：基础设施与 Helm 发布配置。
- `/app/output/Jenkinsfile`：构建、测试、发布等五阶段流水线。
- `/app/output/verification/`：Pod、Service、Helm 和接口检查记录。
- `/app/output/migration_report.md`：迁移步骤、配置选择与运行结果。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

迁移附件中的React、Flask、PostgreSQL三层订单应用，部署到本题隔离K3s单节点。启动 /app/software/start-cluster.sh，使用kubectl与helm。所有镜像已离线缓存，禁止连接真实业务集群。创建命名空间alecn，Helm release名webapp。详细架构见requirements.md。除Helm chart，还须提交Terraform声明、国内团队采用的Jenkins五阶段流水线及真实集群快照。验收将重新查询实时集群、访问健康API、检查HPA当前CPU指标，并实测前端不能访问DB而后端可以。截图/文本不能替代运行状态。


## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

output/helm/webapp-chart（Chart.yaml、values.yaml、templates）；terraform/main.tf；Jenkinsfile；verification/{pods,services,helm-status,health-check}.txt；migration_report.md。所有命令仅对本题集群运行。
