# 调查队列混杂敏感性分析

连接调查队列和用药事件数据，重建分析样本，并比较加入不同混杂因素后的关联估计。

职业：医学研究人员 · `2-01-08-00`

## 运行

需要 Python 3.11+、Docker Compose 和 Harbor 0.22.0。

```bash
pip install harbor==0.22.0
python3 run.py check
python3 run.py oracle --jobs-dir ./runs
python3 run.py nop --jobs-dir ./runs
# 运行自己的智能体，参数交给 Harbor
python3 run.py run -a terminus-2 -m <model> --jobs-dir ./runs
```

`oracle` 运行参考解并评分，`nop` 检查空提交。下载这一任务目录即可运行；`run.py` 会准备资产并调用 Harbor。

## 文件

- [task_card.json](task_card.json)：职业场景、任务说明、文件索引和评分规则
- [instruction.md](instruction.md)：智能体收到的任务说明
- [evaluation.md](evaluation.md)：评分过程、指标、阈值与检查项
- [task.toml](task.toml)：Harbor 运行配置
- `environment/`：容器环境、实际输入与工具
- `solution/`：参考解
- `reference/`：参考解的交付文件
- `tests/`：评分器与评分数据

评分输出位于运行目录的 `verifier/reward.txt` 与 `verifier/score.json`。参考解和评分文件由运行器在对应阶段提供。
