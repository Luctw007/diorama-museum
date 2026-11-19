# TASK-246-A 完成报告

## 交付物清单
- **F-4 口径文档**：新增 `docs/F4切厅性能与灰盒校准_v1.md`（2825 字节）——①切厅性能口径（切换耗时目标 <100ms 白模阶段、清场重建 O(N) 预算、同帧新旧并存峰值预算、B-4 co_active_max 关联、lod_scale L-13 输入、refresh_budget_hint 帧率保护）；②白模灰盒校准清单七条（hub 门框尺寸/颜色/间距、反向门位置、设备朝向、调试圈、相机穿厅耗时——逐条「待实机校准」）；③设备实例预算复核（max_running=1、_placed 去重、调试圈记忆、配额语义）。
- 依据：221-A F-4、236-B 清单、exhibit_host.gd 现状、02 线 1x待办清单 v1.4 B-4（co_active_max 默认 3 待实测）。

## 文档自证（三节命中 + 字节数）
三节命中：`## ① 切厅性能口径` / `## ② 白模灰盒校准清单（逐条待实机校准）` / `## ③ 设备实例预算复核（现状核对，静态）`；字节数 2825 > 1500。校准清单七条为：门框尺寸比例/半透明色可读性/四门框间距动线/反向门位置对齐/设备占位朝向/调试圈站位/相机穿厅耗时——全部标「待实机校准」，无一条预填结论。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：53/53 全 PASS、rc=0（日志块 1）；2. 文档自检：三节命中 + 2825 字节（日志块 2）；3. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）；4. 漂移（校准项清单）见下节。

## 与任务书的漂移
1. 性能目标均为静态口径（未实机），一律标「待实机校准」，不写实测数字（红线遵守）。
2. B-4 co_active_max 引用 02 线 1x待办清单 v1.4 口径（默认 3 待实测、责任线 01 主/02 协）；本口径不预判权威值。
3. 校准清单扩为七条（任务书未列条目数），覆盖 236-B 遗留的碰撞层/门框/朝向项。
4. 前置 6 之 verify_all/release_check 回归共用同一次干净重跑（与 241/246-B 同批状态）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 46，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 146 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（53 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 46，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 146 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（46 包）        PASS  全部 FAIL 0
结果：53/53 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（F-4 文档自检）

```
（三节命中行 + 字节数）
## ① 切厅性能口径
## ② 白模灰盒校准清单（逐条待实机校准）
## ③ 设备实例预算复核（现状核对，静态）
F4文档: 2825 字节
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 53/53 通过（2026-11-20 01:26:06）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 47 ≥ 30
[PASS] R2 槽位 mame-apple2 已登记后端 gw.emulators.mame_apple2
[PASS] R2 槽位 mame-apple2 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 simh-pdp8 已登记后端 gw.emulators.simh_pdp8
[PASS] R2 槽位 simh-pdp8 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 stella 已登记后端 gw.emulators.stella
[PASS] R2 槽位 stella run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 第二批槽位 simh-hp2100 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-nova 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-altair-8800 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 许可记录存在 licenses/MAME.md
[PASS] R2 许可记录存在 licenses/SIMH.md
[PASS] R2 许可记录存在 licenses/Stella.md
[INFO] R4 gw\emulators\mame_apple2.py: 「占位」×1
[INFO] R4 残留扫描完成：命中 1 处（含骨架注记与新发现，只暴露不计 rc）
汇总：硬断言 FAIL 0 处 → rc=0
RELEASE_RC=0
```
