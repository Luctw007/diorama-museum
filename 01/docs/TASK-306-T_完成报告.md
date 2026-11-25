# TASK-306-T 完成报告（306 轮次收口总览卡）

> 任务 306-T（01 线）：306 轮次收口总览卡（20 份产出总登记）。状态：完成。本报告即总览卡交付物。

## ① 本轮 20 份产出总登记表

| # | 主题 | 交付物路径（01/docs 或 01/scripts 或 01/godot） | 状态 |
|---|---|---|---|
| 306-A | R5-a 销账状态登记校验实装 | scripts/release_check.py（R5_HARD + check_r5a） | 完成 |
| 306-B | R5-b 排期状态登记校验实装 | scripts/release_check.py（check_r5b） | 完成 |
| 306-C | R5-c 待实机条数一致性实装 | scripts/release_check.py（check_r5c） | 完成 |
| 306-D | R5-d 封版文档齐备性实装 | scripts/release_check.py（check_r5d） | 完成 |
| 306-E | R5-e 残留扫描 + R5-f 扩展自守实装 | scripts/release_check.py（check_r5e/check_r5f） | 完成 |
| 306-F | R5 实装收口卡 | docs/R5实装收口卡_v1.md | 完成 |
| 306-G | 子树局部位移实装 | godot/scripts/explode_controller.gd（STEP_L2/_subtree_base/explode_subtree） | 完成 |
| 306-H | 相机聚焦运镜实装 | 同文件（FOCUS_DURATION_MIN/MAX/focus_requested/focus_node） | 完成 |
| 306-I | L3 代表件高亮渲染实装 | 同文件（_rep_highlight/_apply_rep_highlight） | 完成 |
| 306-J | 面包屑状态实装 | 同文件（_breadcrumb/get_breadcrumb） | 完成 |
| 306-K | 深层性能回收实装 | 同文件（_set_subtree_visibility） | 完成 |
| 306-L | F-14 六项实机回填录入表 | docs/F14六项实机回填录入表_v1.md | 完成 |
| 306-M | B-4 实测值回写执行卡 | docs/B4实测值回写执行卡_v1.md | 完成 |
| 306-N | F-12/13/14 统一实机排期卡 | docs/F121314统一排期卡_v1.md | 完成 |
| 306-O | 第三批槽位登记方案卡 | docs/第三批槽位登记方案卡_v1.md | 完成 |
| 306-P | 第三批 manifest 预登记核对卡 | docs/第三批manifest预登记核对卡_v1.md | 完成 |
| 306-Q | 全馆功能排期台账 v7 | docs/全馆功能排期台账_v7.md | 完成 |
| 306-R | F 系列待实机清单汇总 v3 | docs/F系列待实机清单汇总_v3.md | 完成 |
| 306-S | 回归测试矩阵 v3 | docs/回归测试矩阵扩展_v3.md | 完成 |
| 306-T | 306 收口总览卡 | docs/TASK-306-T_完成报告.md（本报告） | 完成 |

## ② 台账 v7 ↔ 待实机 v3 一致性核对

- **条数一致**：台账 v7 §② F-7~F-15 验收口径条数与待实机 v3 §① 总表一致；v3 合计 69 项/格，release_check R5-c 机器断言「合计 69 == 母本 9 行加和 69」复跑一致。
- **前置一致**：F-14 前置（301-J/L 已静态落地）+ 306-L 回填表注记在两卡同步；F-13 第三批（306-O/P 等用户点头）两卡同步；F-6 深化引擎续五件（306-G~K 静态落地、观感待实机）两卡同步；B-4（306-M 回写执行卡待实测）两卡同步。
- **阻塞点一致**：阻塞方均为用户（二进制编译/低配机型/实机执行）+ 03 线（第三批产包定案）；01 线侧无阻塞——两卡口径无冲突。

## ③ 本轮遗留交接清单

1. **B-4 待实测**：co_active_max 权威值回写（306-M 四步 + 梯度表单，三条件未齐不执行，B-04 仍 SKIP）；
2. **F-13 待用户二进制 + 第三批待点头**：第二批 SIMH 三槽 dry-run 待转 live；第三批四台待用户点头产包 + 二进制来源核实（306-O/P 方案已出，未建 manifest）；
3. **F-14/F-9/F-10/F-11/F-12/F-15 待用户实机**：共 69 项/格 + F-9 听感，执行卡/回填表/统一排期卡已齐（301-M/N/P + 306-L/N），01 线不代执行；
4. **R5 转硬待 F-1~F-15 收口**：R5_HARD=False 现状，四项前提（B-4 实测/F-13 二进制/F-14 六项/69 项清零或降级）齐备后置 True（306-F §②）；
5. **门禁基线更新**：verify_all 本轮 61/61（较 301 轮 60/60 增 1 项；完工包 52→54 入账，release_check R3 54 ≥ 30）；release_check R1 61/61、R2 五槽位全绿（三台 live + 第二批 SIMH dry-run）、R3 54、R4 残留 1 处（信息）、R5-a~e 信息全过 + R5-f PASS——下一轮以此为新基线。

## 与任务书的漂移

1. 任务书 §3 要求正文 ≥1200 字而红线写 500–600 字：总览卡含 20 份总登记表，按 §3 交付物口径执行（正文区 ≥1200 字），红线字数要求适用于常规报告——本卡为汇总型，与 291-T/301-T 总览卡同口径；总登记表、一致性核对、遗留清单三节即总览卡正文。
2. 产出总登记表按实况 20 份（含本卡）登记；306-A~E 五件共用 release_check.py 一个文件、306-G~K 五件共用 explode_controller.gd 一个文件，表中逐条列了各自新增符号。
3. 执行备注：验收命令按仓库实际用 `python`；两条门禁在无他线 python 进程窗口串行干净复跑（verify 61/61、release_check 硬断言 FAIL 0 处 rc=0），日志见下。
4. 交付落点统计：306 轮次共改 2 个源文件（release_check.py、explode_controller.gd）、新增 10 份文档卡 + 20 份完成报告，全部在 01 线目录内。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== release_check.py（R5 全行 + 汇总）==
[INFO] R5-a 台账 全馆功能排期台账_v7.md §① F-1~F-6 销账登记 6/6 行状态+产物成文（信息级，R5_HARD=False 不计 rc）
[INFO] R5-b 台账 全馆功能排期台账_v7.md §② F-7~F-16 排期登记 10/10 行成文（信息级，R5_HARD=False 不计 rc）
[INFO] R5-c 汇总卡 F系列待实机清单汇总_v3.md 合计 69 vs 母本 9 行加和 69 一致（信息级，R5_HARD=False 不计 rc）
[INFO] R5-d 封版文档齐备性 9/9 文件在案（信息级，R5_HARD=False 不计 rc）
[INFO] R5-e 残留扫描 8 文件：命中 0 处（无臆造残留）（恒不计 rc）
[PASS] R5-f 扩展自守：R1~R5 全硬断言 FAIL 0 处
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
