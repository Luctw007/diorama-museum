# TASK-291-E 完成报告

## 交付物清单
- **回归测试矩阵扩展卡**（docs/回归测试矩阵扩展_v1.md，≥2000 字节）：
  - §①新接线点清单三处：P1 co_active_max 激活判读点（exhibit_host.gd）、P2 导览调度器（narr_tour_controller.gd）、P3 口播序列推进（narr_player.gd），各含位置与关键符号；
  - §②矩阵扩展用例表 14 条（R-291-01~14）：每接线点 3-5 条静态用例，覆盖符号存在/幂等/互斥/上限/独立口径/序列完整/跳过语义/重置/推进；
  - §③回归复跑记录：scene_check（load_steps=19、13 挂点全 PASS、rc=0）+ gd 自检（17 文件 MISS 0/FAIL 0）+ 门禁口径。
- 改动清单：只新增 1 份 md + 本报告；不实机；02/03/04/05 线零改动。

## 矩阵自证
字节数（UTF-8）见报告末自证块（>2000）；三接线点用例表命中：P1 五条（R-291-01~05）、P2 四条（06~09）、P3 五条（10~14）逐条贴出。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. 矩阵自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 任务书前置 2「TASK-291-A/B/C 完成报告（若同批未完成则以任务书为准）」——同批未完成时按任务书接线点口径写矩阵；A/B/C 代码已先落地（本批次顺序：代码→自检→文档卡），矩阵以仓库实际代码为准，与任务书口径等价。
2. 用例数按「每接线点 3-5 条」上限 15 条内取 14 条（P1 5/P2 4/P3 5），满足下限 9 条。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。

---

## 矩阵字节数自证

```
4665 字节
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
