# 智能体平台插件数据政策审计：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 按 action_id 与 data_field_name 对齐字段级违规记录。
2. 核对条款、严重程度及严重性汇总。
3. 按域核对跨域暴露数量与放大率。

## 指标与阈值

- 字段级违规与条款占 65%；严重性汇总占 10%；跨域报告占 25%。
- 违规记录使用联合主键，跨域记录使用 domain；重复主键使相应项记 0。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 字段级违规与条款 | 65% | `lambda: record_score(read_json(OUTPUT / 'policy_violations.json')['violations'], e['violations'], ['action_id', 'data_field_name'])` |
| 严重性汇总 | 10% | `lambda: tree_score({k: v for k, v in read_json(OUTPUT / 'policy_violations.json').items() if k != 'violations'}, {'total_violations': len(e['violations']), 'severity_breakdown': e['severity']})` |
| 跨域放大率 | 25% | `lambda: record_score(read_csv(OUTPUT / 'cross_domain_exposure_report.csv'), e['exposure'], ['domain'])` |

## 业务规则

- **字段违规（65 分）**：按动作 ID 与字段名比对违规记录、条款和严重性，按正确比例计分。
- **违规汇总（10 分）**：比对违规总数和严重性分布，按字段正确比例计分。
- **业务域暴露（25 分）**：按业务域比较聚合人数、数据类型数量和放大率，按正确比例计分。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
