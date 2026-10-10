# 居民个人综合所得年度汇算申报

你是税务业务人员，需要按照任务提供的汇算规则，为三位居民整理年度申报和补退税结果。

1. 核对每位居民的工资、扣除和预缴凭证
2. 计算应纳税所得、应纳税额及补退税差额
3. 在申报页面填写并保存三份申报结果和截图

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/returns/T001.json～T003.json`：三位居民的汇算申报字段与金额。
- `/app/output/screenshots/T001.png～T003.png`：各份申报保存后的页面截图。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`returns/T001.json`至`T003.json`，字段taxpayer_id,year,income,special_deduction,additional_deduction,taxable_income,tax_due,prepaid,balance；`screenshots/T001.png`至T003.png。
