# 05 — SGI Indigo 产包口径卡

> 03 线 TASK-278-B 交付。第三批第 7 台 SGI Indigo（目录占位 `C-WS-0000xx`）的产包准备口径卡，供定案后产包领取。研究卡 `04_SGIIndigo.md`（证据 S129–S130）已由 233-B 就绪。本卡只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 IRIX 系统镜像/固件/二进制。

## 一、模拟器形态（无成熟模拟器，emulator="none"）

- **`runtime.emulator` = `"none"`**——SGI 模拟器成熟度低，无广泛可用的成熟开源模拟器，按预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径，静态 + 3D 渲染原理动画承载。
- **候选（标需核实）**：MAME 对部分 SGI 硬件有支持、QEMU 的 MIPS 目标可运行部分 SGI 系统（许可与 Indigo 具体支持均「需核实」），产包时如核实可用再走合规流程接入，候选记 THIRD_PARTY。
- **隔离形态（若接入）**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；二进制不入库。
- **保守口径**：本卡 `emulator="none"` 即为保守值（同 SPARCstation 1 口径卡「QEMU 需核实 → 保守 none」裁决），不建 01 线槽位 manifest、不下发二进制。

## 二、SGI 系统软件/固件红线

- **IRIX 系统镜像与 SGI 固件不入库、不下载、不提供、不再分发**——IRIX 系统软件（受版权保护）与固件，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 IRIX 安装镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/固件红线惯例（MAME Romset / Apple II ROM / Kickstart ROM / SunOS 镜像等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`sgi-indigo`、era=1991、category=workstation、manufacturer=Silicon Graphics、description 五字段齐备 | 研究卡 04_SGIIndigo.md + 252-B 包 id 建议 |
| runtime.json | emulator=`none`（无成熟模拟器，候选 MAME/QEMU MIPS 记 THIRD_PARTY）、media_hint=`disk`（内置硬盘）、sinks=external_crt+speaker（外接大尺寸 CRT + 扬声器）、input_map 键盘 + 三键鼠标（motion/btn_left/btn_middle/btn_right） | 研究卡 + 分档口径 |
| assemblies | 7 件 glTF（整机 sgi_indigo / 靛蓝色塔式机箱 case / 主板 motherboard 含 cpu_r3000+graphics_engine+ram / 硬盘 disk_drive / 显示器 monitor / 键盘 keyboard / 三键鼠标 mouse），节点名=node_id | 研究卡部件分解草图 |
| annotations | ≥30 条（flow ≥10：图形工作站的视觉革命、电影特效的幕后功臣、3D 图形走向桌面、SGI 黄金年代、靛蓝的符号等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S129]–[S130] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + IRIX 镜像红线声明 + MAME/QEMU MIPS 候选（许可/成熟度需核实）声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（塔式/立式机箱约 40 cm 高 × 15 cm 宽 × 40 cm 深、靛蓝色涂装）、配色——233-B 已标「需核实」，本卡沿用。
- MAME/QEMU MIPS 对 SGI Indigo 的支持度——233-B 已标「需核实」，本卡沿用。
- IRIX 系统镜像的合规获取路径——233-B 已标「需核实」，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 SGI Indigo 条目（现占位 `C-WS-0000xx`，产包前由 02 线 id_registry `allocate` 换真号）→ `status=done`、`device_id=sgi-indigo`、`research_doc=hall-workstation/04_SGIIndigo.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批最新先例 **Acorn Archimedes 口径卡**（`hall-personal-batch2/25_AcornArchimedes产包口径卡.md`）的六节骨架，工作站品类口径对齐 **SPARCstation 1 口径卡**（`hall-workstation/03_SPARCstation1产包口径卡.md`）——`category=workstation`、`emulator`「候选需核实 → 保守 `none`」裁决、`media_hint=disk` 均沿用；差异在 `sinks`：SGI Indigo 为图形工作站接大尺寸 CRT 显示器（`external_crt`）而非字符终端（`terminal`），故 `sinks=external_crt+speaker`，并在本卡显式交代这一品类差异。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线 252-B 验收清单与 id_registry 分配结果。
