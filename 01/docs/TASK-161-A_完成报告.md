# TASK-161-A 完成报告（SIMH PDP-8 后端模块落地与网关注册）

## 交付物清单
- `gw/emulators/simh_pdp8.py`（新增）：`SimhPdp8Backend(BackendBase)`，name=`simh-pdp8`——`_find_binary()`（SIMH_PDP8_BIN → third_party/simh/pdp8(.exe)）；`on_start` 二进制缺失 → `EMULATOR_BINARY_MISSING` + `stopped(reason=binary_missing)` + `SystemExit(1)`（对齐 mame_apple2），否则临时启动脚本 + 命令文件 + Popen 拉起并抽泵 stdout/stderr；**终端文本流转接、不产帧**（TPY 行只记 stderr 日志，就绪横幅触发 `running`）；`on_input` 回显 input_ack + TTY 文本注入（无 keymap 三级回退，与 mame_apple2 差异已注释）；快照/停止为命令文件写入 + 时间戳记账 + terminate；`--check-binary` 缺失 rc=2/找到 rc=0。
- `gw/gateway.py`（改）：`EMULATORS["simh-pdp8"]` 补 `module: "gw.emulators.simh_pdp8"`（其余字段未动）。
- `scripts/slot_loader.py`（改）：`BACKEND_TYPE_MODULE["simh"] = "gw.emulators.simh_pdp8"`。
- `slots/emulators/simh-pdp8/manifest.json`（改）：描述去掉"后端模块预留"字样。
- `licenses/SIMH.md`（改）：接入任务第 3 条标注"后端模块已落地（骨架，TASK-161-A）"。

## 验收日志（原样）
```
python -m gw.emulators.simh_pdp8 --check-binary
SIMH 二进制缺失（third_party/simh/ 或环境变量 SIMH_PDP8_BIN）
rc=2（echo $LASTEXITCODE = 2，符合预期）
```
`slot_loader.py --list`：`simh-pdp8  MISSING(无二进制)  SIMH PDP-8（需用户提供…` —— 不再带"（后端模块预留）"。
`verify_all.py --daily --cache`：**结果：37/37 通过**（slots 步输出与改动前一致"完工包 30，声明 slot 0，SC-01 违规 0"，rc=0）。
`emulator_doctor.py`（可选增强）：`[MISSING] simh_binary third_party\simh\pdp8(.exe)`、`[MISSING] slot:simh-pdp8 third_party\simh\pdp8`（无"后端模块预留"guide），rc=0 不炸。

## 与任务书的漂移 / 需核实（红线：无来源一律标）
- SIMH 启动脚本传参方式、就绪横幅精确字符串、TTY 注入通道（命令文件轮询 vs stdin 直写）、快照 `SAVE/LOAD` 命令名与回执——全部标 `[需核实]`，转交 05 线/用户装真二进制后核对；
- 未下载任何 SIMH 二进制或 PDP-8 软件镜像（仅清单级引用）；未做 git 操作。