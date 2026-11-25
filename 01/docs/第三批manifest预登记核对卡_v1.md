# 第三批 manifest 预登记核对卡 v1（docs/第三批manifest预登记核对卡_v1.md · TASK-306-P）

> TASK-306-P 交付。306-O 方案卡（映射 + 字段模板）→ 四台逐台预登记核对：逐字段核对现状与待核实项。
> 只改 01 目录，**清单级引用、不建 manifest、不改 slot_loader/release_check、不下载/不编译二进制**。

## ① 四台逐台核对表（字段现状 + 结论）

| 字段 | hercules-s370 | openmsx-msx2 | mini-vmac-macplus | 86box-pcxt |
|---|---|---|---|---|
| slot_id | 已定 | 已定 | 已定 | 已定 |
| backend_type | hercules（[需核实]） | openmsx（[需核实]） | minivmac（[需核实]） | 86box（[需核实]） |
| module | null 预留（不建） | null 预留（不建） | null 预留（不建） | null 预留（不建） |
| device_class | mainframe（[需核实]） | computer（[需核实]） | computer（[需核实]） | computer（[需核实]） |
| media_classes | disk（[需核实]） | cartridge（[需核实]） | disk（[需核实]） | disk/cartridge（[需核实]） |
| binary_hint | third_party/hercules/s370（[需核实]） | third_party/openmsx（[需核实]） | third_party/minivmac（[需核实]） | third_party/86box（[需核实]） |
| license | QPL 隔离（需核实） | GPLv2 隔离（需核实） | GPL 许可版本需核实 | GPLv2 隔离（需核实） |
| 现状结论 | 预留，未建 manifest | 预留，未建 manifest | 预留，未建 manifest | 预留，未建 manifest |

- 现状核实：slots/emulators/ 下仅七槽位 manifest（mame-apple2/simh-pdp8/simh-hp2100/simh-nova/simh-altair-8800/stella/fake-slot），四台均未建（slot_loader --list 复跑佐证）。

## ② 登记触发条件（两项齐备才落地）

1. **用户点头产包**：第三批四台产包定案（03 线侧，02 线 287-B v3 口径卡 9/10 已出、产包未完成）；
2. **二进制来源核实**：四台二进制编译路径/许可版本核实完毕（301-O 清单 [需核实] 项关闭）。

## ③ 声明

- **清单级引用，不建 manifest**：本卡只登记字段现状与待核实项；manifest 创建、slot_loader BACKEND_TYPE_MODULE 扩展、release_check 第三批判定落地均待触发条件满足后的后续任务（306-O §④）。
- 转正路径：先 dry-run（module 就位 + 二进制缺失可干跑）→ 二进制就位后 live（release_check R2 口径）。
