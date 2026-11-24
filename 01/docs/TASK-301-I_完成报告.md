# TASK-301-I 完成报告

## 交付物清单
- **F-6 深化 L2/L3 级联爆炸视图分档实装**（explode_controller.gd，20→24 funcs）：
  - `_subtree_focus`/`_rep_focus` 状态（空=整机 L1 视图）；
  - `enter_subtree(asmb_id)`：EXPLODED 中点选某件进入子树视图（L2），校验 asmb_id 在 _depth 拓扑中，不在返回 false；
  - `focus_rep(node)`：子树内点选带 role 标注节点 → L3 代表件高亮（不位移）；`exit_subtree()` 回 L1；
  - `get_depth_level()` 三档返回：L3（rep_focus）/L2（subtree_focus）/L1（EXPLODED）/L0（其余）；
  - `current_view_level()` 查询；set_close/_on_device_loaded 重置分档状态。
- 缺口如实标注：子树运镜（0.9–1.2s）与子树局部位移/面包屑属引擎后续实现（depth_model §4/§6），标「待核实」不臆造。
- 静态验收：gd 符号 MISS 0 / 命名 FAIL 0；待实机项续挂（L2/L3 观感待用户实机）。

## 实装关键行
explode_controller.gd L38-41（分档状态）、L63-66（换设备重置）、L164-166（set_close 重置）、L216-259（get_depth_level 三档 + enter/exit_subtree/focus_rep/current_view_level）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. gd 自检：MISS 0 / FAIL 0（日志块 2）；3. 实装自证：关键行见上节 + 待实机声明（封版硬断言随 301 门禁队列一并复跑，见日志块 3 佐证）。

## 与任务书的漂移
1. 任务书「复用 _depth 拓扑与 _apply_explode 位移」——enter_subtree 复用 _depth 拓扑校验；位移仍全树 _apply_explode（子树局部位移标待核实，depth_model §4 引擎后续实现），如实回写。
2. L3 代表件以 node.has_meta("role") 判定（annotations role 标注依赖 03 线数据），缺失按无 role 处理——不臆造选择标准（depth_model §7-3）。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 52，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：17 文件；符号池 funcs 175 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 17 个 gd；class_name 7 个；FAIL 0
== [budget] scripts/device_budget_check.py
   汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
===== 验收汇总（60 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 52，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：17 文件；符号池 funcs 175 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 17 个 gd；class_name 7 个；FAIL 0
  budget               PASS  汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
  pkg:*（52 包）        PASS  全部 FAIL 0
结果：60/60 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（gd 自检）

```
== explode_controller.gd  [explode_controller] funcs=24 signals=3
== exhibit_host.gd        [exhibit_host] funcs=30 signals=0
   [OK] has_method is_explode_locked → 存在
   [OK] has_method last_exploded_device → 存在
   [OK] has_method play_hall_narr → 存在
== narr_player.gd         [narr_player] funcs=9 signals=0
== narr_tour_controller.gd [narr_tour_controller] funcs=10 signals=0
   [OK] has_method play_hall_narr → 存在
== player.gd              [player] funcs=4 signals=0
汇总：17 文件；符号池 funcs 175 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 17 个 gd；class_name 7 个；FAIL 0
GD_NAMING_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 60/60 通过（2026-11-25 00:49:57）
[INFO] R3 wip 清单（不计入 rc）：xbox
[PASS] R3 完工包 52 ≥ 30
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
