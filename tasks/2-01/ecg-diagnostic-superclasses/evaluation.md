# 12 导联心电诊断类别建模：评分方法

评分器读取交付文件，逐项计算 0～1 的得分，再按权重求加权平均。网站以 100 分制展示结果。

## 计算流程

1. 读取 predictions.csv，验证独立测试集 ECG ID、唯一性与 NORM、MI、STTC、CD、HYP 五个标签列。
2. 将逐记录标签与评分集对齐，计算五类 macro-F1。
3. 记录 classification_metrics.json，并检查模型说明。

## 指标与阈值

- 分类得分 = min(1, macro-F1 / 0.75)，占 98%；说明项占 2%。
- 各类别 F1 等权平均，zero_division=0；模型说明须超过 60 个字符。

## 前置条件

- ECG ID 集合、唯一性、列名和 0/1 标签格式共同决定分类项是否可评分。

## 检查项

| 检查项 | 权重 | 程序入口 |
|---|---:|---|
| 独立测试macro-F1 | 98% | `score` |
| 方法与限制说明 | 2% | `lambda: len((OUTPUT / 'model_report.md').read_text()) > 60` |

## 业务规则

- **分类效果（98 分）**：按测试 ID 对齐预测与参考标签，计算宏平均 F1；本项得分为 98 × min(1, F1 ÷ 0.75)。
- **方法说明（2 分）**：读取方法报告，正文超过 60 个字符取得本项分数。

## 分数与日志

`reward = Σ(weight × check_score) / Σ(weight)；网站得分 = 100 × reward`

缺少文件、解析失败或检查异常时，该检查项记 0 分，并在 score.json 中记录原因。

完整实现见 [grade.py](tests/grade.py) 与 [support.py](tests/support.py)。
