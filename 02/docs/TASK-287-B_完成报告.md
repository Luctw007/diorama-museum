# TASK-287-B 完成报告

> 任务：第三批产包验收清单 v3（口径卡 9 张链接 + Newton 收尾口径）（02 线）。执行账号：02 线（规范/验收清单）。
> 只改 02 目录，纯文档清单，不产包、不改校验器代码、不改 03 线口径卡原文。

## 一、交付物清单

1. 新增 `docs/第三批产包验收清单_v3.md`（5983 字节）：10 台验收口径表「产包口径卡」列更新（9 张已出挂链接 +
   Newton 标待出）+ emulator 口径刷新（新增 4 台）+ Whirlwind category 校正行 + 四道验收命令不变性声明 +
   v2→v3 变更说明。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复跑

```
verify_all --daily --cache
  ...
  结果：55/55 通过
退出码 rc=0
```

### 2.2 v3 自证

```
字节数：5983（>4000 达标）
口径卡列 9 行链接命中（✅ 16/22/23/24/25/26/05/27/19 号）+ 1 行「⏳ 待出」（Newton）
emulator 刷新行：新增 4 台全 none（ZX81/SGI Indigo/Compaq Portable/Whirlwind，Compaq Portable 可升 pc86box）
category 校正行：Whirlwind meta.category = early-computer（非 mainframe）
```

### 2.3 改动清单自证（本任务只新增，未改口径卡/校验器/目录）

```
新增 docs/第三批产包验收清单_v3.md（5983 字节）
新增 docs/TASK-287-B_完成报告.md
改动 03 线口径卡/目录 jsonl/校验器：0（只挂链接、不改原文）
```

## 三、结论

第三批验收清单 v3 完成：口径卡 9/10 挂接（剩 Newton 最后一张）、emulator 口径刷新（新增 4 台全 none）、
Whirlwind category 校正为 early-computer、四道验收命令与分档硬底线不变。

## 四、与任务书的漂移（如实）

1. **Whirlwind category = early-computer（非大型机厅）**：283-B 口径卡发现任务书「Whirlwind 属大型机厅」
   有误——研究卡 15 号明确目录占位 `C-EC-0000xx`（黎明厅），01 线黎明厅设备 `category` 均为
   `early-computer`；本清单据此校正（目录 id C-EC、sinks=indicator_lamps、media_hint=tape）。
2. **Compaq Portable「可升 pc86box」**：283-A 口径卡明确 `emulator="none"` 保守值（候选 86Box/PCem 需核实），
   但「可升 `pc86box`」（参照 24 号 IBM PC XT 先例）；本清单按「none（可升 pc86box）」如实表述，不提前写死。
3. 其余无实质漂移：9 张口径卡存在性已核对（26 号 4585 字节 / 05 号 4659 / 27 号 4916 / 19 号 4759），
   门禁 55/55 与任务书预期一致。

## 五、红线自查

零联网、零下载（纯验收清单）；emulator 口径以口径卡实值为准、Newton 未出卡保持保守口径；只改 02 目录、
不产包、不 allocate、不改 03 线口径卡原文、不改目录 jsonl、不改校验器代码。
