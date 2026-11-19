# TASK-227-B 完成报告

> 任务：第三批首批 10 台过闸口径预检总卡。执行账号：02 线。只改 02 目录，纯预检卡。

## 一、交付物清单

1. 新增 `docs/第三批首批过闸口径预检总卡_v1.md`（6120 字节），10 台逐行三问三答简表 + 三台 GPL 隔离
   口径 + 七台「none」口径 + 校验器放行结论 + 落地清单 + 漂移。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复测

```
verify_all --daily --cache
  catalog_ref          FAIL  FAIL 1
结果：40/41 通过（rc=1）
```

> 40/41 唯一 FAIL = catalog_ref「完工包 hp-2100 无目录反链」（镜像 stale），与本任务纯预检卡改动无关。

### 2.2 总卡自检

```
字节：6120（>1200 达标）
10 台逐行齐（1 System/370 … 10 Apple Newton，含 M-PD 前缀）
三问三答列齐（emulator 写法 / 分档 / 校验器放行）
三台 GPL 隔离：hercules / openmsx / mini-vmac
七台 none：IBM PC XT / Acorn Archimedes / ZX81 / SGI Indigo / Compaq Portable / Whirlwind / Newton
```

## 三、emulator 写法结论摘要

| 类 | 台数 | emulator 写法 |
|---|---|---|
| 有明确 GPL 模拟器（隔离形态） | 3 | `hercules` / `openmsx` / `mini-vmac`（GPL 隔离、二进制不进仓库） |
| 无成熟模拟器 | 7 | `none`（静态+动画，候选记 THIRD_PARTY） |

分档：7 A + 3 B；校验器对 `none` 与三台具体名均放行（schema pattern 匹配）；10 台模拟器可行性均标
「需核实」或 GPL 隔离待登记槽位。

## 四、与任务书的漂移

1. **三台 GPL 隔离均未登记槽位**：任务书「有 GPL 模拟器 → 隔离形态」，本卡把 System/370→`hercules`、
   MSX2→`openmsx`、Macintosh Plus→`mini-vmac` 写具体名 + GPL 隔离声明；但三台均**尚未在 01 线登记槽位**
   （Hercules/Mini vMac 许可仍需核实），故与第二批 `uae`（GPL 已核实）区分，并给「核实不足则降 `none`」备选。
2. **其余七台模拟器可行性均「需核实」**（无明确后端），统一 `none`，与任务书一致。
3. 目录 id 均为占位（`0xx`），本卡不 allocate。

## 五、红线自查

零联网、零下载（纯预检卡）；emulator 写法以 schema 实测 + 名单研究材料为准，无来源标「需核实」；只改
02 目录、不产包、不 allocate、不改 03 线目录 jsonl。
