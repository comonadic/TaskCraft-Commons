# 订单应用 Compose 到 Kubernetes 迁移：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 渲染 Helm chart，解析八类资源、values、Secret、Terraform 和 Jenkins 文件。
2. 连接任务内真实 K3s 集群，检查 Pod、Service、数据库与 API。
3. 读取 HPA 实际 CPU 指标，执行 backend 可连数据库、frontend 不可连数据库的双向连通性检查。
4. 合并静态产物与实时状态分数，输出逐项结果。

## 指标与阈值

- 静态产物占 70%，实时集群占 30%。
- 检查项权重为 20/25/10/10/5/12/4.5/4.5/4.5/4.5%，详情见逐项检查表。
- 网络策略通过实际连接探测评分；HPA 通过实时 CPU 指标评分。

## 前置条件

- Helm chart 必须可渲染、values 文件存在，Secret 必须为合法 base64。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 8项Helm资源覆盖 | 20% | `lambda: sum((x in index for x in required)) / 8` |
| 结构与资源配置 | 25% | `config` |
| Terraform静态合同 | 10% | `terraform` |
| Jenkins五阶段静态合同 | 10% | `ci` |
| 快照与中文报告 | 5% | `lambda: all(((OUTPUT / 'verification' / f).stat().st_size > 20 for f in ['pods.txt', 'services.txt', 'helm-status.txt', 'health-check.txt'])) and len((OUTPUT / 'migration_report.md').read_text()) > 60` |
| 实时Pod可用性 | 12% | `pods` |
| 实时Service | 4.5% | `lambda: all((kub('get', 'service', x)['spec'].get('clusterIP') not in [None, '', 'None'] for x in ['frontend-service', 'backend-service', 'db-service']))` |
| 实时Flask与数据库结果 | 4.5% | `health` |
| HPA真实CPU指标 | 4.5% | `hpa` |
| 实际网络策略正反向连接 | 4.5% | `isolation` |

## 业务规则

- **部署配置（70 分）**：资源覆盖 20 分、资源配置 25 分、Terraform 10 分、五阶段流水线 10 分、运行记录和中文报告 5 分；各项按满足要求的比例计分。
- **集群运行（30 分）**：Pod 可用性 12 分；Service、接口与数据库、HPA 指标、网络连接各 4.5 分，按实际集群检查结果计分。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
