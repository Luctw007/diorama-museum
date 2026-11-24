# 18 — RIM BlackBerry 850 产包口径卡（第四批预研）

> 03 线 TASK-293-E 交付。第四批候选第 10 台 RIM BlackBerry 850（目录占位 `M-MP-0000xx`）的产包口径卡预研，供定案后产包领取。研究卡 `13_BlackBerry850.md`（证据 S155–S156）已由 258-A 就绪。**第四批候选性质：产包未定案，本口径卡为备底**。只出口径、不产包、不改目录 jsonl、不 allocate id、不下载固件/ROM/二进制。至此第四批 10 台口径卡预研全齐。

## 一、模拟器形态（无成熟模拟器，emulator="none"）

- **`runtime.emulator` = `"none"`**——BlackBerry 850 无成熟专用模拟器，对齐 Nokia 8110/3310 先行样板（演示向静态 + 动画），静态 + 邮件推送原理动画承载。
- **候选（标需核实）**：无成熟模拟器，本卡不写后端。
- **红线**：固件受版权保护，**不下载、不提供、不内嵌任何固件/ROM/二进制**；「可玩」用自研复刻承载（邮件推送演示 + 拇指键盘叙事）。

## 二、固件红线

- **BlackBerry 850 固件不入库、不下载、不提供、不再分发**——受版权保护，本卡及后续产包只做**清单级引用**。
- **slots/media 由用户自备**：真跑时固件由用户按合规渠道自备，放入本地 slots，不入仓库、不进 git。
- 参照 01 线既有固件红线惯例。

## 三、产包字段清单（逐件口径）

| 件 | 口径 | 依据 |
|---|---|---|
| meta.json | id=`blackberry-850`、era=1999、category=phone、manufacturer=RIM、description 五字段齐备 | 研究卡 13_BlackBerry850.md + Nokia 8110 先例 |
| runtime.json | emulator=`none`（演示向）、media_hint=`firmware`（固件）、sinks=handheld_lcd+speaker、input_map 拇指键盘（QWERTY） | 研究卡 + 分档口径 |
| assemblies | 7 件 glTF（整机 blackberry_850 / 机身壳 case / 单色 LCD 屏 display / QWERTY 拇指键盘 thumb_keyboard / 主板 motherboard / 电池 battery / 天线 antenna），节点名=node_id | 研究卡部件分解 |
| annotations | ≥30 条（flow ≥10：邮件手机先驱、拇指键盘诞生、黑莓品牌起点、从打电话到移动办公等；role 20–200 字含「在整机」） | 研究卡叙事锚点 |
| encyclopedia | ≥2500 汉字，保留 [S155]–[S156] | 研究卡史实节 |
| THIRD_PARTY | 三件套 + 无模拟器声明 + 固件红线声明 | 分档口径 + 红线 |

## 四、「需核实」清单

- 尺寸（约 11×7×2 cm、QWERTY 拇指键盘、单色 LCD）、配色——258-A 已标，本卡沿用。
- 产包时「需核实」只能进 encyclopedia/MESHES/THIRD_PARTY，不进 role/flow 标注（R-060）。

## 五、目录反链口径（产包时执行）

- 目录 `通讯与移动大类_目录_v3.jsonl` 中 BlackBerry 850 条目（现占位 `M-MP-0000xx`）→ `status=done`、`device_id=blackberry-850`、`research_doc=hall-phone/13_BlackBerry850.md`（本卡不执行，产包时执行）。

## 六、产包体例对齐说明

本卡体例对齐手机厅先例 **Nokia 8110 口径卡**（`hall-phone/08_Nokia8110产包口径卡.md`）六节骨架——`category=phone`（目录 `M-MP`，研究卡 13 号明确「手机」而非 PDA）、`media_hint=firmware`、`sinks=handheld_lcd+speaker`、`emulator="none"` 演示向口径均沿用；差异在 BlackBerry 850 招牌为 QWERTY 拇指键盘 + 邮件推送。**第四批候选性质：产包未定案，口径卡为备底**。

---

> 本卡供后续产包直接取用；产包前请再核对研究卡、02 线验收口径与 id_registry 分配结果。至此第四批 10 台口径卡预研全齐。
