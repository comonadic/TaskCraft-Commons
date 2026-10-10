# 建筑节费与削峰模型预测控制

你是建筑控制工程师，需要在 15 分钟控制周期下比较基线、节费和削峰三种策略。

1. 利用辨识数据估计空气与墙体温度模型
2. 设计两种滚动控制策略并运行 672 步评估
3. 整理温度、动作、费用、峰值和舒适度指标，提交控制器

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/identified_model.json`：辨识得到的模型系数。
- `/app/output/rc_diagnostics.json`：训练误差与诊断。
- `/app/output/*_timeseries.csv / *_actions.csv`：基线、节费、削峰温度轨迹和控制动作。
- `/app/output/metrics.json`：三种策略的费用、峰值和舒适度指标。
- `/app/output/controller.py`：可复现控制结果的程序。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

9项：identified_model.json、rc_diagnostics.json、baseline_timeseries.csv、cost_timeseries.csv、peak_timeseries.csv、cost_actions.csv、peak_actions.csv、metrics.json、controller.py。每timeseries列step,air,wall,cooling；action列step,cooling；指标各策略cost_cny,peak_kw,comfort_violation_degree_hours。
