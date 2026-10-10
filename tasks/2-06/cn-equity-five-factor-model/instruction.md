# 中国股票市场五因子月度重建

你是资产定价研究人员，需要从原始市场和财务数据构建可追踪的五因子序列。

1. 对齐月度行情与当时可获取的财务数据
2. 按规模、价值、盈利与投资特征分组并计算组合收益
3. 生成 MKT_RF、SMB、HML、RMW、CMA 月度序列与样本审计

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/ff5_factors_monthly_2015_onward.csv`：134 个月的五因子收益序列。
- `/app/output/method_audit.json`：每月合格样本数及迟到披露剔除数。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

根据本地允许的数据包重建 2015-01 至 2026-02 的五因子，严格使用 `methodology.md`，不得使用外部因子成品。数据包括股票月收益、月初流通市值、财务披露、无风险利率和交易状态。需要按披露可见性筛选股票，按规模与三个财务特征独立分组，并计算市值加权收益。所有因子以百分数表示（1表示1%）。

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`ff5_factors_monthly_2015_onward.csv`，列 date,MKT_RF,SMB,HML,RMW,CMA，恰好134行；`method_audit.json`，每月 eligible_count 与 late_filing_excluded_count。
