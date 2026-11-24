# TASK-273-A 完成报告

> 03 线 TASK-273-A「IBM PC XT 产包口径卡（第三批第四张）」完成报告。执行账号：03 内容线。只改 `D:\work\03\` 目录，纯文档口径卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物清单

| 路径 | 状态 | 说明 |
|---|---|---|
| `docs/research/hall-personal-batch2/24_IBMPCXT产包口径卡.md` | 新增 | 5048 字节，六节齐备 |
| `docs/TASK-273-A_完成报告.md` | 新增 | 本报告 |

口径卡内容：①模拟器形态（86Box GPLv2 已核实，`runtime.emulator="pc86box"`，无合规路径则降 `none`）；②IBM PC 系统 ROM/BIOS/磁盘镜像红线（只清单级引用）；③产包字段清单（meta/runtime/assemblies/annotations/encyclopedia/THIRD_PARTY 逐项，manufacturer=IBM、era=1983）；④「需核实」清单；⑤目录反链口径；⑥产包体例对齐说明。

## 二、验收日志与退出码

### 1. 门禁只读复测

```
py -3.7 D:\work\01\repo\01\scripts\verify_all.py --daily --cache
...（54 项逐项 PASS）...
结果：54/54 通过
EXIT_CODE=0
```

### 2. 口径卡自证

```
wc -c docs/research/hall-personal-batch2/24_IBMPCXT产包口径卡.md
5048 （>2500 ✔）
grep '^## ' 命中六节：一、模拟器形态 / 二、IBM PC 系统 ROM/BIOS/磁盘镜像红线 / 三、产包字段清单 /
四、「需核实」清单 / 五、目录反链口径 / 六、产包体例对齐说明
「需核实」清单条数：3 类（尺寸 / 86Box 5160 支持细节 / BIOS ROM 路径）
```

### 3. 改动清单自证

本任务仅新增 2 份 md：`24_IBMPCXT产包口径卡.md` + `TASK-273-A_完成报告.md`；未碰目录 jsonl、未产包、未 allocate、未改 01/02/04/05 线。

## 三、与任务书的漂移

1. **emulator id 校正**：任务书写「模拟器候选 86Box」，实际 `runtime.emulator` 采用 `pc86box` 而非 `86box`——因 schema 正则 `^[a-z][a-z0-9_-]*$` 要求首字符为小写字母，「86box」以数字开头不合规，且研究卡 14 号已预留 `pc86box`（对齐 38-B IBM 5150 包口径）。此为合规校正，非漂移。
2. **assemblies 件数**：任务书未指定件数，实际按研究卡部件分解草图产出 7 件 glTF（整机 + 机箱/主板/硬盘/软驱/显示器/键盘，PC XT 有「硬盘」独立件）；件数以研究卡为准，产包时可调。
3. **media_hint 口径**：任务书未指定，实际取 `disk`（首次内置 10MB 硬盘为 PC XT 最鲜明升级点）+ 备选 `floppy`，并在字段清单与体例对齐说明中交代依据。
4. 其余路径、前置文件、红线、边界均与任务书一致，无其他漂移。

## 四、红线自查

零联网、零下载、零二进制/模拟器进程；IBM PC BIOS ROM/磁盘镜像只清单级引用；史实/参数以 `14_IBMPCXT.md` 为准，无源标「需核实」；只改 03 目录。
