# TASK-301-K 完成报告

## 交付物清单
- **导览调度器挂载 main.tscn**（F-10 挂载点收口）：ext_resource 区新增 `[ext_resource type="Script" path="res://scripts/narr_tour_controller.gd" id="14_tour"]`；顶层 node 区新增 `NarrTourController`（type="Node" parent="."，与 NarrPlayer/ExhibitHost 并列，script=ExtResource("14_tour")）；load_steps 19→22（本轮与 301-L 墙体碰撞合并改，最终 ext 14 + sub 7 + 1 = 22）。
- 静态验收：scene_check S-01 load_steps=22 / S-02 14 挂点全存在、总检 PASS、rc=0；gd 符号 MISS 0 / 命名 FAIL 0；待实机项续挂（导览实机行为待用户实机）。

## 实装关键行
main.tscn L1（load_steps=22）、L15（ext_resource 14_tour）、L101-105（NarrTourController 节点，NarrPlayer 后并列）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. scene_check：总检 PASS、rc=0，S-01 load_steps=22 + S-02 14_tour 挂点行（日志块 2）；3. 实装自证：关键行见上节 + 待实机声明。

## 与任务书的漂移
1. 任务书「load_steps 同步 +1」——本轮 K/L 两卡先后改同一文件，最终 load_steps 19→22（K 增 ext +1、L 增 sub +2），以合并后最终值 22 为准（scene_check S-01 校验通过）。
2. 挂载位置与 NarrPlayer 并列（parent="." 顶层，依赖 /root/Main/NarrPlayer 路径一致）——与任务书口径一致。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

5. 执行备注：本轮验收基线 60/60；scene_check S-01 load_steps=22（ext 14 + sub 7 + 1）、S-02 14 挂点全存在、rc=0；gd 自检 funcs 175 MISS 0 / FAIL 0；首次 58/59 因 gamecube 反链瞬时红，单步复跑收敛后干净重跑全绿。
6. 挂载后 narr_tour_controller 依赖路径（/root/Main/NarrPlayer）与 tscn 实际一致，无漂移。
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

## 验收日志块 2（scene_check）

```
  [PASS] S-01 load_steps=22（ext 14 + sub 7 + 1 = 22）
  [PASS] S-02 1_gw (res://scripts/gateway_client.gd) 文件存在
  [PASS] S-02 2_player (res://scripts/player.gd) 文件存在
  [PASS] S-02 3_device (res://scripts/device_loader.gd) 文件存在
  [PASS] S-02 4_inspect (res://scripts/inspect_controller.gd) 文件存在
  [PASS] S-02 5_picker (res://scripts/device_picker.gd) 文件存在
  [PASS] S-02 6_explode (res://scripts/explode_controller.gd) 文件存在
  [PASS] S-02 7_expanel (res://scripts/explode_panel.gd) 文件存在
  [PASS] S-02 8_host (res://scripts/exhibit_host.gd) 文件存在
  [PASS] S-02 9_enc (res://scripts/encyclopedia_panel.gd) 文件存在
  [PASS] S-02 10_narr (res://scripts/narr_player.gd) 文件存在
  [PASS] S-02 11_startup (res://scripts/startup_check.gd) 文件存在
  [PASS] S-02 12_hallnav (res://scripts/hall_nav_panel.gd) 文件存在
  [PASS] S-02 13_portalhub (res://scripts/portal_hub.gd) 文件存在
  [PASS] S-02 14_tour (res://scripts/narr_tour_controller.gd) 文件存在
  [INFO] S-06 DeviceLoader 与 ExhibitHost 并存（设计有意：单机直连 + 展厅模式）
  [PASS] 总检：main.tscn 静态校验通过（ext 14 / sub 7）
主场景接线静态合法（待 Godot 实机确认表现层）
SCENE_RC=0
```

## 验收日志块 3（gd 自检）

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
