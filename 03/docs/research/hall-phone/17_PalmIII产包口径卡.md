# 17 — Palm III 产包口径卡（第四批预研）

> 03 线 TASK-293-E 交付。第四批候选第 9 台 Palm III（目录占位 `M-PD-0000xx`）的产包口径卡预研，供定案后产包领取。研究卡 `12_PalmIII.md`（证据 S153–S154）已由 258-A 就绪。**第四批候选性质：产包未定案，本口径卡为备底**。只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 Palm OS ROM/二进制。

## 一、模拟器形态（无成熟模拟器，emulator="none"）

- **`runtime.emulator` = `"none"`**——Palm III 无广泛可用的成熟开源模拟器，按预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径，静态 + 红外对传/同步原理动画承载。
- **候选（标需核实）**：Palm OS 模拟器（POSE 等）存在（许可与成熟度均「需核实」），产包时如核实可用再走合规流程接入，候选记 THIRD_PARTY。
- **隔离形态（若接入）**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；二进制不入库。

## 二、固件红线

- **Palm OS ROM 不入库、不下载、不提供、不再分发**——受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 Palm OS ROM 由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有固件红线惯例（Palm OS ROM 等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`palm-iii`、era=1998、category=pda、manufacturer=Palm、description 五字段齐备 | 研究卡 12_PalmIII.md + palm-pilot 先例 |
| runtime.json | emulator=`none`（候选 POSE 记 THIRD_PARTY）、media_hint=`firmware`（Palm OS ROM）、sinks=handheld_lcd+speaker、input_map 触控笔（stylus）+ 触控（touch） | 研究卡 + 分档口径 |
| assemblies | 7 件 glTF（整机 palm_iii / 机身壳 case / 触控 LCD 屏 display / 红外端口 ir_port / 主板 motherboard / 电池 battery / 触控笔 stylus / 底座接口 dock_connector），节点名=node_id | 研究卡部件分解 |
| annotations | ≥30 条（flow ≥10：Palm 经典成熟、红外对传巧思、PDA 黄金年代、与 Pilot 谱系等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S153]–[S154] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + Palm OS ROM 红线 + POSE 候选（需核实）声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（约 12×8×1.8 cm、约 160 g、单色触控 LCD 约 160×160）、配色——258-A 已标，本卡沿用。
- POSE 候选许可与成熟度——258-A 已标，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `通讯与移动大类_目录_v3.jsonl` 中 Palm III 条目（现占位 `M-PD-0000xx`）→ `status=done`、`device_id=palm-iii`、`research_doc=hall-phone/12_PalmIII.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐手机厅先例 **Nokia 8110 口径卡**（`hall-phone/08_Nokia8110产包口径卡.md`）六节骨架与 PDA 先例 **palm-pilot**（01 线 `category=pda`）。品类为「PDA」：`category=pda`（目录 `M-PD`，区别于手机 `M-MP`）、`media_hint=firmware`、`sinks=handheld_lcd+speaker`；`emulator=none`（候选 POSE 记 THIRD_PARTY）。**第四批候选性质：产包未定案，口径卡为备底**。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线验收口径与 id_registry 分配结果。
