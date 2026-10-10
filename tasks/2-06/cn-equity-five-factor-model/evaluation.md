# 中国股票市场五因子月度重建：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 按月份读取五因子结果，核对 134 个月的集合和唯一性。
2. 逐月逐因子比较市场、规模、价值、盈利与投资结果。
3. 核对时点筛选审计中的股票池与会计信息使用窗口。

## 指标与阈值

- 因子数值占 90%，时点审计占 10%。
- 因子数值绝对容差 1e−5，rtol=0；月份按 date 主键比较。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 134个月五因子数值与集合 | 90% | `lambda: record_score(read_csv(OUTPUT / 'ff5_factors_monthly_2015_onward.csv'), read_json(TESTS / 'expected.json'), ['date'], atol=1e-05, rtol=0)` |
| 时点筛选审计 | 10% | `lambda: record_score(read_json(OUTPUT / 'method_audit.json'), read_json(TESTS / 'audit.json'), ['date'])` |

## 业务规则

- **五因子序列（90 分）**：按月份比对全部五因子数值及月份集合，绝对容差为 0.00001，按正确比例计分。
- **样本审计（10 分）**：按月份比对合格样本数与迟到披露剔除数，按正确比例计分。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
