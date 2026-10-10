# 流感住院预测评分与模型比较

你是预测评估分析人员，需要把不同模型的预测与观测值对齐，形成可比较的评分表。

1. 根据时间和可用性规则对齐预测与观测值
2. 为共同预测单元计算 WIS、MAE 和区间覆盖率
3. 按模型汇总指标，计算相对基线表现

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/per_cell_scores.csv`：逐模型、地区、日期及预测期的评分明细。
- `/app/output/submission.csv`：各模型的单元数、平均误差、覆盖率及相对 WIS。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`per_cell_scores.csv`列model,location,target_date,horizon,wis,mae,coverage50,coverage95；`submission.csv`列model,n_cells,mean_wis,mean_mae,coverage50,coverage95,rel_wis。
