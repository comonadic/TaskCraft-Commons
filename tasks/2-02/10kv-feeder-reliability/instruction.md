# 10kV 馈线双口径可靠性分析

你是供用电工程人员，需要分析一条 10kV 馈线的停电风险，说明指标口径与计划停电的处理。

1. 读取 CIM/XML 和拓扑图，确认路径与设备参数
2. 累计各负荷点的故障率、停电时长与供电参数
3. 计算 SAIFI、SAIDI、CAIDI、ASAI 和 ENS，交付双口径报告

交付成果：
- loadpoint_metrics.csv：逐变压器故障率、停电时长、用户数与负荷。
- reliability_indices.json：等权口径的系统可靠性指标。
- cn_reliability_report.json：用户加权口径指标及用户总数。
- method.md：路径累计、计划停电和指标口径说明。
