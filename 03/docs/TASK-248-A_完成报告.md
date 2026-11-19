# TASK-248-A 完成报告 · 第四批候选研究卡卷一（Amstrad CPC 464 + Atari 800）

> 03 线 · 第四批候选研究卡卷一（2 张），研究卡先行、为后续产包备料。本任务只出研究卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物

| 卡 | 路径 | 字节 | 证据 |
|---|---|---|---|
| Amstrad CPC 464 | `hall-personal-batch2/18_AmstradCPC464.md` | 4,559 | S137–S138 |
| Atari 800 | `hall-personal-batch2/19_Atari800.md` | 4,580 | S139–S140 |

- 证据索引回填：`hall-personal-batch2/05_证据包索引.md` 追加 S137–S140。

## 二、验收日志（第 4 章）

**1. 字节数（均 >1200）**
```
18_AmstradCPC464.md  4559 字节
19_Atari800.md       4580 字节
```
**2. 五要素自检（逐张七节齐全）**
```
Amstrad CPC 464：七节 7/7 ✔
Atari 800：七节 7/7 ✔
```
**3. 门禁只读复测**
```
catalog_ingest --gate → 摄取 5 文件 1583 行，错误 0（exit=0）
catalog_ref_check → REF-02 报 walkman-tpsl2（05 线）无目录反链，FAIL 1（非 03 线问题，03 线活跃目录 REF-02 缺失 0）
```

## 三、「需核实」清单

- **Amstrad CPC 464**：尺寸、模拟器候选（Caprice32/Arnold）许可与成熟度。
- **Atari 800**：尺寸、模拟器候选（Atari800/Altirra）许可与成熟度。

## 四、取机理由（候选名单序号）

从第二批候选 31-60 名单剩余 10 台（43/44/49/50/51/53/55/57/59/60 号）取**排序前 2 台**：**43 Amstrad CPC 464**、**44 Atari 800**（均 A 档，个人机厅，8 位家用电脑叙事补全）。

## 五、与任务书的漂移

- 无实质漂移。两台均按「无成熟模拟器 → emulator="none"，候选标需核实」口径落模拟器行；未动 jsonl、未产包、未碰 01/02/05 线。
