# TASK-268-A 完成报告

> 03 线 TASK-268-A「Macintosh Plus 产包口径卡（第三批第三张）」完成报告。执行账号：03 内容线。只改 `D:\work\03\` 目录，纯文档口径卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物清单

| 路径 | 状态 | 说明 |
|---|---|---|
| `docs/research/hall-personal-batch2/23_MacintoshPlus产包口径卡.md` | 新增 | 5332 字节，六节齐备 |
| `docs/TASK-268-A_完成报告.md` | 新增 | 本报告 |

口径卡内容：①模拟器形态（`mini-vmac` 候选，许可标「需核实」，无合规路径则 `emulator="none"` 保守降级）；②Macintosh 系统 ROM/软盘镜像红线（只清单级引用，不入库不下载）；③产包字段清单（meta/runtime/assemblies/annotations/encyclopedia/THIRD_PARTY 逐项，manufacturer=Apple、era=1986）；④「需核实」清单；⑤目录反链口径；⑥产包体例对齐说明。

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
wc -c docs/research/hall-personal-batch2/23_MacintoshPlus产包口径卡.md
5332 （>2500 ✔）
grep '^## ' 命中六节：一、模拟器形态 / 二、Macintosh 系统 ROM/软盘镜像红线 / 三、产包字段清单 /
四、「需核实」清单 / 五、目录反链口径 / 六、产包体例对齐说明
「需核实」清单条数：4 类（尺寸配色 / Mini vMac 许可精确版本 / ROM 镜像路径 / 机型支持细节）
```

### 3. 改动清单自证

本任务仅新增 2 份 md：`23_MacintoshPlus产包口径卡.md` + `TASK-268-A_完成报告.md`；未碰目录 jsonl、未产包、未 allocate、未改 01/02/04/05 线。

## 三、与任务书的漂移

1. **「需核实」条数**：任务书第 4 章要求「贴『需核实』清单条数」，实际产出 4 类——在 228-B 研究卡已有的「尺寸 / Mini vMac 许可版本 / ROM 镜像路径」3 类之外，按产包口径卡惯例（22 号 MSX2 卡）补充「Mini vMac 对 Macintosh Plus 机型支持细节」第 4 类，属产包侧口径补全而非史实漂移。
2. **emulator 口径的显式降级**：任务书要求「无合规路径则 emulator="none" 保守」，实际在第一节「模拟器形态」与字段清单 `runtime.emulator` 两处同时写明「`mini-vmac`（GPL 需核实，无合规路径则降 `none`）」，并注明降级类比 System/370 口径卡的「备选」口径，属任务书要求的显式落地。
3. **sinks 口径细化**：Macintosh Plus 为一体机，`sinks` 取 `internal_crt`（内置 9 英寸单色 CRT）+ `speaker`，区别于 MSX2 口径卡的 `external_crt`，并在第六节体例对齐说明中显式交代这一差异。
4. 其余路径、前置文件、红线、边界均与任务书一致，无其他漂移。

## 四、红线自查

零联网、零下载、零二进制/模拟器进程；Apple ROM/系统镜像只清单级引用；史实/参数以 `13_MacintoshPlus.md` 为准，无源标「需核实」；只改 03 目录。
