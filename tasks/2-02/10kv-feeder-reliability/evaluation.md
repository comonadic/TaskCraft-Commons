# 10kV 馈线双口径可靠性分析：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 按 transformer_id 核对每个负荷点的供电路径与累计指标。
2. 比较等权可靠性指标。
3. 重算用户加权及计划停电指标，再检查方法说明。

## 指标与阈值

- 负荷点 40%、等权指标 25%、用户加权与计划停电 30%、说明 5%。
- 逐记录和结构化数值比较采用默认 atol=1e−6、rtol=1e−5。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 负荷点路径累计 | 40% | `lambda: record_score(read_csv(OUTPUT / 'loadpoint_metrics.csv'), e['points'], ['transformer_id'])` |
| 等权指标 | 25% | `lambda: tree_score(read_json(OUTPUT / 'reliability_indices.json'), e['original'])` |
| 用户加权及计划停电 | 30% | `lambda: tree_score(read_json(OUTPUT / 'cn_reliability_report.json'), e['cn'])` |
| 方法说明 | 5% | `lambda: len((OUTPUT / 'method.md').read_text()) >= 60` |

## 业务规则

- **负荷点结果（40 分）**：按变压器 ID 比对路径累计结果和参数，按记录与字段正确比例计分。
- **等权指标（25 分）**：逐字段比对系统等权指标，按正确比例计分。
- **用户加权指标（30 分）**：逐字段比对加权指标与用户总数，按正确比例计分。
- **方法说明（5 分）**：方法正文至少 60 字，取得本项分数。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
