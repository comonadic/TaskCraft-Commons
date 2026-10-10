# 星澜云账单与资源成本优化

你是云平台成本管理人员，需要为运营团队整理一份能够落地的资源优化清单，说明每项建议的依据和预计收益。

1. 结合资源清单、使用数据和截图识别可优化资源
2. 为各项资源选择合适的优化动作，计算现有费用和预计费用
3. 汇总月度节约金额，形成管理摘要和资源明细

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/optimization_report.json`：包含整体费用、节约金额、建议数量与逐资源建议的优化报告。
- `/app/output/savings_summary.csv`：逐资源费用测算表，列出资源名称、动作和节约金额。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`optimization_report.json`含executive_summary（current_cost,projected_cost,monthly_savings,recommendation_count）和recommendations数组；`savings_summary.csv`列resource_id,resource_type,name,action,current_cost,projected_cost,monthly_savings。
