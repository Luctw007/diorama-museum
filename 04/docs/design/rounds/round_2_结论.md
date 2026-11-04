# M1 回归报告 round_2（2026-11-02）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。
> 执行线：04 线（独立复测，不轻信 01 线自证；未修改 01 线任何代码）。

## 结论

**通过（绿灯）** —— 自动化档全绿：m0 23/23、m1 42/42（连续 2 轮）、m1b 19/19、五包键名校验 unknown 全 0。round_1 两条 DEFECT（ROLLBACK-01 / KEYMAP-01）均已独立复测闭环（open → closed，见 defects/INDEX.md）。下游手工档与待实机档按 09 号漏斗规则解锁，重新获得执行资格。

## 自动档

| 脚本 | 断言数 | PASS/FAIL | 备注 |
|---|---|---|---|
| m0_check（17331） | 23 | 23/0 | 含回滚断言：首帧 6 == 保存点 5+1 |
| m1_check 第 1 轮（17333） | 42 | 42/0 | **关键断言**：回滚后第一帧 11 == 保存点 10+1（竞态修复统计性复核 ①） |
| m1_check 第 2 轮（17333，连续复跑） | 42 | 42/0 | **关键断言**：回滚后第一帧 11 == 保存点 10+1（统计性复核 ②，连续 2/2 通过） |
| m1b_check（17334） | 19 | 19/0 | apple-ii 57 键 unknown=0；首键 key_a -> {keyboard: KEY_A} |
| run_profile 五包 --json | 5 包 | 5/0 | baby 36 / eniac 4 / edsac 16 / edvac 4 / apple-ii 57，unknown 全 0，对象/legacy 双形态无漂移 |
| 新增草案 a~i | — | 未执行 | 01 线 m2_check.py 与 docs/m2_assert_draft.md 尚未产出（本节截至 round_2 核验），落位见 08 号 v2.0 §2.2 |

## DEFECT 处置

| 编号 | round_1 状态 | round_2 状态 | 闭环依据 |
|---|---|---|---|
| DEFECT-M1-ROLLBACK-01 | open | **closed** | fake_emulator `_frame_lock` 互斥（L68/L133-136/L215-234）+ m1 连续 2 轮精确命中；本缺陷报告新增 §7 |
| DEFECT-M1B-KEYMAP-01 | open | **closed** | run_profile `MAP_KEY_RE`+`_key_entry` 对象分支 + m1b 19/19 + 五包无漂移；本缺陷报告新增 §6 |

无新 DEFECT 产生；无需按 09 号 §4 提级。

## 手工最小集

round_1 因漏斗红灯搁置；round_2 全绿后恢复执行资格。按 08 号 v2.0 §4.2 新最小集（m0+m1b+内容包校验）自 round_3 起生效，手工 10 条清单执行责任在 01 线按 08 号 §4.1 第 2 层进行。

## 贴证（round_2 完整日志，全部为本轮生成）

- `design/rounds/m0_round_2.log`（23 断言全量输出）
- `design/rounds/m1_round_2_run1.log`（42 断言全量输出）
- `design/rounds/m1_round_2_run2.log`（42 断言全量输出，连续复跑）
- `design/rounds/m1b_round_2.log`（19 断言全量输出）
- `design/rounds/run_profile_round_2.log`（五包 --json 全量 JSON）

## 环境

- 执行机：本机 Windows + Python 3.7.3（`C:\Program Files\Python37\python.exe`；与 round_1 同环境；`__pycache__/*.cpython-37.pyc` 佐证 3.7 兼容，py_compile 全过）
- 网关：01\repo\gw\gateway.py v2（127.0.0.1:17331/17333/17334）
- 内容包：03 线 manchester-baby（36 键 legacy）/ eniac（4 键 demo）/ edsac（16 键，新产）/ edvac（4 键 demo，新产）；05 线 apple-ii（57 键对象形态，1.0.0）
- 卫生处置：执行前独立清空 %TEMP%\diorama_*.json（实查 0 残留）；m1_check 已自带入口自清（01 线已落地 DEFECT 建议）
- 端口复核：执行前 netstat 确认 17331-17334 无占用

## 备注

- round_3 建议入口：待 01 线 16-A 产出 verify_all.py 后以其为标准执行入口（见 09 号 v2.0 §5 增补）；未产出前按 08 号 §6.1 顺序 m0 → m1 → m1b 手动执行。