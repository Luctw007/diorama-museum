# 30 · GBC 与 NGPC 掌机低模样板预研合卡（建模前置备料 · 双机合卡）

> 任务 TASK-325-I（05 线）· 完成日期：2026-11-27。
> 性质：**纯预研合卡（双机合卡）**——为下一轮 `game-boy-color`、`neo-geo-pocket-color` 低模样板建模备好尺寸/配色/识别件证据包；**本卡不做 gltf、不动装配体、不改 meta/annotations/目录 jsonl**。
> 口径：沿用低模样板「不贴图、只用 baseColorFactor」；颜色数值 sRGB 0–1；部件**纯色无贴图、顶点预算 100–4000**（chassis 用 15 盒＝120 顶点，其余件用 13 盒＝104 顶点，均以低模盒体近似）；体例参考 `26_3DS与PSVita掌机低模样板预研卡.md`。
> 条目登记：GBC＝`G-HH-000021`（Nintendo、1998）、NGPC＝`G-HH-000023`（SNK、1999），均为目录实扫已存在 planned 条目，本卡**不登记目录 id、不擅入定案**。

---

# 第一部分 · Game Boy Color

## 一、取机理由（掌机谱系存量 + 未产包）

- **掌机谱系存量**：目录实扫 `G-HH-000021「Game Boy Color」`（Nintendo、1998、`planned`，taxonomy_path＝游戏机/掌机/Game Boy 系，influence＝「GB 彩色升级版，向下兼容」）已存在。
- **未产包**：05 线现有 content 包**无 game-boy-color 包**（仅有 game-boy、gba、nintendo-ds、psp 等），GBC 是 GB 谱系彩色升级节点，尚未产包。
- **谱系位置**：GBC（1998）是任天堂竖版掌机，彩色液晶屏 + 向下兼容 GB 卡带，十字键 + A/B 键布局沿用 GB 经典竖握形态。
- 结论：取 **Game Boy Color（GBC）** 为掌机线低模预研机型之一。

## 二、五要素（对齐掌机谱系）

| 要素 | 内容 |
|---|---|
| 机型 | Game Boy Color（GBC） |
| 年代 | 1998（目录实扫 era=1998） |
| 归属谱系 | 游戏机（掌机）· Game Boy 系 |
| 是否已有包 | 否（无包） |
| 定案理由 | GB 彩色升级版，向下兼容，竖版经典十字键布局 |

> GBC 目录条目 `G-HH-000021` 已存在（planned），本卡不登记目录 id、不擅入定案。

## 三、部件分解草图清单（拆分方案 · 低模部件）

| # | 部件 | node_id | 顶点预算（盒体近似） | 草图说明 |
|---|---|---|---|---|
| 1 | 竖版机身 | chassis | 15 盒＝120 顶点 | 竖版掌机机身，含屏幕区/按键区/卡带口，整机主体 |
| 2 | 屏幕模块 | screen_module | 13 盒＝104 顶点 | 正面彩色液晶屏模块（关机态） |
| 3 | 十字键 | d_pad | 13 盒＝104 顶点 | 左下十字键，供按压识别 |
| 4 | 按键 | buttons | 13 盒＝104 顶点 | 右侧 A/B 键，供按压识别 |
| 5 | 卡带槽 | cartridge_slot | 13 盒＝104 顶点 | 顶部/背部 GB 卡带槽，供卡带插拔动画 |
| 6 | 电池仓 | battery_compartment | 13 盒＝104 顶点 | 机身背部电池仓 |

> 部件清单对齐任务书「chassis / screen_module / d_pad / buttons / cartridge_slot / battery_compartment」6 件；node_id 为**建议命名**（＝node_id），落定须与 02 线目录/建模规范对齐（本卡不登记目录 id）。全部部件**纯色无贴图、顶点 100–4000**，盒体近似（1 盒＝8 顶点）。

## 四、各件尺寸证据表（米，1:1）

| 件 | node_id | 长 × 宽 × 高（米） | 来源 |
|---|---|---|---|
| chassis | chassis | 0.075 × 0.027 × 0.133 | 公开近似值（GBC 约 75×27×133 mm 竖版）[需核实] |
| screen_module | screen_module | 0.044 × 0.003 × 0.040 | 公开近似值（约 2.3 英寸彩色 LCD）[需核实] |
| d_pad | d_pad | 0.020 × 0.006 × 0.020 | 公开近似值（十字键）[需核实] |
| buttons | buttons | 0.020 × 0.006 × 0.018 | 公开近似值（A/B 键区）[需核实] |
| cartridge_slot | cartridge_slot | 0.032 × 0.006 × 0.040 | 公开近似值（GB 卡带槽）[需核实] |
| battery_compartment | battery_compartment | 0.060 × 0.012 × 0.040 | 公开近似值（电池仓）[需核实] |

## 五、各件 baseColorFactor 配色表

| 件 | 材质 | baseColorFactor（R,G,B） | 说明 |
|---|---|---|---|
| chassis | 紫色机身 | 0.35, 0.06, 0.55 | GBC 紫色塑料主体 |
| chassis | 深灰面板 | 0.25, 0.25, 0.28 | 按键区/面板 |
| screen_module | 屏幕黑 | 0.02, 0.02, 0.03 | 彩色液晶屏玻璃（关机态） |
| d_pad | 深灰十字键 | 0.20, 0.20, 0.22 | 十字键 |
| buttons | 深灰按键 | 0.20, 0.20, 0.22 | A/B 键 |
| cartridge_slot | 黑色卡带槽 | 0.05, 0.05, 0.06 | 卡带槽口 |
| battery_compartment | 深灰电池仓 | 0.25, 0.25, 0.28 | 电池仓盖 |

## 六、识别件与动画候选（GBC）

- **d_pad 十字键识别件**：十字键（d_pad）为可按压识别件；**十字键按压动画**以该 node 为按压轴实现。
- **buttons A/B 键识别件**：按键（buttons）为 A/B 键可按压识别件；**A/B 键按压动画**以该 node 为按压轴实现。
- **cartridge_slot 卡带插拔识别件**：卡带槽（cartridge_slot）为可插拔识别件；**卡带插拔动画**以该 node 为插拔轴实现。
- **screen_module 彩色液晶屏识别件**：屏幕模块（screen_module）为彩色液晶屏，是 GBC 相较 GB 的标志性识别特征。
- **动画候选**：十字键按压、A/B 键按压、卡带插拔、开机启动（动画制作排期挂起）。

## 七、模拟器 / 演示行（GBC）

- **模拟器**：mGBA / SameBoy（GBC 模拟器候选）——许可标 [需核实]；不下载 BIOS/ROM 红线。
- **演示**：**静态 + 卡带插拔 + 按键按压动画**——「插入卡带 → 开机 → 十字键/A 键操作」。动画制作排期挂起。

## 八、目录方案预告 + BIOS/ROM 红线（GBC）

- **目录条目**：游戏机目录 `G-HH-000021「Game Boy Color」`（Nintendo、1998、planned）产包时回填 device_id，**无需新建条目**。
- **media_hint**：GBC 使用 **GB/GBC 卡带**，schema `media_hint` 枚举有 `cartridge`（卡带有枚举直取，无需降级），产包时**直接取 `cartridge`（预告标注）**。
- **GBC BIOS/ROM 红线**：GBC 启动固件（BIOS）与游戏 ROM（卡带）受版权保护，**不入库、不下载**，本卡仅清单级引用；无固件时 `runtime.emulator` 保守 `none`。

---

# 第二部分 · Neo Geo Pocket Color

## 一、取机理由（掌机谱系存量 + 未产包）

- **掌机谱系存量**：目录实扫 `G-HH-000023「Neo Geo Pocket Color」`（SNK、1999、`planned`，taxonomy_path＝游戏机/掌机/其他掌机，influence＝「彩色掌机，格斗游戏阵容强，SNK 破产前绝唱」）已存在。
- **未产包**：05 线现有 content 包**无 neo-geo-pocket-color 包**，NGPC 是 SNK 彩色掌机，尚未产包。
- **谱系位置**：NGPC（1999）是 SNK 竖版彩色掌机，特色为 **clicky 摇杆状十字键**，格斗游戏阵容强，是 SNK 破产前最后一代掌机。
- 结论：取 **Neo Geo Pocket Color（NGPC）** 为掌机线低模预研机型之一。

## 二、五要素（对齐掌机谱系）

| 要素 | 内容 |
|---|---|
| 机型 | Neo Geo Pocket Color（NGPC） |
| 年代 | 1999（目录实扫 era=1999） |
| 归属谱系 | 游戏机（掌机）· 其他掌机 |
| 是否已有包 | 否（无包） |
| 定案理由 | SNK 彩色掌机，clicky 摇杆状十字键，格斗阵容强 |

> NGPC 目录条目 `G-HH-000023` 已存在（planned），本卡不登记目录 id、不擅入定案。

## 三、部件分解草图清单（拆分方案 · 低模部件）

| # | 部件 | node_id | 顶点预算（盒体近似） | 草图说明 |
|---|---|---|---|---|
| 1 | 竖版机身 | chassis | 15 盒＝120 顶点 | 竖版掌机机身，含屏幕区/摇杆十字键区/按键区，整机主体 |
| 2 | 屏幕模块 | screen_module | 13 盒＝104 顶点 | 正面彩色液晶屏模块（关机态） |
| 3 | 十字键 | d_pad | 13 盒＝104 顶点 | NGPC 特有 clicky 摇杆状十字键，供按压识别 |
| 4 | 按键 | buttons | 13 盒＝104 顶点 | 右侧 A/B 键，供按压识别 |
| 5 | 卡带槽 | cartridge_slot | 13 盒＝104 顶点 | 顶部/背部 NGPC 卡带槽，供卡带插拔动画 |
| 6 | 电池仓 | battery_compartment | 13 盒＝104 顶点 | 机身背部电池仓 |

> 部件清单对齐任务书「chassis / screen_module / d_pad / buttons / cartridge_slot / battery_compartment」6 件（同 GBC 结构）；node_id 为**建议命名**（＝node_id），落定须与 02 线目录/建模规范对齐（本卡不登记目录 id）。全部部件**纯色无贴图、顶点 100–4000**，盒体近似（1 盒＝8 顶点）。

## 四、各件尺寸证据表（米，1:1）

| 件 | node_id | 长 × 宽 × 高（米） | 来源 |
|---|---|---|---|
| chassis | chassis | 0.075 × 0.025 × 0.130 | 公开近似值（NGPC 约 75×25×130 mm 竖版）[需核实] |
| screen_module | screen_module | 0.045 × 0.003 × 0.040 | 公开近似值（彩色 LCD）[需核实] |
| d_pad | d_pad | 0.022 × 0.008 × 0.022 | 公开近似值（clicky 摇杆状十字键）[需核实] |
| buttons | buttons | 0.018 × 0.006 × 0.016 | 公开近似值（A/B 键区）[需核实] |
| cartridge_slot | cartridge_slot | 0.030 × 0.006 × 0.040 | 公开近似值（NGPC 卡带槽）[需核实] |
| battery_compartment | battery_compartment | 0.060 × 0.010 × 0.038 | 公开近似值（电池仓）[需核实] |

## 五、各件 baseColorFactor 配色表

| 件 | 材质 | baseColorFactor（R,G,B） | 说明 |
|---|---|---|---|
| chassis | 银色机身 | 0.75, 0.77, 0.80 | NGPC 银色塑料主体 |
| chassis | 深灰面板 | 0.25, 0.25, 0.28 | 按键区/面板 |
| screen_module | 屏幕黑 | 0.02, 0.02, 0.03 | 彩色液晶屏玻璃（关机态） |
| d_pad | 深灰十字键 | 0.20, 0.20, 0.22 | clicky 摇杆状十字键 |
| buttons | 深灰按键 | 0.20, 0.20, 0.22 | A/B 键 |
| cartridge_slot | 黑色卡带槽 | 0.05, 0.05, 0.06 | 卡带槽口 |
| battery_compartment | 深灰电池仓 | 0.25, 0.25, 0.28 | 电池仓盖 |

## 六、识别件与动画候选（NGPC）

- **d_pad clicky 摇杆状十字键识别件**：十字键（d_pad）为 NGPC 特有 clicky 摇杆状十字键，是可按压识别件；**十字键按压动画**以该 node 为按压轴实现。
- **buttons A/B 键识别件**：按键（buttons）为 A/B 键可按压识别件；**A/B 键按压动画**以该 node 为按压轴实现。
- **cartridge_slot 卡带插拔识别件**：卡带槽（cartridge_slot）为可插拔识别件；**卡带插拔动画**以该 node 为插拔轴实现。
- **screen_module 彩色液晶屏识别件**：屏幕模块（screen_module）为彩色液晶屏，是 NGPC 相较 Neo Geo Pocket（黑白）的标志性识别特征。
- **动画候选**：摇杆状十字键按压、A/B 键按压、卡带插拔、开机启动（动画制作排期挂起）。

## 七、模拟器 / 演示行（NGPC）

- **模拟器**：NeoPop / Mednafen（NGPC 模拟器候选）——许可标 [需核实]；不下载 BIOS/ROM 红线。
- **演示**：**静态 + 卡带插拔 + 按键按压动画**——「插入卡带 → 开机 → 摇杆十字键/A 键操作」。动画制作排期挂起。

## 八、目录方案预告 + BIOS/ROM 红线（NGPC）

- **目录条目**：游戏机目录 `G-HH-000023「Neo Geo Pocket Color」`（SNK、1999、planned）产包时回填 device_id，**无需新建条目**。
- **media_hint**：NGPC 使用 **NGPC 卡带**，schema `media_hint` 枚举有 `cartridge`（卡带有枚举直取，无需降级），产包时**直接取 `cartridge`（预告标注）**。
- **NGPC BIOS/ROM 红线**：NGPC 系统固件与游戏 ROM（卡带）受版权保护，**不入库、不下载**，本卡仅清单级引用；无固件时 `runtime.emulator` 保守 `none`。

---

## 出处清单与 [需核实] 标注（双机共用）

| 出处 | 用途 |
|---|---|
| `console-batch2/26_3DS与PSVita掌机低模样板预研卡.md` | 体例（掌机预研卡母本，双机合卡） |
| `catalog/游戏机与手持大类_目录_v2.jsonl` | 目录实扫：GBC `G-HH-000021` / NGPC `G-HH-000023` |

- 全部尺寸/配色/布局为公开近似值，**均标 [需核实]**；GBC/NGPC 屏幕尺寸、机身尺寸沿用公开资料标 [需核实]；无任何编造史实断言。
- GBC/NGPC BIOS/ROM 受版权保护，**不入库、不下载**，本卡仅清单级引用；无固件时 `runtime.emulator` 保守 `none`。
- 设备包 id `game-boy-color`、`neo-geo-pocket-color` 为**建议命名**，落定须与 02 线目录规范对齐（本卡不登记目录 id）。
- 两部机型 media_hint 均为 `cartridge`（卡带有枚举），已预告标注，产包时直接取用、无需降级。
- 顶点预算：chassis 15 盒＝120 顶点，其余件 13 盒＝104 顶点，均落在低模样板 100–4000 顶点预算内。
