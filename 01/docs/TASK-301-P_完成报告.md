# TASK-301-P 完成报告

## 交付物清单
- **F-9/F-10 口播与导览实机核对卡**（docs/F9F10口播导览实机核对卡_v1.md，≥1200 字节）：①F-10 七条逐项打勾口径（镜头接管/双档限速/57 号红线/口播镜头同步/馆长路线切换/8 站卡时长/晕动复测，七行全列）；②F-9 听感项 4 行（序列逐条推进听感/切厅重置/未定案跳过/271-A 遗留①⑤）；③共轮走位顺序 3 步（导览镜头与切厅相机衔接同走位）。
- 改动清单：只新增 1 份 md + 本报告；不实机、不代用户执行、不预填「通过」、02/03/04/05 线零改动。

## 核对卡自证
字节数（UTF-8）见报告末自证块（>1200）；F-10 七条 + F-9 听感项 4 行 + 共轮走位命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. 核对卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. F-9 听感项按 296-B/291-C 实装现状登记（序列推进/切厅重置/未定案跳过为新增听感项，271-A 遗留①⑤续挂）——与任务书前置 2/3 一致。
2. 共轮走位 3 步按「先 F-10 主线再穿插 F-9 听感再收尾」编排，与 291-T §②第 3 批建议一致。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

4. 执行备注：本轮验收基线 60/60（52 完工包+8 步，他线新增 gamecube 包并补反链）；首次 58/59 因 gamecube 反链瞬时红，单步复跑收敛后干净重跑全绿。
5. 共轮走位 3 步与 291-T §②第 3 批建议一致。
---

## 核对卡字节数自证

```
2211 字节
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
