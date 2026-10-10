# 云衡软件私募投资初筛备忘录

你是投资研究人员，需要向团队提交一份结构完整、结论明确并能追溯资料的初筛备忘录。

1. 整理八份公司资料，计算八项关键财务指标
2. 形成三条投资论点、四类风险与四项尽调问题
3. 写出 Go、No-Go 或 Hold 建议，逐项引用资料

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/screening_memo.md`：投资建议、公司产品、论点、财务、估值、风险、尽调和证据附录八章。
- `/app/output/analysis.json`：财务指标、论点、风险、尽调问题、建议与理由。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`screening_memo.md`（八个模板章节）；`analysis.json`，包含metrics（8指标）、thesis（3条，每条evidence引用）、risks（4条）、diligence（4项）、recommendation枚举及reason。
