# 第四批 meta/runtime 文本备底 v1

> 03 线 TASK-318-N 交付。补齐第四批 10 台 meta/runtime 文本备底（meta 的 name/intro/era/manufacturer/category/description/sources + runtime 的 emulator/system/media_hint/bios_required），供定案后 05 装配 meta.json。第四批 emulator 全 `none`，runtime 走「静态演示向」。只改 03 目录，纯文本备料，不产包、不改 jsonl。

## 一、10 台逐台 meta/runtime 文本草案

| 设备 | name | era | manufacturer | category | emulator | media_hint | bios_required |
|---|---|---|---|---|---|---|---|
| Amstrad CPC 464 | Amstrad CPC 464 | 1984 | Amstrad | personal-computer | none | tape | false |
| Atari 800 | Atari 800 | 1979 | Atari | personal-computer | none | cartridge | false |
| Nokia 5110 | Nokia 5110 | 1998 | Nokia | phone | none | firmware | false |
| Motorola StarTAC | Motorola StarTAC | 1996 | Motorola | phone | none | firmware | false |
| Manchester Mark 1 | Manchester Mark 1 | 1949 | University of Manchester | early-computer | none | tape | false |
| IBM 701 | IBM 701 | 1952 | IBM | mainframe | none | tape | false |
| Osborne 1 | Osborne 1 | 1981 | Osborne Computer | personal-computer | none | floppy | false |
| TI-99/4A | TI-99/4A | 1981 | Texas Instruments | personal-computer | none | cartridge | false |
| Palm III | Palm III | 1998 | Palm, Inc. | pda | none | firmware | false |
| BlackBerry 850 | BlackBerry 850 | 1999 | Research In Motion | phone | none | firmware | false |

- **sources**（逐台映射研究卡证据编号 S137–S156）：CPC464=[S137][S138]；Atari800=[S139][S140]；Nokia5110=[S141][S142]；StarTAC=[S143][S144]；ManchesterMark1=[S145][S146]；IBM701=[S147][S148]；Osborne1=[S149][S150]；TI994A=[S151][S152]；PalmIII=[S153][S154]；BlackBerry850=[S155][S156]。
- **runtime 走「静态演示向」**：10 台 emulator 全 `none`，候选模拟器记 THIRD_PARTY 备底（见 318-M），不设 emulator；bios_required 全 false。
- **BlackBerry 850**：meta 备底照 device_id=blackberry-850、目录占位 M-MP-000172 标注，不代裁决。

## 二、取用声明

产包时按本卡取用为 meta.json/runtime.json 素材源；本卡**不代产包**、不写 content/<id>/meta.json、不 allocate、不代定案。

---

> 本卡为纯文本备料，不写 content/<id>/meta.json、不产包、不改 jsonl、不 allocate、不代定案。
