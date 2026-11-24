# 28 — Amstrad CPC 464 产包口径卡（第四批预研）

> 03 线 TASK-293-A 交付。第四批候选第 1 台 Amstrad CPC 464（目录占位 `C-PC-0000xx`）的产包口径卡预研，供定案后产包领取。研究卡 `18_AmstradCPC464.md`（证据 S137–S138）已由 248-A 就绪。**第四批候选性质：产包未定案，本口径卡为备底**。只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 ROM/磁带镜像/二进制。

## 一、模拟器形态（无成熟模拟器，emulator="none"）

- **`runtime.emulator` = `"none"`**——Amstrad CPC 464 无广泛可用的成熟开源模拟器，按预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径，静态 + 一体化设计原理动画承载。
- **候选（标需核实）**：Caprice32、Arnold 等 Amstrad CPC 模拟器存在（许可与成熟度均「需核实」），产包时如核实可用再走合规流程接入，候选记 THIRD_PARTY。
- **隔离形态（若接入）**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；二进制不入库。

## 二、系统 ROM/磁带镜像红线

- **CPC 464 系统 ROM 与磁带镜像不入库、不下载、不提供、不再分发**——受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 ROM 与磁带镜像由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/镜像红线惯例。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`amstrad-cpc464`、era=1984、category=personal-computer、manufacturer=Amstrad、description 五字段齐备 | 研究卡 18_AmstradCPC464.md |
| runtime.json | emulator=`none`（候选 Caprice32/Arnold 记 THIRD_PARTY）、media_hint=`tape`（内置磁带机）、sinks=external_crt+speaker（配套显示器 + 扬声器）、input_map 键盘 | 研究卡 + 分档口径 |
| assemblies | 7 件 glTF（整机 amstrad_cpc464 / 一体机箱 case / 键盘 keyboard / 磁带机 cassette_deck / 主板 motherboard 含 cpu_z80+gate_array+ram / 显示器 monitor），节点名=node_id | 研究卡部件分解 |
| annotations | ≥30 条（flow ≥10：一体化性价比、开箱即用、Amstrad 性价比路线、Z80 欧洲血脉等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S137]–[S138] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + ROM/磁带镜像红线 + Caprice32/Arnold 候选（需核实）声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（主机约 46×17×7 cm、配套彩色显示器）、配色——248-A 已标，本卡沿用。
- Caprice32/Arnold 候选许可与成熟度——248-A 已标，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `计算机大类_目录_v2.jsonl` 中 Amstrad CPC 464 条目（现占位 `C-PC-0000xx`）→ `status=done`、`device_id=amstrad-cpc464`、`research_doc=hall-personal-batch2/18_AmstradCPC464.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批 **Compaq Portable 口径卡**（`27_CompaqPortable产包口径卡.md`）六节骨架与 **Sinclair ZX81 口径卡**（`26_SinclairZX81产包口径卡.md`）的家用机 ROM 红线体例。品类为「键盘主机一体 + 内置磁带机」形态：`media_hint=tape`（内置磁带机，同 ZX81 磁带口径）、`sinks=external_crt`（配套外接显示器）。**第四批候选性质：产包未定案，口径卡为备底**。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线验收口径与 id_registry 分配结果。
