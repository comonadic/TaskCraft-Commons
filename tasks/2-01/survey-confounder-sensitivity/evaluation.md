# 调查队列混杂敏感性分析：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 按 id 核对完整病例筛选、变量编码与抽样权重。
2. 比较三种统计模型的估计、区间与敏感性变化。
3. 核对输出行集合与模型标签。

## 指标与阈值

- 病例与字段 40%，三模型估计与变化 60%。
- 模型结果绝对容差 1e−5；按 model 主键对齐，重复键记 0。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 完整病例与字段 | 40% | `lambda: record_score(read_csv(OUTPUT / 'hpyl_nsaid_subset.csv'), e['subset'], ['id'])` |
| 三模型估计与变化 | 60% | `lambda: record_score(read_csv(OUTPUT / 'sensitivity_summary.csv'), e['models'], ['model'], atol=1e-05)` |

## 业务规则

- **分析样本（40 分）**：按个体 ID 比对病例集合和变量，按记录与字段的正确比例计分。
- **模型结果（60 分）**：按模型比对估计值、置信区间、P 值与变化比例，绝对容差为 0.00001。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
