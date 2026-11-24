# TASK-273-B 完成报告

> 03 线 TASK-273-B「Acorn Archimedes 产包口径卡（第三批第五张）」完成报告。执行账号：03 内容线。只改 `D:\work\03\` 目录，纯文档口径卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物清单

| 路径 | 状态 | 说明 |
|---|---|---|
| `docs/research/hall-personal-batch2/25_AcornArchimedes产包口径卡.md` | 新增 | 4572 字节，六节齐备 |
| `docs/TASK-273-B_完成报告.md` | 新增 | 本报告 |

口径卡内容：①模拟器形态（`emulator="none"`，候选 Arculator/ArcEm 标需核实）；②Acorn 系统 ROM/磁盘镜像红线（只清单级引用）；③产包字段清单（meta/runtime/assemblies/annotations/encyclopedia/THIRD_PARTY 逐项，manufacturer=Acorn、era=1987）；④「需核实」清单；⑤目录反链口径；⑥产包体例对齐说明。

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
wc -c docs/research/hall-personal-batch2/25_AcornArchimedes产包口径卡.md
4572 （>2500 ✔）
grep '^## ' 命中六节：一、模拟器形态 / 二、Acorn 系统 ROM/磁盘镜像红线 / 三、产包字段清单 /
四、「需核实」清单 / 五、目录反链口径 / 六、产包体例对齐说明
「需核实」清单条数：3 类（尺寸 / Arculator、ArcEm 候选许可与成熟度 / RISC OS 镜像路径）
```

### 3. 改动清单自证

本任务仅新增 2 份 md：`25_AcornArchimedes产包口径卡.md` + `TASK-273-B_完成报告.md`；未碰目录 jsonl、未产包、未 allocate、未改 01/02/04/05 线。

## 三、与任务书的漂移

1. **emulator 口径显式落地**：任务书要求「候选按研究卡第五节口径，无合规路径则 emulator="none" 保守」，实际研究卡第五节主口径即为 `none`（无成熟模拟器），故本卡 `runtime.emulator="none"` 直接取保守值，候选 Arculator/ArcEm 记 THIRD_PARTY 而非 runtime 槽位，属任务书要求的显式落地。
2. **sinks 口径细化**：Archimedes 为「一体机箱 + 外接 CRT」形态，`sinks` 取 `external_crt`（一体机箱不含显示器，区别于 Macintosh Plus 的 `internal_crt`），并在第六节体例对齐说明中显式交代差异。
3. **assemblies 件数**：任务书未指定件数，实际按研究卡部件分解草图产出 6 件 glTF（整机 + 一体机箱/主板/软驱/显示器/三键鼠标）。
4. 其余路径、前置文件、红线、边界均与任务书一致，无其他漂移。

## 四、红线自查

零联网、零下载、零二进制/模拟器进程；Acorn ROM/RISC OS 镜像只清单级引用；史实/参数以 `15_AcornArchimedes.md` 为准，无源标「需核实」；只改 03 目录。
