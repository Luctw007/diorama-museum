# TASK-233-B 完成报告 · 第三批研究卡卷四（SGI Indigo + Compaq Portable）

> 03 线 · 第三批首批研究卡卷四（2 张），研究卡先行、为定案后产包备料。本任务只出研究卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物

| 卡 | 路径 | 字节 | 证据 |
|---|---|---|---|
| SGI Indigo | `hall-workstation/04_SGIIndigo.md` | 4,885 | S129–S130 |
| Compaq Portable | `hall-personal-batch2/17_CompaqPortable.md` | 4,780 | S131–S132 |

- 证据索引回填：`hall-mainframe/06_证据包索引.md` 追加 S129–S130（SGI Indigo，注归工作站厅）、`hall-personal-batch2/05_证据包索引.md` 追加 S131–S132（Compaq Portable）。

## 二、验收日志（第 4 章）

**1. 字节数（均 >1200）**
```
04_SGIIndigo.md        4885 字节
17_CompaqPortable.md   4780 字节
```
**2. 五要素自检（逐张七节齐全）**
```
SGI Indigo：一史实 / 二尺寸 / 三部件草图 / 四 L1-L3 / 五模拟器行 / 六出处 / 七展呈叙事 ✔
Compaq Portable：一史实 / 二尺寸 / 三部件草图 / 四 L1-L3 / 五模拟器行 / 六出处 / 七展呈叙事 ✔
```
**3. verify_all --daily --cache（49/49 全 PASS，rc=0）**
```
结果：49/49 通过
catalog_ref：REF-02 反链缺失 0 · REF-03 漂移 0（registry 1583 = 目录 1583）· FAIL 0
```

## 三、「需核实」清单

- **SGI Indigo**：尺寸、模拟器候选（MAME/QEMU MIPS）许可与 Indigo 支持度。
- **Compaq Portable**：尺寸（28 磅/12.7kg）、模拟器候选（86Box/PCem）许可与机型支持度。

## 四、与任务书的漂移

- **SGI Indigo 证据登记位置**：任务书前置写「hall-workstation\ 与 hall-personal-batch2\05_证据包索引.md」，但 hall-workstation 无独立证据索引文件（此前 SPARCstation 1 的 S113–S115 亦就近登记于 hall-mainframe/06 索引）。故 S129–S130 就近登记于 `hall-mainframe/06_证据包索引.md` 并注「研究文件归工作站厅」，保持与既有做法一致。
- 其余无漂移：两台均按预检总卡「无成熟模拟器 → emulator="none"」口径落模拟器行；未动 jsonl、未产包、未碰 01/02/05 线。

## 五、第三批研究卡全量汇总（228 + 233，共 8 张）

| 序号 | 研究卡 | 证据编号 | 模拟器口径 |
|---|---|---|---|
| 1 | IBM System/370 | S119–S120 | hercules（QPL，已核实） |
| 2 | MSX2+（Panasonic FS-A1） | S78–S80（复用） | openmsx（GPLv2，已核实） |
| 3 | Macintosh Plus | S121–S122 | mini-vmac（GPL，需核实） |
| 4 | IBM PC XT | S123–S124 | none（86Box 候选，GPLv2 已核实） |
| 5 | Acorn Archimedes | S125–S126 | none（Arculator/ArcEm 候选需核实） |
| 6 | Sinclair ZX81 | S127–S128 | none（EightyOne/sz81 候选需核实） |
| 7 | SGI Indigo | S129–S130 | none（MAME/QEMU 候选需核实） |
| 8 | Compaq Portable | S131–S132 | none（86Box/PCem 候选需核实） |
