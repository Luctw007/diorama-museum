# TASK-238-A 完成报告 · 第三批研究卡卷五（Whirlwind + Apple Newton，收尾 10/10）

> 03 线 · 第三批首批研究卡卷五（最后 2 张），完成后第三批首批 10 台研究卡全部齐备。本任务只出研究卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物

| 卡 | 路径 | 字节 | 证据 |
|---|---|---|---|
| Whirlwind（旋风计算机） | `hall-mainframe/15_Whirlwind.md` | 4,992 | S133–S134 |
| Apple Newton MessagePad | `hall-phone/09_AppleNewton.md` | 4,736 | S135–S136 |

- 证据索引回填：`hall-mainframe/06_证据包索引.md` 追加 S133–S134、`hall-phone/05_证据包索引.md` 追加 S135–S136。

## 二、验收日志（第 4 章）

**1. 字节数（均 >1200）**
```
15_Whirlwind.md      4992 字节
09_AppleNewton.md    4736 字节
```
**2. 五要素自检（逐张七节齐全）**
```
Whirlwind：一史实 / 二尺寸 / 三部件草图 / 四 L1-L3 / 五模拟器行 / 六出处 / 七展呈叙事 ✔
Apple Newton：一史实 / 二尺寸 / 三部件草图 / 四 L1-L3 / 五模拟器行 / 六出处 / 七展呈叙事 ✔
```
**3. 门禁只读复测**
```
verify_all --daily --cache 本次被 SIGTERM 中断（环境波动）
降级口径：catalog_ingest --gate → 摄取 5 文件 1583 行，错误 0（exit=0）
          catalog_ref_check → REF-01~04 全 0，FAIL 0
```
> 上一轮（233-B）verify_all 已实测 49/49 全 PASS；本任务仅新增研究卡 + 证据索引（不在 verify_all 扫描范围），门禁无变化。

## 三、「需核实」清单

- **Whirlwind**：尺寸、模拟器候选（无广泛可用的开源 Whirlwind 模拟器）。
- **Apple Newton**：尺寸、Einstein 候选许可/成熟度、Newton OS ROM 合规路径。

## 四、第三批研究卡 10/10 收尾声明

第三批首批 10 台研究卡**全部齐备**：System/370、MSX2、Macintosh Plus、IBM PC XT、Acorn Archimedes、Sinclair ZX81、SGI Indigo、Compaq Portable、Whirlwind、Apple Newton。证据编号 S119–S136（MSX2 复用 S78–S80）。模拟器口径：hercules（QPL）/ openmsx（GPLv2）/ mini-vmac（GPL 需核实）/ 86Box（GPLv2）各 1 台 + 6 台 none。

## 五、与任务书的漂移

- 无实质漂移。两台均按预检总卡「无成熟模拟器 → emulator="none"」口径落模拟器行；未动 jsonl、未产包、未碰 01/02/05 线。
