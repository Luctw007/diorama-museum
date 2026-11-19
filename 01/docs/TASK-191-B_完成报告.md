# TASK-191-B 完成报告（真跑 need_verify 续核销 + 第二批槽位表扩展准备）

## 交付物清单
1. `docs/realrun_launch_param_check.md`（改/续）：need_verify 续挂 6 项不变（MAME boot.lua 抓帧生效/键码回显、SIMH start.ini 命令名/TTY 注入/SAVE·LOAD、Stella 无头开关/直读 API/注入通道）；为 Stella 补**绕行/替代方案**三条（补运行库 DLL 后按卡逐项验 / 设 STELLA_BIN 指向完整发行版 / 无头抓帧降级为需用户确认路径），明示「不得臆造就绪」。
2. 槽位表扩展准备：新增 `slots/emulators/simh-hp2100/manifest.json`（`module: null` = reserved 预留，backend_type=simh、device_class=minicomputer、binary_env=SIMH_HP2100_BIN、media_classes=["tape"]）；`scripts/slot_loader.py` 支持 manifest 显式 `module`（null=预留，TASK-191-A 同批落地）；`slots/README.md` 补「manifest 字段补充」节（media_classes 枚举含 none、module 预留语义）。
3. `docs/TASK-191-B_完成报告.md`。

## 验收日志（原样）
1. `python .\01\scripts\verify_all.py --daily --cache` → **结果：42/42 通过**（rc=0；hp-2100 已入完工包 35 台 + 7 步）
2. `python .\01\scripts\realrun_launch_check.py` → `[PASS] 三台共用 第3步 缺失提示路径 rc=0`；`汇总：三台×N 步，FAIL 0 处（全 PASS 则 rc=0）`（rc=0）
3. 槽位登记自证（`slot_loader.py --list` 关键行）：
```text
simh-hp2100   OK(native,无二进制要求)（后端模块预留）  SIMH HP 2100（reserved 预留：后端模块未实现，与 simh-pdp8 同构待接入…）
```
   manifest 原文（关键字段）：`{"slot_id":"simh-hp2100","backend_type":"simh","module":null,"binary_env":"SIMH_HP2100_BIN","media_classes":["tape"],…}`——登记可见、module 为 null（决策链将走「后端模块未实现（预留槽位）」分支），不声称可玩、不下发二进制。
4. need_verify 最新分布：核销 5 项（含 186-B 静态 2 项与更早 presmoke 核销项）；续挂 6 项（MAME 2、SIMH 3、Stella 1，全部标转交对象 + Stella 绕行方案）。

## 与任务书的漂移（如实）
1. `simh-hp2100` 的 backend_type 家族（simh）与后端模块映射（simh_pdp8）冲突——若按家族映射会错误绑定 pdp8 后端；故采用「manifest 显式 `module: null`」预留语义（slot_loader 同批扩展），未新增假的 backend_type 枚举值；
2. `--list` 显示行首「OK(native,无二进制要求)」为既有列表对无 binary_hint 槽位的统称显示，实际语义以 desc「reserved 预留」与 module=null 为准（已在报告/README 注明）；
3. need_verify 本轮无新增核销（Stella 缺 DLL 无法推进），只补绕行方案——按红线不臆造；门禁 41→42/42（他线新包）；未下载/未 Popen/未做 git（统筹收口）。