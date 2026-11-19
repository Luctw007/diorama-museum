# TASK-233-A 完成报告 · 第三批研究卡卷三（Acorn Archimedes + Sinclair ZX81）

> 03 线 · 第三批首批研究卡卷三（2 张），研究卡先行、为定案后产包备料。本任务只出研究卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物

| 卡 | 路径 | 字节 | 证据 |
|---|---|---|---|
| Acorn Archimedes | `hall-personal-batch2/15_AcornArchimedes.md` | 4,860 | S125–S126 |
| Sinclair ZX81 | `hall-personal-batch2/16_SinclairZX81.md` | 4,647 | S127–S128 |

- 证据索引回填：`hall-personal-batch2/05_证据包索引.md` 追加 S125–S128。

## 二、验收日志（第 4 章）

**1. 字节数（均 >1200）**
```
15_AcornArchimedes.md  4860 字节
16_SinclairZX81.md     4647 字节
```
**2. 五要素自检（逐张七节齐全）**
```
Acorn Archimedes：一史实 / 二尺寸 / 三部件草图 / 四 L1-L3 / 五模拟器行 / 六出处 / 七展呈叙事 ✔
Sinclair ZX81：一史实 / 二尺寸 / 三部件草图 / 四 L1-L3 / 五模拟器行 / 六出处 / 七展呈叙事 ✔
```
**3. verify_all --daily --cache（49/49 全 PASS，rc=0）**
```
===== 验收汇总（49 项） =====
结果：49/49 通过
catalog_ref：REF-02 反链缺失 0 · REF-03 漂移 0（registry 1583 = 目录 1583）· FAIL 0
```
> 镜像已收口：此前持续存在的 hp-2100 镜像 stale 误报（REF-02）已被 01 线 sync 修复，本轮 verify_all 全 PASS。

## 三、「需核实」清单

- **Acorn Archimedes**：尺寸、模拟器候选（Arculator/ArcEm）许可与成熟度。
- **Sinclair ZX81**：尺寸、模拟器候选（EightyOne/sz81）许可与成熟度、ZX81 ROM 合规路径。

## 四、与任务书的漂移

- 无实质漂移。两台均按预检总卡（227-B）「无成熟模拟器 → emulator="none"」口径落模拟器行，候选模拟器（Arculator/ArcEm、EightyOne/sz81）如实列出并标「需核实」。
- 未动 jsonl、未产包、未碰 01/02/05 线。
