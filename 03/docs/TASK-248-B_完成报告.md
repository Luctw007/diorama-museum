# TASK-248-B 完成报告 · 第四批候选研究卡卷二（Nokia 5110 + Motorola StarTAC）

> 03 线 · 第四批候选研究卡卷二（2 张），研究卡先行、为后续产包备料。本任务只出研究卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物

| 卡 | 路径 | 字节 | 证据 |
|---|---|---|---|
| Nokia 5110 | `hall-phone/10_Nokia5110.md` | 3,965 | S141–S142 |
| Motorola StarTAC | `hall-phone/11_MotorolaStarTAC.md` | 4,151 | S143–S144 |

- 证据索引回填：`hall-phone/05_证据包索引.md` 追加 S141–S144。

## 二、验收日志（第 4 章）

**1. 字节数（均 >1200）**
```
10_Nokia5110.md        3965 字节
11_MotorolaStarTAC.md  4151 字节
```
**2. 五要素自检（逐张七节齐全）**
```
Nokia 5110：七节 7/7 ✔
Motorola StarTAC：七节 7/7 ✔
```
**3. 门禁只读复测**
```
catalog_ingest --gate → 摄取 5 文件 1583 行，错误 0（exit=0）
catalog_ref_check → REF-02 报 walkman-tpsl2（05 线）无目录反链，FAIL 1（非 03 线问题，03 线活跃目录 REF-02 缺失 0）
```

## 三、「需核实」清单

- **Nokia 5110**：尺寸（48×132×31 mm）。
- **Motorola StarTAC**：尺寸、重量（约 88 克）。

## 四、取机理由 + 与 248-A 去重自证

- **取机**：从剩余 10 台取**排序次 2 台**：**49 Nokia 5110**、**50 Motorola StarTAC**（均 A 档，手机厅，功能机叙事补全）。
- **去重自证**：248-A 取 43 Amstrad CPC 464、44 Atari 800；本任务取 49 Nokia 5110、50 Motorola StarTAC——**四台不重复**（43/44 vs 49/50）。

## 五、与任务书的漂移

- 无实质漂移。两台均按「无成熟模拟器 → emulator="none"」口径落模拟器行；未动 jsonl、未产包、未碰 01/02/05 线。
