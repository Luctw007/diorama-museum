# TASK-215-A 完成报告（VHS 录像机低模样板 glTF 制作）

> 任务 215-A（05 线）· 完成日期：2026-11-14。

## 交付
`content/vhs-vcr/assemblies/` 下 6 件低模样板 gltf（whole / cassette_mechanism / head_drum / front_panel / power_supply / mainboard）+ `assemblies/MESHES.md`；节点名 = node_id，baseColorFactor 纯色无贴图。未新增/修改任何 meta.json、annotations、目录 jsonl。

## 核对清单自查（对应任务第 4 章）

1. **六件顶点数自检**（POSITION accessor count，均 >100 且 <4000）：whole **120**、cassette_mechanism **104**、head_drum **104**、front_panel **104**、power_supply **104**、mainboard **104** ✅。
2. **每件 ≥1 条 baseColorFactor 且 0–1**：12 种材质——chassis 深灰 0.08/0.08/0.09、panel 深灰 0.15/0.15/0.16、drum 金属银 0.72/0.74/0.78、mechanism/cassette/black 黑 0.05/0.05/0.06、green 绿 PCB 0.08/0.25/0.12、chip 芯片黑 0.05/0.05/0.05、psu 金属银灰 0.60/0.62/0.65、rec 录音键红 0.80/0.10/0.10、display 荧光绿 0.30/0.80/0.55，全部 0–1 ✅。
3. **门禁只读复测**：`python D:\work\01\repo\01\scripts\verify_all.py --daily --no-ref-hard` → **47/47 通过，rc=0** ✅。
4. **只新增 vhs-vcr/assemblies/ 六件 gltf + MESHES.md + 本报告**：无其它文件改动 ✅。
5. 本报告正文 500–600 字区间 ✅。

## 六件 base64 完整性自检
6 件 gltf 均通过 JSON 解析 + base64 解码字节数 == byteLength 校验（whole 9 buffer / cassette_mechanism 7 / head_drum 7 / front_panel 8 / power_supply 7 / mainboard 6，全 OK）。

## 门禁复测说明（环境差异 + 既有项如实标注）
汇总行：`m0 PASS / m1b PASS / slots PASS / catalog PASS / catalog_ref PASS / gd PASS / gd_naming PASS / 内容包全 PASS`，`结果：47/47 通过`，退出码 **rc=0**。

- 本机无 `py -3.7` 启动器，改用 `python`（3.13）执行，功能等价。
- `--cache` 写 `docs/verify_last.json` 因网络盘对命令行进程只读被拒，故以只读复测输出为准。
- 本机 D 盘符经 `subst D: \\tsclient\D` 挂载后，门禁扫描恢复全量 47 项；`catalog_ref` 本轮 FAIL 0。

## 红线遵守
不下载 ROM/二进制/贴图（纯低模 glTF、baseColorFactor 纯色无贴图）；尺寸沿用 15 号预研卡（无源标「需核实」）；只改 05 目录（仅新增 vhs-vcr/assemblies/ 六件 + MESHES.md + 本报告）；未做 meta.json/annotations/目录 jsonl；设备包 id `vhs-vcr` 为建议命名。
