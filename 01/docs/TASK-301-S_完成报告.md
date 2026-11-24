# TASK-301-S 完成报告

## 交付物清单
- **回归测试矩阵扩展 v2**（docs/回归测试矩阵扩展_v2.md，另存新文件，v1 保留，≥1500 字节）：①四处新接线点清单（P4 级联爆炸 get_depth_level L2/L3、P5 玩家碰撞体 add_to_group("player")、P6 NarrTourController 挂载、P7 墙体 StaticBody3D）；②每处 2-4 条静态用例表 11 条（R-301-01~11：符号存在/分档语义/状态复位/拓扑校验/命名/同步语义/挂载点/依赖路径/尺寸一致性）；③回归复跑记录（scene_check + gd 自检 + 门禁口径）。
- 改动清单：只新增 1 份 md + 本报告；不实机、不改 v1 原文、不改引擎/场景代码（仅写用例+复跑）、02/03/04/05 线零改动。

## 矩阵自证
字节数（UTF-8）见报告末自证块（>1500）；四处新接线点清单 + 用例表 11 条命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. scene_check + gd 自检：全 PASS、rc=0（日志块 2）；3. 矩阵自证见上节。

## 与任务书的漂移
1. P4 用例断言按 301-I 实装源码（enter_subtree/focus_rep/get_depth_level 三档）撰写，与任务书「以实装源码为准」一致。
2. scene_check 复跑为合并后 load_steps=22（K/L 同轮），用例 R-301-08/10 已按 22 断言。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

4. 执行备注：本轮验收基线 60/60；scene_check 复跑 load_steps=22、gd 自检 funcs 175 MISS 0 / FAIL 0；首次 58/59 因 gamecube 反链瞬时红，单步复跑收敛后干净重跑全绿。
5. 用例 11 条覆盖四处接线点全部关键断言（符号/分档/挂载/尺寸）。
---

## 矩阵字节数自证

```
3872 字节
```

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

## 验收日志块 2（scene_check + gd 自检）

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

GD_SYMBOL_RC=0
扫描 17 个 gd；class_name 7 个；FAIL 0
GD_NAMING_RC=0
```
