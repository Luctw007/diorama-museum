# TASK-251-A 完成报告

## 交付物清单
- **F-5 方案文档**：新增 `docs/F5工作台布局方案_v1.md`（三节）——①工作台布局方案（exhibit_workbench.json 第六件布局：hall_group 不加（五值未含 workbench，留 04 线定案）、hub 补 portal 的顺序约束（先建布局再加 portal，P-01）、设备占位 1~2 台 L2/L3、20×12 缺省尺寸、PortalHub 通用解析零新代码）；②拆解台衔接收口静态核对（切厅不打断拆解已证 241-A；最近拆解台续接 F-6 预口径；待实装验证 3 条）；③F-5 实装排期建议（方案先行、实装与 04 线子区布局同轮）。
- 边界遵守：未写 Godot 生产代码、未建布局文件（方案先行）。

## 方案自证（三节命中 + 字节数）
三节命中：`## ① 工作台布局方案（exhibit_workbench 第六件布局）` / `## ② 拆解台衔接收口（静态核对结论）` / `## ③ F-5 实装排期建议`；字节数 2520 > 1500（日志块 2）。①含六行方案表（布局文件/hall_group 不加/hub portal 顺序约束/设备占位/尺寸/传送零新代码）；②含三条静态核对结论与三条待实装验证。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：53/53 全 PASS、rc=0（日志块 1）；2. 方案自检：三节命中 + 字节数（日志块 2）；3. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）；4. 漂移（拆解衔接核对结论）见下节。

## 与任务书的漂移
1. **拆解台衔接静态核对结论**：切厅 exit_explode 无需钩子——clear_devices 只清 ExhibitHost 子树、DeviceRoot 不受切厅影响（241-A 已证）；「最近拆解台续接」归 F-6 实装，本方案只定口径。
2. hall_group 不为 workbench 加枚举（227-A 五值未含），布局缺省视为子厅；扩枚举属 02 线，留 04 线子区定案。
3. 任务书路径 `D:\work\01\repo\godot\` 实为 `01\repo\01\godot\`（既有事实）。
4. 门禁日志与 241/246/251-B 共用同一次干净重跑（同批状态）。

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

## 验收日志块 2（F-5 方案自检）

```
（三节命中行 + 字节数）
## ① 工作台布局方案（exhibit_workbench 第六件布局）
## ② 拆解台衔接收口（静态核对结论）
## ③ F-5 实装排期建议
F5文档: 2520 字节
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
