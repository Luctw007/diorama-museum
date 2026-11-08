# TASK-166-B 完成报告（三台真跑工程预演干跑收口）

## 交付物清单
- `scripts/realrun_dryrun.py`（新增）：内置三台设备表（mame-apple2→apple-ii→gw.emulators.mame_apple2；simh-pdp8→pdp8→gw.emulators.simh_pdp8；stella→atari-2600→gw.emulators.stella）；每台三步断言（①槽位 module 非空且 desc 无「预留」②launch_device --dry-run 含「未就位」与「EMULATOR_BINARY_MISSING」③`python -m <模块> --check-binary` rc=2 且 stdout 含「缺失」）；全过 rc=0，失败指明哪台/第几步/实际输出；零二进制零下载。
- `docs/realrun_drill_v3.md`（新增）：①三台干跑结果表 ②need_verify 收口清单（v2 §7 四项 + 161-A/B 六项，逐条 [需核实] 并标转交对象）③二进制就位后切换点（decision_chain 就位分支 / doctor --fix-check / 真跑通道）。

## 验收日志（原样）
1. `python 01/scripts/realrun_dryrun.py` → 三台×三步共 9 条 `[PASS]`（槽位登记 / 决策链干跑命中「未就位 → EMULATOR_BINARY_MISSING」/ 后端自测 rc=2）；`汇总：三台×三步，FAIL 0 处（全 PASS 则 rc=0）`，$LASTEXITCODE=0
2. 三后端自测（cwd=D:\work\01\repo\01）：
```text
python -m gw.emulators.mame_apple2 --check-binary → MAME 二进制缺失（…）；rc=2
python -m gw.emulators.simh_pdp8 --check-binary  → SIMH 二进制缺失（…）；rc=2
python -m gw.emulators.stella --check-binary    → Stella 二进制缺失（…）；rc=2
```
3. 三条决策链（均落在未就位分支，原文见 v3 剧本表）：
```text
apple-ii     emulator=mame … 决策: 二进制未就位 → EMULATOR_BINARY_MISSING + doctor 指引: … MAME_BIN
pdp8         emulator=simh-pdp8 … 决策: 二进制未就位 → … SIMH_PDP8_BIN
atari-2600   emulator=stella … 决策: 二进制未就位 → … STELLA_BIN
```
4. `verify_all.py --daily --cache` → **结果：37/37 通过**（新增脚本未破坏门禁）
5. `emulator_doctor.py` → 三台二进制均 `[MISSING]`、`slot:mame-apple2|simh-pdp8|stella` 均 MISSING 且无「后端模块预留」、`汇总：11 项，6 项阻断`、rc=0（预期不中断）

## 与任务书的漂移
- 任务书预期三台决策链「二进制未就位 → EMULATOR_BINARY_MISSING + doctor 指引」——实跑三条完全一致（apple-ii 现为 mame → mame-apple2 canonical 后进入未就位分支，与 v2 时代「槽位未建立 → MISSING」不同，属 161 轮落地后的预期变化，已在 v3 剧本注明）。
- 无其他漂移；未下载任何二进制/ROM；03/05 内容包只读未改；未做 git/提交/推送。