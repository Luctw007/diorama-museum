# 30 — Osborne 1 产包口径卡（第四批预研）

> 03 线 TASK-293-B 交付。第四批候选第 7 台 Osborne 1（目录占位 `C-PC-0000xx`）的产包口径卡预研，供定案后产包领取。研究卡 `20_Osborne1.md`（证据 S149–S150）已由 253-B 就绪。**第四批候选性质：产包未定案，本口径卡为备底**。只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 ROM/磁盘镜像/二进制。

## 一、模拟器形态（无成熟模拟器，emulator="none"）

- **`runtime.emulator` = `"none"`**——Osborne 1 无广泛可用的专用开源模拟器，按预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径，静态 + 便携计算原理动画承载。
- **候选（标需核实）**：Z80/CP/M 通用模拟器可部分覆盖（许可与成熟度均「需核实」），产包时如核实可用再走合规流程接入，候选记 THIRD_PARTY。
- **隔离形态（若接入）**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；二进制不入库。

## 二、系统 ROM/磁盘镜像红线

- **Osborne 1 系统 ROM 与 CP/M/软件包磁盘镜像不入库、不下载、不提供、不再分发**——受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 CP/M 与软件包镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/镜像红线惯例。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`osborne-1`、era=1981、category=personal-computer、manufacturer=Osborne、description 五字段齐备 | 研究卡 20_Osborne1.md |
| runtime.json | emulator=`none`（候选 Z80/CP/M 记 THIRD_PARTY）、media_hint=`floppy`（双软驱）、sinks=internal_crt+speaker（内置 5 英寸 CRT + 扬声器）、input_map 键盘 | 研究卡 + 分档口径 |
| assemblies | 6 件 glTF（整机 osborne_1 / 手提箱式外壳 case 含提手 / 内置 CRT builtin_crt / 双软驱 floppy_drives / 主板 motherboard 含 cpu_z80+ram / 折叠键盘 keyboard），节点名=node_id | 研究卡部件分解 |
| annotations | ≥30 条（flow ≥10：首台便携电脑、附赠软件包创新、奥斯本效应教训、便携线先驱等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S149]–[S150] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + ROM/磁盘镜像红线 + Z80/CP/M 候选（需核实）声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（整机约 50×33×23 cm、约 24 磅/10.7 kg、内置 5 英寸 CRT）、配色——253-B 已标，本卡沿用。
- Z80/CP/M 通用模拟器覆盖程度——253-B 已标，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 Osborne 1 条目（现占位 `C-PC-0000xx`）→ `status=done`、`device_id=osborne-1`、`research_doc=hall-personal-batch2/20_Osborne1.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批 **Compaq Portable 口径卡**（`27_CompaqPortable产包口径卡.md`）六节骨架。品类为「手提箱式便携一体机（内置 CRT）」形态：`sinks=internal_crt`（内置 5 英寸 CRT，同 Compaq Portable 口径）、`media_hint=floppy`（双软驱）。**第四批候选性质：产包未定案，口径卡为备底**。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线验收口径与 id_registry 分配结果。
