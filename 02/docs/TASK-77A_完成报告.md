# TASK-77A 完成报告（02 线 1/2）：规范 v0.6.2 增补

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-77A（02 线 1/2）：规范 v0.6.2 增补 |
| 前置 | TASK-72、01 线 71-A/71-B/76-A/76-B |
| 状态 | 完成 |

## 一、交付物

- `docs/规范增补_v0.6.2.md`：含 4 条款（单一真相源 / gateway 错误码 / 门禁产物 / 兼容说明）；
- `emulators_registry.json/md` 同步：全 26 条补 `module` + `backend_status` 列，并重新生成 md 与桌面清单。

## 二、条款摘要

1. **单一真相源**：一切模拟器经 `slots/emulators/<id>/manifest.json` 声明；网关内置 EMULATORS 仅最小兜底
   且与同名槽位 manifest 语义一致；新后端必须走槽位（对应 76-A 折叠）。
2. **错误码注册**：`EMULATOR_NOT_FOUND`（未登记）/ `EMULATOR_BINARY_MISSING`（有模块无二进制）/
   `EMULATOR_BACKEND_MISSING`（无模块预留槽位）三条独立路径 + 样例时序（依据 71-B 修复记录）。
3. **门禁产物**：`verify_last.json`（最近一次快照，71-A 已落地）+ `verify_history.jsonl`（趋势行
   {time,total,passed}，76-B 落地）schema 与语义，供 04 线仪表盘/外部门禁取数。
4. **兼容说明**：存量 27 台包无需改动；manifest 沿用 v0.5 §2；emulators_registry 新增 module/backend_status 列。

## 三、与 01 线对齐说明

- 错误码三条路径已由 71-B 在 `gw/gateway.py` 实现（`_spawn` 判 module 缺失抛 BACKEND_MISSING、`cmd_start_device`
  回发对应码），本增补据此注册语义，贴证据见 71-B 报告 §3。
- 门禁产物 verify_last.json 已存在（71-A，total 27 / passed 27）；verify_history.jsonl 由 76-B 落地，
  **执行时 76-B 尚未交付**，本增补按 76-B 任务文档定义其 schema（{time,total,passed} 追加行）。
- 单一真相源折叠由 76-A 落地，**执行时 76-A 尚未交付**（slots/emulators 仍仅 fake-slot），本增补按 76-A
  任务文档定义治理条款，registry 侧 module/backend_status 列已按"mame 骨架 / simh 预留"预填。

## 四、开放问题

1. 76-A/76-B 落地后，回填本增补中"贴 launch/slot_loader 输出"的证据（当前缺）；
2. 内置 EMULATORS 最小兜底保留哪几项，待 76-A 折叠结果确认；
3. verify_history.jsonl 保留长度/清理策略待定。
