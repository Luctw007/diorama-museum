# TASK-291-F 完成报告

## 交付物清单
- **HUD 诊断行汇总收口口径卡**（docs/HUD诊断行汇总口径_v1.md，≥2000 字节）：
  - §①三行现状对照表：拆解层级行（inspect_controller._diag_label，16,150 绿）、真跑候选标记行（gateway_client._candidate_label，16,38 金）、口播状态行（narr_player._hud_label，16,240）——触发/内容/刷新方式/位置逐列；
  - §②统一规格建议：行序登记（顶部固定区六行坐标）、`[诊断]` 前缀、刷新频率（状态行事件驱动/诊断行 60 帧节流）、占位文案字典、颜色 token（26 号 c-text-2 #A8A6A3 收口）；
  - §③实装轮次建议：本卡不实装（任务书边界），gd 改动三项标待排。
- 改动清单：只新增 1 份 md + 本报告；不改 gd、不改 04 线 26 号文档、02/03/05 线零改动。

## 口径卡自证
字节数（UTF-8）见报告末自证块（>2000）；三行对照表命中（拆解/真跑/口播三行六列齐）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. 口径卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 任务书前置 2/3 所给行号（inspect_controller L163-169、gateway_client L75-80）以仓库实际为准（inspect 诊断行 L157-169、gateway 标记行 L75-80 一致；narr 口播状态行为 271-A 新增，无 L 号对账）——已在卡内按实际位置登记。
2. 统一规格建议为**口径**（本卡不实装）；三行现状均可用，未发现需立即修复项。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。
4. 三行坐标以仓库实际代码登记（inspect 诊断行 16,150、gateway 候选行 16,38、narr 口播行 16,240）；统一规格建议的行序含 291-B 新增的馆长路线行（16,258），收口口径覆盖四行。

---

## 口径卡字节数自证

```
3522 字节
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
