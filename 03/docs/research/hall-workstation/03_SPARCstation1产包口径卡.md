# 03 — SPARCstation 1 产包口径卡

> 03 线 TASK-208-B 交付。第二批第 10 台 SPARCstation 1（目录 `C-WS-000005`）的产包准备口径卡，供后续产包领取。研究卡 `02_SPARCstation1.md`（证据 S113–S115）已由 193-B 就绪。本卡只出口径、不产包、不改目录 jsonl、不下载 SunOS/Solaris 镜像/二进制。

## 一、模拟器形态（QEMU sparc「需核实」→ 保守 none）

- **emulator 口径裁决**：QEMU 的 sparc 目标是 SPARCstation 的候选后端，但其许可与成熟度**需核实**；且 01 线 `slots/emulators/` 目前**无 qemu 槽位**（无 bone 后端登记）。按 02 线《第二批分档验收口径 v2》S 档「无 bone → `emulator="none"` + 静态+动画」口径，**产包时采用 `emulator="none"`（保守口径）**，并在 THIRD_PARTY/NOTE 中标注「QEMU sparc 候选，许可需核实」。
- **若后续 QEMU 许可核实 + 01 线登记槽位**：可升为 `emulator="qemu"`（GPL 隔离，独立进程接入 ADR D1，二进制不进仓库），走「占位 → 正式」升级。
- **QEMU 二进制不进仓库声明**：无论哪种口径，QEMU 二进制均不随仓库分发（GPL 隔离，用户自备进 slots）。

## 二、SunOS/Solaris 镜像红线

- **SunOS/Solaris 系统镜像不入库、不下载、不提供、不再分发**——SunOS/Solaris 受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 SunOS/Solaris 安装镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/固件红线惯例（MAME Romset / Apple II ROM / Kickstart ROM 均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`sparcstation-1`、era=1989、category=workstation、manufacturer=Sun Microsystems、description 五字段齐备 | 研究卡 02_SPARCstation1.md |
| runtime.json | emulator=`none`（保守口径，QEMU sparc 需核实标注）、media_hint=`disk`（内置硬盘）、sinks=external_crt+terminal、input_map 键盘+鼠标 | 研究卡 + 分档口径 |
| assemblies | 6 件 glTF（机身 case / 主板 motherboard 含 SPARC 处理器 / 电源 power_supply / 硬盘 disk / I/O 接口 io_ports / 显示器 monitor），节点名=node_id | 研究卡部件分解 |
| annotations | ≥30 条（flow ≥10：RISC 走向桌面、披萨盒工业设计、Sun 黄金年代、网络即计算机等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S113]–[S115] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + QEMU sparc 需核实声明 + SunOS/Solaris 镜像红线声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（机身约 40×10×40 cm）、参数、QEMU sparc 许可与成熟度——193-B 已标「需核实」，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 `C-WS-000005` → `status=done`、`device_id=sparcstation-1`、`research_doc=hall-workstation/02_SPARCstation1.md`（本卡不执行，产包时执行）。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡与 02 线分档验收口径。
