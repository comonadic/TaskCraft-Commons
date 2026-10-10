# Kubernetes runtime assets v1

供 `2-02/orders-compose-kubernetes-migration` 使用的 Linux ARM64 运行资产：K3s、Helm、K3s 离线镜像及任务内 Python、PostgreSQL 和订单应用镜像。

固定资产包由 GitHub Release 分发，任务目录中的 `assets.lock.json` 固定下载 URL、归档 SHA-256 与每个解压文件的 SHA-256。`python3 run.py prepare` 下载、校验并解压至 `environment/assets/`；运行时自动准备。

K3s、Helm、Python、PostgreSQL 等工具分别遵循上游许可证。任务内应用为本项目的本地业务环境。
