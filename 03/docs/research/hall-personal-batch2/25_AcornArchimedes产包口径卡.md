# 25 — Acorn Archimedes 产包口径卡

> 03 线 TASK-273-B 交付。第三批第 5 台 Acorn Archimedes（目录占位 `C-PC-0000xx`）的产包准备口径卡，供定案后产包领取。研究卡 `15_AcornArchimedes.md`（证据 S125–S126）已由 233-A 就绪。本卡只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 Acorn ROM/RISC OS 磁盘镜像/二进制。

## 一、模拟器形态（无成熟模拟器，emulator="none"）

- **`runtime.emulator` = `"none"`**——Acorn Archimedes 无广泛可用的成熟开源模拟器，按预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径，静态 + RISC 原理动画承载。
- **候选（标需核实）**：Arculator、ArcEm 等 Acorn Archimedes 模拟器存在（许可与成熟度均「需核实」），产包时如核实可用再走合规流程接入，候选记 THIRD_PARTY。
- **隔离形态（若接入）**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；二进制不入库。
- **保守口径**：本卡 `emulator="none"` 即为保守值，不建 01 线槽位 manifest、不下发二进制。

## 二、Acorn 系统 ROM/磁盘镜像红线

- **Acorn ROM 与 RISC OS 磁盘镜像不入库、不下载、不提供、不再分发**——RISC OS 系统镜像与 Acorn ROM 受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 RISC OS 镜像与软件磁盘镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/镜像红线惯例（MAME Romset / Apple II ROM / Kickstart ROM / MSX2 BIOS ROM 等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`acorn-archimedes`、era=1987、category=personal-computer、manufacturer=Acorn、description 五字段齐备 | 研究卡 15_AcornArchimedes.md + 252-B 包 id 建议 |
| runtime.json | emulator=`none`（无成熟模拟器，候选 Arculator/ArcEm 记 THIRD_PARTY）、media_hint=`floppy`（软驱）、sinks=external_crt+speaker（外接 CRT + 扬声器）、input_map 键盘 + 三键鼠标（motion/btn_left/btn_middle/btn_right） | 研究卡 + 分档口径 |
| assemblies | 6 件 glTF（整机 acorn_archimedes / 一体机箱 case 键盘一体式 / 主板 motherboard 含 cpu_arm2+vidc_chip+memc_chip+ram / 软驱 floppy_drive / 显示器 monitor / 三键鼠标 mouse），节点名=node_id | 研究卡部件分解草图 |
| annotations | ≥30 条（flow ≥10：ARM 芯片帝国的起点、RISC 的先行者、英国计算机的遗产、ARM 低调崛起、首台 ARM 电脑等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S125]–[S126] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + RISC OS 镜像红线声明 + Arculator/ArcEm 候选（许可/成熟度需核实）声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（一体机箱约 40 cm 宽 × 30 cm 深 × 7 cm 高、三键鼠标）、配色——233-A 已标「需核实」，本卡沿用。
- Arculator/ArcEm 候选许可与成熟度——233-A 已标「需核实」，本卡沿用。
- RISC OS 镜像的合规获取路径——233-A 已标「需核实」，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 Acorn Archimedes 条目（现占位 `C-PC-0000xx`，产包前由 02 线 id_registry `allocate` 换真号）→ `status=done`、`device_id=acorn-archimedes`、`research_doc=hall-personal-batch2/15_AcornArchimedes.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批最新先例 **Macintosh Plus 口径卡**（`hall-personal-batch2/23_MacintoshPlus产包口径卡.md`）的六节骨架与 **MSX2 口径卡**（`hall-personal-batch2/22_MSX2产包口径卡.md`）的 ROM 红线体例。品类上 Archimedes 为「一体机箱 + 外接 CRT」形态：`sinks` 取 `external_crt`（外接 CRT，一体机箱不含显示器，区别于 Macintosh Plus 的 `internal_crt`）；`emulator` 取 `none`（无成熟模拟器，同第三批 Archimedes/ZX81 等 `none` 档口径），候选 Arculator/ArcEm 记 THIRD_PARTY 而非 runtime 槽位。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线 252-B 验收清单与 id_registry 分配结果。
