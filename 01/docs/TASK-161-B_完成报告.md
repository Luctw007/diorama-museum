# TASK-161-B 完成报告（Stella 后端模块与全链路登记）

## 交付物清单
- `gw/emulators/stella.py`（新增）：`StellaBackend(BackendBase)`，name=`stella`——`_find_binary()`（STELLA_BIN → third_party/stella/stella(.exe)）；`on_start` 二进制缺失 → `EMULATOR_BINARY_MISSING` + `stopped` + `SystemExit(1)`，否则命令文件 + Popen（仅传卡带路径）；帧（rgba8）/音频（pcm16）通道格式对齐 05 线 runtime.json，但**直读 API 未核实 → 骨架不落帧、不造假数据**（与 mame_apple2 同等诚实）；`on_input` 回显 + 按 input_map 语义（joystick axis/btn、keyboard KEY_*）字面下发记账，**未把 keymap_atari-2600.json 的 MAME 字段当翻译层**（已注释）；快照/停止同骨架；`--check-binary` rc=2/0。
- 四条登记：①`gw/gateway.py` 新增 `stella` 条目（module/binary_env/binary_hint/keymap/GPL-2.0[需核实版本]）；②`slots/emulators/stella/manifest.json`（新增，backend_type=stella、media_classes=[cartridge]）+ `slot_loader.py` `BACKEND_TYPE_MODULE["stella"]`；③`emulator_doctor.py` 新增 `find_stella()`、体检项 `stella_binary`、rom_hints 补 `third_party/roms/a2600/`；④`licenses/Stella.md`（新增，清单级许可记录，GPL-2.0 标需核实）。

## 验收日志（原样）
```
python -m gw.emulators.stella --check-binary
Stella 二进制缺失（third_party/stella/ 或环境变量 STELLA_BIN）
rc=2（echo $LASTEXITCODE = 2，符合预期）
```
`slot_loader.py --list`：`stella  MISSING(无二进制)  Stella（Atari 2600 模拟器…  [GPL-2.0（[需核实具体版本]…]` —— 槽位出现且非"预留"。
`emulator_doctor.py`：`[MISSING] stella_binary third_party\stella\stella(.exe)`、`[MISSING] slot:stella third_party\stella\stella`、`rom_location_hint` 含 a2600；汇总 11 项，rc=0（预期 MISSING 不中断）。
`verify_all.py --daily --cache`：**结果：37/37 通过**；slots 步输出与改动前一致（"完工包 30，声明 slot 0，SC-01 违规 0"）、catalog_ref 步 PASS FAIL 0——回归无破。

## 与任务书的漂移 / 需核实（红线）
- Stella 启动参数、帧/音频直读 API、键码注入通道、GPL-2.0 具体版本——均标 `[需核实]`，转交 05 线/用户装真二进制后核对；
- 未下载任何 Stella 二进制或 2600 ROM（仅清单级引用）；05 线内容包只读未改；未做 git 操作。