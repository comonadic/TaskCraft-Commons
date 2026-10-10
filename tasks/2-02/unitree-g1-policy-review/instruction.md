# Unitree G1 八组控制策略回放评估

你是机器人控制评估人员，需要向研发团队说明不同控制策略的表现和问题出现的时间。

1. 对八组控制设置进行完整回放
2. 记录高度、跟踪误差与跌倒时间，判断策略表现
3. 逐案例整理中文观察、关键指标、视频和轨迹

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/policy_evaluation_report.json`：八个案例的分类、中文观察与量化证据。
- `/app/output/visual_demos/`：每个案例的六秒回放视频和 trajectory.csv。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`policy_evaluation_report.json`：8项数组，含case_id,verdict,observation,evidence（min_base_height,tracking_rmse,fall_time）；`visual_demos/<case_id>/rollout.mp4`及`trajectory.csv`，每例完整6秒回放。
