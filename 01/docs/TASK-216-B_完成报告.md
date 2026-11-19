# TASK-216-B 完成报告（第二批 SIMH 真跑矩阵启动器适配）

## 交付物清单
1. 启动器适配（结论：**无需代码改动**）：`launch_lib.py` 的 `decision_chain()` 已泛化（`slot_loader.canonical` + `slots_available()` 合并视图 + 缺失态文案按 entry 的 binary_hint/binary_env 生成），第二批 SIMH 三台（hp2100/nova/altair-8800）经 201-A/B 槽位转正 + 206-A binary_hint/ALIASES 收口后，`launch_device --dry-run` 自动落入与 simh-pdp8 同构的「未就位」分支——本任务以实测三台 dry-run + 登记回写交付，未改启动器代码（避免无谓改动）。
2. 登记回写：`slots/README.md` 新增「launch_device 支持说明」节（三台设备 id → 槽位映射、ALIASES 归一、缺失态分支与实测 rc=0）。
3. `docs/TASK-216-B_完成报告.md`。

## 验收日志（原样）
1. hard 门禁：`verify_all.py --daily --cache` → **结果：47/47 通过** rc=0
2. launch_device dry-run 三台自证（均 rc=0）：
```text
hp-2100          slot 提示: simh-hp2100（media_class=? bios_hint=?）
                 决策: 二进制未就位 → EMULATOR_BINARY_MISSING + doctor 指引: 把二进制放入 third_party/simh/hp2100 或设环境变量 SIMH_HP2100_BIN
data-general-nova slot 提示: simh-nova（…）→ third_party/simh/nova 或 SIMH_NOVA_BIN
altair-8800      slot 提示: simh-altair8800 → simh-altair-8800（ALIASES 归一）
                 → third_party/simh/altair8800 或 SIMH_ALTAIR_BIN
```
3. `release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`

## 与任务书的漂移（如实）
1. 任务书定位「launch_lib.py 适配」：实测启动器族**无需代码改动**（决策链泛化已覆盖），交付转为实测自证 + README 回写——不制造无谓 diff；
2. altair 决策链命中前经 `slot 提示: simh-altair8800 → simh-altair-8800` 别名归一（206-A 收口，[需核实] 建议 03 线统一命名）；
3. 二进制名 hp2100/nova/altair8800 与 start.ini 命令名等推定项仍 [需核实]；三台均为「骨架已接、二进制待用户侧编译」，未臆造就绪；
4. 未下载/未编译/未启动模拟器、未改 02/03/05 线、未做 git（统筹收口）。