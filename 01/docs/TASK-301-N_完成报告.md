# TASK-301-N 完成报告

## 交付物清单
- **F-14 六项实机执行卡**（docs/F14六项实机执行卡_v1.md，≥1200 字节）：①六项逐项执行步骤 + PASS 判据 + 回填栏（①四厅双向可达 ②切厅清场无残留 ③图鉴与大厅面板同显 ④真跑进程跨厅存活 ⑤点选传送 ⑥碰撞传送，六行全列）；②前置标注（⑥碰撞传送需玩家碰撞体 301-J + 墙体碰撞 301-L 已静态落地后可达，实机可达性待验证）；③失败项回写为下一轮修复任务输入（241-B 口径）。
- 改动清单：只新增 1 份 md + 本报告；不实机、不代用户执行、不预填「通过」、02/03/04/05 线零改动。

## 执行卡自证
字节数（UTF-8）见报告末自证块（>1200）；六项逐项步骤 6 行 + 前置标注命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. 执行卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 任务书前置 2「godot_first_boot.md §5」已读；六项判据以 241-B 验收单原文为准逐条转写，不增删判据。
2. ⑥前置标注按本轮 301-J/L 实装后现状登记（「已静态落地、实机可达性待验」），比任务书背景（碰撞体缺失）前进一步。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

4. 执行备注：本轮验收基线 60/60；首次 58/59（catalog_ref 瞬时红 gamecube 反链），单步复跑收敛后干净重跑全绿。
5. 六项判据与 241-B 验收单原文逐字一致，未增删判据。
---

## 执行卡字节数自证

```
2237 字节
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
