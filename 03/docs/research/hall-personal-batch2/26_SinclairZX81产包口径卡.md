# 26 — Sinclair ZX81 产包口径卡

> 03 线 TASK-278-A 交付。第三批第 6 台 Sinclair ZX81（目录占位 `C-PC-0000xx`）的产包准备口径卡，供定案后产包领取。研究卡 `16_SinclairZX81.md`（证据 S127–S128）已由 233-A 就绪。本卡只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 ZX81 ROM/磁带镜像/二进制。

## 一、模拟器形态（无成熟模拟器，emulator="none"）

- **`runtime.emulator` = `"none"`**——ZX81 模拟器成熟度一般，无广泛可用的成熟开源模拟器，按预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径，静态 + 编程入门原理动画承载。
- **候选（标需核实）**：EightyOne、sz81 等 Sinclair 家用机模拟器存在（可模拟 ZX81，许可与成熟度均「需核实」），产包时如核实可用再走合规流程接入，候选记 THIRD_PARTY。
- **隔离形态（若接入）**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；二进制不入库。
- **保守口径**：本卡 `emulator="none"` 即为保守值，不建 01 线槽位 manifest、不下发二进制。

## 二、Sinclair 系统 ROM 红线

- **ZX81 ROM 不入库、不下载、不提供、不再分发**——ZX81 系统 ROM（受版权保护），本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 ZX81 ROM 与磁带镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/镜像红线惯例（MAME Romset / Apple II ROM / Kickstart ROM / MSX2 BIOS ROM 等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`sinclair-zx81`、era=1981、category=personal-computer、manufacturer=Sinclair、description 五字段齐备 | 研究卡 16_SinclairZX81.md + 252-B 包 id 建议 |
| runtime.json | emulator=`none`（无成熟模拟器，候选 EightyOne/sz81 记 THIRD_PARTY）、media_hint=`tape`（外接磁带录音机加载 BASIC 程序）、sinks=external_crt+speaker（外接电视经 RF 调制器 + 扬声器）、input_map 键盘（40 键薄膜键盘） | 研究卡 + 分档口径 |
| assemblies | 6 件 glTF（整机 sinclair_zx81 / 机箱 case 键盘一体式 / 键盘 keyboard / 主板 motherboard 含 cpu_z80+ula_chip+ram / RF 调制器 rf_modulator / 电源 power），节点名=node_id | 研究卡部件分解草图 |
| annotations | ≥30 条（flow ≥10：超低价编程普及、ZX 家族的起点、极简主义、Sinclair「把电脑做成日用品」理念、49.95 英镑的电脑等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S127]–[S128] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + ZX81 ROM 红线声明 + EightyOne/sz81 候选（许可/成熟度需核实）声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（主机约 16.5 cm 宽 × 17.5 cm 深 × 3.5 cm 高、40 键薄膜键盘）、配色——233-A 已标「需核实」，本卡沿用。
- EightyOne/sz81 候选许可与成熟度——233-A 已标「需核实」，本卡沿用。
- ZX81 ROM 的合规获取路径——233-A 已标「需核实」，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 Sinclair ZX81 条目（现占位 `C-PC-0000xx`，产包前由 02 线 id_registry `allocate` 换真号）→ `status=done`、`device_id=sinclair-zx81`、`research_doc=hall-personal-batch2/16_SinclairZX81.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批最新先例 **Acorn Archimedes 口径卡**（`hall-personal-batch2/25_AcornArchimedes产包口径卡.md`）的六节骨架与 **MSX2 口径卡**（`hall-personal-batch2/22_MSX2产包口径卡.md`）的 ROM 红线体例。品类上 ZX81 为「键盘一体式机箱 + 外接电视（RF 输出）」形态：`sinks` 取 `external_crt`（外接电视，区别于一体机内置 CRT 的 `internal_crt`），`media_hint` 取 `tape`（外接磁带录音机加载，为 ZX81 的程序载体）；`emulator` 取 `none`（无成熟模拟器，同第三批 Archimedes 等 `none` 档口径），候选 EightyOne/sz81 记 THIRD_PARTY。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线 252-B 验收清单与 id_registry 分配结果。
