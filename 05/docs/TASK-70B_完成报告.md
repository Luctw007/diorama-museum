# TASK-70B 完成报告（Game Boy 设备包 · 掌机第二台正式入包）

> 任务：TASK-70B（05 线 2/2）· 里程碑 M1 · 与 70-A 共同构成 TASK-70 两份。
> 依据：console-batch2/03_GameBoy.md、09/10 号建模卡与验收清单。
> 完成日期：2026-11-04。

---

## 一、交付物清单与校验结果

| 文件 | 内容 | 状态 |
|---|---|---|
| `content/game-boy/meta.json` | era=1989、localized、7 装配体 + 2 元器件（LR35902/LCD 控制器） | ✅ |
| `content/game-boy/runtime.json` | sameboy 0.16、**handheld_lcd**+speaker+led、input_map 9 动作（十字/AB/Start/Select/power） | ✅ |
| `content/game-boy/assemblies/*.gltf` | 6 件真实尺寸占位盒（前壳屏窗+AB位/后壳电池仓/主板/屏模组/十字键模组/卡带） | ✅ |
| `content/game-boy/annotations/annotations.json` | 32 条（绿点阵屏、俄罗斯方块捆绑、更换卡带生态讲锚） | ✅ |
| `content/game-boy/encyclopedia.md` | 2589 字（手提机第一王朝、横井哲平线、俄罗斯方块捆绑） | ✅ |
| `content/game-boy/THIRD_PARTY.md` | 四档许可清册 | ✅ |

**硬件验收**：`validate.py content/game-boy` → **总计 84 条：PASS 84，FAIL 0**。

## 二、尺寸对照表（对照 09 号建模卡）

| 参数 | 09 号建模卡 | 本包取值 | 对照结论 |
|---|---|---|---|
| CPU | Sharp LR35902 @ 4.19 MHz | `cpu_lr35902` part_no=LR35902 | 一致 |
| 屏幕 | 160×144 点阵 4 级灰度 | runtime `handheld_lcd`（MESHES.md 注明"任务书 91x78 为笔误，以 160×144 为准"） | 一致 |
| 卡带 | 32 针背部插卡 | `cartridge`（几何不涉 ROM） | 一致 |
| 按键 | 十字键 + A/B/Start/Select | input_map hat_0/btn0-1/KEY_ENTER/KEY_RSHIFT | 一致 |
| 电池 | 4 节 AA | `back_shell` 电池仓 | 一致 |
| 前/后壳、屏模组、十字键模组 | 09 号 6 卡 | 6 件 glTF | 一致 |

## 三、与 G&W 的"手持双雄"展呈建议

GB 与 G&W 是任天堂手持线的"双雄"（G&W=段码 LCD 起点，GB=点阵屏巅峰），建议在"手提机破题"专区**并列展示**：

| 维度 | Game & Watch（已建模卡） | Game Boy（本包） |
|---|---|---|
| 显示 | 段码 LCD（预制固定图形） | 点阵屏（160×144 任意画面） |
| 游戏 | 一台一游戏 | 可换卡带，数千款游戏 |
| 叙事 | "够用就好" | "够用且能承载伟大" |

**对比台设计**：两台并列，中间设"显示技术演进"讲解点——G&W 的段码图案 vs GB 的点阵画面，直观呈现"从固定图形到任意画面"的演进。GB 侧设可玩演示（SameBoy 模拟器播《俄罗斯方块》），G&W 侧设段码 LCD 原理讲解，两台共同构成"手提机破题"专区"从起点到巅峰"的完整叙事。

## 四、开放问题

1. **"91x78 像素"笔误**：任务书"屏模组 91x78 像素注记"与 GB 权威规格 160×144 不符，本包以 160×144 为准，已在 MESHES.md 注明。
2. **SameBoy 版本**：runtime 声明 0.16，正式接入以 `runtime.version` 写死。
3. **GB 屏幕两级方案**：点阵屏的"纹理模拟 vs 几何像素网格"两级方案（09 号卡卡片 4），本包屏模组为占位盒，正式建模时按 09 号卡执行。
4. **R-087 role.en 缺失**：11 处 role 未配英文，非阻塞，双语首发前补齐。

## 五、TASK-70 两份总收尾

- **70-A（家电外设目录第二轮）**：`家电影音与外设大类_目录_v2.jsonl/.md`，351 条（≥350），键名迁移英文定稿键、分类路径对齐 62-A 官方树、办公外设大类码按 `P` 码执行；**catalog_check FAIL 0**。
- **70-B（Game Boy 设备包）**：`content/game-boy/`，6 件 glTF + 32 条标注 + 2589 字百科，**validate 84 PASS / 0 FAIL**，掌机第二台正式入包。
- **05 线本轮收尾**：家电影音外设目录完成第二轮（累计 351 条，键名与分类树对齐 57-A/62-A）；Game Boy 正式入包（与 G&W 构成"手持双雄"），游戏机线内容包增至 6 个（2600/FC/MD/SFC/MVS/GB）。
