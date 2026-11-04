# TASK-24A 完成报告（04 线 1/2 · 绑定设置界面规格）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。
> 完成日期：2026-11-02 ｜ 执行线：04 线（全程未修改 01/02/03/05 线文件）

## 1. 交付物与字数统计

| 文件 | 去空白字符数 | 说明 |
|---|---|---|
| `docs/design/14_绑定设置界面规格.md` | 7,077 | 三模式全量表 + 预设模板 + 冲突规则 + 读写映射 |
| `docs/design/15_绑定设置用例.md` | 3,636 | 23 条（T-111~T-133），四要素齐全 |
| `docs/design/02号_增量补丁_绑定设置页.md` | 1,352 | 02 号增量（P1~P5） |
| 合计 | **12,065** | ≥6000 字要求满足（14 号单文件 7,077 亦已达标） |

## 2. 与 01 线 sync_and_profile.md §4 移交事项的逐条回应

| § 条目 | 移交内容 | 14 号回应 | 状态 |
|---|---|---|---|
| §4 ① | 字母/数字：键名同字符（key_a…key_0） | §3.1 字母区渲染与捕捉：绑定串原样显示 `key_a`…`key_0`，捕捉后回填 Godot 小写蛇形 | 已回应 |
| §4 ② | 转盘 paddle_axis_0/1 → 手柄左摇杆 X/Y；双人 paddle_axis_2/3 复用同一摇杆（待玩家设置界面分流） | §3.2 摇杆轴行 + §2.3 apple-ii 行标注「paddle_axis_2/3 复绑同摇杆待分流」，动作行支持逐个重新捕捉实现分流 | 已回应 |
| §4 ③ | paddle_btn_N → 手柄按钮 0/1/2 | §3.2 按钮行：捕捉回填 `joy_button_0~2`，与生成值一致 | 已回应 |
| §4 ④ | 早期面板机（baby/eniac/edsac/edvac）全部 unbound，进设置界面按面板分区绑定 | §2.3 四包全部 unbound 置顶渲染；§4.1 面板分区折叠（含 32 store_bit 四分区）；§4.2 P1/P2 预设；§4.3 edsac 磁带模板 | 已回应 |
| §3 ① | unbound 顶部置顶 | §3.1 列表规则：「unbound 行置顶」，§5 unbound 高亮 + 统计条 | 已回应 |
| §3 ② | baby 引导玩家用「整面板快捷切换」而非逐键绑定 | §4.1 整区绑定 N 连击 + §4.2 三套预设一键套用 | 已回应 |
| §3 ③ | input_profile.gd 三表结构一致性 | §6 读写映射表逐字段对照（只写三表+unbound/note，保持 loader 兼容） | 已回应 |
| §3 ④ | 额外顶层键对 loader 安全 | §2.2 loader 约束条款 + §6 写回文件恒含五键 | 已回应 |
| §5 | 玩家层配置不入内容包规范 / 不改 03 05 源仓 | §6 约定：禁止写 input_map；绑定页只读写 `godot/content/` 副本 | 已回应 |

结论：§4 四条 + §3 四条 + §5 一条共 **9 项移交逐一回应，无遗漏项**。

## 3. 与 01 线字段命名的核对结论表

| 14 号引用 | 01 线实际字段（核对来源） | 一致性 |
|---|---|---|
| `actions` / `keyboard` / `mouse` / `unbound` / `note` | input_profile.gd L36-39 + 五包 JSON 实读 | 一致 |
| 绑定串 `key_w` 小写蛇形 | input_profile.gd 注释 L15 与 apple-ii 档案实值 | 一致 |
| `mouse_button_left` 等 mouse 串 | gen_input_profile.py MOUSE_KEYS（L37-41） | 一致 |
| `joy_axis_x/y`、`joy_button_N`、`joy_hat_N` | gen_input_profile.py JOY_AXIS + btn/hat 分支（L36/L53-61） | 一致 |
| 有空串=unbound 语义 | gen build_profile（L79-86） | 一致 |
| apple-ii 7 actions + 50 keyboard = 57；baby 36 全 unbound（含 32 store_bit） | 五包 JSON 实读 | 一致 |
| edsac 16 动作清单（tape_load/clock_slow…） | edsac input_profile.json 实读 | 一致 |
| 存疑项（`joy_trigger_l/r`、`joy_axis_x+/-` 方向后缀、组合键串、符号键拼写、手柄型号探测） | 01 线无对应实现可核对 | 标 [需实机核对]，见下 §4 |

## 4. 开放问题

1. 组合键「修饰+主键」串 loader 兼容性（14 号 §8.5）——input_profile.gd 暂无组合解析；不支持时 T-130 降级为单键并回填 15 号。
2. 跨设备共享档案是否开放（02 号补丁 P5）——待作者拍板。
3. VR 手势屏桌面预填的保存触发时机（即时保存 vs 出页保存）——14 号定为关闭时自动保存，与设置页其余分页一致。
4. 15 号新增「自动化（Godot 单测）」档类需 08 号档位定义在下轮补一句说明（本轮以 15 号 §首 self-describe 为准）。

## 5. 红线自查

- [x] 不虚构 Godot Control 类名：仅引用 OptionButton/ScrollContainer/VBox/HBox/PopupPanel/PanelContainer/CheckButton/TextureRect/Button/Label（均为引擎既有类）；
- [x] 不确定处全部标 [需实机核对]（14 号 §8 共 6 项，逐条挂接 15 号用例）；
- [x] 字数统计（全量表不缩写）：14 号 9 节表全量、15 号 23 条四要素、补丁 P1~P5——文本合计见附录。

## 附录：三个交付文件字数（PowerShell 去空白口径）

| 文件 | 去空白字符数 |
|---|---|
| 14_绑定设置界面规格.md | 7,077 |
| 15_绑定设置用例.md | 3,636 |
| 02号_增量补丁_绑定设置页.md | 1,352 |
| 合计 | 12,065 |