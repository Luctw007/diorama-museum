# M1 回归报告 round_1（2026-10-31）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。

## 结论

**失败（红灯）** —— m0 通过；m1 失败（1 断言）；m1b 失败（1 断言）。按 09 号漏斗规则：下游手工档与待实机档搁置，待 01/05 线修复后重开 round_2。

## 自动档

| 脚本 | 断言数 | PASS/FAIL | 备注 |
|---|---|---|---|
| m0_check | 23 | 23/0 | 网关 v1 基础链路全绿 |
| m1_check | 26 | 25/1 | 失败：回滚后第一帧 frame_id==保存点（期望 ≥保存点+1）→ DEFECT-M1-ROLLBACK-01 |
| m1b_check | 11 | 10/1 | 失败：apple-ii 57 键全判未知（input_map 对象化契约漂移）→ DEFECT-M1B-KEYMAP-01 |
| 新增草案 a~i | — | 未执行 | 待 01 线实现 m2_check 后纳入 |

## 手工最小集（10 条）

搁置（漏斗红灯，按 08 号 §4.2/09 号 §8 规则）。

## 贴证

- design/defects/DEFECT-M1-ROLLBACK-01.md（open，归 01 线）
- design/defects/DEFECT-M1B-KEYMAP-01.md（open，归 05/01 线）

## 环境

- 执行机：本机 Windows + Python 3.7.3（全部脚本 `from __future__ import annotations` 兼容，py_compile 全过）
- 网关：01\repo\gw\gateway.py v2（127.0.0.1:17331/17333/17334）
- 内容包：03 线 eniac / manchester-baby（旧 input_map 格式）；05 线 apple-ii（input_map 已切对象格式，1.0.0）
- 卫生处置：本轮已清理 %TEMP%\diorama_*.json 残留；建议 m1_check 增加首行自清（见 DEFECT 备注）

## 备注

- m0_check 日志：design/rounds/m0_round_1.log
- m1_check 日志：design/rounds/m1_round_1.log（含两轮完整输出与 stderr 尾）
- m1b_check 日志：design/rounds/m1b_round_1.log