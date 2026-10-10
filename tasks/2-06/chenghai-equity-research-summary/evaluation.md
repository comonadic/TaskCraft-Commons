# 澄海精密权益研究摘要工作簿：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 读取 Excel 工作簿的原始输入、派生指标和公式。
2. 核对估值、盈利、增长与资产负债指标。
3. 对关键输入应用四组扰动，检查公式计算是否等价，再核对来源时点。

## 指标与阈值

- 数值占 65%，动态公式占 25%，公司、币种和报价时点占 10%。
- 公式项按四组输入扰动后的计算结果判断等价，支持等价写法。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 全部输入与派生数值 | 65% | `lambda: tree_score({k: read_xlsx(OUTPUT / 'CN_Financial_Summary.xlsx')[0].get(k) for k in e}, e)` |
| 动态公式四组扰动等价 | 25% | `lambda: equivalence(read_xlsx(OUTPUT / 'CN_Financial_Summary.xlsx')[1], f, e)` |
| 来源与时点 | 10% | `lambda: tree_score(read_json(OUTPUT / 'sources.json'), {'quote_time': '2025-03-31 15:00', 'company': '澄海精密', 'currency': 'CNY', 'pages': ['quote.html', 'statistics.html', 'annual_report.html']})` |

## 业务规则

- **数据与计算结果（65 分）**：比较模板单元格的输入与派生数值，按正确比例计分。
- **动态公式（25 分）**：在四组输入变化下重新检查公式结果，按与要求公式等价的比例计分。
- **资料索引（10 分）**：比对行情时点、公司、币种和三个资料页面，按字段正确比例计分。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
