# 19 — Whirlwind 产包口径卡

> 03 线 TASK-283-B 交付。第三批第 9 台 Whirlwind（旋风计算机，目录占位 `C-EC-0000xx`）的产包准备口径卡，供定案后产包领取。研究卡 `15_Whirlwind.md`（证据 S133–S134）已由 238-A 就绪。本卡只出口径、不产包、不改目录 jsonl、不 allocate id、不下载系统软件/程序带镜像/二进制。

## 一、模拟器形态（实时计算机/军机系统，emulator="none"）

- **`runtime.emulator` = `"none"`**——Whirlwind 为实时计算机/军机系统，模拟器成熟度低，无广泛可用的开源模拟器（SIMH 等主流模拟器未覆盖此机），按预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径，静态 + 磁芯内存读写/实时计算原理动画承载。
- **候选（标需核实）**：无广泛可用的开源 Whirlwind 模拟器（候选「需核实」），产包时如核实有可用后端再走合规流程接入。
- **隔离形态（若接入）**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；二进制不入库。
- **保守口径**：本卡 `emulator="none"` 即为保守值，不建 01 线槽位 manifest、不下发二进制。

## 二、系统软件/程序带红线

- **Whirlwind 系统软件与 SAGE 程序带镜像不入库、不下载、不提供、不再分发**——Whirlwind 作为 SAGE 防空系统的底座，其系统软件与程序带受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时程序带镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/镜像红线惯例（MAME Romset / Apple II ROM / IBM 操作系统镜像等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`whirlwind`、era=1951、category=early-computer、manufacturer=MIT、description 五字段齐备 | 研究卡 15_Whirlwind.md + 252-B 包 id 建议 |
| runtime.json | emulator=`none`（无成熟模拟器，无候选）、media_hint=`tape`（磁带机，程序与数据 I/O）、sinks=indicator_lamps+speaker（控制台指示灯 + 扬声器）、input_map 控制台（拨键/开关） | 研究卡 + 分档口径 |
| assemblies | 6 件 glTF（整机 whirlwind / 主机柜 cpu_cabinet 真空管运算与控制 / 磁芯内存柜 core_memory / 控制台 console / 磁带机 tape_drive / 电源与冷却 power_cooling），节点名=node_id | 研究卡部件分解草图 |
| annotations | ≥30 条（flow ≥10：磁芯内存的先驱、实时计算的诞生、SAGE 的底座、黎明厅真空管群像、从实验室走向真实世界等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S133]–[S134] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + 系统软件/程序带红线声明 + 无成熟模拟器声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（多机柜组成，约一个房间约 200 平方米、机柜各约 2 m 高、约 5000 根真空管）、配色——238-A 已标「需核实」，本卡沿用。
- 模拟器候选（无广泛可用的开源 Whirlwind 模拟器）——238-A 已标「需核实」，本卡沿用。
- 系统软件/程序带镜像的合规获取路径——238-A 已标「需核实」，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 Whirlwind 条目（现占位 `C-EC-0000xx`，产包前由 02 线 id_registry `allocate` 换真号）→ `status=done`、`device_id=whirlwind`、`research_doc=hall-mainframe/15_Whirlwind.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批最新先例 **Sinclair ZX81 口径卡**（`hall-personal-batch2/26_SinclairZX81产包口径卡.md`）的六节骨架与 **System/370 口径卡**（`hall-mainframe/16_System370产包口径卡.md`）的大型机品类口径——`media_hint` 磁带口径、`sinks=indicator_lamps` 控制台指示灯口径、镜像红线均沿用。差异在两点：①Whirlwind 属「计算机黎明厅」（研究卡明确目录占位 `C-EC-0000xx`，01 线黎明厅设备 `eniac`/`edsac`/`edvac`/`manchester-baby` 的 `category` 均为 `early-computer`），故 `category=early-computer`（非 mainframe）；②`emulator` 取 `none`（无候选，不同于 System/370 的 hercules QPL 已核实）。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线 252-B 验收清单与 id_registry 分配结果。
