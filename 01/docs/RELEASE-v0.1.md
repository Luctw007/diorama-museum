# RELEASE-v0.1（v0.1 封版发布说明）

> 项目封版版本 **0.1.0**（单一落点：`01/scripts/release_check.py` 的 `PROJECT_RELEASE_VERSION`）。
> 本说明不含任何提交/推送内容；发布由统筹统一收口。

## 一、版本关系

| 版本号 | 含义 | 落点 | 本任务是否改动 |
|---|---|---|---|
| 0.1.0 | 项目封版版本（v0.1 三件套封版） | `scripts/release_check.py` `PROJECT_RELEASE_VERSION` | 新增（单一落点） |
| 0.2.0 | 网关自身版本（随网关代码演进，与发布节奏无关） | `gw/__init__.py` `__version__` | **不改**（只读引用） |
| 2 | 网关协议版本 | `gw/__init__.py` `PROTOCOL_VERSION` | 不改 |

## 二、三件套运行说明

1. **黎明厅实机 + 一台可拆解**：Godot 4.4 打开 `01/godot`（首启手册见 `01/docs/godot_first_boot.md`；包清单自查表见 `01/godot/content/README.md`）；走近设备 → 准星点选（左键）→ **E** 进入拆解视图（滑杆 0..1 分层爆炸）→ **Esc/B** 回到行走/观察。点选修复（RUN-07）待用户实机最终确认。
2. **三台真跑（MAME apple2 / SIMH pdp8 / Stella 2600）**：二进制由用户自备——放 `third_party\mame\mame(.exe)`、`third_party\simh\pdp8(.exe)`、`third_party\stella\stella(.exe)`，或设环境变量 `MAME_BIN` / `SIMH_PDP8_BIN` / `STELLA_BIN`（见 `licenses/MAME.md`、`SIMH.md`、`Stella.md`）。装好后 `python 01/scripts/emulator_doctor.py --fix-check` 一键体检+冒烟，`python 01/scripts/launch_device.py --device apple-ii | pdp8 | atari-2600` 直跑。**当前三后端均为骨架**：无二进制时优雅失败（`EMULATOR_BINARY_MISSING`），装二进制后行为按 `docs/realrun_drill_v3.md` 的 [需核实] 清单逐条核验。
3. **图鉴可用**：Godot 内 **Tab** 打开目录图鉴（Tab 归目录图鉴；设备装载面板改 **F1**），左 28 中分类 → 右「名称·年代·厂商」三列 → 底部详情行；条目排序默认开（同名按年代），可关。

## 三、验收基线

- 冻结快照：`docs/verify_baseline_v0.1.json`（time=2026-11-07 13:18:26，**passed=37 / total=37**）。
- 门禁口径：`python 01/scripts/verify_all.py --daily --cache` → 结果：37/37 通过（30 完工包 + 7 步：m0/m1b/slots/catalog/catalog_ref/gd/gd_naming）。
- 发布自检：`python 01/scripts/release_check.py` → R1/R2/R3 全 PASS、rc=0；`--smoke` 演示帧可再生成（“画廊已生成”+5 帧 PNG）。
- 三台真跑干跑预演：`python 01/scripts/realrun_dryrun.py` → 三台×三步全 PASS（优雅失败链成立）。

## 四、许可清单（均“未见二进制”；细节 [需核实]）

| 组件 | 许可（初查） | 许可记录 | 状态 |
|---|---|---|---|
| MAME（apple2 驱动） | 上游 GPLv2+/BSD-3-Clause 双许可（版本需核实） | `licenses/MAME.md` | 未安装二进制；后端骨架已登记 |
| SIMH（PDP-8） | SIMH 自定许可（允许免费使用与再分发，保留版权声明；分叉或为 MIT）【需核实】 | `licenses/SIMH.md` | 未安装二进制；后端骨架已登记（TASK-161-A） |
| Stella（Atari 2600） | GPL-2.0（具体版本）【需核实】 | `licenses/Stella.md` | 未安装二进制；后端骨架已登记（TASK-161-B） |

GPL 组件一律进程隔离接入（ADR D1），防许可传染；本仓库不随附任何二进制与介质。

## 五、已知需核实清单（汇总，逐条转交）

来源：TASK-161-A/B 完成报告与 `docs/realrun_drill_v3.md` 的 need_verify 清单。

| # | 项 | 出处 | 转交 |
|---|---|---|---|
| 1 | SIMH 启动脚本传参方式/命令名、就绪横幅精确字符串、TTY 注入通道、快照 SAVE/LOAD 命令名 | 161-A | 05 线预研/用户装真二进制后核对 |
| 2 | Stella 启动参数（窗口/无头开关）、帧 rgba8/音频 pcm16 直读 API、键码注入通道、GPL-2.0 具体版本 | 161-B | 05 线/用户核对 |
| 3 | MAME 位图直读 API、natkeyboard 键码映射（need_verify §7 四项） | realrun_drill_v2 §7 | 用户装 MAME 后按 m2a 断言核对 |
| 4 | Stella 键码翻译层：`keys/keymap_atari-2600.json` 为 MAME 语义遗留，Stella 以 runtime.input_map 为语义参照 | 161-B | 05 线/02 线规范对齐 |