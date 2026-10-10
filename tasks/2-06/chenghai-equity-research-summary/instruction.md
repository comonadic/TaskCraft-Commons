# 澄海精密权益研究摘要工作簿

你是证券研究人员，需要把澄海精密的市场与财务信息整理进统一研究模板，供团队进一步分析。

1. 读取行情、统计及年报页面，提取指定时点的数据
2. 填入研究摘要模板，建立派生指标公式
3. 检查工作簿计算结果并整理资料索引

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/CN_Financial_Summary.xlsx`：“研究摘要”工作表，包含输入值、派生指标和动态公式。
- `/app/output/sources.json`：行情时点、公司、币种与资料页面索引。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`CN_Financial_Summary.xlsx`，单页“研究摘要”，按template行坐标填B列；`sources.json`字段quote_time,company,currency,pages。公式行见 output_contract.json。
