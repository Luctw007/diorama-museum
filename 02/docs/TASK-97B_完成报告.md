# TASK-97B 完成报告（02 线 2/2 · 轻量）

## 一、交付物

`emulators_registry.json` 新增 `gateway_key` / `slot_manifest` / `ci_involved` 三列（26 条）；
`emulators_registry.md` 重新生成（对齐 01 线 monorepo `01/repo/01/` 实况）。

## 二、对照证据（三行已对齐）

| sim_id | 网关登记键 | 槽位 manifest | CI | 后端 |
|---|---|---|---|---|
| fake-slot | `fake`（非 fake-slot） | 齐 | 是（m0） | 已实现 |
| mame-apple2 | `mame-apple2` | 齐 | 是（m1b） | 骨架 |
| simh-pdp8 | `simh-pdp8` | 齐 | 是（slot_consistency） | 预留 |

## 三、待协清单（3 条，不改 01 文件）

1. **fake vs fake-slot 键名**：网关 EMULATORS 内置键为 `fake`，槽位 manifest/registry 为
   `fake-slot`，指向同一后端 `gw.emulators.fake_emulator`，slot_loader 会注册出两个条目，建议 01 线统一；
2. **simh-pdp8 media_classes**：registry=`[tape,disk]` vs 01 manifest=`[firmware]`，PDP-8 实为纸带/磁盘，
   疑似 01 manifest 笔误；
3. **mame-apple2 media_classes**：registry=`[disk,tape]` vs 01 manifest=`[disk]`，建议 01 线确认是否补 tape。

## 四、开放问题

- 待协 3 条需 01 线确认后回写（涉及 01 侧文件，本线不改）。
