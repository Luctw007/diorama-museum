# TASK-206-A 完成报告（第二批 SIMH presmoke 适配）

## 交付物清单
1. `scripts/realrun_smoke.py`（改——仓库实际 presmoke 入口，无 realrun_presmoke.py，见漂移）：新增 `SIMH_MATRIX`（四台：槽位→后端模块→内容包设备 id）与 `probe_simh_matrix()`：逐台 `--check-binary`（rc=0 就位 / rc=2 缺失均 PASS，打印路径提示）+ 三台新槽位 `launch_device --dry-run` 决策链缺失态断言（EMULATOR_BINARY_MISSING 或 槽位未建立/不在完工包）；汇总文案更新。
2. `scripts/slot_loader.py`（改）：ALIASES 增 `simh-altair8800 → simh-altair-8800`（03 线 runtime 语义名归一）；`resolve_entry()` 支持 manifest 显式 `binary_hint`（决策链缺失态提示指向 third_party 唯一内置定位路径）。
3. 三份 manifest（改）：simh-hp2100/nova/altair 补 `binary_hint: third_party/simh/<hp2100|nova|altair8800>`；`slots/README.md` 字段表补 binary_hint 行。
4. `docs/realrun_launch_param_check.md`（改）：§六「第二批 SIMH presmoke 适配结论」（四台实测 + 二进制名 [需核实] 清单）。
5. `docs/TASK-206-A_完成报告.md`。

## 验收日志（原样）
1. 门禁（hard）→ **44/45**（catalog_ref FAIL 1：REF-02 完工包 apple-iie 无目录反链，他线在制包未回填——非本任务引入；`--no-ref-hard` 降级口径 → **45/45 通过** rc=0）
2. presmoke 四台自证（矩阵段 9 条全 PASS）：
```text
simh-pdp8 --check-binary: SIMH 二进制: …third_party\simh\pdp8.exe   [PASS] rc=0
simh-hp2100 --check-binary: SIMH HP2100 二进制缺失（third_party/simh/hp2100 或环境变量 SIMH_HP2100_BIN） [PASS] rc=2
  决策: 二进制未就位 → EMULATOR_BINARY_MISSING + doctor 指引: 把二进制放入 third_party/simh/hp2100 或设环境变量 SIMH_HP2100_BIN  [PASS] rc=0
simh-nova / simh-altair-8800 同型（third_party/simh/nova|altair8800 · SIMH_NOVA_BIN|SIMH_ALTAIR_BIN）
```
（整体 smoke rc=1 仅因 stella 缺 DLL 的既有 FAIL，与矩阵无关）
3. `release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`

## 与任务书的漂移（如实）
1. 仓库无 `realrun_presmoke.py`（176-A 实际入口为 `realrun_smoke.py`）——按其扩展矩阵段；
2. altair 包 runtime 声明 `simh-altair8800` 与槽位 id 不一致——以 01 侧 ALIASES 归一（[需核实] 建议 03 线统一命名），未改 03 线文件；
3. 三台新槽位原缺 binary_hint 致缺失态提示回退到 `slots/emulators/<id>/`——已补 manifest binary_hint，提示路径与部署手册 §2 一致；
4. 二进制名 hp2100/nova/altair8800 为推定 [需核实]；未下载/未编译/未 Popen；未做 git（统筹收口）。