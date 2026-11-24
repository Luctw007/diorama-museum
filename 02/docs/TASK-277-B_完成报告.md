# TASK-277-B 完成报告

> 任务：第三批产包验收清单 v2（口径卡 5 张链接 + emulator 口径更新）（02 线）。执行账号：02 线（规范/验收清单）。
> 只改 02 目录，纯文档清单，不产包、不改校验器代码、不改 03 线口径卡原文。

## 一、交付物清单

1. 新增 `docs/第三批产包验收清单_v2.md`（5254 字节）：10 台验收口径表追加「产包口径卡」列（5 张已出挂链接 +
   5 张待出）+ emulator 口径逐台刷新（IBM PC XT→pc86box）+ 四道验收命令不变性声明 + v1→v2 变更说明。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复跑

```
verify_all --daily --cache
  ...
  结果：55/55 通过
退出码 rc=0
```

### 2.2 v2 自证

```
字节数：5254（>3500 达标）
口径卡列 5 行链接命中（✅ 16/22/23/24/25 号）+ 5 行「⏳ 待出」
emulator 刷新行：IBM PC XT 由「86Box」→「pc86box」（86Box，GPLv2 已核实，schema 正则首字符小写字母）
```

### 2.3 改动清单自证（本任务只新增，未改口径卡/校验器/目录）

```
新增 docs/第三批产包验收清单_v2.md（5254 字节）
新增 docs/TASK-277-B_完成报告.md
改动 03 线口径卡/目录 jsonl/校验器：0（只挂链接、不改原文）
```

## 三、结论

第三批验收清单 v2 完成：5 张产包口径卡（System/370·MSX2·Macintosh Plus·IBM PC XT·Archimedes）已挂链接，
emulator 口径刷新（IBM PC XT→pc86box 为 schema 合规修正），剩余 5 台标待出、保持 v1 保守口径不提前写死。
四道验收命令、分档硬底线、反链判据均不变。

## 四、与任务书的漂移（如实）

1. **emulator 刷新仅 1 处（IBM PC XT→pc86box）**：任务书列「pc86box GPLv2」，实测 273-A 口径卡明确
   `runtime.emulator="pc86box"`（86Box；「86box」数字开头不合 schema `^[a-z][a-z0-9_-]*$`，故 id 预留
   `pc86box`），本清单据此刷新；其余 4 台已出卡 emulator 与 v1 一致（hercules/openmsx/mini-vmac/none）。
2. **「pc86box」非「pc86box GPLv2」并列错误**：任务书背景 emulator 口径写「hercules QPL/openmsx GPLv2/
   mini-vmac 需核实/pc86box GPLv2/none」，其中 pc86box 即 86Box 的 emulator id（GPLv2），非独立第五个
   模拟器；本清单按「pc86box（86Box，GPLv2 已核实）」表述，避免误解。
3. 其余无实质漂移：5 张口径卡存在性已核对（16 号 3859 字节 / 22 号 5295 / 23 号 5332 / 24 号 5048 / 25 号 4572），
   门禁 55/55 与任务书预期一致。

## 五、红线自查

零联网、零下载（纯验收清单）；emulator 口径以口径卡实值为准、未出卡保持保守口径；只改 02 目录、不产包、
不 allocate、不改 03 线口径卡原文、不改目录 jsonl、不改校验器代码。
