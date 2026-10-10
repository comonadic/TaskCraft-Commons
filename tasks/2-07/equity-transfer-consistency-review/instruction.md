# 四份股权转让公告一致性审阅

你是法律与交易文件审核人员，需要帮助团队识别公告之间影响交易理解的信息差异。

1. 阅读四份公告，按交易事项对齐金额、股份与日期等信息
2. 判断哪些差异构成实质冲突
3. 为每项发现记录两份文件的页码与原文，编写审核报告

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/audit_report.md`：按“发现”分节的一致性审核报告。
- `/app/output/findings.json`：每项发现的事项、字段、冲突值与双文档证据。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`audit_report.md`：每项发现用“## 发现N”分节；`findings.json`：数组，每项含 subject、field、values（两个原文值）、evidence（两个{document,page,quote}）。field可选 amount/share_count/ownership/approval_date/address/contact/payment_deadline。
