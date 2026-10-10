# TaskCraft 任务格式

任务目录是运行、审核和发布的基本单元。Task Card 描述专业工作，Harbor 配置控制执行与评分；网站展示同一份任务卡中的字段。

## 题面与材料

`instruction.md` 明确工作场景、输入路径、软件、具体工作要求和 `/app/output` 交付文件。输入放在 `environment/input/`，Docker 构建时复制到 `/app/input/`；工具放在 `environment/software/`。`materials.json` 列出实际文件路径、字节数和 SHA-256。

`task_card.json` 包含简短介绍 `brief`、完整题面 `taskPrompt`、工作步骤 `agentMustDo`、职业编码、输入文件、交付要求 `deliverables`、实际参考文件 `referenceFiles`、评分说明和运行配置。字段结构见 `task-card.schema.json`。

## 执行环境

每题包含自己的 Dockerfile、依赖锁、Compose 配置及工具。参考解入口是 `solution/solve.sh`。文件型任务声明 `artifacts = ["/app/output"]`，采用 separate verifier，在新评分环境中读取交付文件；需要核对真实服务状态的任务采用 shared verifier。

大型运行资产可以放在固定版本 Release 中，用任务内 `assets.lock.json` 固定下载地址和 SHA-256。`run.py` 在运行前准备资产，不依赖仓库上层目录。添加任务时复制现有入口 `infra/task_runner.py` 到任务目录即可。

## 评分约定

`tests/test.sh` 运行评分程序，写入 `/logs/verifier/reward.txt` 与 `/logs/verifier/score.json`。reward 范围为 0～1；网站分数为 `100 × reward`。评分程序须记录每项检查的名称、权重、得分和异常原因。

`evaluation.json` 与 `evaluation.md` 说明评分步骤、指标公式、容差、前置条件、权重和失败处理。文档应对应实际评分代码。新增任务可以使用确定性评分或补充专业评议；专业评议若参与最终分数，须定义独立入口、量表和评分配置。

参考解与评分数据放在任务目录中，由 Harbor 在各自阶段提供；环境 Dockerfile 只复制输入和工具。可执行的提交代码在新目录中复跑，独立验证器的评分数据目录使用专门访问权限。

## 贡献检查

1. `python3 run.py check`：验证目录、评分权重与输入哈希。
2. `python3 run.py oracle`：参考解完成任务并取得预期分数。
3. `python3 run.py nop`：空提交取得 0 分。
4. 用至少一项格式合法但业务错误的提交，检查评分器是否区分正确结果。
5. `python3 infra/validate.py`：检查任务索引、职业范围、文件引用和评分数据一致性。

修改任务材料或评分规则时同步更新题面、参考解、参考产物、评测文档与版本。
