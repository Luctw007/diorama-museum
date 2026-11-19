# TASK-228-B 完成报告 · 第三批研究卡卷二（Macintosh Plus + IBM PC XT）

> 03 线 · 第三批首批研究卡卷二（2 张），研究卡先行、为定案后产包备料。本任务只出研究卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物

| 卡 | 路径 | 字节 | 证据 |
|---|---|---|---|
| Macintosh Plus | `hall-personal-batch2/13_MacintoshPlus.md` | 5,023 | S121–S122（续 S120） |
| IBM PC XT | `hall-personal-batch2/14_IBMPCXT.md` | 5,342 | S123–S124（续 S122） |

- 证据索引回填：`hall-personal-batch2/05_证据包索引.md` 追加 S121–S124。

## 二、验收日志（第 4 章）

**1. 字节数（均 >1200）**
```
13_MacintoshPlus.md   5023 字节
14_IBMPCXT.md         5342 字节
```
**2. 五要素自检（逐张七节齐全）**
```
Macintosh Plus：一史实 / 二尺寸 / 三部件草图 / 四 L1-L3 / 五模拟器行 / 六出处 / 七展呈叙事 ✔
IBM PC XT：一史实 / 二尺寸 / 三部件草图 / 四 L1-L3 / 五模拟器行 / 六出处 / 七展呈叙事 ✔
```
**3. verify_all --daily --cache（40/41，exit=0）**
```
结果：40/41 通过
catalog_ref  FAIL 1  →  [REF-02] 完工包 hp-2100 无目录反链
```
> 降级口径（02 线 catalog_ref_check 直扫 03 线活跃目录）：REF-02=0、REF-03 漂移 0、FAIL 0。该 FAIL 为 01 线镜像目录未同步 hp-2100 回填所致（同 218-B/223/228-A 记录），非本任务新增缺陷。

## 三、「需核实」清单

- **Macintosh Plus**：尺寸、Mini vMac 许可精确版本、Apple ROM/系统镜像合规路径。
- **IBM PC XT**：尺寸、86Box 对 5160 支持细节、IBM BIOS ROM 合规路径。

## 四、与任务书的漂移

- **86Box 许可**：任务书标「模拟器需核实」，经核实 86Box 许可 **GPLv2 已核实**（38-B 检索确认），故标「GPLv2（已核实）」，需核实的点落在 PC XT（5160）支持细节与 BIOS ROM 路径（对齐定案表 v3 草案「模拟器可行性、参数」需核实字段）。
- 其余无漂移：只出研究卡 + 证据索引回填，未动 jsonl、未产包、未碰 01/02/05 线。

## 五、第三批卷一/卷二汇总（228-A + 228-B）

| 序号 | 研究卡 | 证据编号 | 模拟器口径 |
|---|---|---|---|
| 1 | IBM System/370 | S119–S120 | Hercules（QPL，已核实） |
| 2 | MSX2+（Panasonic FS-A1） | S78–S80（复用） | openMSX（GPLv2，已核实） |
| 3 | Macintosh Plus | S121–S122 | Mini vMac（GPL，需核实） |
| 4 | IBM PC XT | S123–S124 | 86Box（GPLv2，已核实） |
