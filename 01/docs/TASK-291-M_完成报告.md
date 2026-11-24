# TASK-291-M 完成报告

## 交付物清单
- **gateway_client 真跑 HUD 收口核对卡**（docs/真跑HUD收口核对_v1.md，≥2000 字节）：
  - §①标记行/直起入口现状核对表 4 行（RUN_CANDIDATE_SLOTS 与 251-B 逐台一致/标记行静态提示/request_direct_launch 恒拒绝/与 251-B 不建 manifest 口径一致）；
  - §②待用户实机 4 条复核（281-A 清单逐条续挂/更新：①维持②维持③维持④维持，全部如实）；
  - §③与 06 线 RUN-07/RUN-08 衔接说明（只登记口径不越权：RUN-07 点选复测归 06 线、RUN-08 捕获互斥模式可复用、不新增 RUN 编号）。
- 改动清单：只新增 1 份 md + 本报告；不实机、不下载/不启动模拟器、不处理 06 线 RUN 事务、02/03/04/05 线零改动。

## 核对卡自证
字节数（UTF-8）见报告末自证块（>2000）；现状核对表 4 行命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. 核对卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 任务书前置 3「第三批真跑候选槽位预留_v1.md（251-B 四台槽位）」与实际一致（若路径有出入以仓库实际为准——实际在 docs/ 下，无出入）。
2. RUN-07/RUN-08 只登记口径：任务书「不越权处理 06 线事务，只登记口径」——按边界执行，未动 06 线任何文件。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。
4. 复核时发现本轮验收基线已升至 59/59（51 完工包，他线新入册 playstation-2/sega-dreamcast 等），与 281-A 时期 58/58 不同——以本轮干净重跑为准；真跑 HUD 三件现状不受新包影响。

---

## 核对卡字节数自证

```
3283 字节
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
