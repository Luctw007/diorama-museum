# TASK-283-A 完成报告

> 03 线 TASK-283-A「Compaq Portable 产包口径卡（第三批第八张）」完成报告。执行账号：03 内容线。只改 `D:\work\03\` 目录，纯文档口径卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物清单

| 路径 | 状态 | 说明 |
|---|---|---|
| `docs/research/hall-personal-batch2/27_CompaqPortable产包口径卡.md` | 新增 | 4916 字节，六节齐备 |
| `docs/TASK-283-A_完成报告.md` | 新增 | 本报告 |

口径卡内容：①模拟器形态（IBM 兼容机口径，`emulator="none"`，候选 86Box/PCem 标需核实，可升 `pc86box`）；②Compaq 系统 ROM/BIOS/磁盘镜像红线（只清单级引用）；③产包字段清单（meta/runtime/assemblies/annotations/encyclopedia/THIRD_PARTY 逐项，manufacturer=Compaq、era=1983）；④「需核实」清单；⑤目录反链口径；⑥产包体例对齐说明。

## 二、验收日志与退出码

### 1. 门禁只读复测

```
py -3.7 D:\work\01\repo\01\scripts\verify_all.py --daily --cache
...（55 项逐项 PASS）...
结果：55/55 通过
EXIT_CODE=0
```

### 2. 口径卡自证

```
wc -c docs/research/hall-personal-batch2/27_CompaqPortable产包口径卡.md
4916 （>2500 ✔）
grep '^## ' 命中六节：一、模拟器形态 / 二、Compaq 系统 ROM/BIOS/磁盘镜像红线 / 三、产包字段清单 /
四、「需核实」清单 / 五、目录反链口径 / 六、产包体例对齐说明
「需核实」清单条数：3 类（尺寸 / 86Box、PCem 机型支持度 / BIOS ROM 路径）
```

### 3. 改动清单自证

本任务仅新增 2 份 md：`27_CompaqPortable产包口径卡.md` + `TASK-283-A_完成报告.md`；未碰目录 jsonl、未产包、未 allocate、未改 01/02/04/05 线。

## 三、与任务书的漂移

1. **emulator 口径的「候选可升」显式落地**：任务书要求「IBM 兼容机口径，参照 24 号 PC XT 卡 pc86box 先例——候选与许可标需核实，无合规路径则 emulator="none" 保守」，实际研究卡 17 号主口径为 `none`（候选许可与机型支持均需核实），故 `runtime.emulator="none"` 取保守值，并在第一节写明「若核实 86Box 支持充分可升 `pc86box`」的升级路径，属任务书要求的显式落地。
2. **sinks 口径细化**：Compaq Portable 为「便携一体机（内置 CRT）」，`sinks=internal_crt+speaker`（内置 9 英寸 CRT，区别于 PC XT 的外接 `external_crt`），差异在第六节体例对齐说明中显式交代。
3. **assemblies 件数**：任务书未指定件数，实际按研究卡部件分解草图产出 6 件 glTF（整机 + 机箱/内置 CRT/主板/软驱/键盘）。
4. 其余路径、前置文件、红线、边界均与任务书一致，无其他漂移。

## 四、红线自查

零联网、零下载、零二进制/模拟器进程；Compaq BIOS ROM/磁盘镜像只清单级引用；史实/参数以 `17_CompaqPortable.md` 为准，无源标「需核实」；只改 03 目录。
