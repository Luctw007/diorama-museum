# 第二批 SIMH 三槽转 live 预检卡 v1（docs/第二批SIMH转live预检卡_v1.md · TASK-311-L）

> TASK-311-L 交付。第二批 SIMH 三槽当前 dry-run（后端模块就绪、二进制缺失），本卡产出转 live 预检：
> 二进制就位核对清单 + 转 live 后 R2 断言口径。只改 01 目录，纯文档，**不下载/不代编译/不放置二进制**。

## ① 三槽逐台转 live 核对表

| slot_id | 当前 run_status | 二进制就位待办（用户侧） | 转 live 后 R2 口径 |
|---|---|---|---|
| simh-hp2100 | dry-run（MISSING 无二进制） | 编译 SIMH HP 2100 目标，放置 third_party/simh/hp2100（binary_hint 已配） | run_status=live（binary_path 命中即 live） |
| simh-nova | dry-run（MISSING 无二进制） | 编译 SIMH Data General Nova，放置 third_party/simh/nova | 同上 |
| simh-altair-8800 | dry-run（MISSING 无二进制） | 编译 SIMH Altair 8800（二进制名 altair8800 为推定 [需核实]），放置 third_party/simh/altair8800 | 同上 |

- 现状佐证：slot_loader --list 三槽均 MISSING(无二进制)（复跑输出见 311-L 报告日志块）；release_check R2 三槽 run_status=dry-run 判合法。

## ② 转 live 判定

- **二进制就位即 live，仍缺则保持 dry-run**：run_status_of 判定——module 非空 + binary_path 命中 → live；binary_path 未命中 → dry-run（196-B 口径不变）。转 live 不涉及 release_check 改码（判定函数已就绪），仅依赖二进制物理就位。

## ③ 用户动作清单（01 线不代做）

1. 编译三台 SIMH 目标二进制（许可口径见 licenses/SIMH.md，二进制不进仓）；
2. 放置到各槽位 binary_hint 指定路径（third_party/simh/<target>）；
3. 复跑 slot_loader --list 确认三槽 OK(二进制就位)。

## ④ 声明

- **不下载、不代编译二进制**：本卡只登记就位核对口径与转 live 判定；三槽转 live 后 F-13 前提推进（311-A 盘点卡同步更新），R5 转硬仍待其余三前提。
