# 调查队列混杂敏感性分析

你是医学研究分析人员，需要检验幽门螺杆菌与 NSAID 用药等因素对目标关联估计的影响。

1. 连接四张数据表，整理符合条件的完整病例
2. 拟合三组逐步调整混杂因素的模型
3. 比较样本量、优势比、置信区间与变化幅度，交付分析表

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/hpyl_nsaid_subset.csv`：逐人的分析样本及研究变量。
- `/app/output/sensitivity_summary.csv`：三个模型的样本量、估计值、区间、P 值和变化比例。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`hpyl_nsaid_subset.csv`列id,ulcer,multimorbidity,age,sex,bmi,weight,hpyl,nsaid；`sensitivity_summary.csv`列model,n,odds_ratio,ci_low,ci_high,p_value,or_change_pct。
