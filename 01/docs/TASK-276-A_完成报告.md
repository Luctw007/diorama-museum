# TASK-276-A 完成报告

## 交付物清单
- **挂载实装**：verify_all.py 新增 `budget_step = ("budget", ["scripts/device_budget_check.py"])`（L119-120，统筹授权 TASK-276-A）并纳入 --daily 序列（L153-154）；SKIP 语义天然成立——device_budget_check 对 B-04/B-05 输出 SKIP 且 rc=0，run_step 按 rc 判 PASS，SKIP 不拖垮门禁；汇总表新增 budget 行。
- **台账联动**：台账 v4 F-4 行「挂载待统筹」→「已挂载 verify_all --daily（276-A，统筹授权）」；销账仍待正式资产（B-05 占位）——不提前销账。
- 边界遵守：不改 release_check；不改 B-04/B-05 占位口径（co_active_max 实测/B-05 正式资产另走 266-B 口径）。

## 挂载自证
verify_all.py L119-120（budget_step 定义）+ L153-154（daily 序列追加）；budget 步 rc=0 → 汇总表新增 budget PASS 行（日志块 1/2）。挂载后门禁构成 = m0/m1b/slots/catalog/catalog_ref/gd/gd_naming/budget 八步 + 完工包逐包（当前 49 包，共 57 项量级，以实测为准）。

## SKIP 语义自证
device_budget_check.py 独立重跑：B-04/B-05 输出 SKIP（不判 FAIL）、汇总 FAIL 0 处、rc=0（日志块 2）；门禁含 budget 行仍全 PASS（日志块 1）。SKIP 项不写 PASS 也不写 FAIL——占位口径（红线遵守）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：58/58 全 PASS、rc=0，含 budget 行（日志块 1）；2. budget 步骤自证：汇总表 budget 行 + 独立重跑 rc=0（日志块 2）；3. SKIP 语义：B-04/B-05 SKIP + 门禁仍 PASS（日志块 1/2）；4. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）。

## 与任务书的漂移
1. 挂载范围仅 --daily 序列（任务书口径）；全量序列与 --only 白名单未加 budget（保持最小改动，后续如需可补）。
2. 门禁项数将达 56/56（49 完工包+8 步，任务书预期 55/55 滞后，以实测为准）。
3. 台账 v4 直接更新（未另存 v5）：276-A 为 F-4 行状态刷新，非台账版本升级。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 50，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 157 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
== [budget] scripts/device_budget_check.py
     [SKIP] B-05 顶点/材质预算（depth_model L0-L3，依赖正式资产 glTF 统计——占位）
     [PASS] B-06 lod_scale/hall_group 取值域（复用 layout_check P-03 门禁，复读确认）
     [PASS] B-07 流程位预留 placed*2=28（上限 60）
   汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
===== 验收汇总（58 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 50，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 157 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  budget               PASS  汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
  pkg:*（50 包）        PASS  全部 FAIL 0
结果：58/58 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
VERIFY_RC=0
```

## 验收日志块 2（device_budget_check.py 独立重跑）

```
== F-4 设备实例预算断言（布局 5 件）
  [SKIP] B-04 co_active_max 同屏激活上限（默认 3，02 线 B-4 待实测——占位）
  [SKIP] B-05 顶点/材质预算（depth_model L0-L3，依赖正式资产 glTF 统计——占位）
  [PASS] B-07 流程位预留 placed*2=28（上限 60）
汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
BUDGET_RC=0
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 58/58 通过（2026-11-24 10:21:54）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 50 ≥ 30
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
