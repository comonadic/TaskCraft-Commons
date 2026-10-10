# 0.3.0 执行验证

在 Docker 28.0.4、Linux ARM64、Harbor 0.22.0 下运行公开标准目录：

- 28/28 参考解 reward = 1。
- 28/28 空提交 reward = 0。
- 28/28 Task Card、输入哈希、文件引用、Python 语法与目录结构通过检查。
- Kubernetes 从独立任务文件夹自动下载公开 Release 资产，归档与解压文件 SHA-256 均通过校验。
- 原始题包 11,477 个文件的 SHA-256 与字节数保持不变。

逐题结果见 [summary.json](summary.json)，各题 `tasks/<taskId>/oracle.json` 与 `nop.json` 是实际验证器产生的分项日志。

文件型任务使用独立验证器；Odoo 与 Kubernetes 使用运行环境中的真实业务或集群状态。参考解验证评估的是任务执行与评分的一致性。

机器人任务首次打包缺少网格资源，补齐输入与评分环境的完整资源后已单独复跑通过，汇总使用修复后的结果。
