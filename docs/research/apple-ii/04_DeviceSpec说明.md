# 04 · DeviceSpec 草稿说明（字段依据与「需核实」点）

> 配套文件：`04_DeviceSpec草稿.json`。本文说明每个字段的依据、出处与待对齐项。
> 依据基准：《箱庭电子博物馆初期设计文档 v0.1》附录 A（Schema 示例草案）。《内容包规范 v0.1》（TASK-02）**彼时尚未产出**，故本稿以附录 A 为准，并在 §3 列出待对齐项。

---

## 1. 字段依据说明

| 字段 | 取值 | 依据 / 出处 | 需核实点 |
|---|---|---|---|
| `device_id` | `apple-ii` | 附录 A 示例、设计文档 §2.1 | — |
| `meta.name_zh/name_origin` | Apple II | S01 | — |
| `meta.category` | `personal-computer` | 附录 A 示例 | — |
| `meta.era` | 1977 | S01 | — |
| `meta.manufacturer` | Apple Computer, Inc. | S01 | — |
| `meta.intro` | 百科卡文案 | 02 章 §4 | 发布前人工审查核准 |
| `meta.sources` | S01/S02/S03/S05/S06/S12/S13 | 01 章编号 | 正式入库时替换为真实 URL + 获取日期 |
| `accuracy_level` | `L2+L3` | ADR D4；本机有模拟方案 → L3 | — |
| `root_assembly` | `apple2` | 03 章层级树根 | — |
| `assemblies[].transform` | 全为 `[0,0,0,0,0,0]` 占位 | 附录 A 占位约定 | **需 3D 生产阶段按 1:1 尺寸填真实值** |
| `assemblies[].mesh` | `meshes/<id>.glb` 占位 | D6 管线 | 资产尚未生成，路径为命名占位 |
| `assemblies[].materials` | `materials/*.gdmat` 占位 | D6 | 材质名待定 |
| `assemblies[].annotations` | role/flow | 02 章 §3、FR-C2/C3 | flow 动画资产待 L4 阶段 |
| `components[]` | 6 个明星件 | 03 章 ★ | part_no 待 S03 零件表核实 |
| `runtime.emulator` | `mame`（主） | 05 章选型论证 | **[TBD] 由作者拍板** |
| `runtime.emulator_alt` | `applewin` | 05 章 | [TBD] |
| `runtime.version` | `0.2xx` | 附录 A 占位 | 发布时写死具体版本（内容包 F2 版本依赖） |
| `runtime.system` | `apple2`（主）/ `apple2p`（备） | MAME Driver:Apple II（S07） | [TBD] |
| `runtime.media_hint` | 5.25 软盘 + 磁带 | S01/S12 | 磁带/磁盘二选一由运行档决定 |
| `runtime.bios_required` | `true` | Apple II 需系统 ROM（S15） | 见 05 章授权清单 |
| `runtime.bios_guide_url` | MAME Driver wiki | S07 | 正式文案指向"合法获取引导"（FR-E3） |
| `runtime.output_sinks` | `crt:internal` rgba8 | 附录 A、FR-E4 | 内屏 CRT 效果为可选 |
| `runtime.input_map` | 见 §2 | PROTOCOL.md v1、FR-E6 | 与 TASK-01 对齐（见 §2） |
| `license_register` | `THIRD_PARTY.md` | FR-J3 | 内容包生产时生成 |

---

## 2. input_map 映射草案与对齐说明

### 2.1 键盘（Apple II → 通用键名）

Apple II 为 52 键大写键盘，含 RESET、RETURN、←/→/↑/↓、ESC、CTRL、SHIFT、REPT。通用键名映射（对齐 `gw/PROTOCOL.md` v1 的 `input_event` 的 `map:"keyboard"` + 按键名）：

| Apple II 键 | 通用键名（key） | 备注 |
|---|---|---|
| A–Z | `key_a` … `key_z` | 仅大写 |
| 0–9 | `key_0` … `key_9` | — |
| 空格 | `key_space` | — |
| RETURN | `key_return` | 对应 `enter` 语义 |
| ESC | `key_escape` | — |
| CTRL | `key_ctrl` | — |
| SHIFT | `key_shift` | — |
| REPT | `key_repeat` | 可选 |
| ← / → / ↑ / ↓ | `key_left`/`key_right`/`key_up`/`key_down` | — |
| RESET | `key_reset` | 独立复位键 |

### 2.2 摇杆/手柄（游戏 I/O）

Apple II 游戏接口为模拟摇杆 + 按钮，映射到通用 joystick（对齐 PROTOCOL.md `map:"joystick"`，轴 −1..1 浮点、按钮 bool）：

| Apple II 信号 | 通用（key） | 备注 |
|---|---|---|
| PDL0（摇杆 X） | `joy1_axis_x` | −1..1 |
| PDL1（摇杆 Y） | `joy1_axis_y` | −1..1 |
| 按钮 0 | `joy1_btn0` | bool |
| 按钮 1 | `joy1_btn1` | bool |

### 2.3 对齐要求

- **TASK-01 `gw/PROTOCOL.md`（已产出，协议 v1）**：`input_event` 已支持 `map ∈ {keyboard, mouse, joystick}` 与按键名/轴值。本映射**直接落在该协议内**，无需扩协议；但 v1 尚无"虚拟键 → 设备键"的可视化映射层（FR-E6），该层属 M1 引擎工作，本任务只定义映射表。
- **TASK-02 内容包规范（未产出）**：input_map 的字段结构以附录 A 为准；待 TASK-02 定稿后，需复核 `input_map` 是否要求键名为枚举（否则本稿自由键名需收敛为枚举常量）。
- **待对齐项**：PROTOCOL.md 的键盘键名目前为自由字符串；若后续 MAME/AppleWin 后端需要精确键位码，需在网关后端做一层"通用键名 → 模拟器键码"翻译，本表即为翻译的契约输入。

---

## 3. 与《内容包规范 v0.1》的待对齐清单

| # | 待对齐项 | 说明 |
|---|---|---|
| 1 | `assemblies[].transform` 六元组语义（位置 xyz + 旋转欧拉角？） | 附录 A 未定义顺序，需规范明确 |
| 2 | `components[]` 与 `assemblies[]` 的引用关系（是否用 id 关联） | 本稿用相同 id 关联，需规范确认 |
| 3 | `input_map` 键名是否枚举、是否允许 `key_a` 通配 | 需规范定义 |
| 4 | `runtime.emulator_alt/system_alt` 是否属于规范字段 | 本稿临时扩展，规范定稿后收敛 |
| 5 | `output_sinks[].surface` 取值枚举（`crt:internal` 等） | 需规范定义 sink 类型 |
| 6 | `meta.sources` 是编号还是 URL | 本稿用编号（01 章），正式包建议 URL |

---

## 4. 「需核实」点汇总

1. 尺寸/重量（transform 与建模基准）——见 01 章 §2.1。
2. 键盘编码器型号（A1026 是否准确）——[需核实]。
3. `components[].part_no` 的官方零件号——需 S03 零件表核对。
4. 铭牌/序列号标签图样——缺可引用源（01 章 §4）。
5. `runtime.emulator/system/version`——[TBD] 作者决策 + 发布时写死。
