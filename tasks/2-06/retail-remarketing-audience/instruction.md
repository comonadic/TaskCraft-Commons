# 零售企业再营销受众与渠道资格

你是零售企业营销分析人员，需要为下一轮活动准备一份符合客户授权和业务规则的受众名单。

1. 连接客户、交易、邮件及工单资料
2. 按活动规则筛选受众，逐客户确定可用渠道
3. 整理分群定义、受众名单和与现有分群的重叠结果

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/segment_definition.json`：分群规则、人数和关键统计。
- `/app/output/audience_roster.csv`：受众名单及逐客户渠道资格。
- `/app/output/overlap_report.tsv`：与现有分群的重叠人数和比例。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`segment_definition.json`，`audience_roster.csv`，`overlap_report.tsv`；字段及计算口径见 brief.md。
