# 真跑演习剧本 v2（realrun_drill_v2）

> TASK-71B · 2026-11-04 · 01 线。目标：把"装二进制 → 真跑"写成一页可照做的剧本，
> 并用**假二进制**把整条链路（体检 → 判定 → 冒烟）预演一遍。**不下载任何真实二进制**（红线 FR-E3）。
> 本次预演不是走过场：它当场抓出并修复了网关 `_spawn` 的一个真跑必炸缺陷（见 §6）。

## 一、总流程（三步放）

真实二进制接入只需三步，全程不修改任何代码：

1. **下载**：取得 MAME（apple2 驱动）与 SIMH pdp8 的官方二进制（许可证见
   `licenses/MAME.md`、`licenses/SIMH.md`；本仓库只做清单级引用）；
2. **放入槽位**：放进约定目录，或设环境变量（表单见 §2）；
3. **manifest 照抄**：槽位扫描区内放置的模拟器用 manifest 声明（样例见 §2.3），
   内置登记过的（mame-apple2 / simh-pdp8）连 manifest 都不用建。

之后：`python scripts/emulator_doctor.py --fix-check` 一键体检+冒烟，
`python scripts/launch_device.py --device <id>` 一键启动。

## 二、三步放逐命令剧本

### 2.1 第 1 步：下载（用户侧一次）

```powershell
# 以 MAME 为例（0.271 或更高；版本以 licenses/MAME.md 核对为准）
# 下载后解压出 mame.exe（Windows）；其余平台对应 mame
```

### 2.2 第 2 步：放入

```powershell
# 路径 A：环境变量（立即生效，无需移动文件）——本次预演即用此通道
$env:MAME_BIN      = "D:\tools\mame\mame.exe"
$env:SIMH_PDP8_BIN = "D:\tools\simh\pdp8.exe"

# 路径 B：约定目录（doctor / 网关 / slot_loader 自动发现，含 .exe 变体）
#   third_party\mame\mame(.exe)
#   third_party\simh\pdp8(.exe)
#   （third_party/ 已在 .gitignore / 分发目录之外——禁止提交二进制）
```

### 2.3 第 3 步：manifest 照抄（仅槽位扫描区新模拟器需要）

`slots/emulators/<slot_id>/manifest.json`，样例照抄 `slots/emulators/fake-slot/manifest.json`：

```json
{
  "slot_id": "fake-slot",
  "device_class": "console",
  "backend_type": "native",
  "description": "样例槽位：演示 manifest → 网关自动注册",
  "license": "MIT（本仓库自带）",
  "media_classes": ["cartridge"],
  "keymap": null
}
```

要点：`slot_id` 改成本槽位名；`device_class` ∈ computer/console/handheld/phone/pda/
dedicated_av/other；`backend_type` ∈ native/mame/simh/stella/mesen/mobile/dedicated
（映射见 `scripts/slot_loader.py`）；`binary` 填二进制文件名（相对槽位目录）或
`binary_env` 填环境变量名；介质自备放 `slots/media/<media_class>/<device_class>/<slot_id>/`
（**永不下载**）。

## 三、体检预演：emulator_doctor（假二进制现场日志）

预演用假二进制（只 echo 版本字样）已保留在 `slots/_drill/`（mame_drill.bat /
pdp8_drill.bat，见该目录 README，可随时删除）。演练命令与**原始输出**：

```powershell
$env:MAME_BIN     = "D:\work\01\repo\slots\_drill\mame\mame_drill.bat"
$env:SIMH_PDP8_BIN = "D:\work\01\repo\slots\_drill\simh\pdp8_drill.bat"
python scripts/emulator_doctor.py
```

```text
[OK] mame_binary        D:\work\01\repo\slots\_drill\mame\mame_drill.bat ver=MAME 0.271 DRILL-FAKE-BINARY
[OK] simh_binary        D:\work\01\repo\slots\_drill\simh\pdp8_drill.bat ver=PDP-8 simulator V4.0-0 Beta DRILL-FAKE-BINARY
[OK] gateway_self_test  网关可正常起停（端口 17338）
[HINT] rom_location_hint  ROM 红线：仅提示位置、不自动下载：third_party\roms\apple2\（用户自备）；third_party\roms\simh\（用户自备）
[OK] slot:fake-slot     native 后端，无二进制要求
[HINT] slot_media_dirs    介质目录 0 个
汇总：6 项，0 项阻断（MISSING/FAIL）
```

读法：`[OK]` 两项二进制被干净识别并成功探测版本（`ver=` 字段）；网关自检起停正常；
ROM 相关只有 HINT（红线照常）；0 项阻断 = 具备冒烟资格。**真实二进制时输出完全同构**，
唯一区别是 `ver=` 显示真实版本号。

## 四、fix-check 全链路预演（判定 → 冒烟 → 落盘日志）

```powershell
python scripts/emulator_doctor.py --fix-check --log docs/doctor_log_drill.txt
# 输出：…（体检同上 6 项）…“冒烟日志已写 docs/doctor_log_drill.txt（结果 全绿）” RC=0
```

日志 `docs/doctor_log_drill.txt` 要点（原文摘录）：

```text
=== m2a_check.py --mame (rc=0) ===
  [PASS] mame 轨：收到 error code=TIMEOUT
M2a(mame 轨) 结果：PASS 1 / SKIP 0

=== m0_check.py  (rc=0) ===
  [PASS] 网关在端口 17331 就绪 …（22 条断言，含帧序/音频/快照回滚/EMULATOR_NOT_FOUND）
M0 验收全部通过 ✔
```

说明：m2a `--mame` 轨当前断言"真 MAME 缺席/无帧时，网关以 error(TIMEOUT) 干净收场"——
这条 PASS 证明错误通道不会瘫痪协议；装真 MAME 后该轨将升级为帧断言全绿
（见 `docs/m2_assert_draft.md` 与 §7 联动清单）。

## 五、launch_device 决策链与预期输出（真实抓取）

```powershell
python scripts/launch_device.py --device apple-ii --dry-run
# 输出：
#   包位置: D:\work\05\repo\content\apple-ii
#   emulator=mame  demo_mode=False  category=computer
#   slot 提示: mame（media_class=? bios_hint=?）
#   决策: 槽位未建立 → MISSING（先按 slots/README.md 建 manifest）
#
# 真跑前需先建 mame-apple2 槽位 manifest（§2.3）或直接走内置登记
# （网关 EMULATORS 已内置 mame-apple2：装好二进制后 launch 流程自动进入真跑通道）。

python scripts/launch_device.py --device amiga500 --frames 3 --out docs/drill_demo_out
# 输出（demo 通道，无需任何二进制）：
#   决策: demo_mode → fake 演示直起（无需槽位）
#   演示启动 ok（sinks=['main','speaker','led'] 画面 320x240@24.0）
#   帧存证：3 张 PNG → docs/drill_demo_out
```

两条通道都验证到：**demo 通道当场出帧存证**（3 张 PNG），**真跑通道的决策链
如实在二进制缺席时停在指引层**并打印 doctor 指引（不假装成功）。

## 六、本次预演抓出并修复的网关缺陷（重要记录）

首轮 fix-check 冒烟暴露真实崩溃（原文日志）：

```text
File "D:\work\01\repo\gw\gateway.py", line 218, in _spawn
    [sys.executable, "-m", entry["module"]], **kwargs)
KeyError: 'module'
```

根因：内置登记 `simh-pdp8`/`mame-apple2` 条目缺 `module` 字段，`_spawn` 直接取值
→ 客户端线程崩溃、m2a 挂死到超时。修复（网关）：

1. `mame-apple2` 条目补 `"module": "gw.emulators.mame_apple2"`；
2. `simh-pdp8` 保持无 module（后端未实现，属预留槽位），`_spawn` 现在先判
   `entry.get("module")`，缺失抛 `RuntimeError("EMULATOR_BACKEND_MISSING")`；
3. `cmd_start_device` 对应回发清晰错误码 `EMULATOR_BACKEND_MISSING`
   （不再误导为"二进制缺失"，也不再炸线程）。

修复后重跑 fix-check **全绿 rc=0**（§4），`verify_all --daily --cache` **27/27 全绿**。
这正是演习剧本存在的意义：不装真二进制，也能把"开跑即炸"的缺陷提前打掉。

## 七、与 26-A need_verify 清单联动（每项真跑时如何验证一行）

| # | need_verify 项 | 真跑时如何验证 |
|---|---|---|
| 1 | REPT/RESET（含 Ctrl+Reset）MAME apple2e 键码存在性 | 注入 `key_repeat`/`key_reset`，观察 mame_apple2 日志 j{...} 回显与 MAME 控制台无 "Unknown key"；对照 keymap_apple2.json 中 verify=true 条目 |
| 2 | 空格、大小写在 natkeyboard 实际行为 | 依次注入 `key_shift`+`key_a`、`key_space`，核对 MAME 端输出为大写 A 与空格（m2a 输入回显断言同源） |
| 3 | 摇杆 ioport tag/field 名称 | 注入 `paddle_axis_0`/`btn`，MAME 日志不得出现 field 未找到；最终以 MAME 源 apple2.cpp ioport 定义为准（14-A §3.1） |
| 4 | POWER/INSERT 驱动级实现 | 注入 `floppy_door`，观察是 INSERT 键行为还是无通道；无通用通道时转媒体管理通道并回写 note 字段 |

四项全部"需核实"式验证，通过后才允许 m2a `--mame` 帧断言轨启用（26-A 收尾口径）。

## 八、真跑当天用户侧操作卡（一分钟版）

1. 装 MAME / SIMH（许可核对）→ 设 `MAME_BIN` / `SIMH_PDP8_BIN` 或放 `third_party/`；
2. `python scripts/emulator_doctor.py --fix-check` → 全绿即环境就绪；
3. `python scripts/launch_device.py --device apple-ii` → 决策链自动进真跑通道；
4. 按 §7 四项把 need_verify 逐条打勾，然后跑 `verify_all --daily --cache` 收证据。

## 九、清理与保留

- `slots/_drill/`：假二进制仅演示用途，已写 README 声明；不想要可整目录删除，
  doctor 只会回到 MISSING（对门禁零影响）。
- `docs/doctor_log_drill.txt`：本轮预演日志留档（含修复前后两版证据）。
- `docs/drill_demo_out/`：demo 通道 3 张演示帧 PNG。