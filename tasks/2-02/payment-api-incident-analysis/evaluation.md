# 支付服务 Kubernetes 故障归因与恢复计划：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 读取 RCA JSON，逐项匹配根因、受影响资源与逐字日志证据。
2. 检查结构化整改参数，包括配置键、目标值与操作步骤。
3. 核对回滚版本、镜像与中文诊断摘要和验证步骤。

## 指标与阈值

- 根因和证据占 50%；受影响资源 F1 占 10%；整改参数占 25%；回滚占 10%；摘要占 5%。
- 根因证据按材料中的原文核验；资源集合使用 F1。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 根因与逐字证据 | 50% | `roots` |
| 受影响资源 | 10% | `lambda: f1_set(read_json(OUTPUT / 'root_cause_analysis.json')['affected_resources'], e['affected_resources'])` |
| 中文整改结构化参数 | 25% | `params` |
| 回滚版本与镜像 | 10% | `lambda: tree_score({k: read_json(OUTPUT / 'root_cause_analysis.json')['rollback'][k] for k in e['rollback']}, e['rollback'])` |
| 诊断摘要与验证步骤 | 5% | `lambda: len(read_json(OUTPUT / 'root_cause_analysis.json')['summary']) >= 20 and len(read_json(OUTPUT / 'root_cause_analysis.json')['rollback']['verify']) >= 10` |

## 业务规则

- **根因与证据（50 分）**：逐项比较根因类型、资源和日志原文，按正确比例计分。
- **影响范围（10 分）**：受影响资源集合采用 F1 计分。
- **整改计划（25 分）**：检查动作说明、整数优先级和结构化参数，按参数正确比例计分。
- **回滚方案（10 分）**：比对回滚版本和镜像，按字段正确比例计分。
- **摘要与验证（5 分）**：诊断摘要至少 20 字且恢复验证说明至少 10 字，取得本项分数。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
