# 医院多系统事件表 SA-AKI 表型提取

你是医学数据分析人员，需要将分散在不同系统的事件整理为一致的住院时间线和表型结果。

1. 连接 720 次 ICU 住院的感染、器官功能与肾功能事件
2. 按给定 Sepsis-3、KDIGO 和七天时间窗规则判定
3. 整理唯一患者名单，记录每次住院的起始时间与判定理由

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/sa_aki_patients.csv`：符合条件的唯一 subject_id 名单。
- `/app/output/phenotype_audit.csv`：逐 stay_id 的起始时间、资格与判定理由。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`sa_aki_patients.csv`，只有subject_id一列，严格唯一；`phenotype_audit.csv`列stay_id,sepsis_hour,aki_hour,eligible,reason。缺失时间填空字符串。
