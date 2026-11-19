# TASK-232-B 完成报告

> 任务：第三批研究卡进度总表 + 待出 4 张排期。执行账号：02 线。只改 02 目录，纯排期表。

## 一、交付物清单

1. 新增 `docs/第三批研究卡进度总表_v1.md`（5245 字节），10 台逐行（已出 6 张路径+证据号 + 待出 4 张排期
   + 模拟器口径）+ 与 227-B 口径对照 + 漂移。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复测（预期 49/49）

```
verify_all --daily --cache
  ...
  结果：49/49 通过（rc=0）
```

### 2.2 总表自检

```
字节：5245（>1200 达标）
10 台逐行齐（1 System/370 … 10 Apple Newton）
已出 6 张：System/370 [S119] / MSX2 [S78/S79/S80] / Macintosh Plus [S121] / IBM PC XT [S123] /
          Acorn Archimedes [S125] / Sinclair ZX81 [S127]
待出 4 张：SGI Indigo / Compaq Portable / Whirlwind / Apple Newton（均下一轮 235 排期，责任线=03 线）
模拟器口径：hercules / openmsx / mini-vmac / 86Box 各 1 台 + 6 台 none
```

## 三、进度结论摘要

**已出 6 张 / 待出 4 张**；4 台有明确模拟器（System/370→hercules QPL、MSX2→openmsx GPLv2、Macintosh
Plus→mini-vmac、IBM PC XT→86Box GPLv2）+ 6 台 `none`；待出 4 张下一轮并行领办、无先后依赖。

## 四、与任务书的漂移

1. **已出 6 张（非 4 张）**：任务书说「已出 4 张（228-A/B：System/370、MSX2、Macintosh Plus、IBM PC XT）」，
   实测 03 线 233-A 又产 **Acorn Archimedes、Sinclair ZX81** 两张，故已出 6 张、待出 4 张（非 6 张）。
2. **IBM PC XT 模拟器口径更新**：227-B 预检总卡原写 `none`，228-B 研究卡补正为 `86Box`（GPLv2 已核实），
   本表按研究卡口径对齐（任务书 232-B 的「86Box」即此）。
3. **MSX2 代表机 = Panasonic FS-A1（MSX2+）**：研究卡选取 MSX2+ 代表机，本表如实记录。

## 五、红线自查

零联网、零下载（纯排期表）；进度以 03 线实际产出（6 张研究卡路径 + 证据号）为准，未臆造；只改 02 目录、
不代 03 线写研究卡、不改 03 线文件。
