# 23 · NDS 与 PSP 掌机低模样板预研卡（建模前置备料 · 双机合卡）

> 任务 315-D（05 线）· 完成日期：2026-11-26。
> 性质：**轻量预研/备料卡（双机合卡）**——掌机线继续回归：为下一轮 `nintendo-ds`、`psp` 低模样板建模备好尺寸/配色/面板布局证据包；**本卡不做 gltf、不动装配体、不改 meta/annotations/目录**。
> 口径：沿用低模样板「不贴图、只用 baseColorFactor」；颜色数值 sRGB 0–1（体例参考 `20_GBA低模样板预研卡.md`、`GameBoy掌机谱系参考资材清单_20261106.md`）。

---

# 第一部分 · Nintendo DS

## 一、取机理由（掌机谱系存量 + 未产包）

- **掌机谱系存量**：`console-batch2/GameBoy掌机谱系参考资材清单_20261106.md` 已收录掌机谱系口径，NDS 是双屏触控掌机的开创者，史上最畅销掌机（销量超 1.5 亿）。
- **未产包**：05 线现有 content 包**无 nintendo-ds 包**（仅 game-boy、gba）。
- **谱系位置**：NDS（2004）是任天堂双屏掌机，上屏显示、下屏触控，开创触摸游戏大众化。
- 结论：取 **Nintendo DS** 为掌机线下一台低模预研机型。

## 二、五要素（对齐掌机谱系）

| 要素 | 内容 |
|---|---|
| 机型 | Nintendo DS（NDS） |
| 年代 | 2004 [需核实] |
| 归属谱系 | 游戏机（掌机） |
| 是否已有包 | 否（无包） |
| 定案理由 | 双屏加触控的开创者，史上最畅销掌机，销量超 1.5 亿 |

> 五要素对齐掌机谱系卡；NDS 目录条目 `G-HH-000033` 已存在（planned），本卡不登记目录 id、不擅入定案。

## 三、部件分解草图清单（低模部件）

| # | 部件 | node_id | 草图说明 |
|---|---|---|---|
| 1 | 翻盖机身 | chassis | 翻盖式掌机机身，含铰链/按键区，整机主体（翻盖开合） |
| 2 | 上屏 | top_screen | 翻盖内上屏，主显示屏幕 |
| 3 | 下触屏 | touch_screen | 翻盖内下屏，触控输入屏幕 |
| 4 | 卡带槽 | cartridge_slot | 背部 DS 卡带槽，供卡带插拔动画 |
| 5 | 肩键区 | shoulder_buttons | 机身两侧 L/R 肩键 |
| 6 | 电池仓 | battery_compartment | 机身底部电池仓 |

> 部件清单对齐任务书「chassis / top_screen / touch_screen / cartridge_slot / shoulder_buttons / battery_compartment」6 件；node_id 为**建议命名**，落定须与 02 线目录/建模规范对齐（本卡不登记目录 id）。

## 四、各件尺寸证据表（米，1:1）

| 件 | node_id | 长 × 宽 × 高（米） | 来源 |
|---|---|---|---|
| chassis | chassis | 0.149 × 0.029 × 0.085 | 公开近似值（NDS 约 149×29×85 mm 合盖）[需核实] |
| top_screen | top_screen | 0.062 × 0.002 × 0.047 | 公开近似值（3 英寸上屏）[需核实] |
| touch_screen | touch_screen | 0.062 × 0.002 × 0.047 | 公开近似值（3 英寸下触屏）[需核实] |
| cartridge_slot | cartridge_slot | 0.055 × 0.01 × 0.015 | 公开近似值（DS 卡带槽）[需核实] |
| shoulder_buttons | shoulder_buttons | 0.015 × 0.01 × 0.03 | 公开近似值（L/R 肩键）[需核实] |
| battery_compartment | battery_compartment | 0.06 × 0.012 × 0.04 | 公开近似值（电池仓）[需核实] |

## 五、各件 baseColorFactor 配色表

| 件 | 材质 | baseColorFactor（R,G,B） | 说明 |
|---|---|---|---|
| chassis | 银色机身 | 0.75, 0.77, 0.80 | 掌机银色塑料主体 |
| chassis | 深灰面板 | 0.25, 0.25, 0.28 | 按键区/面板 |
| top_screen | 屏幕黑 | 0.02, 0.02, 0.03 | 上屏玻璃（关机态） |
| touch_screen | 屏幕黑 | 0.02, 0.02, 0.03 | 下触屏玻璃（关机态） |
| cartridge_slot | 黑色卡带槽 | 0.05, 0.05, 0.06 | 背部卡带槽 |
| shoulder_buttons | 深灰肩键 | 0.25, 0.25, 0.28 | L/R 肩键 |
| battery_compartment | 深灰电池仓 | 0.25, 0.25, 0.28 | 电池仓盖 |

## 六、识别件与动画候选（NDS）

- **下屏触控识别件**：下触屏（touch_screen）为标志性识别件，可作「触控笔点击/滑动」示意。
- **卡带插拔识别件**：卡带槽（cartridge_slot）为可插拔识别件；**卡带插拔动画**以该 node 为插拔轴实现。
- **翻盖开合识别件**：机身（chassis）为翻盖形态，**翻盖开合动画**以铰链为轴实现。
- **动画候选**：卡带插拔、翻盖开合、开机启动（动画制作排期挂起）。

## 七、模拟器 / 演示行（NDS）

- **模拟器**：melonDS / DeSmuME（NDS 模拟器候选）——许可标 [需核实]；不下载 BIOS/ROM 红线。
- **演示**：**静态 + 卡带插拔动画**——「插入卡带 → 翻盖开机 → 下屏触控」。动画制作排期挂起。

## 八、目录方案预告 + BIOS/ROM 红线（NDS）

- **目录条目**：游戏机目录 `G-HH-000033「Nintendo DS」`（Nintendo、2004、planned）产包时回填 device_id，**无需新建条目**。
- **media_hint**：NDS 使用 **DS 卡带**，schema `media_hint` 枚举有 `cartridge`，产包时**直接取 `cartridge`（显式说明，无需降级）**。
- **NDS BIOS/ROM 红线**：NDS 系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，本卡仅清单级引用；无固件时 `runtime.emulator` 保守 `none`。

---

# 第二部分 · PlayStation Portable

## 一、取机理由（掌机谱系存量 + 未产包）

- **掌机谱系存量**：`console-batch2/GameBoy掌机谱系参考资材清单_20261106.md` 已收录掌机谱系口径，PSP 是索尼首台掌机，多媒体能力强，全球销量可观。
- **未产包**：05 线现有 content 包**无 psp 包**。
- **谱系位置**：PSP（2004）是索尼横置宽屏掌机，UMD 光盘介质，性能接近当时家用机。
- 结论：取 **PlayStation Portable** 为掌机线下一台低模预研机型。

## 二、五要素（对齐掌机谱系）

| 要素 | 内容 |
|---|---|
| 机型 | PlayStation Portable（PSP） |
| 年代 | 2004 [需核实] |
| 归属谱系 | 游戏机（掌机） |
| 是否已有包 | 否（无包） |
| 定案理由 | 索尼首台掌机，横置宽屏 + UMD，多媒体能力强 |

> 五要素对齐掌机谱系卡；PSP 目录条目 `G-HH-000034` 已存在（planned），本卡不登记目录 id、不擅入定案。

## 三、部件分解草图清单（低模部件）

| # | 部件 | node_id | 草图说明 |
|---|---|---|---|
| 1 | 横置机身 | chassis | 横置宽屏掌机机身，含按键区，整机主体（横置握持） |
| 2 | 屏幕 | screen | 正面宽屏屏幕（4.3 英寸） |
| 3 | UMD 光盘仓 | umd_drive | 背部 UMD 光盘仓，供仓盖开合动画 |
| 4 | 按键区 | control_buttons | 正面十字键/△○×□/摇杆按键区 |
| 5 | 肩键区 | shoulder_buttons | 顶部 L/R 肩键 |
| 6 | 电池仓 | battery_compartment | 机身底部电池仓 |

> 部件清单对齐任务书「chassis / screen / umd_drive / control_buttons / shoulder_buttons / battery_compartment」6 件；node_id 为**建议命名**，落定须与 02 线目录/建模规范对齐（本卡不登记目录 id）。

## 四、各件尺寸证据表（米，1:1）

| 件 | node_id | 长 × 宽 × 高（米） | 来源 |
|---|---|---|---|
| chassis | chassis | 0.170 × 0.023 × 0.074 | 公开近似值（PSP-1000 约 170×23×74 mm）[需核实] |
| screen | screen | 0.095 × 0.002 × 0.054 | 公开近似值（4.3 英寸宽屏）[需核实] |
| umd_drive | umd_drive | 0.065 × 0.005 × 0.065 | 公开近似值（UMD 光盘仓）[需核实] |
| control_buttons | control_buttons | 0.05 × 0.008 × 0.03 | 公开近似值（十字键/△○×□/摇杆区）[需核实] |
| shoulder_buttons | shoulder_buttons | 0.015 × 0.01 × 0.04 | 公开近似值（L/R 肩键）[需核实] |
| battery_compartment | battery_compartment | 0.06 × 0.012 × 0.04 | 公开近似值（电池仓）[需核实] |

## 五、各件 baseColorFactor 配色表

| 件 | 材质 | baseColorFactor（R,G,B） | 说明 |
|---|---|---|---|
| chassis | 黑色机身 | 0.05, 0.05, 0.06 | 掌机黑色塑料主体 |
| chassis | 深灰面板 | 0.25, 0.25, 0.28 | 按键区/面板 |
| screen | 屏幕黑 | 0.02, 0.02, 0.03 | 宽屏玻璃（关机态） |
| screen | 屏幕边框 | 0.15, 0.15, 0.17 | 屏幕边框 |
| umd_drive | 金属银灰 | 0.60, 0.62, 0.65 | UMD 仓金属件 |
| control_buttons | 按键黑 | 0.20, 0.20, 0.22 | 十字键/△○×□/摇杆 |
| shoulder_buttons | 深灰肩键 | 0.25, 0.25, 0.28 | L/R 肩键 |
| battery_compartment | 深灰电池仓 | 0.25, 0.25, 0.28 | 电池仓盖 |

## 六、识别件与动画候选（PSP）

- **UMD 光盘仓识别件**：UMD 仓（umd_drive）为标志性识别件；**UMD 仓盖开合动画**以该 node 为开合轴实现。
- **横置宽屏握持识别件**：机身（chassis）为横置宽屏掌机形态，十字键左、△○×□ 右的布局是 PSP 操作特色。
- **动画候选**：UMD 仓开合、开机启动、宽屏游戏示意（动画制作排期挂起）。

## 七、模拟器 / 演示行（PSP）

- **模拟器**：PPSSPP（PSP 模拟器候选）——许可标 [需核实]；不下载 BIOS/ROM 红线。
- **演示**：**静态 + UMD 仓开合动画**——「放入 UMD → 开机 → 宽屏游戏」。动画制作排期挂起。

## 八、目录方案预告 + BIOS/ROM 红线（PSP）

- **目录条目**：游戏机目录 `G-HH-000034「PlayStation Portable」`（Sony、2004、planned）产包时回填 device_id，**无需新建条目**。
- **media_hint 预告**：PSP 使用 **UMD 光盘**，schema `media_hint` 枚举无 umd，产包时取最接近的 **`cd_rom` 代指并显式标注**（对齐 Dreamcast GD-ROM 降级先例）。
- **PSP BIOS/ROM 红线**：PSP 系统固件与游戏 ROM（UMD）受版权保护，**不入库、不下载**，本卡仅清单级引用；无固件时 `runtime.emulator` 保守 `none`。

---

## 出处清单与 [需核实] 标注（双机共用）

| 出处 | 用途 |
|---|---|
| `console-batch2/20_GBA低模样板预研卡.md` | 体例（掌机预研卡母本） |
| `console-batch2/GameBoy掌机谱系参考资材清单_20261106.md` | 掌机谱系 + NDS/PSP 归属 |
| `console-batch1/31_PS2产包准备卡.md` | 产包字段口径参照 |

- 全部尺寸/配色/布局为公开近似值，**均标 [需核实]**；NDS/PSP CPU 主频、内存、屏幕参数沿用公开资料标 [需核实]；无任何编造史实断言。
- NDS/PSP BIOS/ROM 受版权保护，**不入库、不下载**，本卡仅清单级引用。
- 设备包 id `nintendo-ds`、`psp` 为**建议命名**，落定须与 02 线目录规范对齐（本卡不登记目录 id）。
