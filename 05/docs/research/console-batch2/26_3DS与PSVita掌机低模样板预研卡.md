# 26 · 3DS 与 PSVita 掌机低模样板预研卡（建模前置备料 · 双机合卡）

> 任务 TASK-320-E（05 线）· 完成日期：2026-11-26。
> 性质：**轻量预研/备料卡（双机合卡）**——掌机线继续回归：为下一轮 `nintendo-3ds`、`psvita` 低模样板建模备好尺寸/配色/面板布局证据包；**本卡不做 gltf、不动装配体、不改 meta/annotations/目录**。
> 口径：沿用低模样板「不贴图、只用 baseColorFactor」；颜色数值 sRGB 0–1；部件**纯色无贴图、顶点预算 100–4000**（体例参考 `23_NDS与PSP掌机低模样板预研卡.md`、`GameBoy掌机谱系参考资材清单_20261106.md`）。

---

# 第一部分 · Nintendo 3DS

## 一、取机理由（掌机谱系存量 + 未产包）

- **掌机谱系存量**：`console-batch2/GameBoy掌机谱系参考资材清单_20261106.md` 已收录掌机谱系口径，3DS 是任天堂双屏触控掌机的续作，主打裸眼 3D 上屏。
- **未产包**：05 线现有 content 包**无 nintendo-3ds 包**（仅 game-boy、gba、nintendo-ds、psp）。
- **谱系位置**：3DS（2011）是任天堂横置双屏掌机，上屏支持裸眼 3D，下屏触控，延续 NDS 触摸游戏大众化并引入 3D 显示。
- 结论：取 **Nintendo 3DS** 为掌机线下一台低模预研机型。

## 二、五要素（对齐掌机谱系）

| 要素 | 内容 |
|---|---|
| 机型 | Nintendo 3DS（3DS） |
| 年代 | 2011 [需核实] |
| 归属谱系 | 游戏机（掌机） |
| 是否已有包 | 否（无包） |
| 定案理由 | 双屏触控 + 裸眼 3D 上屏，任天堂双屏掌机续作 |

> 五要素对齐掌机谱系卡；3DS 目录条目 `G-HH-000045` 已存在（planned），本卡不登记目录 id、不擅入定案。

## 三、部件分解草图清单（低模部件）

| # | 部件 | node_id | 草图说明 |
|---|---|---|---|
| 1 | 翻盖机身 | chassis | 翻盖式掌机机身，含铰链/按键区/摇杆，整机主体（翻盖开合） |
| 2 | 上屏 | top_screen | 翻盖内上屏，裸眼 3D 主显示屏幕 |
| 3 | 下触屏 | touch_screen | 翻盖内下屏，触控输入屏幕 |
| 4 | 卡带槽 | cartridge_slot | 背部 3DS 卡带槽，供卡带插拔动画 |
| 5 | 肩键区 | shoulder_buttons | 机身两侧 L/R 肩键 |
| 6 | 电池仓 | battery_compartment | 机身底部电池仓 |

> 部件清单对齐任务书「chassis / top_screen / touch_screen / cartridge_slot / shoulder_buttons / battery_compartment」6 件；node_id 为**建议命名**，落定须与 02 线目录/建模规范对齐（本卡不登记目录 id）。全部部件**纯色无贴图、顶点 100–4000**。

## 四、各件尺寸证据表（米，1:1）

| 件 | node_id | 长 × 宽 × 高（米） | 来源 |
|---|---|---|---|
| chassis | chassis | 0.134 × 0.021 × 0.074 | 公开近似值（3DS 约 134×21×74 mm 合盖）[需核实] |
| top_screen | top_screen | 0.078 × 0.002 × 0.047 | 公开近似值（3.53 英寸上屏）[需核实] |
| touch_screen | touch_screen | 0.067 × 0.002 × 0.040 | 公开近似值（3.02 英寸下触屏）[需核实] |
| cartridge_slot | cartridge_slot | 0.035 × 0.004 × 0.040 | 公开近似值（3DS 卡带槽）[需核实] |
| shoulder_buttons | shoulder_buttons | 0.015 × 0.010 × 0.030 | 公开近似值（L/R 肩键）[需核实] |
| battery_compartment | battery_compartment | 0.060 × 0.012 × 0.040 | 公开近似值（电池仓）[需核实] |

## 五、各件 baseColorFactor 配色表

| 件 | 材质 | baseColorFactor（R,G,B） | 说明 |
|---|---|---|---|
| chassis | 蓝色机身 | 0.16, 0.42, 0.66 | 掌机蓝色塑料主体 |
| chassis | 深灰面板 | 0.25, 0.25, 0.28 | 按键区/面板 |
| top_screen | 屏幕黑 | 0.02, 0.02, 0.03 | 上屏玻璃（关机态） |
| touch_screen | 屏幕黑 | 0.02, 0.02, 0.03 | 下触屏玻璃（关机态） |
| cartridge_slot | 黑色卡带槽 | 0.05, 0.05, 0.06 | 背部卡带槽 |
| shoulder_buttons | 深灰肩键 | 0.25, 0.25, 0.28 | L/R 肩键 |
| battery_compartment | 深灰电池仓 | 0.25, 0.25, 0.28 | 电池仓盖 |

## 六、识别件与动画候选（3DS）

- **翻盖开合识别件**：机身（chassis）为翻盖形态，**翻盖开合动画**以铰链为轴实现。
- **卡带插拔识别件**：卡带槽（cartridge_slot）为可插拔识别件；**卡带插拔动画**以该 node 为插拔轴实现。
- **下屏触控识别件**：下触屏（touch_screen）为标志性识别件，可作「触控笔点击/滑动」示意。
- **裸眼 3D 上屏识别件**：上屏（top_screen）为裸眼 3D 屏幕，是 3DS 的标志性识别特征。
- **动画候选**：卡带插拔、翻盖开合、开机启动（动画制作排期挂起）。

## 七、模拟器 / 演示行（3DS）

- **模拟器**：Citra / Mikage（3DS 模拟器候选）——许可标 [需核实]；不下载 BIOS/ROM 红线。
- **演示**：**静态 + 卡带插拔动画**——「插入卡带 → 翻盖开机 → 下屏触控」。动画制作排期挂起。

## 八、目录方案预告 + BIOS/ROM 红线（3DS）

- **目录条目**：游戏机目录 `G-HH-000045「Nintendo 3DS」`（Nintendo、2011、planned）产包时回填 device_id，**无需新建条目**。
- **media_hint**：3DS 使用 **3DS 卡带**，schema `media_hint` 枚举有 `cartridge`，产包时**直接取 `cartridge`（显式说明，无需降级）**。
- **3DS BIOS/ROM 红线**：3DS 系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，本卡仅清单级引用；无固件时 `runtime.emulator` 保守 `none`。

---

# 第二部分 · PlayStation Vita

## 一、取机理由（掌机谱系存量 + 未产包）

- **掌机谱系存量**：`console-batch2/GameBoy掌机谱系参考资材清单_20261106.md` 已收录掌机谱系口径，PSVita 是索尼 PSP 后继掌机，前后双触控 + 双摇杆。
- **未产包**：05 线现有 content 包**无 psvita 包**（仅 game-boy、gba、nintendo-ds、psp）。
- **谱系位置**：PSVita（2011）是索尼横置宽屏掌机，OLED 屏 + 背部触控板 + 双摇杆，性能延续 PSP 家用机化路线。
- 结论：取 **PlayStation Vita** 为掌机线下一台低模预研机型。

## 二、五要素（对齐掌机谱系）

| 要素 | 内容 |
|---|---|
| 机型 | PlayStation Vita（PSVita） |
| 年代 | 2011 [需核实] |
| 归属谱系 | 游戏机（掌机） |
| 是否已有包 | 否（无包） |
| 定案理由 | 索尼 PSP 后继机型，前后双触控 + 双摇杆 |

> 五要素对齐掌机谱系卡；PSVita 目录条目 `G-HH-000046` 已存在（planned），本卡不登记目录 id、不擅入定案。

## 三、部件分解草图清单（低模部件）

| # | 部件 | node_id | 草图说明 |
|---|---|---|---|
| 1 | 横置机身 | chassis | 横置宽屏掌机机身，含按键区/双摇杆，整机主体（横置握持） |
| 2 | 屏幕 | screen | 正面宽屏 OLED 屏幕（5 英寸） |
| 3 | 背触板 | rear_touchpad | 背部触控板，供背面触控示意 |
| 4 | 卡带槽 | cartridge_slot | 顶部 PSVita 专用卡带槽，供卡带插拔动画 |
| 5 | 按键区 | control_buttons | 正面双摇杆/十字键/△○×□按键区 |
| 6 | 肩键区 | shoulder_buttons | 顶部 L/R 肩键 |

> 部件清单对齐任务书「chassis / screen / rear_touchpad / cartridge_slot / control_buttons / shoulder_buttons」6 件；node_id 为**建议命名**，落定须与 02 线目录/建模规范对齐（本卡不登记目录 id）。全部部件**纯色无贴图、顶点 100–4000**。

## 四、各件尺寸证据表（米，1:1）

| 件 | node_id | 长 × 宽 × 高（米） | 来源 |
|---|---|---|---|
| chassis | chassis | 0.182 × 0.0186 × 0.0835 | 公开近似值（PSVita 约 182×18.6×83.5 mm）[需核实] |
| screen | screen | 0.111 × 0.002 × 0.062 | 公开近似值（5 英寸 OLED 宽屏）[需核实] |
| rear_touchpad | rear_touchpad | 0.120 × 0.003 × 0.070 | 公开近似值（背部触控板）[需核实] |
| cartridge_slot | cartridge_slot | 0.030 × 0.003 × 0.020 | 公开近似值（PSVita 专用卡带槽）[需核实] |
| control_buttons | control_buttons | 0.080 × 0.008 × 0.030 | 公开近似值（双摇杆/十字键/△○×□区）[需核实] |
| shoulder_buttons | shoulder_buttons | 0.015 × 0.010 × 0.040 | 公开近似值（L/R 肩键）[需核实] |

## 五、各件 baseColorFactor 配色表

| 件 | 材质 | baseColorFactor（R,G,B） | 说明 |
|---|---|---|---|
| chassis | 黑色机身 | 0.08, 0.08, 0.09 | 掌机黑色塑料主体 |
| chassis | 深灰面板 | 0.25, 0.25, 0.28 | 按键区/面板 |
| screen | 屏幕黑 | 0.02, 0.02, 0.03 | OLED 宽屏玻璃（关机态） |
| screen | 屏幕边框 | 0.12, 0.12, 0.14 | 屏幕边框 |
| rear_touchpad | 深色背触板 | 0.10, 0.10, 0.12 | 背部触控板 |
| cartridge_slot | 黑色卡带槽 | 0.05, 0.05, 0.06 | 顶部专用卡带槽 |
| control_buttons | 按键黑 | 0.20, 0.20, 0.22 | 双摇杆/十字键/△○×□ |
| shoulder_buttons | 深灰肩键 | 0.25, 0.25, 0.28 | L/R 肩键 |

## 六、识别件与动画候选（PSVita）

- **背触板识别件**：背触板（rear_touchpad）为 PSVita 标志性识别件，可作「背面触控」示意。
- **双摇杆识别件**：按键区（control_buttons）为双摇杆布局，双摇杆是 PSVita 操作特色。
- **卡带插拔识别件**：卡带槽（cartridge_slot）为可插拔识别件；**卡带插拔动画**以该 node 为插拔轴实现。
- **动画候选**：卡带插拔、开机启动、宽屏游戏示意（动画制作排期挂起）。

## 七、模拟器 / 演示行（PSVita）

- **模拟器**：Vita3K（PSVita 模拟器候选）——许可标 [需核实]；不下载 BIOS/ROM 红线。
- **演示**：**静态 + 卡带插拔动画**——「插入卡带 → 开机 → 宽屏游戏」。动画制作排期挂起。

## 八、目录方案预告 + BIOS/ROM 红线（PSVita）

- **目录条目**：游戏机目录 `G-HH-000046「PlayStation Vita」`（Sony、2011、planned）产包时回填 device_id，**无需新建条目**。
- **media_hint**：PSVita 使用 **PSVita 专用卡带**，schema `media_hint` 枚举有 `cartridge`，产包时**直接取 `cartridge`（显式说明，无需降级）**。
- **PSVita BIOS/ROM 红线**：PSVita 系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，本卡仅清单级引用；无固件时 `runtime.emulator` 保守 `none`。

---

## 出处清单与 [需核实] 标注（双机共用）

| 出处 | 用途 |
|---|---|
| `console-batch2/23_NDS与PSP掌机低模样板预研卡.md` | 体例（掌机预研卡母本，双机合卡） |
| `console-batch2/GameBoy掌机谱系参考资材清单_20261106.md` | 掌机谱系 + 3DS/PSVita 归属 |
| `console-batch1/31_PS2产包准备卡.md` | 产包字段口径参照 |

- 全部尺寸/配色/布局为公开近似值，**均标 [需核实]**；3DS/PSVita CPU 主频、内存、屏幕参数沿用公开资料标 [需核实]；无任何编造史实断言。
- 3DS/PSVita BIOS/ROM 受版权保护，**不入库、不下载**，本卡仅清单级引用。
- 设备包 id `nintendo-3ds`、`psvita` 为**建议命名**，落定须与 02 线目录规范对齐（本卡不登记目录 id）。
- 两部机型 media_hint 均为 `cartridge`（3DS 卡带 / PSVita 专用卡带有枚举），已预告标注，产包时直接取用、无需降级。
