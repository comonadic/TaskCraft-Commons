# 10kV 馈线双口径可靠性分析

你是供用电工程人员，需要分析一条 10kV 馈线的停电风险，说明指标口径与计划停电的处理。

1. 读取 CIM/XML 和拓扑图，确认路径与设备参数
2. 累计各负荷点的故障率、停电时长与供电参数
3. 计算 SAIFI、SAIDI、CAIDI、ASAI 和 ENS，交付双口径报告

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/loadpoint_metrics.csv`：逐变压器故障率、停电时长、用户数与负荷。
- `/app/output/reliability_indices.json`：等权口径的系统可靠性指标。
- `/app/output/cn_reliability_report.json`：用户加权口径指标及用户总数。
- `/app/output/method.md`：路径累计、计划停电和指标口径说明。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`reliability_indices.json`：SAIFI,SAIDI,CAIDI,ASAI,ENS_kWh；`cn_reliability_report.json`同字段加total_customers；`loadpoint_metrics.csv`列transformer_id,lambda_per_year,outage_hours,customers,kw；`method.md`。
