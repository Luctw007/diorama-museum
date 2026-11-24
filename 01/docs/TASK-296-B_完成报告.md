# TASK-296-B 完成报告

## 交付物清单
- **F-10 导览调度器实装——复核确认**：narr_tour_controller.gd 五件齐备：①TOUR_STATIONS 39 号 8 站卡序列；②start_tour/next_station/stop_tour 调度接口 + HUD 徽标行；③STATION_LAYOUT + _notify_station_narr 与 F-9 口播联动（复用单口播互斥通道）；④57 号常量组（1.4/2.5 m/s、200°/s、FOV 50~100、阻尼 0.15s、宽限 15s）；⑤_process 超时计时。
- **F-9 深化——复核确认**：narr_player.gd HALL_NARR_IDS 每厅序列（dawn 7/mainframe 6/personal 8/console 9/hub 1，按四厅台本条目顺序，未定案标 [待定案]）+ 逐条推进（切厅重置、跳过未定案、advance_narr 手动、finished 信号自动推进）；占位轨沿用 116。
- 静态验收：gd 符号 MISS 0 / FAIL 0；待实机项续挂：F-10 七条（276-B §③）+ 271-A 遗留①⑤（④正式轨替换待 04 线）。

## 实装自证（关键行 + 待实机清单）
narr_tour_controller.gd L13-24（8 站卡）、L34-43（常量组）、L61-100（调度接口）、L118-148（超时+口播联动）；narr_player.gd L23-47（每厅序列）、L106-146（重置+跳过+推进）。待实机七条：镜头接管手感/双档限速/57 号红线/口播镜头同步/馆长路线切换/8 站卡时长/晕动复测；+271-A 遗留①⑤。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁 59/59 PASS rc=0（日志块 1）；2. gd 自检 MISS 0/FAIL 0（日志块 2）；3. 实装自证见上节；4. release_check FAIL 0 处 rc=0（日志块 3）。

## 与任务书的漂移
1. 任务书背景「F-10 未实装/F-9 遗留③」为撰写时现状；执行时实装已于 **291-B/291-C** 落地——本轮为复核 + 回归，不重复实装。
2. 57 号常量落 narr_tour_controller.gd（任务书未指定文件，与 276-B 预研口径一致；player.gd 同款为 291-I 落地）。
3. 导览调度器未挂 main.tscn，挂载点待实机轮。
4. 未定案条目以 `[待定案:站名]` 前缀落地并播放时跳过；占位轨仅 2 条。
5. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（本轮干净重跑）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 51，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 17 个 gd；class_name 7 个；FAIL 0
== [budget] scripts/device_budget_check.py
   汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
===== 验收汇总（59 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 51，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 17 个 gd；class_name 7 个；FAIL 0
  budget               PASS  汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
  pkg:*（51 包）        PASS  全部 FAIL 0
结果：59/59 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== exhibit_host.gd        [exhibit_host] funcs=30 signals=0
   [OK] has_method is_explode_locked → 存在
   [OK] has_method last_exploded_device → 存在
   [OK] has_method play_hall_narr → 存在
== narr_player.gd         [narr_player] funcs=9 signals=0
== narr_tour_controller.gd [narr_tour_controller] funcs=10 signals=0
   [OK] has_method play_hall_narr → 存在
汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 17 个 gd；class_name 7 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 59/59 通过（2026-11-25 00:01:15）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 51 ≥ 30
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
