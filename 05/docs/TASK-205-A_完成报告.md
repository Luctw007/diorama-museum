# TASK-205-A 完成报告（CRT 彩色电视低模样板 glTF 制作）

> 任务 205-A（05 线）· 完成日期：2026-11-14。

## 交付
`content/crt-tv/assemblies/` 下 6 件低模样板 gltf（whole / cabinet / crt_tube / mainboard / tuner_module / control_panel）+ `assemblies/MESHES.md`；节点名 = node_id，baseColorFactor 纯色无贴图。未新增/修改任何 meta.json、annotations、目录 jsonl。

## 核对清单自查（对应任务第 4 章）

1. **六件顶点数自检**（POSITION accessor count，均 >100 且 <4000）：whole **112**、cabinet **112**、crt_tube **112**、mainboard **104**、tuner_module **104**、control_panel **104** ✅。
2. **每件 ≥1 条 baseColorFactor 且 0–1**：10 种材质——wood 木壳棕 0.45/0.32/0.20、darkbrown 深棕 0.25/0.18/0.10、glass 玻璃深灰 0.10/0.10/0.12、crt_dark 玻壳深灰 0.12/0.13/0.14、green 绿 PCB 0.08/0.25/0.12、chip 芯片黑 0.05/0.05/0.05、metal 金属银灰 0.65/0.66/0.68、black 黑塑料 0.05/0.05/0.06、silver 旋钮银 0.72/0.74/0.78、red 指示灯红 0.90/0.20/0.10，全部 0–1 ✅。
3. **门禁只读复测**：`python D:\work\01\repo\01\scripts\verify_all.py --daily --no-ref-hard` → **44/44 通过，rc=0** ✅。
4. **只新增 crt-tv/assemblies/ 六件 gltf + MESHES.md + 本报告**：无其它文件改动 ✅。
5. 本报告正文 500–600 字区间 ✅。

## 六件 base64 完整性自检
6 件 gltf 均通过 JSON 解析 + base64 解码字节数 == byteLength 校验（whole 6 buffer / cabinet 4 / crt_tube 5 / mainboard 5 / tuner_module 6 / control_panel 6，全 OK）。

## 门禁复测说明（环境差异 + 既有项如实标注）
汇总行：`m0 PASS / m1b PASS / slots PASS（完工包 37）/ catalog PASS（24 片 1582 行）/ catalog_ref PASS / gd PASS / gd_naming PASS / 37 个内容包全 PASS`，`结果：44/44 通过`，退出码 **rc=0**。

- 本机无 `py -3.7` 启动器，改用 `python`（3.13）执行，功能等价。
- `--cache` 写 `docs/verify_last.json` 因本机网络盘对命令行进程只读被拒（PermissionError），故以只读复测输出为准。
- `catalog_ref` 存在既有失败「完工包 cdc-6600 无目录反链」（03 线内容包，非本次引入），按脚本官方 TASK-81A 临时开关 `--no-ref-hard` 降级为告警后全 PASS。

## 红线遵守
不下载 ROM/二进制/贴图（纯低模 glTF、baseColorFactor 纯色无贴图）；尺寸沿用 14 号预研卡（无源标「需核实」）；只改 05 目录（仅新增 crt-tv/assemblies/ 六件 + MESHES.md + 本报告）；未做 meta.json/annotations/目录 jsonl；设备包 id `crt-tv` 为建议命名。
