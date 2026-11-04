# TASK-72B 完成报告（02 线 2/2）：模拟器档案 v1.1 + 桌面清单联动

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-72B（02 线 2/2）：模拟器档案 v1.1 |
| 前置 | TASK-72A |
| 状态 | 完成 |

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `docs/emulators_registry.json` | v1.1（每条补 `media_classes_allowed` 交叉索引 + 补 6 个模拟器） | **26 条目** |
| `tools/index/gen_emulator_doc.py` | 文档生成器 | 108 行（≤120） |
| `docs/emulators_registry.md` | 自动生成（替换手写） | 26 条目 |
| `其它信息/模拟器清单_20261104.md` | 桌面清单自动刷新（替换手写版） | 已生成 |

## 二、变更点

1. **media_classes_allowed 交叉索引**：每条补 `{目标设备: [media_class...]}` 全配对；
2. **补 6 个模拟器**（结构搬运自桌面手写清单，不新增研究）：hercules（System/360）、86Box/PCem（IBM 5150）、
   Mini vMac（Macintosh 128K）、Fuse（ZX Spectrum）、Snes9x/Mesen（SFC）、MAME neogeo（Neo Geo MVS）——
   现 registry 共 26 条目。

## 三、生成日志 + 交叉自检

```
已生成 26 条目的两份文档：
  docs/emulators_registry.md
  其它信息/模拟器清单_20261104.md
backend_type 非法：无（全部 26 条目在 01 slot_loader 7 项枚举内）
```

**出处变更说明**：`其它信息/模拟器清单_*.md` 由"五线手写"改为"registry.json 自动渲染"；手写版仍含
"接入优先级建议、可运行性分级"等策展性内容，已随 v1.1 迁移为 registry 的 status/risks 字段，
生成器只渲染结构性字段（策展性长文另留，见开放问题）。

## 四、TASK-72 两份总收尾

- **72-A**：catalog_check 重复 id 检测升级（跨文件 + id_registry 台账对账），反例 10/10 全绿，全库 1987 条 CC-02 0 冲突；手册补"v 全量文件替代制"。
- **72-B**：registry v1.1（26 条目 + media_classes_allowed 交叉索引）+ gen_emulator_doc.py 双文档自动生成，backend_type 自检全绿。

## 五、开放问题

1. 策展性长文（接入优先级、可运行性分级说明）尚未纳入 registry schema，是否新增 `notes` 字段待定；
2. registry 回写协作流程（05/01 线增改如何回写母表）仍未定；
3. 手写版旧 `模拟器清单_20261104.md` 已被本次生成覆盖（同日期同名），如需保留手写历史需另行归档。
