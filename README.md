# TaskCraft Commons

中文知识工作任务基准与开放共建目录。当前收录 28 项任务，覆盖金融与会计、法律与合规、医学研究、科学分析、软件与云系统、工程设计、文献信息和供应链业务。

## 从一个任务目录开始

每个 `tasks/<领域编码>/<任务名称>/` 目录是独立的 Harbor 任务包，包含实际输入、环境定义、参考解、参考产物和确定性评分器。职业场景与详细评测说明由 Task Card 描述，运行生命周期交给 Harbor。

需要 Python 3.11+、Docker Compose 和 Harbor 0.22.0：

```bash
pip install harbor==0.22.0
cd tasks/2-06/chenghai-balance-sheet-2024
python3 run.py check
python3 run.py oracle --jobs-dir ./runs
python3 run.py nop --jobs-dir ./runs
python3 run.py run -a terminus-2 -m <model> --jobs-dir ./runs
```

`oracle` 运行参考解并评分；`nop` 运行空提交。普通任务在独立验证器中核对输出文件，Odoo 和 Kubernetes 在运行环境中核对真实服务状态。最终结果为 0～1 的 reward，网站按 100 分制展示。

```text
task-folder/
├── task_card.json        职业、场景、工作步骤、输入、交付与评测
├── instruction.md        智能体任务说明
├── evaluation.md         评分过程、指标、阈值与权重
├── evaluation.json       机器可读评分说明
├── task.toml             Harbor 配置与成果路径
├── materials.json        输入文件大小与 SHA-256 清单
├── run.py                独立运行入口
├── environment/
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   ├── requirements-lock.txt
│   ├── input/            实际任务材料
│   └── software/         任务内工具与接口
├── solution/             参考解 solve.sh / solve.py
├── reference/            参考解交付文件
└── tests/                test.sh、grade.py、评分数据与独立验证环境
```

首次构建会安装锁定的运行依赖。Kubernetes 任务的 K3s、Helm 和离线镜像通过固定版本 GitHub Release 分发，运行入口会根据 `assets.lock.json` 下载并核验；该题需要 Linux ARM64，使用任务内特权容器启动 K3s。

## 批量运行

从仓库根目录运行：

```bash
python3 infra/suite.py check
python3 infra/suite.py oracle --concurrency 1 --jobs-dir runs
python3 infra/suite.py nop --task 2-06/chenghai-balance-sheet-2024
```

可重复使用 `--task <taskId>` 选题、`--exclude <taskId>` 排除题目。具体评分输出位于 Harbor 运行目录中的 `verifier/reward.txt`、`verifier/score.json`；任务还可能生成分类、动力学或业务状态诊断文件。

## 职业范围

站内采用 21 个领域、527 个知识工作职业，沿用中国职业分类编码，按“领域 → 具体职业”组织。收录规则与扩充方式见 [taxonomy/SCOPE.md](taxonomy/SCOPE.md)。

## 任务目录

| 任务 | 职业 | 评分说明 |
|---|---|---|
| [厂房与塔楼图纸三维重建](tasks/4-08/factory-tower-3d-reconstruction) | 建筑信息模型技术员 | [Evaluation](tasks/4-08/factory-tower-3d-reconstruction/evaluation.md) |
| [澄海精密 2024 年合并资产负债表重构](tasks/2-06/chenghai-balance-sheet-2024) | 会计专业人员 | [Evaluation](tasks/2-06/chenghai-balance-sheet-2024/evaluation.md) |
| [星澜云账单与资源成本优化](tasks/2-02/xinglan-cloud-cost-review) | 云计算工程技术人员 | [Evaluation](tasks/2-02/xinglan-cloud-cost-review/evaluation.md) |
| [县域十年地块轮作资格审计](tasks/2-02/county-crop-rotation-audit) | 地理信息系统工程技术人员 | [Evaluation](tasks/2-02/county-crop-rotation-audit/evaluation.md) |
| [零售企业再营销受众与渠道资格](tasks/2-06/retail-remarketing-audience) | 市场营销专业人员 | [Evaluation](tasks/2-06/retail-remarketing-audience/evaluation.md) |
| [12 导联心电心律与传导分类](tasks/2-01/ecg-rhythm-conduction-classification) | 医学研究人员 | [Evaluation](tasks/2-01/ecg-rhythm-conduction-classification/evaluation.md) |
| [12 导联心电诊断类别建模](tasks/2-01/ecg-diagnostic-superclasses) | 医学研究人员 | [Evaluation](tasks/2-01/ecg-diagnostic-superclasses/evaluation.md) |
| [流感住院预测评分与模型比较](tasks/2-06/influenza-forecast-scoring) | 统计专业人员 | [Evaluation](tasks/2-06/influenza-forecast-scoring/evaluation.md) |
| [澄海精密权益研究摘要工作簿](tasks/2-06/chenghai-equity-research-summary) | 证券投资专业人员 | [Evaluation](tasks/2-06/chenghai-equity-research-summary/evaluation.md) |
| [中国股票市场五因子月度重建](tasks/2-06/cn-equity-five-factor-model) | 证券投资专业人员 | [Evaluation](tasks/2-06/cn-equity-five-factor-model/evaluation.md) |
| [地区四周流感住院预测](tasks/2-01/regional-influenza-hospital-forecast) | 医学研究人员 | [Evaluation](tasks/2-01/regional-influenza-hospital-forecast/evaluation.md) |
| [湖泊多年水温剖面参数率定](tasks/2-01/lake-temperature-calibration) | 地球科学研究人员 | [Evaluation](tasks/2-01/lake-temperature-calibration/evaluation.md) |
| [Unitree G1 八组控制策略回放评估](tasks/2-02/unitree-g1-policy-review) | 机器人工程技术人员 | [Evaluation](tasks/2-02/unitree-g1-policy-review/evaluation.md) |
| [订单应用 Compose 到 Kubernetes 迁移](tasks/2-02/orders-compose-kubernetes-migration) | 云计算工程技术人员 | [Evaluation](tasks/2-02/orders-compose-kubernetes-migration/evaluation.md) |
| [支付服务 Kubernetes 故障归因与恢复计划](tasks/2-02/payment-api-incident-analysis) | 云计算工程技术人员 | [Evaluation](tasks/2-02/payment-api-incident-analysis/evaluation.md) |
| [四份股权转让公告一致性审阅](tasks/2-07/equity-transfer-consistency-review) | 法律顾问 | [Evaluation](tasks/2-07/equity-transfer-consistency-review/evaluation.md) |
| [智能体平台插件数据政策审计](tasks/2-06/agent-plugin-data-policy-audit) | 企业合规师 | [Evaluation](tasks/2-06/agent-plugin-data-policy-audit/evaluation.md) |
| [图书馆书目修复与 FOLIO 覆盖计划](tasks/2-10/library-marc-folio-remediation) | 文献信息专业人员 | [Evaluation](tasks/2-10/library-marc-folio-remediation/evaluation.md) |
| [建筑节费与削峰模型预测控制](tasks/2-02/building-model-predictive-control) | 自动控制工程技术人员 | [Evaluation](tasks/2-02/building-model-predictive-control/evaluation.md) |
| [调查队列混杂敏感性分析](tasks/2-01/survey-confounder-sensitivity) | 医学研究人员 | [Evaluation](tasks/2-01/survey-confounder-sensitivity/evaluation.md) |
| [医疗资源分配的费用代理偏差审计](tasks/2-02/medical-allocation-proxy-audit) | 数据分析处理工程技术人员 | [Evaluation](tasks/2-02/medical-allocation-proxy-audit/evaluation.md) |
| [Odoo 企业采购制造交付与退款](tasks/4-02/odoo-manufacturing-fulfillment) | 供应链管理师 | [Evaluation](tasks/4-02/odoo-manufacturing-fulfillment/evaluation.md) |
| [云衡软件私募投资初筛备忘录](tasks/2-06/yunheng-investment-screening) | 证券投资专业人员 | [Evaluation](tasks/2-06/yunheng-investment-screening/evaluation.md) |
| [10kV 馈线双口径可靠性分析](tasks/2-02/10kv-feeder-reliability) | 供用电工程技术人员 | [Evaluation](tasks/2-02/10kv-feeder-reliability/evaluation.md) |
| [中文 AI 使用体验文本心理编码](tasks/2-01/chinese-ai-experience-text-coding) | 心理学研究人员 | [Evaluation](tasks/2-01/chinese-ai-experience-text-coding/evaluation.md) |
| [医院多系统事件表 SA-AKI 表型提取](tasks/2-02/icu-sa-aki-phenotyping) | 数据分析处理工程技术人员 | [Evaluation](tasks/2-02/icu-sa-aki-phenotyping/evaluation.md) |
| [企业年度报告批量抽取与跨报告问答](tasks/2-06/enterprise-annual-report-analysis) | 会计专业人员 | [Evaluation](tasks/2-06/enterprise-annual-report-analysis/evaluation.md) |
| [居民个人综合所得年度汇算申报](tasks/2-06/individual-income-tax-return) | 税务专业人员 | [Evaluation](tasks/2-06/individual-income-tax-return/evaluation.md) |

## 格式与参考

任务格式遵循 [Harbor 任务规范](https://docs.harborframework.com/tasks/overview)。Task Card 的专业场景与评测预览参考 [Agents’ Last Exam](https://github.com/rdi-berkeley/agents-last-exam) 的任务组织方式，界面与中文内容由 TaskCraft Commons 编写。文件与模型的第三方许可见 [NOTICE.md](NOTICE.md) 及任务内许可证。
