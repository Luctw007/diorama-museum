# 14 — Apple Newton 产包口径卡

> 03 线 TASK-288-A 交付。第三批第 10 台 Apple Newton MessagePad（目录占位 `M-PD-0000xx`）的产包准备口径卡，供定案后产包领取。研究卡 `09_AppleNewton.md`（证据 S135–S136）已由 238-A 就绪。本卡只出口径、不产包、不改目录 jsonl、不 allocate id、不下载 NewtonOS 固件/ROM/二进制。至此第三批 10 台口径卡全齐。

## 一、模拟器形态（Newton PDA，emulator="none"）

- **`runtime.emulator` = `"none"`**——Newton PDA 模拟器成熟度低，无广泛可用的成熟开源模拟器，按预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径，静态 + 手写识别原理动画承载。
- **候选（标需核实）**：Einstein（开源 Newton OS 模拟器）存在（许可与成熟度均「需核实」），产包时如核实可用再走合规流程接入，候选记 THIRD_PARTY。
- **隔离形态（若接入）**：参照 01 线「独立进程（ADR D1）经 stdio 设备通道接入网关、不链接不派生」惯例；二进制不入库。
- **保守口径**：本卡 `emulator="none"` 即为保守值（同 Nokia 8110 功能机「无成熟模拟器，演示向」口径），不建 01 线槽位 manifest、不下发二进制。

## 二、NewtonOS 固件红线

- **NewtonOS ROM 与固件不入库、不下载、不提供、不再分发**——NewtonOS ROM（受版权保护），本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时 NewtonOS ROM 由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有 ROM/固件红线惯例（MAME Romset / Apple II ROM / Symbian 固件 / Palm OS ROM 等均不入库）。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`apple-newton`、era=1993、category=pda、manufacturer=Apple、description 五字段齐备 | 研究卡 09_AppleNewton.md + 252-B 包 id 建议 + palm-pilot 先例（category=pda） |
| runtime.json | emulator=`none`（无成熟模拟器，候选 Einstein 记 THIRD_PARTY）、media_hint=`firmware`（Newton OS ROM）、sinks=handheld_lcd+speaker（掌上触控 LCD + 扬声器）、input_map 触控笔（stylus）+ 触控（touch） | 研究卡 + 分档口径 |
| assemblies | 7 件 glTF（整机 apple_newton / 机身壳 case / 触控 LCD 屏 display / 主板 motherboard 含 cpu_arm610+rom+ram / 电池 battery / 触控笔 stylus / 扩展槽 expansion_slot），节点名=node_id | 研究卡部件分解草图 |
| annotations | ≥30 条（flow ≥10：PDA 的先驱、手写识别的早熟、ARM 的早期用户、概念超前的代价、早熟的先知等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S135]–[S136] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + NewtonOS 固件红线声明 + Einstein 候选（许可/成熟度需核实）声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（整机约 18.4 cm 长 × 11.4 cm 宽 × 1.9 cm 厚、约 410 g、单色触控 LCD 约 336×240）、配色——238-A 已标「需核实」，本卡沿用。
- Einstein 候选许可与成熟度——238-A 已标「需核实」，本卡沿用。
- NewtonOS ROM 的合规获取路径——238-A 已标「需核实」，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `通讯与移动大类_目录_v3.jsonl` 中 Apple Newton 条目（现占位 `M-PD-0000xx`，产包前由 02 线 id_registry `allocate` 换真号）→ `status=done`、`device_id=apple-newton`、`research_doc=hall-phone/09_AppleNewton.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐第三批最新先例 **Compaq Portable 口径卡**（`hall-personal-batch2/27_CompaqPortable产包口径卡.md`）的六节骨架，PDA 品类口径对齐手机厅先例 **Nokia 8110 口径卡**（`hall-phone/08_Nokia8110产包口径卡.md`）——`media_hint=firmware`、`sinks=handheld_lcd+speaker`、`emulator="none"` 演示向口径均沿用。差异在 category：Newton 为 PDA（`category=pda`，同 palm-pilot 先例、目录 `M-PD`），区别于 Nokia 8110 的 `phone`（`M-MP`）。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线 252-B 验收清单与 id_registry 分配结果。至此第三批 10 台口径卡全齐。
