# 合成市场练习方法 v1
每月只保留 financials_visible=1 且 tradable=1。return_decimal 已经复权，不能再乘 adjustment_factor。市值为月初值。
月度规模按合格样本市值中位数，<=为S，否则B。BM、OP、INV各用全合格样本的30%、70%线性插值分位点分L/M/H，<=30为L，>70为H，其余M。分别构造2x3组合，组合内以月初市值加权。独立重分组每月发生，不做年度持有。
MKT_RF=合格全市场市值加权收益-rf。SMB为三个特征中各自(SL+SM+SH-BL-BM-BH)/3的均值。
HML=(SH+BH-SL-BL)/2（BM分组）；RMW同式（OP分组）；CMA=(SL+BL-SH-BH)/2（INV分组）。输出均乘100，允许绝对误差1e-5个百分点。
method_audit.json为134个对象的数组，按月份顺序。late_filing_excluded_count只统计financials_visible=0，独立于tradable。
