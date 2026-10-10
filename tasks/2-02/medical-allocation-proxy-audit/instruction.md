# 医疗资源分配的费用代理偏差审计

你是医疗数据分析人员，需要评估费用评分作为资源分配依据时产生的群体差异。

1. 保留原始评分并重建基线入选名单
2. 建立需要导向的修订评分，按固定名额选择对象
3. 比较两种方案的群体构成与需要覆盖，说明差异机制

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/full_predictions.csv`：原始与修订评分，以及两种方案的入选标记。
- `/app/output/baseline_report.json / revised_report.json`：入选数量、群体占比与需要覆盖指标。
- `/app/output/analysis.md`：对费用代理、差异机制和适用范围的分析。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`full_predictions.csv`列patient_id,baseline_score,revised_score,baseline_selected,revised_selected；`baseline_report.json`与`revised_report.json`含selected_count,group_a_share,group_b_share,mean_need,total_need_captured；`analysis.md`。
