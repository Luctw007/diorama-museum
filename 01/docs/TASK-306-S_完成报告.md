# TASK-306-S 完成报告

> 任务 306-S（01 线）：回归测试矩阵 v3（306 轮次新接线点静态用例扩展）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\回归测试矩阵扩展_v3.md`（新增另存，3400 字节 ≥1500；v2 保留原文）：①两处新接线点清单（P8 release_check R5-a~f、P9 explode_controller 引擎续五件）；②每处 2-4 条静态用例表（P8 四条：符号存在/信息级不误杀/自守判硬/转硬开关；P9 五条：符号存在/常量口径/面包屑 push-pop/高亮集合清空/命名纪律）；③回归复跑记录（release_check + gd 自检 + verify_all）。
- `D:\work\01\repo\01\docs\TASK-306-S_完成报告.md`（本报告）。

## 矩阵自证

- 字节数：3400（>1500 达标）。
- 接线点 P8/P9 关键符号成文：check_r5a~f/R5_HARD/_r5_report/_latest_doc/_ledger_section_rows；explode_subtree/focus_node/_apply_rep_highlight/get_breadcrumb/_set_subtree_visibility + STEP_L2/_subtree_base/_rep_highlight/_breadcrumb/focus_requested。
- 用例表 9 条（R-306-01~09）全部为不实机可复跑断言；复跑记录引用干净重跑日志（2026-11-25）。

## 与任务书的漂移

1. P9 用例数取 5 条（任务书「每处 2-4 条」上限 4 条）：引擎续五件符号面较大，拆分符号存在/常量口径/面包屑/高亮/命名五条更可断言——超出 1 条，属用例拆分非新增范围。
2. P8 用例数取 4 条（上限内）：符号存在/信息级不误杀/自守判硬/转硬开关。
3. 执行备注：只写用例+复跑，不改引擎/脚本（边界遵守）；验收命令按仓库实际用 `python`；三条命令在无他线 python 进程窗口串行干净复跑，日志见下。
4. 用例断言全部以实装源码为准：R-306-02/03 复跑数字（69==69、FAIL 0）与门禁干净重跑日志一致，未臆造。
5. 矩阵 v3 用例 9 条与 v2 11 条、v1 既有用例构成当前回归矩阵全集，实机行为用例统一标「待用户实机」。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== release_check.py（汇总）==
[PASS] R5-f 扩展自守：R1~R5 全硬断言 FAIL 0 处
汇总：硬断言 FAIL 0 处 → rc=0
RC=0

== gd 自检 ==
汇总：17 文件；符号池 funcs 182 / signals 8；MISS 0；已知缺口 KG 0
扫描 17 个 gd；class_name 7 个；FAIL 0
```
