# 地区四周流感住院预测

你是公共卫生预测研究人员，需要为 53 个地区整理未来四周的住院需求预测。

1. 分析 104 周的历史住院与辅助数据
2. 为各地区未来四周生成点预测和 95% 区间
3. 整理预测文件、预测程序与方法说明

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/submission.csv`：212 条地区与预测期记录，包含点预测和 95% 区间。
- `/app/output/forecast.py`：使用输入材料生成预测的程序。
- `/app/output/method.md`：模型、特征、训练与区间估计方法。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`submission.csv`列location,horizon,point,lower95,upper95，212行；`forecast.py`与`method.md`。预测非负且lower95<=point<=upper95。
