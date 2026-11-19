# 16 — IBM System/370 产包口径卡

> 03 线 TASK-243-B 交付。第三批第 1 台 IBM System/370（目录占位 `C-MF-0000xx`）的产包准备口径卡，供定案后产包领取。研究卡 `14_IBMSystem370.md`（证据 S119–S120）已由 228-A 就绪。本卡只出口径、不产包、不改目录 jsonl、不下载 IBM 操作系统镜像/二进制。

## 一、模拟器形态（Hercules QPL 隔离）

- **`runtime.emulator` = `"hercules"`**（通过 schema 正则 `^[a-z][a-z0-9_-]*$`，小写字母/数字/连字符合法）。
- **许可**：Hercules 上游为 **Q Public License（QPL）**，**非 GPL**（228-A 已核实，18-B 检索确认）；QPL 为 OSI 认证，允许个人/商业使用，但**「不得分发修改后的副本、不得复制源码片段」**——与 GPL 不同，嵌入/衍生须单独评估。
- **隔离形态**：**独立进程接入（ADR D1），经 stdio 设备通道接入网关**（`gw/PROTOCOL.md` §2.2），与 MIT 主程序**不链接、不派生**——运行 Hercules 不构成本项目代码的许可传染；但**随仓库分发 Hercules 二进制的行为须另行法律评估**，故本仓库不随附。
- **槽位**：`dedicated` 预留，`binary_env` 由 01 线后续登记；本卡不建 01 线槽位 manifest、不下发二进制。
- **备选（227-B 已列）**：若核实 Hercules 对 S/370 具体型号支持不足，降为 `emulator="none"`（静态 + 通道 I/O 原理动画），候选记 THIRD_PARTY。

## 二、IBM 操作系统磁盘镜像红线

- **IBM 操作系统磁盘镜像不入库、不下载、不提供、不再分发**——MVS/VM/DOS 等 IBM 操作系统磁盘镜像受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 IBM 操作系统磁盘镜像与磁带镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/镜像红线惯例（MAME Romset / Apple II ROM / Kickstart ROM 等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`system370`、era=1970、category=mainframe、manufacturer=IBM、description 五字段齐备 | 研究卡 14_IBMSystem370.md |
| runtime.json | emulator=`hercules`（QPL 隔离）、media_hint=`tape`（磁带机）+ 备选 `disk`、sinks=indicator_lamps+terminal、input_map 8 动作（控制台拨键口径） | 研究卡 + 预检总卡 |
| assemblies | 6 件 glTF（whole + cpu_cabinet 主机柜 / console 控制台 / tape_drive 磁带机 / dasd 磁盘存储 / printer 打印机），节点名=node_id | 研究卡部件分解 |
| annotations | ≥30 条（flow ≥10：兼容架构传承、虚拟内存 DAT、Hercules「大型机回家」、通道式 I/O、IBM 大型机黄金年代等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S119]–[S120] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + Hercules（QPL）许可声明 + IBM 操作系统镜像红线声明 | 预检总卡 + 红线 |

## 四、「需核实」清单

- 尺寸（主机柜/控制台/磁带机/磁盘柜）、Hercules 对 S/370 具体型号支持程度、IBM 操作系统镜像合规路径——228-A 已标，本卡沿用并补产包侧口径。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 System/370 条目（现占位 `C-MF-0000xx`，产包前由 02 线 id_registry `allocate` 换真号）→ `status=done`、`device_id=system370`、`research_doc=hall-mainframe/14_IBMSystem370.md`（本卡不执行，产包时执行）。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线预检总卡与 id_registry 分配结果。
