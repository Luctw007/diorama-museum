# TASK-281-A 完成报告

## 交付物清单
- **真跑台标记实装**：gateway_client.gd 新增 `RUN_CANDIDATE_SLOTS`（hercules-s370/openmsx-msx2/mini-vmac-macplus/86box-pcxt，静态数据源=251-B 槽位登记）+ HUD 真跑候选标记行（「真跑候选：…（预留态，待产包定案+用户编译二进制）」）。
- **launch_device 直起入口静态定义**：`request_direct_launch(slot_id)`——真跑条件满足时才触发；当前四台为预留槽位 → 一律 false + 状态行提示，**不实际启动任何模拟器**（红线遵守）。
- 回归：gd 符号 MISS 0 / 命名 FAIL 0（gateway_client 15 funcs）。

## F-8 实装关键行
gateway_client.gd L14-16（RUN_CANDIDATE_SLOTS）、L75-80（HUD 标记行）、L88-95（request_direct_launch 直起入口）。

## 待用户实机清单
①四台真跑需 03 线产包定案 + 用户编译二进制（F-13 前置未满足，直起入口恒拒绝）；②HUD 标记行观感与位置；③真跑条件满足后 request_direct_launch 接真实启动链（launch_device 决策链）的接线点待转正轮次；④真跑标记与「可玩台」正式视觉（F-8 完整口径）待 04 线标记规格。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：58/58 全 PASS、rc=0，含 budget 行（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. F-8 自证：关键行见上节；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 标记数据源按 251-B 四台预留槽位（任务书口径）；标记为**静态提示文本**而非设备级视觉标记——四台尚无布局设备可挂（第三批未产包），设备级标记待产包定案后接。
2. 直起入口放 gateway_client（真跑 HUD 所在地），返回恒 false（预留态）——「调用仅在真跑条件满足时触发」以当前恒拒绝形态体现，不臆造可用。
3. F-8 不销账（边界遵守：验收待用户实机）。
4. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 50，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 157 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
== [budget] scripts/device_budget_check.py
     [SKIP] B-05 顶点/材质预算（depth_model L0-L3，依赖正式资产 glTF 统计——占位）
     [PASS] B-06 lod_scale/hall_group 取值域（复用 layout_check P-03 门禁，复读确认）
     [PASS] B-07 流程位预留 placed*2=28（上限 60）
   汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
===== 验收汇总（58 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 50，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 157 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  budget               PASS  汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
  pkg:*（50 包）        PASS  全部 FAIL 0
结果：58/58 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== gateway_client.gd      [gateway_client] funcs=15 signals=0
汇总：16 文件；符号池 funcs 157 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 58/58 通过（2026-11-24 10:21:54）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 50 ≥ 30
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
