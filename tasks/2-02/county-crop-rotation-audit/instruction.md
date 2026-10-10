# 县域十年地块轮作资格审计

你负责县域农业地块数据审计，需要将逐年的种植记录转为可追踪的资格和风险结果。

1. 读取地块和年度作物数据，按规则处理缺失与未知编码
2. 为符合条件的地块计算八项审计字段
3. 分别导出合格地块及风险子集，保留地块空间信息

## 工作空间

输入材料位于 `/app/input/`，工具与接口位于 `/app/software/`。成果保存到 `/app/output/`。

## 交付文件

- `/app/output/eligible_units.gpkg`：合格地块图层，包含原始属性与八项审计字段。
- `/app/output/flagged_units.gpkg`：需要关注的风险地块图层。

## 运行约定

保留输入材料，以交付文件或服务状态提交结果。根据任务说明使用提供的离线数据与工具。

## 具体工作要求

输入目录 `/app/input`，工具目录 `/app/software`，工作目录 `/app`。仅向 `/app/output` 写入最终产物。可用 Python 科学计算环境；无需外网或私有账号。输入保持不变，所有报告正文使用中文，技术字段、ID 和枚举保持约定值。

## 交付要求

`eligible_units.gpkg`图层eligible_units；`flagged_units.gpkg`图层flagged_units。新增eight fields见rules.md，几何保持原始EPSG:4547。
