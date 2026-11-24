# TASK-291-C 完成报告

## 交付物清单
- **F-9 深化——多条口播序列逐条推进实装**（narr_player.gd，9 funcs）：
  - `HALL_NARR_IDS` 由单条扩为**每厅序列**：dawn 7 / mainframe 6 / personal 8 / console 9 / hub 1 条——按四厅台本（16/22/27/41 号）条目顺序挂接，条目 id 未定案处标 `[待定案:xxx]` 不臆造；
  - 推进逻辑：`play_hall_narr` 切厅重置游标（单口播互斥语义不变）；`_play_seq_current` 跳过未定案条目（HUD 提示）；`advance_narr` 手动推进；`_on_finished` 挂 `_player.finished` 信号实现「播完推进下一条」；占位轨沿用 116。
- 271-A 遗留③「多条口播逐条推进」销账；遗留①④⑤保持（实机/04 线产出）。
- 静态验收：gd 符号 MISS 0 / FAIL 0；四厅台本文本零落地 01（只读引用）。

## 实装关键行
narr_player.gd L23-47（每厅序列）、L63-65（游标）、L106-130（切厅重置+跳过 [待定案]）、L133-146（advance_narr/_on_finished）。

## 待实机清单（271-A 遗留续挂）
①口播切换手感；②语音播放实机；⑤HUD 状态行观感；新增：序列自动推进听感、[待定案] 跳过提示观感。④正式轨替换待 04 线产出。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. 实装自证：序列挂接+逐条推进关键行见上节；4. release_check：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 条目 id 未定案以 `[待定案:站名]` 前缀落地并**播放时跳过**；占位轨仅 2 条，实机当前每厅只播已定案条目（黎明厅 2 条、其余厅 1 条）。
2. 自动推进采用引擎内置 `finished` 信号（点号连接，不经字符串符号池，零 MISS）。
3. 黎明厅 CRT 辅厅合为 crt_room 一条；54 号听单分 crt/crt_lab 两条——差异已登记 291-J 清单 v2。
4. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。

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
[PASS] R1 验收基线 59/59 通过（2026-11-24 23:01:11）
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
