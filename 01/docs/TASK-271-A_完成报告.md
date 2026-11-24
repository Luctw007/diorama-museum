# TASK-271-A 完成报告

## 交付物清单
- **四厅台本接入实装**：narr_player.gd 新增 `HALL_NARR_IDS`（五件布局 → 口播 id 序列，占位轨 116 口径；黎明厅两条含 narr_eniac）+ `play_hall_narr()`（切厅播本厅首条；未知厅降级 FALLBACK_NARR；多条序列逐条推进待 04 线台本时序定案）；exhibit_host.gd 切厅钩子 `_notify_hall_narr()`（switch_hall 成功后触发）。
- **口播单互斥收口**：play_hall_narr → play_narr 既有「停旧播新」语义（116）——同一时刻仅一条口播，切厅打断旧口播；同一口播在播时幂等不重启。
- 台本文本零落地 01（数据源=04 线 16/22/27/41 号台本只读引用，路径写进注释）；四台本文件存在性已核对（OK×4）。
- 回归：gd 符号 MISS 0（play_hall_narr 符号命中）/ 命名 FAIL 0。

## F-9 接入关键行
narr_player.gd L23-29（HALL_NARR_IDS 挂接表）、L78-83（play_hall_narr）；exhibit_host.gd L229（切厅钩子调 _notify_hall_narr）、L232-237（_notify_hall_narr 触发）。

## 待实装验证清单
①口播切换手感（切厅打断旧口播的实际听感）；②语音播放实机（占位轨 wav 加载/播放）；③多条口播逐条推进（现只播首条，待 04 线台本时序）；④正式解说轨替换占位轨（04 线配音/TTS 产出后）；⑤HUD 口播状态行位置观感。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：56/56 全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. F-9 接入自证：关键行见上节；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 黎明厅两条口播（hall_intro + eniac）为挂接演示；其余三厅先挂 intro——四厅台本条目级挂接待 04 线台本条目 id 定案后扩展（不臆造条目 id）。
2. 口播 id 沿用 116 占位轨（正式解说轨待 04 线产出替换，红线遵守零联网引用）。
3. F-9 不销账（边界遵守：销账待 04 线同轮确认）。
4. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 49，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 156 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（56 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 49，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 156 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（49 包）        PASS  全部 FAIL 0
结果：56/56 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== exhibit_host.gd        [exhibit_host] funcs=26 signals=0
   [OK] has_method play_hall_narr → 存在
== narr_player.gd         [narr_player] funcs=6 signals=0
汇总：16 文件；符号池 funcs 156 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 56/56 通过（2026-11-21 23:46:21）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 49 ≥ 30
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
