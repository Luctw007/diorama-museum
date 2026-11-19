# TASK-211-A 完成报告（第二批 SIMH 启动器参数核对卡 v2）

## 交付物清单
1. `docs/realrun_launch_param_check.md`（改）：新增 **§七 第二批 SIMH 启动器参数核对卡 v2**——hp2100/nova/altair 三台逐项三列核对表（启动参数 / 工作目录 / 键码 TTY 注入 / ROM·介质缺失提示 / 就绪横幅 / 快照 SAVE·LOAD / presmoke 实测），每项标 [已对齐（代码口径）] 或 [需核实]（标出处，不臆造）；三台与 simh_pdp8 母本逐字同构，差异仅 machine/binary_env/binary_hint。
2. need_verify 关联：三台新槽位待核项（start.ini 命令名/横幅/TTY 注入通道/SAVE·LOAD，3×4 项）并入既有续挂清单同一转交口径（05 线预研/用户编译后实跑），不单列计数膨胀；altair 语义名 ALIASES 归一已注。
3. `docs/TASK-211-A_完成报告.md`。

## 验收日志（原样）
1. `verify_all.py --daily --cache` → `catalog_ref PASS FAIL 0`；**结果：46/46 通过** rc=0（apple-iie 反链 210-A 已回填，hard 门禁恢复全绿——211-B 同口径）
2. `release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`
3. 核对卡自证（逐项状态计数）：三台 × 7 项 = 21 格——**[已对齐] 12 格 / [需核实] 9 格**（关键行：三台启动参数均 `cmd=[binary, <start.ini>]` [已对齐（代码口径）] + start.ini 命令名 [需核实]；cwd 三台 [已对齐]；缺失提示三台 [已对齐]（SIMH_*_BIN + third_party/simh/<target>）；横幅与 SAVE·LOAD 三台 [需核实]；presmoke 三台实测 rc=2 + 决策链「未就位 → EMULATOR_BINARY_MISSING」[已对齐]）

## 与任务书的漂移（如实）
1. 三台后端结构逐字同构（201-A/B 以母本复制转正），故核对卡三列高度一致——差异仅在 binary_env/binary_hint/machine，已在表头注明；
2. 任务书未列「就绪横幅」「快照」两行——按 206-A presmoke 卡体例补入（同为真跑前置参数）；
3. 二进制名 hp2100/nova/altair8800 与 start.ini 命令名等推定项全部 [需核实]，无源码/实测支撑处未标 [已对齐]；
4. 未下载/未编译/未启动模拟器、未改 02/03/05 线、未做 git（统筹收口）。