# TASK-306-P 完成报告

> 任务 306-P（01 线）：第三批产包 · 四台 manifest 预登记核对卡 v1（清单级不落地）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\第三批manifest预登记核对卡_v1.md`（新增，2417 字节 ≥1200）：①四台逐台核对表（slot_id/backend_type/module=null 预留/device_class/media_classes/binary_hint 标需核实，各列现状+结论）；②登记触发条件（用户点头产包 + 二进制来源核实）；③声明「清单级引用，不建 manifest」。
- `D:\work\01\repo\01\docs\TASK-306-P_完成报告.md`（本报告）。

## 核对卡自证

- 字节数：2417（>1200 达标）。
- 四台逐台核对表八字段（slot_id/backend_type/module/device_class/media_classes/binary_hint/license/现状结论）成文，全部待核实项显式标注。
- 现状核实：slots/emulators/ 下仅七槽位 manifest（mame-apple2/simh-pdp8/simh-hp2100/simh-nova/simh-altair-8800/stella/fake-slot），四台均未建——slot_loader --list 复跑佐证。
- 触发条件两项齐备才落地（用户点头产包 + 二进制来源核实关闭 301-O 需核实项）；「不建 manifest」声明成文。

## 与任务书的漂移

1. device_class 四台均标 [需核实]（mainframe/computer 为建议值）：现有槽位 manifest 无第三批同型参照，不臆造定值。
2. 核对表比任务书列多出 license 列：许可隔离（QPL/GPLv2）是 301-O 清单既有字段，纳入核对成文。
3. 执行备注：不建 manifest、不改 slot_loader/release_check（边界遵守）；验收命令按仓库实际用 `python`；日志见下。
4. 核对卡与 306-O 方案卡字段逐一对齐：backend_type 建议值/module 预留 null/media_classes 枚举/binary_hint 路径全部同步，两卡无字段漂移。
5. 四台 device_class 建议值成文（mainframe/computer）：现无第三批同型 manifest 参照，全部标 [需核实]，等 03 线产包定案后据实修订。
6. slot_loader --list 复跑输出八槽位（七 manifest + 内置 fake），四台未出现在列表——与核对卡「现状结论：预留，未建 manifest」互证。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== slot_loader.py --list（节选：四台仍未建 manifest）==
mame-apple2        OK(二进制就位)   ...
simh-altair-8800   MISSING(无二进制)  ...
simh-hp2100        MISSING(无二进制)  ...
simh-nova          MISSING(无二进制)  ...
simh-pdp8          OK(二进制就位)   ...
stella             OK(二进制就位)   ...
介质目录 0 个：（空，红线下仅建目录）
SLOT_RC=0
```
