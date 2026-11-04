# TASK-67B 完成报告（02 线 2/2）：模拟器官方档案 emulators_registry.json

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-67B（02 线 2/2）：模拟器官方档案 |
| 前置 | TASK-67A |
| 目标 | 把散落各线的模拟器调研结构化为官方档案，供三方同源 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `docs/emulators_registry.json` | 模拟器官方档案（机器可读，全字段） | **20 条目**（≥20） |
| `docs/emulators_registry.md` | 人类可读版（生成自 json） | 20 条目 |
| `docs/TASK-67B_完成报告.md` | 本报告 | — |

## 二、20 条目状态分布

| 状态 | 条目 | 数量 |
|---|---|---|
| bone（成熟可接入） | fake-slot、mame-apple2、mame-handheld、simh-pdp8、stella、mesen、eka2l1、cloudpilotemu | 8 |
| reserved（预留待映射） | simh-pdp11、simh-vax11、qemu、system360-emulator | 4 |
| researched（调研中） | vice、beebem、blastem、pc86box、qedsac、davidpsharp-baby、sameboy、madrigal | 8 |

**backend_type 分布**：native 1 / mame 2 / simh 3 / stella 1 / mesen 1 / mobile 2 / dedicated 10。

## 三、backend_type 自检（用 01 slot_loader 枚举）

```
条目数：20
backend_type 非法条目：无（全部 bone 条目 backend_type 均在 01 slot_loader 枚举内）
```

01 线 `slot_loader.BACKEND_TYPE_MODULE` 的 7 项枚举（native/mame/simh/stella/mesen/mobile/dedicated）
全覆盖本 registry 的 backend_type；8 个 bone 条目中，native/mame 已映射模块，simh/stella/mesen/mobile
在枚举内但模块为预留（None），列入"待映射清单"（见 01 线 slot_loader.py）。

## 四、给 05 线 emu-eco 的修订输入（与 registry 不一致处清单）

| # | 不一致点 | emu-eco 现状 | registry 定稿 | 建议 |
|---|---|---|---|---|
| 1 | backend_type 命名 | 用 `custom` | 用规范枚举 `dedicated` | 05 线 emu-eco 后续改 custom→dedicated |
| 2 | media_class 语义 | 用 `runnable_mame/runnable_custom/展示向`（可运行性分级） | 用介质类目 `cartridge/disk/firmware/...`（v0.5 §3.3） | 两套语义并存：可运行性分级归 slot 能力位，介质类目归 media_class，勿混用 |
| 3 | EKA2L1/CloudpilotEmu 状态 | "可运行（有限）" | `bone`（成熟可接入但需 spike） | 保留"需 spike"风险标注 |
| 4 | MADrigal 许可 | [需核实] | 需核实（沿用） | 一致，无需改 |
| 5 | QEMU 早期 iOS | "不可运行" | `reserved`（实验预留） | 一致，保留"实验性"风险 |

## 五、与桌面《模拟器清单》的同步关系

本 registry 是桌面《模拟器清单》的**结构化母表**——桌面清单由 registry.json 渲染（同 emulators_registry.md
的生成路径），三方同源：01 线 slot 系统读 backend_type/media_classes 做槽位注册、05 线 emu-eco 读
target_devices/risks 做调研续补、桌面清单读 name/license 做展示。任何一方增改模拟器，应回写 registry
（而非各自维护副本）。

## 六、TASK-67 两份总收尾

- **67-A**：`规范增补_v0.6.1.md`（media_class 规则章 + CC-08）+ catalog_check 增 CC-08 + 反例 8/8 全绿 + 1562 条全量 0 冲突。
- **67-B**：`emulators_registry.json`（20 条目，全字段）+ backend_type 自检通过 + 05 线修订输入清单。

## 七、开放问题

1. **registry 回写机制**：目前 registry 由 02 线维护，05/01 线增改模拟器如何回写（PR/直接改）需定协作流程；
2. **researched 条目的许可补全**：vice/beebem/blastem/pc86box/qedsac/davidpsharp-baby/sameboy 等 10 条的许可仍"需核实"，待 05 线 emu-eco 补 SPIX + URL；
3. **mobile 后端模块**：eka2l1/cloudpilotemu 归 mobile，但 01 线 slot_loader 的 mobile 模块为预留，接入需 spike（同 emu-eco 结论）；
4. **system360-emulator 待定**：大型机 System/360 无成熟模拟器，backend_type 暂标 dedicated + reserved，实际后端名待调研。
