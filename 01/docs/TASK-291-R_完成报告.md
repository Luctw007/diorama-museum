# TASK-291-R 完成报告

## 交付物清单
- **家电影音厅导览动线核对卡**（docs/家电影音动线核对_v1.md，≥2000 字节）：
  - §①台本动线逐站核对表 5 行（96 号 v3 站 2~6：CRT/VHS/DVD/Walkman/CD）——01 线现状逐台核对：crt-tv 包在 content 但无第五厅布局；vhs-vcr/dvd-player 未产；walkman-tpsl2/cd-player 跨线未同步（05 线侧已产/在产）——五站全部无布局接线，如实标注；
  - §②F-9 家电影音厅接入口径登记：第五厅未挂 HALL_NARR_IDS/导航/layout_check（无 exhibit_appliance.json）；接入顺序建议五步（产包→布局→三处挂接→预算复核）；
  - §③待实机项 4 行（停留/半径/音效建议值、互动判定部件级断言、新增音频 4 条待 08 线、图鉴/时间轴墙衔接）。
- 改动清单：只新增 1 份 md + 本报告；不实机、不改 04 线 77/96 号文档、02/03/05 线零改动。

## 核对卡自证
字节数（UTF-8）见报告末自证块（>2000）；逐站核对表 5 行命中（任务书要求「5 行」）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. 核对卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 任务书背景「家电影音厅 5 台产包收官」——01 线 content 实测仅 crt-tv 一台在仓（vhs/dvd 未产、walkman/cd 在 05 线未同步），卡内以仓库实际为准如实标注（不臆造收官）。
2. 任务书「台本动线 vs 布局/接线现状」核对结论=第五厅整体未上线（无布局文件），逐站核对表 5 行即该结论的逐台证据。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。

---

## 核对卡字节数自证

```
3529 字节
```

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 51，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 17 个 gd；class_name 7 个；FAIL 0
== [budget] scripts/device_budget_check.py
   汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
===== 验收汇总（59 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 51，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 17 个 gd；class_name 7 个；FAIL 0
  budget               PASS  汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
  pkg:*（51 包）        PASS  全部 FAIL 0
结果：59/59 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```
