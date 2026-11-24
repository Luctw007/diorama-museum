# TASK-288-A 完成报告

> 03 线 TASK-288-A「Apple Newton 产包口径卡（第三批第十张·收官）」完成报告。执行账号：03 内容线。只改 `D:\work\03\` 目录，纯文档口径卡，不产包、不改目录 jsonl、不 allocate id。

## 一、交付物清单

| 路径 | 状态 | 说明 |
|---|---|---|
| `docs/research/hall-phone/14_AppleNewton产包口径卡.md` | 新增 | 4555 字节，六节齐备 |
| `docs/TASK-288-A_完成报告.md` | 新增 | 本报告 |

口径卡内容：①模拟器形态（`emulator="none"`，Newton PDA 模拟器成熟度低，候选 Einstein 标需核实）；②NewtonOS 固件红线（只清单级引用）；③产包字段清单（meta/runtime/assemblies/annotations/encyclopedia/THIRD_PARTY 逐项，manufacturer=Apple、era=1993、category=pda）；④「需核实」清单；⑤目录反链口径；⑥产包体例对齐说明。至此第三批 10 台口径卡全齐。

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
wc -c docs/research/hall-phone/14_AppleNewton产包口径卡.md
4555 （>2500 ✔）
grep '^## ' 命中六节：一、模拟器形态 / 二、NewtonOS 固件红线 / 三、产包字段清单 /
四、「需核实」清单 / 五、目录反链口径 / 六、产包体例对齐说明
「需核实」清单条数：3 类（尺寸 / Einstein 候选许可与成熟度 / NewtonOS ROM 路径）
```

### 3. 改动清单自证

本任务仅新增 2 份 md：`14_AppleNewton产包口径卡.md` + `TASK-288-A_完成报告.md`；未碰目录 jsonl、未产包、未 allocate、未改 01/02/04/05 线。

## 三、与任务书的漂移

1. **前置 4 版本回写**：任务书前置 4 写「`第三批产包验收清单_v2.md`（或 v3 若已出）」，实际 02 线当前只有 v1、v2（`第三批产包验收清单_v2.md`，277-B），**v3 未出**，本卡按 v2 口径（Newton 占位 `M-PD-0000xx`、`none`/Einstein 候选）。已如实回写。
2. **category 口径**：任务书未明写 category，实际取 `pda`（目录 `M-PD`，对齐 01 线 palm-pilot 先例 `category="pda"`），区别于手机厅 Nokia 8110 的 `phone`，差异在第六节体例对齐说明中显式交代。
3. **assemblies 件数**：任务书未指定件数，实际按研究卡部件分解草图产出 7 件 glTF（整机 + 机壳/触控 LCD/主板/电池/触控笔/扩展槽）。
4. 其余路径、前置文件、红线、边界均与任务书一致，无其他漂移。

## 四、红线自查

零联网、零下载、零二进制/模拟器进程；NewtonOS 固件只清单级引用；史实/参数以 `09_AppleNewton.md` 为准，无源标「需核实」；只改 03 目录。
