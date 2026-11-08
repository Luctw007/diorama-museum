# SLOT Deploy 指南 v0.1 —— 三台真跑用户自装部署手册（终版）

> TASK-171-A · 01 工程线。让用户照本页即插即用自装 v0.1「三台真跑」（MAME apple2 /
> SIMH PDP-8 / Stella Atari 2600）。
> **红线：本手册只讲「放哪、怎么验」，不提供任何获取渠道——二进制与介质一律用户自备
> （任何外部来源站点、获取命令均不在本手册出现）。**

## 0. 总览：装好后一条命令验证

```powershell
cd D:\work\01\repo\01
python .\scripts\emulator_doctor.py            # 体检：三台二进制应为 OK
python .\scripts\emulator_doctor.py --fix-check --log docs\doctor_log.txt   # 齐备后自动冒烟
python .\scripts\emulator_doctor.py --deploy-report docs\deploy_report.json # 落盘部署签字
python .\scripts\launch_device.py --device apple-ii   # 或 pdp8 / atari-2600，直起真跑
```

## 1. 自装三步（装二进制 → 装介质 → 验真跑）

| 步 | 动作 | 目标 |
|---|---|---|
| 1 | 装二进制（§2 唯一内置定位路径或其环境变量覆盖） | `mame_binary / simh_binary / stella_binary` 三项 OK |
| 2 | 装介质（§3 三介质目录，占位自备） | 对应游戏的磁盘/固件/卡带就位 |
| 3 | 验真跑（§5 一键体检与真跑链路） | `--fix-check` 全绿 → `launch_device` 直起 → 按 `realrun_drill_v3.md` need_verify 逐条勾 |

## 2. 三台二进制唯一内置定位路径（与 doctor/gateway 同一口径）

| 模拟器 | 内置路径 | 环境变量覆盖 |
|---|---|---|
| MAME（apple2 驱动） | `third_party\mame\mame(.exe)` | `MAME_BIN` |
| SIMH（PDP-8） | `third_party\simh\pdp8(.exe)` | `SIMH_PDP8_BIN` |
| Stella（Atari 2600） | `third_party\stella\stella(.exe)` | `STELLA_BIN` |

- 三个 `third_party\...` 路径即 `emulator_doctor.py` 的 `find_*` 与网关 `EMULATORS`
  `binary_hint` 的唯一内置口径；二选一即可（路径放文件，或设环境变量指向你的安装位置）。
- `third_party\` 全目录不入版本库（红线防线），放这里的二进制只有你本机可见。
- 版本与启动参数细则标「需核实」：见 `docs/realrun_drill_v3.md` §二 need_verify 清单
  （就绪横幅、启动参数、注入通道等，装真二进制后逐条核对）。

## 3. 三介质目录（占位 · 自备放置）

```
slots\media\disk\computer\mame-apple2\        # apple-ii 磁盘镜像（用户自备）
slots\media\firmware\computer\simh-pdp8\      # PDP-8 磁带/固件镜像（用户自备）
slots\media\cartridge\console\stella\         # Atari 2600 卡带镜像（用户自备）
```

目录只占位用途；介质文件一律自备并放入对应槽位目录，**仓库不代置、不代取**。

## 4. Batocera 式即插即用：新模拟器走 manifest 契约

- 新模拟器 = 在 `slots\emulators\<id>\` 放 `manifest.json`（字段表见 `slots\README.md`：
  slot_id / device_class / backend_type / description / license / binary(可选) /
  binary_env(可选) / media_classes(可选) / keymap(可选)）；
- `scripts\slot_loader.py` 启动即扫描并自动注册（`--list` 查看），
  `emulator_doctor` / `launch_device` 读同一 `slots_available()` 合并视图——**不存在第二套清单**；
- backend_type 与后端模块映射见 `slot_loader.py` `BACKEND_TYPE_MODULE`
  （native/mame/simh/stella 已接；mesen/mobile/dedicated 预留）。

## 5. 一键体检与真跑链路

1. `python .\scripts\emulator_doctor.py` → 人类可读体检表（三态 见 §7）；
   `--json` 机器可读（含 `deploy_readiness`）；`--deploy-report <path>` 落盘签字 JSON；
   `--fix-check` 仅在三台二进制齐备时自动跑 `m2a --mame` + `m0` 冒烟（缺二进制时只提示不跑）。
2. `python .\scripts\launch_device.py --device apple-ii | pdp8 | atari-2600`
   → 决策链自动落在真实后端；`--dry-run` 可先看决策链。
3. 真跑当天按 `docs\realrun_drill_v3.md` §二 need_verify（7 条）逐条勾；
   再用 `python .\scripts\verify_all.py --daily --cache` 收门禁证据。

## 6. 键码表与手柄接入位置

- `gw\emulators\keys\keymap_apple2.json`：MAME apple2 键码表（真跑 need_verify #1-4 对照）；
- `gw\emulators\keys\keymap_atari-2600.json`：**MAME 语义遗留**（mame_field/mame_code），
  Stella 侧以内容包 `runtime.json` 的 `input_map`（joystick axis_x/axis_y/btn*、keyboard KEY_*）
  为语义参照（见 161-B 报告与 `licenses\Stella.md` 接入任务 #4）；
- 手柄/摇杆宿主编排：设备逻辑动作 → 宿主绑定由 `scripts\gen_input_profile.py` 生成骨架
  （`--all --dry-run` 预览），三级回退口径见 `docs\keymap_register.md` §2。

## 7. 排障表

| 现象 | 状态 | 动作 |
|---|---|---|
| `[MISSING] mame_binary …` | 二进制缺失（阻断真跑） | 按 `>>>` 指引放 §2 路径或设对应环境变量后重跑 |
| `[FAIL] gateway_self_test` | 网关自检失败 | 端口 17338 残留：`Get-NetTCPConnection -LocalPort 17338` 清残留进程 |
| `[HINT] rom_location_hint` | 只提示位置 | 自备介质放 §3 目录即可，不阻断 |
| 环境变量设了但不生效 | — | 重新开一个 PowerShell 窗再跑（当前会话未刷新环境变量）；确认变量名完全一致（MAME_BIN/SIMH_PDP8_BIN/STELLA_BIN） |
| `launch_device` 仍报未就位 | — | `slot_loader.py --list` 对照三槽位状态；确认二进制放的是 §2 唯一内置路径（不是 slots\emulators 目录） |
| 装配成功但仍不出画面/不出声 | — | 属后端骨架直读 API 待核实项，按 `realrun_drill_v3.md` need_verify 逐条记录并反馈 01/05 线 |

## 8. 红线声明（与本手册相关）

- 本手册不含任何二进制/ROM/介质的获取渠道与来源站点，**获取一律用户自备**；
- 三台后端当前均为**骨架**：无二进制时优雅失败（`EMULATOR_BINARY_MISSING`），
  装二进制后的行为细节按 `realrun_drill_v3.md` 的「需核实」清单核验，本手册不预告编辑为
  已确认可运行成品；
- 许可：MAME（GPLv2+/BSD-3-Clause 双许可，版本需核实）、SIMH（自定许可，需核实）、
  Stella（GPL-2.0，需核实），详见 `licenses\MAME.md / SIMH.md / Stella.md`；GPL 组件进程隔离接入。