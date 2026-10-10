# 订单应用 Compose 到 Kubernetes 迁移

你是云平台工程师，需要迁移包含 React 前端、Flask 后端和 PostgreSQL 数据库的订单应用。

1. 把 Compose 服务整理为 Helm Chart 和配置参数
2. 准备 Terraform、Jenkins 流水线及持久化和扩缩容设置
3. 部署应用，检查接口、数据库、网络策略并提交运行记录

交付成果：
- helm/webapp-chart/：可渲染的 Helm Chart、values 与资源模板。
- terraform/main.tf：基础设施与 Helm 发布配置。
- Jenkinsfile：构建、测试、发布等五阶段流水线。
- verification/：Pod、Service、Helm 和接口检查记录。
- migration_report.md：迁移步骤、配置选择与运行结果。
