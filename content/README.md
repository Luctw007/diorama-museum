# content/ — 设备内容包（预留）

按设计文档：一台设备 = 一个内容包（`content/<device-id>/`），包含 DeviceSpec JSON、
glTF 资产、原理标注与 THIRD_PARTY.md 许可清册。

- 目录结构与字段规范：见《内容包规范 v0.1》（TASK-02 任务产出，位于 `docs/`）。
- M0 状态：**空**（不包含任何具体设备内容）。
- 生产流程：设备包任务模板见设计文档附录 C；自动校验工具位于 `tools/validate/`（TASK-02）。