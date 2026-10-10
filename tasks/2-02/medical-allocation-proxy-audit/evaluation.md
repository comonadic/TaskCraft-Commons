# 医疗资源分配的费用代理偏差审计：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 读取 6,000 人预测，核对基线分数、入选标志和改进分数。
2. 按改进分数与 patient_id 排序选取 1,200 人，比较目标人群。
3. 核对两个人群报告中的需要程度与构成，并检查机制解释。

## 指标与阈值

- 排序项 = 0.3 × 基线分数正确率 + 0.2 × 基线入选F1 + 0.3 × 改进入选F1 + 0.2 × 重排入选F1；该项占 65%。
- baseline、revised 报告各占 15%，机制说明占 5%。

## 前置条件

- 预测文件须恰好包含 6,000 个唯一患者 ID。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 原分数与两种排序 | 65% | `predictions` |
| 机制及外推限制说明 | 5% | `lambda: len((OUTPUT / 'analysis.md').read_text()) >= 60` |
| baseline人群需要与构成 | 15% | `lambda name=name: tree_score(read_json(OUTPUT / f'{name}_report.json'), e[name + '_report'])` |
| revised人群需要与构成 | 15% | `lambda name=name: tree_score(read_json(OUTPUT / f'{name}_report.json'), e[name + '_report'])` |

## 业务规则

- **评分与排序（65 分）**：本项内原始分数保留占 30%，基线入选 F1 占 20%，修订入选 F1 占 30%，按修订分数排序的名单 F1 占 20%。
- **群体与需要指标（30 分）**：基线与修订报告各占 15 分，逐字段比较入选数量、群体占比与需要指标。
- **分析说明（5 分）**：分析正文至少 60 字，取得本项分数。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
