# TASK-25A 完成报告（Atari 2600 设备包生产 · 游戏机厅首台开产）

> 任务：TASK-25A（05 线 1/2）· 里程碑 M1 · 前置：任务 20（console-batch1 预研兜底）。
> 规范：02 线《内容包规范 v0.2.1》（`meta.spec_version` 仍为 `"0.2"`）。
> 完成日期：2026-11-02。

---

## 一、交付物清单与校验结果

| 文件 | 内容 | 状态 |
|---|---|---|
| `content/atari-2600/meta.json` | DeviceSpec：era=1977、localized、18 装配体 + 5 元器件 + runtime 内嵌 | ✅ |
| `content/atari-2600/runtime.json` | RuntimeProfile：Stella、external_crt 160×192、input_map 12 动作 | ✅ |
| `content/atari-2600/assemblies/*.gltf` | 6 件真实尺寸占位盒（节点名=node_id） | ✅ |
| `content/atari-2600/assemblies/MESHES.md` | 占位网格说明 + 尺寸依据 + 信号域差异 | ✅ |
| `content/atari-2600/annotations/annotations.json` | 28 条标注（23 role + 2 flow + 3 anim） | ✅ |
| `content/atari-2600/encyclopedia.md` | 2551 字（专利诉讼史 / 雅达利冲击 / TIA 声画一体） | ✅ |
| `content/atari-2600/THIRD_PARTY.md` | 四档许可清册（R-091 三件套合法） | ✅ |

**硬件验收**：`python tools/validate/validate.py content/atari-2600` → **总计 128 条：PASS 128，FAIL 0**（退出码 0）。

## 二、尺寸对照表（对照 01_Atari2600.md 档案逐条）

| 参数 | 预研档案（01_Atari2600.md (b)） | 本包实际取值 | 对照结论 |
|---|---|---|---|
| CPU | MOS 6507 @ 1.19 MHz | `component.cpu` part_no=6507 | 一致 |
| 图形/声音芯片 | TIA（CO10444 NTSC / CO11903 PAL） | `component.tia` part_no=CO10444 | 一致（取 NTSC） |
| RAM/IO 芯片 | RIOT 6532（128 字节 RAM） | `component.riot` part_no=6532 | 一致 |
| 分辨率 | 160×192 可见像素（NTSC），128 色 | runtime `external_crt` sink（160×192 游戏分辨率，MESHES.md 注明信号域差异） | 一致（游戏分辨率域） |
| 卡带 | 2 KB / 4 KB ROM，24-pin 卡带槽 | `cart_slot`（24-pin）+ `cartridge`（几何+说明，不涉 ROM） | 一致（红线：不涉 ROM 内容） |
| 手柄 | CX40 摇杆 + 射击键 | input_map `fire`/`joy_*`/`paddle_axis` | 一致 |
| 六开关 | 电源/黑白彩色/选择/复位/左右难度 | `switch_panel` 六子装配体 | 一致 |
| 整机三围 | 预研未定值（`[需核实]`） | 占位盒 0.345×0.092×0.232 m（六开关木纹版近似） | **本包补定值**，见开放问题 |

**装配体尺寸（占位盒，米）**：top_shell 0.345×0.045×0.232 · bottom_shell 0.345×0.047×0.232 · switch_panel 0.345×0.030×0.040 · mainboard 0.300×0.010×0.200 · cart_slot 0.090×0.020×0.060 · cartridge 0.100×0.020×0.070。

## 三、与 Stella 真跑路径衔接说明

本包 runtime 以 **`emulator: "stella"`（version 7.0）** 为技术基线声明（"demo_mode 起步"），当前不接真实二进制。与 Stella 真跑的衔接路径沿用 13 号 MAME 接入预研的"独立进程 + 协议"模式，落点为 01 线网关新增 `stella` 后端：

1. **启动**：网关 spawn Stella 子进程（`stella a2600 ...`），产出首帧后回 `state:running`。
2. **画面**：Stella 输出 160×192 → 网关/后端放大为 2×（320×384）或按需整数倍，转 rgba8 上行，投放到 `external_crt` sink；扫描线伪影为可选后处理（FR-E4）。
3. **输入**：`input_map` 的 joystick（axis_x/axis_y/btn0）→ Stella 手柄映射；keyboard（KEY_POWER/KEY_RESET/KEY_F1~F4）→ 面板开关，由后端翻译层处理（"KEY_* → 键码"，规范 §11.3）。
4. **卡带**：`media_hint=cartridge`，运行时导入玩家自备卡带 ROM（红线：游戏绝不内置），Stella 通过 `-cart` 参数加载。

**Stella 技术基线依据**：Stella 对 TIA 提供 cycle-exact 仿真、覆盖全部 bank switching（预研 01 号 (g)）；许可 GPL-2.0，独立进程分发 = 聚合不传染（ADR D1）。

## 四、开放问题

1. **整机三围定值**：占位盒采用 2600 六开关木纹版公开近似值（0.345×0.092×0.232 m），正式建模前建议实机/工程图复核（延续预研 `04_证据包索引` 的"整机三围 [需核实]"）。
2. **Stella 版本锁定**：runtime 声明 7.0，正式接入时以内容包 `runtime.version` 写死（同 13 号 §三 V18）。
3. **joystick 轴/方向语义**：CX40 为 8 向数字摇杆，本包以 `axis_x/axis_y` 表达方向（value 正负定方向），Stella 后端翻译时需约定方向→轴值映射。
4. **panel 开关键位**：复位/选择/难度/黑白彩色映射到 `KEY_RESET`/`KEY_F1~F4`（F 键为宿主侧临时绑定，正式宿主绑定由 09 线交互规格定）。
5. **R-087 role.en 缺失警告**：23 处 role 未配英文（与 apple-ii V19 同类），非阻塞，正式双语首发前补齐。
