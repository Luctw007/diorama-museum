# TASK-301-M 完成报告

## 交付物清单
- **F-11/F-12/F-15 共轮实测执行卡**（docs/F11F12F15共轮实测执行卡_v1.md，≥1200 字节）：①统一走位顺序 4 阶段（F-15 表 A/B 采集 → F-12 七条校准 → 低载档表 C+F-11 五条 → 04 线 94 号对齐与 F-1/F-2 交叉复测，同一实机窗口三卡共用走位）；②数据回填路径（F-15 表 A 15 格/表 B 10 格/表 C 10 格 + F-12 偏差回写 246-A 清单 + F-11 五条判据）；③明确「不实机、供用户实机轮执行」。
- 改动清单：只新增 1 份 md + 本报告；不实机、不代用户执行、不下载/不启动模拟器、02/03/04/05 线零改动。

## 执行卡自证
字节数（UTF-8）见报告末自证块（>1200）；走位顺序 4 阶段 + 数据回填路径 5 行命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：全 PASS、rc=0（日志块 1）；2. 执行卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 走位顺序按「先常规档后低载档」编排（任务书「先 F-12 采 F-15 表 A/B 再切低载档」口径一致）。
2. F-12 待实机为 4 条（286-A §③），其中七条校准为主线——执行卡以七条校准为走位骨架、③④为收尾关联，条数口径不变。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数以本轮干净重跑为准。

4. 执行备注：本轮验收基线 60/60（52 完工包+8 步，他线新增 gamecube 包）；首次 58/59 因 gamecube 反链瞬时缺失，单步复跑 catalog_ref 收敛后干净重跑全绿。
5. 走位四阶段与 291-T §②第 2 批共轮建议一致。
---

## 执行卡字节数自证

```
2369 字节
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
