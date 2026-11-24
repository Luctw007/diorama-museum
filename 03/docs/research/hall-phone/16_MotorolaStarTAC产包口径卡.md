# 16 — Motorola StarTAC 产包口径卡（第四批预研）

> 03 线 TASK-293-C 交付。第四批候选第 4 台 Motorola StarTAC（目录占位 `M-MP-0000xx`）的产包口径卡预研，供定案后产包领取。研究卡 `11_MotorolaStarTAC.md`（证据 S143–S144）已由 248-B 就绪。**第四批候选性质：产包未定案，本口径卡为备底**。只出口径、不产包、不改目录 jsonl、不 allocate id、不下载固件/ROM/二进制。

## 一、模拟器形态（无成熟模拟器，emulator="none"）

- **`runtime.emulator` = `"none"`**——功能机无成熟专用模拟器，对齐 Nokia 8110/3310 先行样板（演示向静态 + 动画），静态 + 翻盖开合动画演示承载。
- **候选（标需核实）**：无成熟功能机模拟器，本卡不写后端。
- **红线**：功能机固件受版权保护，**不下载、不提供、不内嵌任何固件/ROM/二进制**；「可玩」用自研复刻承载（翻盖开合互动）。

## 二、固件红线

- **Motorola StarTAC 固件不入库、不下载、不提供、不再分发**——受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时固件由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有固件红线惯例。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`motorola-startac`、era=1996、category=phone、manufacturer=Motorola、description 五字段齐备 | 研究卡 11_MotorolaStarTAC.md + Nokia 8110 先例 |
| runtime.json | emulator=`none`（演示向）、media_hint=`firmware`（功能机固件）、sinks=handheld_lcd+speaker、input_map 8 动作（0-9/拨号/挂断等） | 研究卡 + Nokia 8110 先例 |
| assemblies | 7 件 glTF（整机 motorola_startac / 上盖 upper_cover / 下机身 lower_body / 铰链 hinge / 键盘 keypad / 主板 motherboard / 电池 battery），节点名=node_id | 研究卡部件分解 |
| annotations | ≥30 条（flow ≥10：翻盖形态开端、小巧标杆、上承下启、Motorola 设计基因等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S143]–[S144] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + 无模拟器声明 + 固件红线声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（约 55×94 mm 展开 × 19 mm 厚、约 88 克、翻盖铰链结构）、配色——248-B 已标，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `通讯与移动大类_目录_v3.jsonl` 中 Motorola StarTAC 条目（现占位 `M-MP-0000xx`）→ `status=done`、`device_id=motorola-startac`、`research_doc=hall-phone/11_MotorolaStarTAC.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐手机厅先例 **Nokia 8110 口径卡**（`hall-phone/08_Nokia8110产包口径卡.md`）六节骨架——`category=phone`、`media_hint=firmware`、`sinks=handheld_lcd+speaker`、`emulator="none"` 演示向口径均沿用；差异在 StarTAC 招牌为翻盖开合（动画锚点：翻盖开合互动，与 Nokia 8110 滑盖开合同类）。**第四批候选性质：产包未定案，口径卡为备底**。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线验收口径与 id_registry 分配结果。
