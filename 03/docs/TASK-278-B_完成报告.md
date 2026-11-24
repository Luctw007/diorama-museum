# TASK-278-B 完成报告

> 03 线 TASK-278-B「SGI Indigo 产包口径卡（第三批第七张）」完成报告。执行账号：03 内容线。只改 `D:\work\03\` 目录，纯文档口径卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物清单

| 路径 | 状态 | 说明 |
|---|---|---|
| `docs/research/hall-workstation/05_SGIIndigo产包口径卡.md` | 新增 | 4659 字节，六节齐备 |
| `docs/TASK-278-B_完成报告.md` | 新增 | 本报告 |

口径卡内容：①模拟器形态（`emulator="none"`，候选 MAME/QEMU MIPS 标需核实）；②SGI 系统软件/固件红线（IRIX 只清单级引用）；③产包字段清单（meta/runtime/assemblies/annotations/encyclopedia/THIRD_PARTY 逐项，manufacturer=SGI、era=1991）；④「需核实」清单；⑤目录反链口径；⑥产包体例对齐说明。

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
wc -c docs/research/hall-workstation/05_SGIIndigo产包口径卡.md
4659 （>2500 ✔）
grep '^## ' 命中六节：一、模拟器形态 / 二、SGI 系统软件/固件红线 / 三、产包字段清单 /
四、「需核实」清单 / 五、目录反链口径 / 六、产包体例对齐说明
「需核实」清单条数：3 类（尺寸 / MAME、QEMU MIPS 支持度 / IRIX 镜像路径）
```

### 3. 改动清单自证

本任务仅新增 2 份 md：`05_SGIIndigo产包口径卡.md` + `TASK-278-B_完成报告.md`；未碰目录 jsonl、未产包、未 allocate、未改 01/02/04/05 线。

## 三、与任务书的漂移

1. **前置 5 的缺失回写**：任务书前置 5 写「`hall-workstation/05_证据包索引.md`（若存在；否则按既有索引）」，实际 `hall-workstation/` 目录**无 05_证据包索引.md**（证据 S129–S130 就近登记于 `hall-mainframe/06_证据包索引.md`），本卡按任务书「否则按既有索引」口径处理，本卡不新增证据。已在漂移节如实回写。
2. **emulator 口径显式落地**：任务书要求「SGI 模拟器成熟度低——候选需核实，无合规路径则 emulator="none" 保守」，实际研究卡第五节主口径即为 `none`，故 `runtime.emulator="none"` 取保守值，候选 MAME/QEMU MIPS 记 THIRD_PARTY，属任务书要求的显式落地。
3. **sinks 口径细化**：SGI Indigo 为图形工作站，`sinks=external_crt+speaker`（外接大尺寸 CRT 而非字符终端），区别于 SPARCstation 1 的 `external_crt+terminal`，差异在第六节体例对齐说明中显式交代。
4. 其余路径、前置文件、红线、边界均与任务书一致，无其他漂移。

## 四、红线自查

零联网、零下载、零二进制/模拟器进程；IRIX/固件只清单级引用；史实/参数以 `04_SGIIndigo.md` 为准，无源标「需核实」；只改 03 目录。
