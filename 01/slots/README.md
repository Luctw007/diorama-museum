# slots/ —— 模拟器与介质插槽系统（TASK-46A，类 Batocera 体验）

> 把模拟器二进制与介质放入约定目录即可被网关/doctor/门禁自动发现使用。**本仓库永不下载、永不随附真实二进制与介质**（红线 FR-E3），这里只有接口、位置与样例。

## 目录契约

```
slots/
  emulators/<slot_id>/manifest.json     # 槽位声明（schema 由 02 线 v0.5 规范定稿，见 47-A）
  emulators/<slot_id>/<binary 文件>     # 模拟器二进制（可选——纯 native 后端无需二进制）
  media/<media_class>/<device_class>/<slot_id>/   # 介质目录（cartridge/disk/tape/cd/dvd/card/firmware/app_package）
```

## 单一真相源（TASK-76A）

- 一切模拟器经 `slots/emulators/<id>/manifest.json` 声明；网关内置 EMULATORS 仅作
  **最小兜底**（模块/二进制路径/键码表），同名必与槽位 manifest 语义一致（内置优先）。
- 内容包 runtime 的语义名（如 `emulator=mame`）经 `scripts/slot_loader.py` 的
  `canonical()` 映射到规范槽位 id（`mame` → `mame-apple2`、`simh` → `simh-pdp8`）。
- `emulator_doctor` 与 `launch_device` 决策链读的是同一个 `slots_available()`
  合并视图——不存在第二套清单；新模拟器一律走槽位 manifest，不要在别处私藏登记。
- 内置兜底现存三条：`mame-apple2` / `simh-pdp8` / `stella`（后端模块均已登记骨架，
  见 TASK-161-A/B；二进制未装时 start 报 `EMULATOR_BINARY_MISSING`）。

## manifest.json 字段（当前实现版；以 02 线规范 v0.5 为准绳）

| 字段 | 必需 | 说明 |
|---|---|---|
| slot_id | ✓ | 槽位名（= 网关注册键） |
| device_class | ✓ | computer/console/handheld/phone/pda/dedicated_av/other |
| backend_type | ✓ | native/mame/simh/stella/mesen/mobile/dedicated（映射见 scripts/slot_loader.py） |
| description | ✓ | 描述 |
| license | ✓ | 许可说明字符串（三件套详见 v0.5） |
| binary | 可选 | 二进制文件名（相对槽位目录）；缺省=后端无需外部二进制 |
| binary_env | 可选 | 环境变量覆盖名 |
| media_classes | 可选 | 支持的介质类目列表 |
| keymap | 可选 | 键码表路径（默认 keys/keymap_<machine>.json 三级回退不变） |

## 使用三步（以 MAME apple2 为例，其余设备同理）

1. 自备 MAME → 放 `third_party\mame\mame(.exe)`（或设环境变量 `MAME_BIN` 指向安装位置）
   ——这是网关 `binary_hint` 与 `emulator_doctor` 的**唯一内置定位路径**（槽位目录内不放
   二进制；manifest 无需手写，本仓库已带三台真跑的三份 manifest）；
2. 自备介质 → `slots/media/disk/computer/mame-apple2/`；
3. `python scripts/launch_device.py --device apple-ii` —— 自动注册、自动起真跑。
   或 `python scripts/emulator_doctor.py --fix-check` 一键体检+冒烟。
   完整自装手册见 `docs/SLOT_DEPLOY-Guide-v0.1.md`。

## 样例槽位

- `emulators/fake-slot/`：native 后端零二进制样例；`python scripts/slot_loader.py --list`
  应显示该槽位，启动网关后 `start_device{emulator:"fake-slot"}` 等同 fake 后端。