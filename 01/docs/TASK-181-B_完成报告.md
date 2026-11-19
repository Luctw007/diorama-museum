# TASK-181-B 完成报告（三台真跑启动器前置参数核对卡）

## 交付物清单
1. `docs/realrun_launch_param_check.md`（新增）：三后端逐项核对卡——启动参数 / 工作目录 / 键码注入参数 / ROM·介质缺失提示路径，每项 `[已对齐]` 或 `[需核实]` 并指向源码行（mame_apple2.py L106-113、simh_pdp8.py L87-90、stella.py L80-86、launch_lib.py:74-77 等）与 presmoke/v3 出处；末节 need_verify 续清单（本轮核销 3 项、续挂 8 项并标转交对象）。
2. `scripts/realrun_launch_check.py`（新增）：免 ROM/零介质/零下载/零联网、**不 Popen 任何真实模拟器**——三设备 `--dry-run`（断言 rc=0 + 「二进制就位/真实后端/slot 提示」）、三后端 `--check-binary`（断言 rc=0 + 路径打印）、doctor 就绪判定行与 rom 提示路径（断言 third_party/roms）；全过 rc=0。
3. `docs/TASK-181-B_完成报告.md`。

## 验收日志（原样）
1. `python .\scripts\realrun_launch_check.py` → 三台第 1 步决策链均 `[PASS]`（原文：`决策: 槽位 mame-apple2 二进制就位（D:\work\01\repo\01\third_party\mame\mame.exe）→ 真实后端（管线待后端实现）`，pdp8/stella 同型）；第 2 步三后端 rc=0 路径打印 `[PASS]`；第 3 步 `[HINT] rom_location_hint ROM 红线：仅提示位置、不自动下载：third_party\roms\apple2\…` + `部署就绪判定：三台真跑二进制 齐 · 介质目录已建 0 个` `[PASS]`；`汇总：三台×N 步，FAIL 0 处`，rc=0
2. 三后端自测：`MAME 二进制: …third_party\mame\mame.exe` rc=0；`SIMH 二进制: …\pdp8.exe` rc=0；`Stella 二进制: …\stella.exe` rc=0
3. 三设备 `--dry-run`：均命中「二进制就位 → 真实后端」（原文同 1，slot 提示行含 `mame → mame-apple2` 等），rc=0
4. 回归：`verify_all.py --daily --cache` → **结果：40/40 通过**（rc=0；中途一次 38/39 系 catalog_ref 瞬时 FAIL 1，独立复跑 FAIL 0 后门禁收敛，他线在写抖动）；`release_check.py` → rc=0

## 与任务书的漂移（如实）
1. 三台 `slot 提示` 行均 `media_class=? bios_hint=?`（运行时映射未带媒体类/BIOS 字段，非本任务改动项；与任务书第 3 章预期「打印 slot 提示」一致）；
2. Stella 无头/抓帧开关、SIMH start.ini 命令名、MAME boot.lua 通道等仍 [需核实]（本轮只核对不修骨架，遵守「不做貌似能跑改动」）；presmoke 核销项（SIMH quit/横幅、MAME -version/createconfig）继续有效；
3. `print_doctor_guide()`（launch_lib.py:141-146）在二进制齐备时仅打印表头与脚注（MISSING 指引只在缺失态出现）——核对卡以 doctor「部署就绪判定：齐」+ rom_location_hint 为证据，已注明。
未下载任何 ROM/介质/二进制；三台二进制只读未动；未做 git（统筹收口）。