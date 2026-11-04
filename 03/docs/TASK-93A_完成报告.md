# TASK-93A 完成报告（03 线 1/2）：Commodore VIC-20 设备包（定案表领取 · 个人机厅第十一台）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。

| 项 | 内容 |
|---|---|
| 任务 | TASK-93A：Commodore VIC-20 设备包 |
| 前置 | 88-A 定案表 §三/§四（第一台从定案表领取） |
| 状态 | 完成 |

## 交付物

- **research 简报**：`docs/research/vic20_简报.md`（史实 + 模拟器 VICE xvic=GPLv2【需核实】，槽位 dedicated 预留，未下载二进制）。
- **内容包** `content/vic20/`：meta（era 1980、category=personal-computer）/ runtime（demo_mode，external_crt+speaker）/ 6 占位盒（一体机身、键盘、主板 6502+VIC 芯片、电源、数据磁带机、显示器）/ annotations 30 条（销量破百万、面向家庭价格、彩色图形、C64 前身等 flow 锚点）/ encyclopedia **2,609 汉字** / THIRD_PARTY 三件套 + ROM 红线。
- **目录联动**：`计算机大类_目录_v2.jsonl` 回填 `C-PC-000016` → status=done、device_id=vic20（路径三级）。

## 校验

- `validate.py`：**84 PASS / 0 FAIL**。
- `model_check.py`：MR-001~004 全过（6/6 网格）。
- `catalog_check`：FAIL 0（CC-08 device_id 存在性 PASS）。
- `catalog_ref_check`：REF-01~04 全 0（反链当天闭环，内容包 25 个无反链缺失）。

## 说明

- 本任务是**第一台从 88-A 定案表领取生产的包**（定案表 27#），流程条款生效验证：从表里领、不临时起意。
- glTF 节点名与 assembly id 一一对应，R-090 通过。

## 开放问题

1. VICE xvic 许可（GPLv2）需核实；真跑需 BASIC ROM + 字符 ROM 合规。
2. 尺寸为调研近真值，标「需核实」；正式建模以存世实机为准。
