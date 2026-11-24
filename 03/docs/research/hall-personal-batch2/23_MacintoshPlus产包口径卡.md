# 23 — Macintosh Plus 产包口径卡

> 03 线 TASK-268-A 交付。第三批第 3 台 Macintosh Plus（目录占位 `C-PC-0000xx`）的产包准备口径卡，供定案后产包领取。研究卡 `13_MacintoshPlus.md`（证据 S121–S122）已由 228-B 就绪。本卡只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 Apple ROM/系统镜像/二进制。

## 一、模拟器形态（Mini vMac GPL 需核实）

- **`runtime.emulator` = `"mini-vmac"`**（通过 schema 正则 `^[a-z][a-z0-9_-]*$`，小写字母开头，与 01 线既有 `stella`/`pc86box`/`openmsx` 槽位同构）。
- **许可**：Mini vMac 上游为 **GPL**（**「需核实」**——需以 Mini vMac 官方仓库 LICENSE 为准；历史版本存在 GPLv2 / GPLv2+ 表述差异，228-B 已标注）。
- **候选口径**：Mini vMac 面向早期 Macintosh（128K/512K/Plus/SE）的轻量开源模拟器，可运行早期 Macintosh 系统与软件。
- **保守降级**：若产包前核实 Mini vMac 许可无合规路径（或对 Macintosh Plus 具体支持不足），**降为 `emulator="none"`**（静态 + 桌面出版/SCSI 原理动画），候选记 THIRD_PARTY（类比 System/370 口径卡「备选」降级口径）。
- **隔离形态**：**独立进程接入（ADR D1），经 stdio 设备通道接入网关**（`gw/PROTOCOL.md` §2.2），与 MIT 主程序**不链接、不派生**——运行 Mini vMac 不构成本项目代码的许可传染；但**随仓库分发 Mini vMac 二进制的行为须另行法律评估**，故本仓库不随附。
- **槽位**：`dedicated` 预留，`binary_env=MINIVMAC_BIN` 由 01 线后续登记（251-B 槽位预留已登记）；本卡不建 01 线槽位 manifest、不下发二进制。

## 二、Macintosh 系统 ROM / 软盘镜像红线

- **Macintosh ROM（128K）与系统软盘镜像不入库、不下载、不提供、不再分发**——Apple 的 Macintosh ROM 与 System 系统镜像受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 Macintosh ROM 与系统/磁盘镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/镜像红线惯例（MAME Romset / Apple II ROM / Kickstart ROM / MSX2 BIOS ROM 等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`macintosh-plus`、era=1986、category=personal-computer、manufacturer=Apple、description 五字段齐备 | 研究卡 13_MacintoshPlus.md + 252-B 包 id 建议 |
| runtime.json | emulator=`mini-vmac`（GPL 需核实，无合规路径则降 `none`）、media_hint=`floppy`（800KB 双面 3.5 英寸软驱）、sinks=internal_crt+speaker（一体机内置 9 英寸单色 CRT + 扬声器）、input_map 键盘 + 鼠标（motion/btn_left） | 研究卡 + 分档口径 |
| assemblies | 6 件 glTF（整机 macintosh_plus 含内置 CRT / 机壳 case / 主板 motherboard 含 cpu_68000+ram+scsi_controller / 软驱 floppy_drive / 键盘 keyboard / 鼠标 mouse），节点名=node_id | 研究卡部件分解草图 |
| annotations | ≥30 条（flow ≥10：Mac 走向实用化、SCSI 接口开端、桌面出版革命、68000 的 Mac 血脉、1MB 内存补短板、LaserWriter 配合等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S121]–[S122] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + Mini vMac（GPL 需核实）许可声明 + Apple ROM/系统镜像红线声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（一体机约 34.5 cm 宽 × 24.4 cm 深 × 27.7 cm 高、9 英寸单色 CRT 512×342）、配色——228-B 已标「需核实」，本卡沿用。
- Mini vMac 许可精确版本（GPLv2 / GPLv2+ 差异）——228-B 已标「需核实」，本卡沿用。
- Macintosh Plus ROM 与系统镜像的合规获取路径——228-B 已标「需核实」，本卡沿用。
- Mini vMac 对 Macintosh Plus 具体机型支持细节——本卡补充产包侧口径。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 Macintosh Plus 条目（现占位 `C-PC-0000xx`，产包前由 02 线 id_registry `allocate` 换真号）→ `status=done`、`device_id=macintosh-plus`、`research_doc=hall-personal-batch2/13_MacintoshPlus.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批最新先例 **MSX2 口径卡**（`hall-personal-batch2/22_MSX2产包口径卡.md`）的六节骨架（模拟器形态 → 红线 → 字段逐件口径 → 需核实 → 目录反链 → 体例对齐），并沿用 **System/370 口径卡**（`hall-mainframe/16_System370产包口径卡.md`）的「独立进程不链接不派生」隔离表述与「备选降级 `emulator="none"`」口径。品类上与 Macintosh Plus 最接近的仍是家用机/一体机：`media_hint` 取 `floppy`（同 Amiga1000 口径卡），`sinks` 取 `internal_crt`（一体机内置 CRT，区别于 MSX2 的 `external_crt`）。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线 252-B 验收清单与 id_registry 分配结果。
