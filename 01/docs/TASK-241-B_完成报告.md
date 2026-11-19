# TASK-241-B 完成报告

## 交付物清单
- **实机验收单**：新增 `docs/F1F2实机验收单_v1.md`（2810 字节）——§0 全局前置（玩家碰撞体 add_to_group("player") 契约说明）+ 六项逐条「前置/操作步骤/预期/结果记录栏」+ 结果汇总栏；**结果栏一律留空（待用户填写），不预填「通过」**。
- **手册更新**：godot_first_boot.md 步 3 改枢纽大厅启动口径（241-A 定案联动）+ 新增 §5「F-1/F-2 传送点实机验收」指引（玩家碰撞体前置、启动即 hub、点选传送、双向可达、失败回写方式）。
- 回归：gd MISS 0 / FAIL 0；scene_check PASS；layout_check --all 5 份全 PASS。

## 验收单自证（六项逐条 + 字节数）
六项：①四厅双向可达 ②切厅清场无残留 ③图鉴与大厅面板同显 ④真跑进程跨厅存活 ⑤点选传送 ⑥碰撞传送；每条含前置/操作步骤/预期/结果记录栏（☐ 通过 ☐ 失败 备注：留空）。字节数 2810 > 1500（日志块 2）。

## 手册更新自证
godot_first_boot.md 增补节原文见日志块 2；步 3 改为「枢纽大厅（默认厅，241-A 定案）：1 台 altair-8800 白模占位 + 4 个半透明门框；黎明厅 4 台需经门框传送进入后核对」。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：53/53 全 PASS、rc=0（日志块 1）；2. 验收单自检：六项逐条 + 字节数 2810（日志块 2）；3. 手册增补节原文（日志块 2）；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 验收单与手册更新联动 241-A 启动厅定案（默认厅=hub）：步 3 预期与 §5 指引按 hub 口径写——两任务同轮落地，避免手册与代码漂移。
2. 04 线 66 号文档存在（DOC66_OK），仅作口径参照未修改（只读红线）。
3. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。
4. 门禁预期 49/49 落后实测（46 完工包+7 步=53 项）。门禁曾两度瞬时红（m0 端口被占、catalog_ref 他线新包反链未跟上），独立复跑收敛 FAIL 0，最终干净重跑 53/53。

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

## 验收日志块 2（验收单自检 + 手册增补节原文）

```
（验收单字节数）
验收单字节数: 2810

（手册增补节 §5 原文节选）
## 5. F-1/F-2 传送点实机验收（TASK-241-B 增补）
1. 玩家碰撞体前置：player.gd 为 M0 无碰撞自由相机（无 PhysicsBody）——需给玩家节点挂
   碰撞体（建议 Camera 子节点 Area3D + CollisionShape3D，或 CharacterBody3D）并
   add_to_group("player")（过滤契约 = portal_hub.gd PLAYER_GROUP）。
2. 启动即枢纽大厅：默认厅已定案为 exhibit_hub.json（241-A）。预期：1 台 altair-8800
   白模 + 4 个半透明门框。
3. 点选传送：鼠标捕获中对准门框点左键（18px 屏幕拾取），命中即切厅；大厅导航面板（M 键）
   按「枢纽 / 子厅」分组列出五厅。
4. 双向可达：hub 四门框进四厅 → 各厅入口门框（z=+5.5）回 hub；对照验收单①~⑥填结果。
5. 失败时：红色报错整段 + 失败条目号回写验收单「结果汇总」栏。

（gd/场景/布局回归）
汇总：16 文件；符号池 funcs 146 / signals 7；MISS 0；已知缺口 KG 0
GD_SYMBOL_RC=0
扫描 16 个 gd；class_name 6 个；FAIL 0
GD_NAMING_RC=0
  [PASS] 总检：main.tscn 静态校验通过（ext 13 / sub 5）
SCENE_RC=0
--all 完成：5 份布局
LAYOUT_RC=0
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
