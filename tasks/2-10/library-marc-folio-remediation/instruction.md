# 图书馆书目修复与 FOLIO 覆盖计划

你是图书馆文献信息人员，需要把批量书目中的字段问题修复为可导入的记录，并说明每条处理决定。

1. 结合权威映射、馆藏和编目政策修复字段
2. 与 FOLIO 记录匹配，逐记录确定处理动作
3. 生成导入计划、质量报告和可复用的处理程序

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/submission/scripts/remediate_catalog.py`：支持输入与输出目录参数的书目处理程序。
- `/app/output/submission/outputs/public_case/`：修复 XML、处理决策 CSV、导入计划 JSON、QA 报告与修复摘要。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`submission/scripts/remediate_catalog.py`支持 --case-dir 与 --output-dir；公开输出位于submission/outputs/public_case：remediated_records.xml、overlay_decisions.csv、folio_import_plan.json、qa_report.json、remediation_summary.md。
