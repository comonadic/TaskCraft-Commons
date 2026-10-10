# 零售企业再营销受众与渠道资格：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 读取客户、订单和偏好材料，按业务规则构造目标受众与渠道资格。
2. 按 customer_id 对齐提交名单，比较人员和字段。
3. 核对分群定义以及各已有分群的交集、并集与分母。

## 指标与阈值

- 受众名单占 65%，分群摘要占 15%，重叠报告占 20%。
- 重叠率数值绝对容差 1e−6，默认相对容差 1e−5；重复 customer_id 记 0。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 精确受众与渠道资格 | 65% | `lambda: record_score(read_csv(OUTPUT / 'audience_roster.csv'), e['roster'], ['customer_id'])` |
| 分群摘要 | 15% | `lambda: tree_score(read_json(OUTPUT / 'segment_definition.json'), e['definition'])` |
| 正确分母重叠率 | 20% | `lambda: record_score(read_csv(OUTPUT / 'overlap_report.tsv', '\t'), e['overlap'], ['segment_id'], atol=1e-06)` |

## 业务规则

- **受众与渠道（65 分）**：按客户 ID 比对入选名单和渠道资格，按记录与字段的正确比例计分。
- **分群摘要（15 分）**：比对分群定义与统计字段，按正确比例计分。
- **重叠分析（20 分）**：按既有分群 ID 比较重叠人数及比例，数值绝对容差为 0.000001。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
