# 湖泊多年水温剖面参数率定

你是湖泊环境研究人员，需要确定能够解释多年观测的模型参数，并整理全时段水温结果。

1. 读取气象驱动、观测记录和模型参数范围
2. 调整混合、交换与衰减参数，运行水温模拟
3. 导出时间与深度剖面，计算观测点 RMSE 并记录率定参数

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/calibrated.nml`：最终混合、交换与衰减参数。
- `/app/output/output.nc`：完整时间与深度的水温 NetCDF。
- `/app/output/calibration_report.json`：观测误差、观测数量和率定参数。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`calibrated.nml`、`output.nc`（time×depth，变量temperature，摄氏度）、`calibration_report.json`（rmse,n_observations,parameters）；原始input不改。
