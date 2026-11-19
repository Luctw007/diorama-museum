# TASK-246-B 完成报告

## 交付物清单
- **排期台账 v2**：新增 `docs/全馆功能排期台账_v2.md`（3705 字节）——①F-1~F-3 销账行（实装产物+完成轮次+待实机项，以各完成报告为据）；②F-4~F-16 剩余排期刷新表（每项责任线/前置依赖/建议轮次/验收口径/实机依赖，F-12/F-13/F-14 标注「待用户实机」）；③与 221-A 16 子任务映射核对（F-1 范围按实装事实微调、总数不变）。销账依据覆盖 231-A 至 241-B 六份完成报告与 F1F2 验收单。

## 台账自证（销账行 + 排期行数 + 字节数）
销账 3 行（F-1/F-2/F-3，各含实装产物+完成轮次+待实机项）；剩余排期 13 行（F-4~F-16，其中 F-12 白模灰盒实测/F-13 槽位≥5/F-14 首启动线首验三项标注「待用户实机」，F-13 另挂「待用户编译第二批 SIMH 二进制」）；映射核对 1 节（F-1 范围微调、总数不变）；字节数 3705 > 1500。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：53/53 全 PASS、rc=0（日志块 1）；2. 台账自检：销账行+排期行+字节数（日志块 2）；3. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）；4. 漂移（F-4~F-16 排期变化）见下节。

## 与任务书的漂移
1. F-1 原「大厅总览面板」实装口径调整为 Hub 骨架+传送点（231-A），面板归类在 F-3 落地，「镇馆之宝入口+真跑标记」并入 F-8——16 子任务总数不变、范围微调。
2. F-4 口径本轮（246-A）先行于台账（任务书前置 4 的「若未出则跳过引用」条件未触发）。
3. F-13 依赖用户侧（第二批 SIMH 二进制待编译、need_verify 续挂 6），标注「待用户」不臆造排期。
4. 门禁日志与 241/246-A 共用同一次干净重跑（同批状态）。

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

## 验收日志块 2（台账自检）

```
（销账行/排期行命中 + 字节数）
| F-1 销账 | 大厅总览面板 | portal_hub.gd+hub 布局+main.tscn（231-A）；玩家过滤（236-B）；面板归类部分并入 F-3 | ...
| F-2 销账 | 传送点 schema 落地 | layout_check P-01~P-03（231-B）；exhibit_hub 正式化+反向 portal+点选（236-A） | ...
| F-3 销账 | 大厅枢纽厅布局 | HallNavPanel 归类+启动厅定案 hub+三系统衔接收口（241-A） | ...
## ② F-4~F-16 剩余排期刷新
## ③ 与 221-A 16 子任务映射核对
台账v2: 3705 字节
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
