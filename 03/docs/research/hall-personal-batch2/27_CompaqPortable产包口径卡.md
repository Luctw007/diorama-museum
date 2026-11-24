# 27 — Compaq Portable 产包口径卡

> 03 线 TASK-283-A 交付。第三批第 8 台 Compaq Portable（目录占位 `C-PC-0000xx`）的产包准备口径卡，供定案后产包领取。研究卡 `17_CompaqPortable.md`（证据 S131–S132）已由 233-B 就绪。本卡只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 Compaq BIOS ROM/磁盘镜像/二进制。

## 一、模拟器形态（IBM 兼容机口径，emulator="none"）

- **`runtime.emulator` = `"none"`**——Compaq Portable 为 IBM 兼容便携机，参照 24 号 IBM PC XT 卡 `pc86box` 先例的 IBM 兼容机口径，但研究卡 17 号主口径为 `none`（候选许可与具体机型支持均「需核实」），故取保守值，静态 + BIOS 逆向工程原理动画承载。
- **候选（标需核实）**：86Box、PCem 等 x86 模拟器对 Compaq Portable 有支持（许可与具体机型支持均「需核实」），产包时如核实可用再走合规流程接入，候选记 THIRD_PARTY。
- **升级路径**：若核实 86Box 对 Compaq Portable 支持充分，可升为 `emulator="pc86box"`（GPLv2 隔离，同 24 号 PC XT 卡口径），走「占位 → 正式」升级；否则维持 `none`。
- **隔离形态（若接入）**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；二进制不入库。

## 二、Compaq 系统 ROM/BIOS/磁盘镜像红线

- **Compaq BIOS ROM 与系统磁盘镜像不入库、不下载、不提供、不再分发**——Compaq 净室逆向工程重写的 BIOS（受版权保护）与 DOS 等系统磁盘镜像，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 Compaq BIOS ROM 与系统磁盘镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/镜像红线惯例（MAME Romset / Apple II ROM / Kickstart ROM / IBM PC BIOS ROM 等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`compaq-portable`、era=1983、category=personal-computer、manufacturer=Compaq、description 五字段齐备 | 研究卡 17_CompaqPortable.md + 252-B 包 id 建议 |
| runtime.json | emulator=`none`（IBM 兼容机口径，候选 86Box/PCem 记 THIRD_PARTY）、media_hint=`floppy`（软驱）、sinks=internal_crt+speaker（内置 9 英寸 CRT + 扬声器）、input_map 键盘（外接键盘，兼作机箱盖） | 研究卡 + 分档口径 |
| assemblies | 6 件 glTF（整机 compaq_portable / 手提箱式机箱 case 含提手 / 内置 CRT builtin_crt / 主板 motherboard 含 cpu_8088+bios+ram / 软驱 floppy_drive / 键盘 keyboard），节点名=node_id | 研究卡部件分解草图 |
| annotations | ≥30 条（flow ≥10：兼容机的合法性里程碑、手提箱式便携、开放架构的果实、Compaq 的崛起、净室逆向的胜利等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S131]–[S132] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + Compaq BIOS ROM/磁盘镜像红线声明 + 86Box/PCem 候选（许可/成熟度需核实）声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（整机约 50 cm 宽 × 20 cm 深 × 20 cm 高、约 28 磅 / 12.7 kg）、配色——233-B 已标「需核实」，本卡沿用。
- 86Box/PCem 对 Compaq Portable 机型支持度——233-B 已标「需核实」，本卡沿用。
- Compaq BIOS ROM 的合规获取路径——233-B 已标「需核实」，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 Compaq Portable 条目（现占位 `C-PC-0000xx`，产包前由 02 线 id_registry `allocate` 换真号）→ `status=done`、`device_id=compaq-portable`、`research_doc=hall-personal-batch2/17_CompaqPortable.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批最新先例 **Sinclair ZX81 口径卡**（`hall-personal-batch2/26_SinclairZX81产包口径卡.md`）的六节骨架，IBM 兼容机口径对齐 **IBM PC XT 口径卡**（`hall-personal-batch2/24_IBMPCXT产包口径卡.md`）——`category=personal-computer`、`media_hint` 软驱口径、BIOS ROM 红线均沿用。差异在两点：①Compaq Portable 为「便携一体机（内置 CRT）」，`sinks=internal_crt`（内置 9 英寸 CRT，区别于 PC XT 的外接 `external_crt`）；②`emulator` 取 `none`（PC XT 的 86Box 已核实 GPLv2 用 `pc86box`，Compaq 的 86Box/PCem 候选仍「需核实」，故保守 `none`，核实后可升 `pc86box`）。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线 252-B 验收清单与 id_registry 分配结果。
