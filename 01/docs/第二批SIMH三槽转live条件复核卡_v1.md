# 第二批 SIMH 三槽转 live 条件复核卡 v1（docs/第二批SIMH三槽转live条件复核卡_v1.md · TASK-321-C）

> TASK-321-C 交付。复核第二批三槽（simh-hp2100/simh-nova/simh-altair-8800）二进制就位现状与转 live 条件。
> 只改 01 目录，纯文档复核，**不下载/不编译二进制、不改 manifest binary_hint**。

## ① 三槽逐槽现状表

| slot_id | run_status（--list 实测） | 二进制是否就位 | 转 live 条件 |
|---|---|---|---|
| simh-hp2100 | dry-run（MISSING 无二进制） | 未就位（third_party/simh/hp2100 无二进制） | 用户编译 SIMH HP 2100 并放置至 binary_hint 路径 |
| simh-nova | dry-run（MISSING 无二进制） | 未就位（third_party/simh/nova 无二进制） | 用户编译并放置 |
| simh-altair-8800 | dry-run（MISSING 无二进制） | 未就位（third_party/simh/altair8800 无二进制，名仍 [需核实]） | 用户编译并放置（二进制名 altair8800 为推定） |

## ② 结论

- **二进制仍未就位 → 维持 dry-run，不转 live**：三槽 run_status=dry-run 判合法（release_check R2 复跑 [PASS] 佐证），不臆造「已就位」。
- 转 live 判定口径不变（311-L）：二进制就位即 live，仍缺则保持 dry-run——release_check 无需改码。

## ③ 转 live 动作登记

- **一台一台验，不批量**：单槽二进制放置后单独跑 `slot_loader.py --list` 确认该槽 OK(二进制就位) + release_check R2 该槽 run_status=live；
- 转 live 后联动：F-13 前提推进（311-A 盘点卡更新）、R5 转硬四前提之一（F-13 二进制）部分推进；
- 01 线不代编译、不代放置（用户动作，301-O/311-L/311-O 口径）。
