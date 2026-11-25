# 第三批 meta/runtime 文本备底 v1

> 03 线 TASK-318-C 交付。补齐第三批 10 台 meta/runtime 文本备底（meta 的 name/intro/era/manufacturer/category/description/sources + runtime 的 emulator/system/media_hint/bios_required），供点头后 05 装配 meta.json。只改 03 目录，纯文本备料，不产包、不改 jsonl。

## 一、10 台逐台 meta/runtime 文本草案

### 有模拟器 4 台

| 设备 | name | era | manufacturer | category | emulator | media_hint | bios_required |
|---|---|---|---|---|---|---|---|
| IBM System/370 | IBM System/370 | 1970 | IBM | mainframe | hercules | tape | false |
| MSX2（FS-A1） | MSX2（FS-A1） | 1988 | Panasonic | personal-computer | openmsx | cartridge | false |
| Macintosh Plus | Macintosh Plus | 1986 | Apple | personal-computer | mini-vmac | floppy | false |
| IBM PC XT | IBM PC XT | 1983 | IBM | personal-computer | pc86box | disk | false |

- **intro/description**：各台以一句话定位 + 年代 + 关键参数 + 影响为核心（照 313-B/C encyclopedia 初稿），description 含需核实参数标注。
- **sources**：System/370=[S119][S120]；MSX2=[S78][S79][S80]；Macintosh Plus=[S121][S122]；IBM PC XT=[S123][S124]。

### none 6 台

| 设备 | name | era | manufacturer | category | emulator | media_hint | bios_required |
|---|---|---|---|---|---|---|---|
| Acorn Archimedes | Acorn Archimedes | 1987 | Acorn | personal-computer | none | floppy | false |
| Sinclair ZX81 | Sinclair ZX81 | 1981 | Sinclair | personal-computer | none | tape | false |
| SGI Indigo | SGI Indigo | 1991 | Silicon Graphics | workstation | none | disk | false |
| Compaq Portable | Compaq Portable | 1983 | Compaq | personal-computer | none | floppy | false |
| Whirlwind | Whirlwind | 1951 | MIT | early-computer | none | tape | false |
| Apple Newton | Apple Newton | 1993 | Apple | pda | none | firmware | false |

- **sources**：Archimedes=[S125][S126]；ZX81=[S127][S128]；SGI Indigo=[S129][S130]；Compaq Portable=[S131][S132]；Whirlwind=[S133][S134]；Newton=[S135][S136]。
- **runtime 走「静态演示向」**：none 6 台候选模拟器记 THIRD_PARTY 备底（见 318-B），不设 emulator。

## 二、取用声明

产包时按本卡取用为 meta.json/runtime.json 素材源；本卡**不代产包**、不写 content/<id>/meta.json、不 allocate、不代点头。

---

> 本卡为纯文本备料，不写 content/<id>/meta.json、不产包、不改 jsonl、不 allocate、不代点头。
