# TASK-231-B 完成报告

## 交付物清单
- **P-01~P-03 实装**：`01/scripts/layout_check.py` 新增 portals 段（P-01/P-02，L96-123）与 hall_group/lod_scale 段（P-03，L124-130）、模块级 `HALL_GROUPS` 五值（L33-34）、docstring 规则说明（L13-16）。三字段均为顶层可选，缺省等价旧行为。
- **零破坏回归**：存量四厅（dawn/mainframe/personal/console）复跑全 PASS，三字段缺省下 L-01~L-04 行为不变。
- **门禁挂钩**：verify_all 与 release_check 均不含 layout 步（既有事实，任务书「若含」条件不成立），layout 校验口径为 `layout_check.py --all` 独立直跑；本轮未改动门禁步构成。

## 断言关键行（layout_check.py）
P-01（L110-114）target 非空 string 且 ∈ {content 下 .json 去后缀} ∪ HALL_GROUPS，否则报「不可解析」；P-02（L115-121）position 3 元数值 + L-03 厅界（|x|≤w/2、y≥0、|z|≤d/2）；P-03（L125-130）hall_group ∈ 五值、lod_scale 数值 >0。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：50/50 全 PASS、rc=0（日志块 1）；
2. P-01~P-03 自证：内存断言——合法样例（hall_group=hub、lod_scale=1.5、target=exhibit_dawn）零错误；四条非法样例各命中 P-01（target=nonexistent）/P-02（position=[100,0,0]）/P-03（hall_group=wing）/P-03（lod_scale=0）；三字段全缺省零错误（旧行为）；存量 `--all` 四厅全 PASS（日志块 2）；
3. release_check：硬断言 FAIL 0 处、rc=0（日志块 3）；
4. 断言落点：layout_check.py L96-123（P-01/P-02）、L124-130（P-03）、L33-34（HALL_GROUPS）。

## 与任务书的漂移
1. lod_scale 取值域用 227-A「>0」（L-13 规范），任务书所写 0.5~2.0 属 226-A 旧提案口径；hall_group 用 227-A 五值（hub/dawn/mainframe/personal/console），非提案的 hub/wing。
2. 门禁预期 49/49 实为 50/50：完工包 43 + 7 步（他线产包增长，任务书预期滞后）。
3. verify_all 无 layout 步（「若含」条件不成立）：零破坏以 `layout_check.py --all` 直跑全 PASS 为证据，未改门禁步构成。
4. portals[].rotation 沿用既有 devices.rotation 口径（4 元数值数组），不额外接受朝向角写法——与 layout_check 既有 L-04 一致；exhibit_host 运行时「position 第 4 元存朝向角」的兼容不影响本断言。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 139 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（50 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 43，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 139 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（43 包）        PASS  全部 FAIL 0
结果：50/50 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（P-01~P-03 自证）

```
=== exhibit_console.json
  OK（设备 2 台）
=== exhibit_dawn.json
  OK（设备 4 台）
=== exhibit_mainframe.json
  OK（设备 4 台）
=== exhibit_personal.json
  OK（设备 3 台）
--all 完成：4 份布局
LAYOUT_RC=0

（内存断言）
LEGAL errors: []
P-01~P-03 内存断言全 PASS
RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 50/50 通过（2026-11-19 23:48:34）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 43 ≥ 30
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
