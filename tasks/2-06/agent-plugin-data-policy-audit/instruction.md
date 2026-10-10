# 智能体平台插件数据政策审计

你是企业合规人员，需要评估智能体与插件的数据使用是否符合给定政策。

1. 读取插件接口、动作字段和数据类型
2. 逐字段匹配政策条款，记录违规及严重性
3. 按业务域汇总数据类型和暴露放大率，形成审计清单

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/policy_violations.json`：字段级违规、政策条款、严重性与汇总。
- `/app/output/cross_domain_exposure_report.csv`：各业务域的数据类型、智能体数量及暴露放大率。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

审计虚构平台“星桥智能体”的离线插件接口，严格执行附带平台政策，不引用现实平台或法律规则。仅用Python标准库解析字段实体、分类表、政策映射和插件元数据。按字段识别 CRITICAL/HIGH，保留条款与字段证据。另对被至少3个不同agent使用的后端domain计算数据类型暴露放大率。

## 运行与提交

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`policy_violations.json`：total_violations、severity_breakdown、violations列表（action_id,severity,policy_clause,action_domain,api_name,data_field_name,data_type）。`cross_domain_exposure_report.csv`：domain,agent_count,union_datatypes_count,avg_datatypes_per_action,amplification（3位小数加x）。
