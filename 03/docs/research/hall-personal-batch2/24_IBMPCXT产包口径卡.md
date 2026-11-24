# 24 — IBM PC XT 产包口径卡

> 03 线 TASK-273-A 交付。第三批第 4 台 IBM PC XT（型号 5160，目录占位 `C-PC-0000xx`）的产包准备口径卡，供定案后产包领取。研究卡 `14_IBMPCXT.md`（证据 S123–S124）已由 228-B 就绪。本卡只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 IBM BIOS ROM/磁盘镜像/二进制。

## 一、模拟器形态（86Box GPLv2 已核实）

- **`runtime.emulator` = `"pc86box"`**（86Box 模拟器；**emulator id 预留 `pc86box`**——对齐 38-B IBM 5150 包口径，「86box」以数字开头不合 schema 正则 `^[a-z][a-z0-9_-]*$`，首字符须小写字母）。
- **许可**：86Box 上游为 **GPLv2**（已核实，38-B 检索确认）。
- **覆盖**：86Box 面向 x86 PC 的开源模拟器，模拟 IBM PC/XT 及大量兼容机的硬件配置（8088、MDA/CGA、硬盘控制器等），官网 `https://86box.net/`。
- **隔离形态**：**独立进程接入（ADR D1），经 stdio 设备通道接入网关**（`gw/PROTOCOL.md` §2.2），与 MIT 主程序**不链接、不派生**——运行 86Box 不构成本项目代码的许可传染；但**随仓库分发 86Box 二进制的行为须另行法律评估**，故本仓库不随附。
- **槽位**：`dedicated` 预留，`binary_env=PC86BOX_BIN` 由 01 线后续登记（251-B 槽位预留已登记）；本卡不建 01 线槽位 manifest、不下发二进制。
- **保守降级**：若核实 86Box 对 PC XT 具体型号（5160）支持不足，降为 `emulator="none"`（静态 + BIOS 自检/硬盘启动原理动画），候选记 THIRD_PARTY。

## 二、IBM PC 系统 ROM/BIOS/磁盘镜像红线

- **IBM PC BIOS ROM 与操作系统磁盘镜像不入库、不下载、不提供、不再分发**——IBM PC BIOS ROM（受版权保护）与 DOS 等系统磁盘镜像，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 IBM PC BIOS ROM 与 DOS 系统磁盘镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/镜像红线惯例（MAME Romset / Apple II ROM / Kickstart ROM / MSX2 BIOS ROM 等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`ibm-pc-xt`、era=1983、category=personal-computer、manufacturer=IBM、description 五字段齐备 | 研究卡 14_IBMPCXT.md + 252-B 包 id 建议 |
| runtime.json | emulator=`pc86box`（86Box，GPLv2 已核实）、media_hint=`disk`（首次内置 10MB 硬盘）+ 备选 `floppy`、sinks=external_crt+speaker（外接 MDA/CGA 显示器 + 扬声器）、input_map 键盘（83 键 Model F） | 研究卡 + 分档口径 |
| assemblies | 7 件 glTF（整机 ibm_pc_xt / 机箱 case 含电源 / 主板 motherboard 含 cpu_8088+ram+isa_slots / 硬盘 hard_drive / 软驱 floppy_drive / 显示器 monitor / 键盘 keyboard），节点名=node_id | 研究卡部件分解草图 |
| annotations | ≥30 条（flow ≥10：硬盘的普及、商用标准配置的开端、PC 兼容机的巩固、IBM 5150 谱系衔接、从软盘到硬盘存储革命等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S123]–[S124] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + 86Box（GPLv2）许可声明 + IBM PC BIOS ROM/磁盘镜像红线声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（卧式机箱约 50 cm 宽 × 41 cm 深 × 15 cm 高、10MB 全高 5.25 英寸硬盘）、配色——228-B 已标「需核实」，本卡沿用。
- 86Box 对 PC XT 具体型号（5160）的支持细节——228-B 已标「需核实」，本卡沿用。
- PC XT BIOS ROM 的合规获取路径——228-B 已标「需核实」，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 IBM PC XT 条目（现占位 `C-PC-0000xx`，产包前由 02 线 id_registry `allocate` 换真号）→ `status=done`、`device_id=ibm-pc-xt`、`research_doc=hall-personal-batch2/14_IBMPCXT.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批最新先例 **Macintosh Plus 口径卡**（`hall-personal-batch2/23_MacintoshPlus产包口径卡.md`）的六节骨架，模拟器许可（GPLv2 已核实）与隔离表述对齐 **MSX2 口径卡**（`hall-personal-batch2/22_MSX2产包口径卡.md`）的 openMSX GPLv2 口径。品类上 PC XT 为「卧式机箱 + 外接显示器」形态：`sinks` 取 `external_crt`（外接 MDA/CGA，区别于 Macintosh Plus 一体机的 `internal_crt`），`media_hint` 取 `disk`（首次内置硬盘，为 PC XT 最鲜明的存储升级点）并配 `floppy` 备选，`emulator` 采用 38-B 预留的 `pc86box` id。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线 252-B 验收清单与 id_registry 分配结果。
