# 企业年度报告批量抽取与跨报告问答

你是财务数据分析人员，需要把六家企业三年的报告整理为结构化数据，为研究团队提供可追溯的分析结果。

1. 从 18 份年报提取指定财务指标，统一数值与单位
2. 保留原文并完成三项跨报告分析问题
3. 重复处理指定五份报告，检查结果一致性

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/extractions/`：18 份结构化财务指标 JSON。
- `/app/output/raw_extractions/`：对应报告的原文摘录。
- `/app/output/qa_answers.json`：三项跨报告问题的答案。
- `/app/output/run2_extractions/`：指定五份报告再次处理的结果。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`extractions/<id>.json`、`raw_extractions/<id>.txt`（18份），`qa_answers.json`，`run2_extractions/<id>.json`（5份）。
