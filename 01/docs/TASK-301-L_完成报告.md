# TASK-301-L 完成报告

## 交付物清单
- **启动厅四面墙碰撞化**（main.tscn）：新增 2 个 BoxShape3D sub_resource（box_shape_wall_z 尺寸 20×3×0.3、box_shape_wall_x 尺寸 0.3×3×20，与既有 wall mesh 逐值一致）；WallN/S/W/E 四面墙各挂 Body（StaticBody3D）+ Shape（CollisionShape3D）子节点，白模视觉不变；load_steps 与 301-K 合并改至 22（ext 14 + sub 7 + 1）。
- 静态验收：scene_check 全 PASS、rc=0；待实机项续挂（碰撞走查待用户实机，F-14 执行卡 301-N 前置）。
- 改动清单：只改 main.tscn + 本报告；不改 02/03/04/05 线。

## 实装关键行
main.tscn L1（load_steps=22）、L17-25（2 个 BoxShape3D sub_resource）、L48-82（四面墙各 +Body/Shape 节点）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. scene_check：总检 PASS、rc=0，S-01 load_steps=22 + S-02 挂点行（日志块 2）；3. 实装自证：关键行见上节 + 待实机声明。

## 与任务书的漂移
1. 任务书「四面墙各加 StaticBody3D + CollisionShape3D（BoxShape3D 尺寸与对应 Wall MeshInstance3D 一致）」——按 box_wall_z/x 两个共享 shape 复用（同尺寸墙共用 sub_resource），不逐墙复制，语义等价。
2. load_steps 与 301-K 同轮合并改（任务书「同步」）——最终 22，scene_check S-01 通过。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

5. 执行备注：本轮验收基线 60/60；scene_check S-01 load_steps=22（ext 14 + sub 7 + 1）、总检 PASS、rc=0；首次 58/59 因 gamecube 反链瞬时红，单步复跑收敛后干净重跑全绿。
4. 碰撞盒复用 box_shape_wall_z/x 两个共享 sub_resource（同尺寸墙共用），语义等价于逐墙复制。
5. 白模视觉零改动（mesh 与 transform 原样保留），仅新增物理层。
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
