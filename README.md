# TaskCraft Commons

中文职业任务基准与任务共建目录。每张任务卡包含工作介绍、任务步骤、输入材料、交付成果和评分方法。

当前收录 **28 道任务**。职业目录包含此前整理的 **1,636 个具体职业、74 个职业领域**，取自《职业分类大典》2022 年社会公示稿。

## 目录

```text
tasks/<职业领域代码>/<任务名>/
  task_card.json
  instruction.md
  README.md
taxonomy/china_occupations.json
index.json
```

本仓库发布任务卡、材料清单与评分说明。文件清单对应的执行材料、参考答案和运行环境由任务维护者管理。

## 任务卡字段

`taskId`、`title`、`brief`、`category`、`occupation`、`taskPrompt`、`agentMustDo`、`software`、`inputFiles`、`referenceFiles`、`evaluation`、`language`、`version`。`evaluation.criteria` 逐项说明分值及计算方法。

## 任务目录

| 任务 | 职业 |
|---|---|
| [厂房与塔楼图纸三维重建](tasks/4-08/factory-tower-3d-reconstruction/task_card.json) | 建筑信息模型技术员 |
| [澄海精密 2024 年合并资产负债表重构](tasks/2-06/chenghai-balance-sheet-2024/task_card.json) | 会计专业人员 |
| [星澜云账单与资源成本优化](tasks/2-02/xinglan-cloud-cost-review/task_card.json) | 云计算工程技术人员 |
| [县域十年地块轮作资格审计](tasks/2-02/county-crop-rotation-audit/task_card.json) | 地理信息系统工程技术人员 |
| [零售企业再营销受众与渠道资格](tasks/2-06/retail-remarketing-audience/task_card.json) | 市场营销专业人员 |
| [12 导联心电心律与传导分类](tasks/2-01/ecg-rhythm-conduction-classification/task_card.json) | 医学研究人员 |
| [12 导联心电诊断类别建模](tasks/2-01/ecg-diagnostic-superclasses/task_card.json) | 医学研究人员 |
| [流感住院预测评分与模型比较](tasks/2-06/influenza-forecast-scoring/task_card.json) | 统计专业人员 |
| [澄海精密权益研究摘要工作簿](tasks/2-06/chenghai-equity-research-summary/task_card.json) | 证券投资专业人员 |
| [中国股票市场五因子月度重建](tasks/2-06/cn-equity-five-factor-model/task_card.json) | 证券投资专业人员 |
| [地区四周流感住院预测](tasks/2-01/regional-influenza-hospital-forecast/task_card.json) | 医学研究人员 |
| [湖泊多年水温剖面参数率定](tasks/2-01/lake-temperature-calibration/task_card.json) | 地球科学研究人员 |
| [Unitree G1 八组控制策略回放评估](tasks/2-02/unitree-g1-policy-review/task_card.json) | 机器人工程技术人员 |
| [订单应用 Compose 到 Kubernetes 迁移](tasks/2-02/orders-compose-kubernetes-migration/task_card.json) | 云计算工程技术人员 |
| [支付服务 Kubernetes 故障归因与恢复计划](tasks/2-02/payment-api-incident-analysis/task_card.json) | 云计算工程技术人员 |
| [四份股权转让公告一致性审阅](tasks/2-07/equity-transfer-consistency-review/task_card.json) | 法律顾问 |
| [智能体平台插件数据政策审计](tasks/2-06/agent-plugin-data-policy-audit/task_card.json) | 企业合规师 |
| [图书馆书目修复与 FOLIO 覆盖计划](tasks/2-10/library-marc-folio-remediation/task_card.json) | 文献信息专业人员 |
| [建筑节费与削峰模型预测控制](tasks/2-02/building-model-predictive-control/task_card.json) | 自动控制工程技术人员 |
| [调查队列混杂敏感性分析](tasks/2-01/survey-confounder-sensitivity/task_card.json) | 医学研究人员 |
| [医疗资源分配的费用代理偏差审计](tasks/2-02/medical-allocation-proxy-audit/task_card.json) | 数据分析处理工程技术人员 |
| [Odoo 企业采购制造交付与退款](tasks/4-02/odoo-manufacturing-fulfillment/task_card.json) | 供应链管理师 |
| [云衡软件私募投资初筛备忘录](tasks/2-06/yunheng-investment-screening/task_card.json) | 证券投资专业人员 |
| [10kV 馈线双口径可靠性分析](tasks/2-02/10kv-feeder-reliability/task_card.json) | 供用电工程技术人员 |
| [中文 AI 使用体验文本心理编码](tasks/2-01/chinese-ai-experience-text-coding/task_card.json) | 心理学研究人员 |
| [医院多系统事件表 SA-AKI 表型提取](tasks/2-02/icu-sa-aki-phenotyping/task_card.json) | 数据分析处理工程技术人员 |
| [企业年度报告批量抽取与跨报告问答](tasks/2-06/enterprise-annual-report-analysis/task_card.json) | 会计专业人员 |
| [居民个人综合所得年度汇算申报](tasks/2-06/individual-income-tax-return/task_card.json) | 税务专业人员 |

资料与贡献说明见 [NOTICE.md](NOTICE.md)。
