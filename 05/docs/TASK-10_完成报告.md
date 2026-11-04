# TASK-10 完成报告 · Apple II 调研定稿 + 内容包正式草稿 + 建模生产 brief

> 任务：TASK-10（续 05 线）· 里程碑 M1 · 完成日期 2026-10-31
> 前置依据：《内容包规范 v0.1》（02 线，经比对 04 线同名文件逐字节一致，采用 v0.1）；`02/repo/tools/validate/validate.py`；`04/repo/docs/design/05_M1测试用例清单.md`；`01/repo/gw/PROTOCOL.md`（协议 v1）。

---

## 一、交付物清单与字数统计

| # | 文件 | 说明 | 汉字数 |
|---|---|---|---|
| 1 | `docs/research/apple-ii/10_定稿决策.md` | 版本拍板、模拟器 8 维对比、授权复核、输入映射对齐、商标登记 | 3116 |
| 2 | `content/apple-ii/meta.json` | DeviceSpec（55 装配体 + 12 元器件 = 67 节点、5 层深） | 2552 |
| 3 | `content/apple-ii/runtime.json` | RuntimeProfile（与 meta.runtime 逐字节等价） | 0（纯键名） |
| 4 | `content/apple-ii/annotations/annotations.json` | 72 条标注（67 role + 3 flow + 2 anim） | 2469 |
| 5 | `content/apple-ii/THIRD_PARTY.md` | 许可清册（原创 5 行 + 来源 10 行） | 491 |
| 6 | `content/apple-ii/meshes/`（4 个 glTF 占位 + MESHES.md） | 机箱/主板/键盘/软驱占位，节点名 = node_id | 345 |
| 7 | `docs/research/apple-ii/11_建模生产brief.md` | 总则 + 67 行条目表 + 详解 + 拆解主轴 | 2574 |
| 8 | `docs/research/apple-ii/12_运行向导文案.md` | FR-E3 五步文案 + 合规解释 + 10 渠道 | 1641 |
| — | `docs/TASK-10_完成报告.md` | 本报告 | — |

**汉字总计（不含本报告）：13188 字**，满足"≥9000 字"下限；分文件下限全部达标（10 号 3116 ≥3000、11 号 2574 ≥2500、12 号 1641 ≥1500）。

**关于 `assemblies.json` 的说明**：任务交付表第 3 项写"`assemblies.json`（或按规范目录结构）"。因《内容包规范 v0.1》§2/§3 规定装配树内嵌于 `meta.json` 的 `assemblies` 字段（无独立 assemblies.json，且校验器 R-001/R-002/R-010~R-013/R-016/R-018 全部从 meta.json 读取），故本包**按规范目录结构**将装配树放入 `meta.json.assemblies`，未另建与规范冲突的独立文件。

---

## 二、validate 运行日志原文 + 迭代记录

**迭代记录**：
- **第 1 轮**：首次生成契约数据后运行，结果为 258 PASS / 0 FAIL，退出码 0。因首轮即全绿，无 FAIL 可修。
- **第 2 轮**：无修改复跑（确定性验证）+ `budget_check.py` 抽查（mainboard.gltf：1 节点、1 三角面，L2 预算内）。结果仍为 258 PASS / 0 FAIL，退出码 0。

> 说明：v0.1 校验策略为降级模式——R-042 面数预算仅统计不阻塞（由 `budget_check.py` 报告）；glTF 为手写单位三角占位（非真实几何），故面数统计为 1，符合"禁止伪造复杂几何"红线。正式网格替换后 `budget_check.py` 才承载真实预算核对。

### 第 1 轮日志原文

```text
PASS  R-001  meta.json                  meta.json 存在且为合法 JSON
PASS  R-002  meta.json                  meta.json 通过 device_spec.schema.json 校验
PASS  R-003  runtime.json               runtime.json 通过 $defs/runtime 校验
PASS  R-004  runtime.json               runtime.json 与 meta.json.runtime 一致
PASS  R-005  annotations/annotations.json annotations.json 通过 $defs/annotations_document 校验
PASS  R-010  -                          所有 parent 引用存在
PASS  R-011  -                          所有 children 引用存在
PASS  R-012  -                          装配树无环
PASS  R-013  -                          parent/children 双向一致
PASS  R-014  -                          所有 component.assembly 引用存在
PASS  R-015  -                          所有 annotation.target 引用存在
PASS  R-016  -                          所有 mesh_ref 文件存在
PASS  R-018  -                          所有 annotations 引用存在
PASS  R-020  meta.id                    device-id 'apple-ii' 符合 kebab-case
PASS  R-021  nodes                      所有节点 id 符合 snake_case
PASS  R-022  annotations/output_sinks   annotation/surface id 符合 snake_case
PASS  R-023  nodes                      节点 id 全局唯一
PASS  R-030  assemblies[apple_ii]       translation 为 3 个有限实数
PASS  R-031  assemblies[apple_ii]       rotation 为单位四元数
PASS  R-032  assemblies[apple_ii]       scale 各分量 > 0
PASS  R-033  assemblies[apple_ii]       scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[case]           translation 为 3 个有限实数
PASS  R-031  assemblies[case]           rotation 为单位四元数
PASS  R-032  assemblies[case]           scale 各分量 > 0
PASS  R-033  assemblies[case]           scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[lid]            translation 为 3 个有限实数
PASS  R-031  assemblies[lid]            rotation 为单位四元数
PASS  R-032  assemblies[lid]            scale 各分量 > 0
PASS  R-033  assemblies[lid]            scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[bottom]         translation 为 3 个有限实数
PASS  R-031  assemblies[bottom]         rotation 为单位四元数
PASS  R-032  assemblies[bottom]         scale 各分量 > 0
PASS  R-033  assemblies[bottom]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[badge]          translation 为 3 个有限实数
PASS  R-031  assemblies[badge]          rotation 为单位四元数
PASS  R-032  assemblies[badge]          scale 各分量 > 0
PASS  R-033  assemblies[badge]          scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[handle]         translation 为 3 个有限实数
PASS  R-031  assemblies[handle]         rotation 为单位四元数
PASS  R-032  assemblies[handle]         scale 各分量 > 0
PASS  R-033  assemblies[handle]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[vent_grille]    translation 为 3 个有限实数
PASS  R-031  assemblies[vent_grille]    rotation 为单位四元数
PASS  R-032  assemblies[vent_grille]    scale 各分量 > 0
PASS  R-033  assemblies[vent_grille]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_supply]   translation 为 3 个有限实数
PASS  R-031  assemblies[power_supply]   rotation 为单位四元数
PASS  R-032  assemblies[power_supply]   scale 各分量 > 0
PASS  R-033  assemblies[power_supply]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[psu_case]       translation 为 3 个有限实数
PASS  R-031  assemblies[psu_case]       rotation 为单位四元数
PASS  R-032  assemblies[psu_case]       scale 各分量 > 0
PASS  R-033  assemblies[psu_case]       scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_switch]   translation 为 3 个有限实数
PASS  R-031  assemblies[power_switch]   rotation 为单位四元数
PASS  R-032  assemblies[power_switch]   scale 各分量 > 0
PASS  R-033  assemblies[power_switch]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[psu_board]      translation 为 3 个有限实数
PASS  R-031  assemblies[psu_board]      rotation 为单位四元数
PASS  R-032  assemblies[psu_board]      scale 各分量 > 0
PASS  R-033  assemblies[psu_board]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_cord]     translation 为 3 个有限实数
PASS  R-031  assemblies[power_cord]     rotation 为单位四元数
PASS  R-032  assemblies[power_cord]     scale 各分量 > 0
PASS  R-033  assemblies[power_cord]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[transformer]    translation 为 3 个有限实数
PASS  R-031  assemblies[transformer]    rotation 为单位四元数
PASS  R-032  assemblies[transformer]    scale 各分量 > 0
PASS  R-033  assemblies[transformer]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[rectifier]      translation 为 3 个有限实数
PASS  R-031  assemblies[rectifier]      rotation 为单位四元数
PASS  R-032  assemblies[rectifier]      scale 各分量 > 0
PASS  R-033  assemblies[rectifier]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[regulator]      translation 为 3 个有限实数
PASS  R-031  assemblies[regulator]      rotation 为单位四元数
PASS  R-032  assemblies[regulator]      scale 各分量 > 0
PASS  R-033  assemblies[regulator]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[output_harness] translation 为 3 个有限实数
PASS  R-031  assemblies[output_harness] rotation 为单位四元数
PASS  R-032  assemblies[output_harness] scale 各分量 > 0
PASS  R-033  assemblies[output_harness] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[keyboard]       translation 为 3 个有限实数
PASS  R-031  assemblies[keyboard]       rotation 为单位四元数
PASS  R-032  assemblies[keyboard]       scale 各分量 > 0
PASS  R-033  assemblies[keyboard]       scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[keycap_array]   translation 为 3 个有限实数
PASS  R-031  assemblies[keycap_array]   rotation 为单位四元数
PASS  R-032  assemblies[keycap_array]   scale 各分量 > 0
PASS  R-033  assemblies[keycap_array]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[keyswitch_array] translation 为 3 个有限实数
PASS  R-031  assemblies[keyswitch_array] rotation 为单位四元数
PASS  R-032  assemblies[keyswitch_array] scale 各分量 > 0
PASS  R-033  assemblies[keyswitch_array] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[keyboard_pcb]   translation 为 3 个有限实数
PASS  R-031  assemblies[keyboard_pcb]   rotation 为单位四元数
PASS  R-032  assemblies[keyboard_pcb]   scale 各分量 > 0
PASS  R-033  assemblies[keyboard_pcb]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[key_encoder]    translation 为 3 个有限实数
PASS  R-031  assemblies[key_encoder]    rotation 为单位四元数
PASS  R-032  assemblies[key_encoder]    scale 各分量 > 0
PASS  R-033  assemblies[key_encoder]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[mainboard]      translation 为 3 个有限实数
PASS  R-031  assemblies[mainboard]      rotation 为单位四元数
PASS  R-032  assemblies[mainboard]      scale 各分量 > 0
PASS  R-033  assemblies[mainboard]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[rom_section]    translation 为 3 个有限实数
PASS  R-031  assemblies[rom_section]    rotation 为单位四元数
PASS  R-032  assemblies[rom_section]    scale 各分量 > 0
PASS  R-033  assemblies[rom_section]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[ram_section]    translation 为 3 个有限实数
PASS  R-031  assemblies[ram_section]    rotation 为单位四元数
PASS  R-032  assemblies[ram_section]    scale 各分量 > 0
PASS  R-033  assemblies[ram_section]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[ram_row_c]      translation 为 3 个有限实数
PASS  R-031  assemblies[ram_row_c]      rotation 为单位四元数
PASS  R-032  assemblies[ram_row_c]      scale 各分量 > 0
PASS  R-033  assemblies[ram_row_c]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[ram_row_d]      translation 为 3 个有限实数
PASS  R-031  assemblies[ram_row_d]      rotation 为单位四元数
PASS  R-032  assemblies[ram_row_d]      scale 各分量 > 0
PASS  R-033  assemblies[ram_row_d]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[ram_row_e]      translation 为 3 个有限实数
PASS  R-031  assemblies[ram_row_e]      rotation 为单位四元数
PASS  R-032  assemblies[ram_row_e]      scale 各分量 > 0
PASS  R-033  assemblies[ram_row_e]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[clock_circuit]  translation 为 3 个有限实数
PASS  R-031  assemblies[clock_circuit]  rotation 为单位四元数
PASS  R-032  assemblies[clock_circuit]  scale 各分量 > 0
PASS  R-033  assemblies[clock_circuit]  scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[video_section]  translation 为 3 个有限实数
PASS  R-031  assemblies[video_section]  rotation 为单位四元数
PASS  R-032  assemblies[video_section]  scale 各分量 > 0
PASS  R-033  assemblies[video_section]  scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[video_ttl_group] translation 为 3 个有限实数
PASS  R-031  assemblies[video_ttl_group] rotation 为单位四元数
PASS  R-032  assemblies[video_ttl_group] scale 各分量 > 0
PASS  R-033  assemblies[video_ttl_group] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[video_connector] translation 为 3 个有限实数
PASS  R-031  assemblies[video_connector] rotation 为单位四元数
PASS  R-032  assemblies[video_connector] scale 各分量 > 0
PASS  R-033  assemblies[video_connector] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[io_section]     translation 为 3 个有限实数
PASS  R-031  assemblies[io_section]     rotation 为单位四元数
PASS  R-032  assemblies[io_section]     scale 各分量 > 0
PASS  R-033  assemblies[io_section]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[cassette_ports] translation 为 3 个有限实数
PASS  R-031  assemblies[cassette_ports] rotation 为单位四元数
PASS  R-032  assemblies[cassette_ports] scale 各分量 > 0
PASS  R-033  assemblies[cassette_ports] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[game_port]      translation 为 3 个有限实数
PASS  R-031  assemblies[game_port]      rotation 为单位四元数
PASS  R-032  assemblies[game_port]      scale 各分量 > 0
PASS  R-033  assemblies[game_port]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_connector] translation 为 3 个有限实数
PASS  R-031  assemblies[power_connector] rotation 为单位四元数
PASS  R-032  assemblies[power_connector] scale 各分量 > 0
PASS  R-033  assemblies[power_connector] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_array]     translation 为 3 个有限实数
PASS  R-031  assemblies[slot_array]     rotation 为单位四元数
PASS  R-032  assemblies[slot_array]     scale 各分量 > 0
PASS  R-033  assemblies[slot_array]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[bus_logic]      translation 为 3 个有限实数
PASS  R-031  assemblies[bus_logic]      rotation 为单位四元数
PASS  R-032  assemblies[bus_logic]      scale 各分量 > 0
PASS  R-033  assemblies[bus_logic]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[decoupling_group] translation 为 3 个有限实数
PASS  R-031  assemblies[decoupling_group] rotation 为单位四元数
PASS  R-032  assemblies[decoupling_group] scale 各分量 > 0
PASS  R-033  assemblies[decoupling_group] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[speaker]        translation 为 3 个有限实数
PASS  R-031  assemblies[speaker]        rotation 为单位四元数
PASS  R-032  assemblies[speaker]        scale 各分量 > 0
PASS  R-033  assemblies[speaker]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[disk_ii]        translation 为 3 个有限实数
PASS  R-031  assemblies[disk_ii]        rotation 为单位四元数
PASS  R-032  assemblies[disk_ii]        scale 各分量 > 0
PASS  R-033  assemblies[disk_ii]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[disk_mech]      translation 为 3 个有限实数
PASS  R-031  assemblies[disk_mech]      rotation 为单位四元数
PASS  R-032  assemblies[disk_mech]      scale 各分量 > 0
PASS  R-033  assemblies[disk_mech]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[disk_platter]   translation 为 3 个有限实数
PASS  R-031  assemblies[disk_platter]   rotation 为单位四元数
PASS  R-032  assemblies[disk_platter]   scale 各分量 > 0
PASS  R-033  assemblies[disk_platter]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[spindle]        translation 为 3 个有限实数
PASS  R-031  assemblies[spindle]        rotation 为单位四元数
PASS  R-032  assemblies[spindle]        scale 各分量 > 0
PASS  R-033  assemblies[spindle]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[read_write_head] translation 为 3 个有限实数
PASS  R-031  assemblies[read_write_head] rotation 为单位四元数
PASS  R-032  assemblies[read_write_head] scale 各分量 > 0
PASS  R-033  assemblies[read_write_head] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[head_coil]      translation 为 3 个有限实数
PASS  R-031  assemblies[head_coil]      rotation 为单位四元数
PASS  R-032  assemblies[head_coil]      scale 各分量 > 0
PASS  R-033  assemblies[head_coil]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[drive_motor]    translation 为 3 个有限实数
PASS  R-031  assemblies[drive_motor]    rotation 为单位四元数
PASS  R-032  assemblies[drive_motor]    scale 各分量 > 0
PASS  R-033  assemblies[drive_motor]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[disk_door]      translation 为 3 个有限实数
PASS  R-031  assemblies[disk_door]      rotation 为单位四元数
PASS  R-032  assemblies[disk_door]      scale 各分量 > 0
PASS  R-033  assemblies[disk_door]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_0]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_0]         rotation 为单位四元数
PASS  R-032  assemblies[slot_0]         scale 各分量 > 0
PASS  R-033  assemblies[slot_0]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_1]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_1]         rotation 为单位四元数
PASS  R-032  assemblies[slot_1]         scale 各分量 > 0
PASS  R-033  assemblies[slot_1]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_2]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_2]         rotation 为单位四元数
PASS  R-032  assemblies[slot_2]         scale 各分量 > 0
PASS  R-033  assemblies[slot_2]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_3]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_3]         rotation 为单位四元数
PASS  R-032  assemblies[slot_3]         scale 各分量 > 0
PASS  R-033  assemblies[slot_3]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_4]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_4]         rotation 为单位四元数
PASS  R-032  assemblies[slot_4]         scale 各分量 > 0
PASS  R-033  assemblies[slot_4]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_5]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_5]         rotation 为单位四元数
PASS  R-032  assemblies[slot_5]         scale 各分量 > 0
PASS  R-033  assemblies[slot_5]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_6]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_6]         rotation 为单位四元数
PASS  R-032  assemblies[slot_6]         scale 各分量 > 0
PASS  R-033  assemblies[slot_6]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_7]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_7]         rotation 为单位四元数
PASS  R-032  assemblies[slot_7]         scale 各分量 > 0
PASS  R-033  assemblies[slot_7]         scale 各分量在 [1e-6, 1e6]
PASS  R-040  meta.precision_level       precision_level=L2 合法
PASS  R-041  assemblies[case]           glTF 可解析（version=2.0）
PASS  R-042  assemblies[case]           预算统计（v0.1 降级）：nodes=1, triangles=1；超限由 budget_check.py 报告，不阻塞（预算数字可调）
PASS  R-041  assemblies[keyboard]       glTF 可解析（version=2.0）
PASS  R-042  assemblies[keyboard]       预算统计（v0.1 降级）：nodes=1, triangles=1；超限由 budget_check.py 报告，不阻塞（预算数字可调）
PASS  R-041  assemblies[mainboard]      glTF 可解析（version=2.0）
PASS  R-042  assemblies[mainboard]      预算统计（v0.1 降级）：nodes=1, triangles=1；超限由 budget_check.py 报告，不阻塞（预算数字可调）
PASS  R-041  assemblies[disk_ii]        glTF 可解析（version=2.0）
PASS  R-042  assemblies[disk_ii]        预算统计（v0.1 降级）：nodes=1, triangles=1；超限由 budget_check.py 报告，不阻塞（预算数字可调）
PASS  R-050  THIRD_PARTY.md             THIRD_PARTY.md 存在
PASS  R-051  THIRD_PARTY.md             第三方资产行均含来源 URL 与获取日期
PASS  R-052  meta.sources               所有 source.url 为 http/https
PASS  R-053  meta.sources               所有 source.license 为四档枚举
PASS  R-054  meta.sources               所有 source.accessed_at 为 YYYY-MM-DD
PASS  R-060  annotations                标注文本不含未定标记
PASS  R-061  role                       role 文案均含「在整机」
PASS  R-062  annotations                role 标注字数 20-200
PASS  R-063  annotations                标注 sources URL 合法
PASS  R-070  meta.version               version='1.0.0' 为合法 semver
PASS  R-071  meta.spec_version          spec_version='0.1' 为 0.1
PASS  R-072  meta.engine_min_version    engine_min_version='0.1.0' 为合法 semver
------------------------------------------------------------------------------
总计 258 条：PASS 258，FAIL 0
```

### 第 2 轮日志原文（复跑确认，尾部）

```text
PASS  R-001  meta.json                  meta.json 存在且为合法 JSON
PASS  R-002  meta.json                  meta.json 通过 device_spec.schema.json 校验
PASS  R-003  runtime.json               runtime.json 通过 $defs/runtime 校验
PASS  R-004  runtime.json               runtime.json 与 meta.json.runtime 一致
PASS  R-005  annotations/annotations.json annotations.json 通过 $defs/annotations_document 校验
PASS  R-010  -                          所有 parent 引用存在
PASS  R-011  -                          所有 children 引用存在
PASS  R-012  -                          装配树无环
PASS  R-013  -                          parent/children 双向一致
PASS  R-014  -                          所有 component.assembly 引用存在
PASS  R-015  -                          所有 annotation.target 引用存在
PASS  R-016  -                          所有 mesh_ref 文件存在
PASS  R-018  -                          所有 annotations 引用存在
PASS  R-020  meta.id                    device-id 'apple-ii' 符合 kebab-case
PASS  R-021  nodes                      所有节点 id 符合 snake_case
PASS  R-022  annotations/output_sinks   annotation/surface id 符合 snake_case
PASS  R-023  nodes                      节点 id 全局唯一
PASS  R-030  assemblies[apple_ii]       translation 为 3 个有限实数
PASS  R-031  assemblies[apple_ii]       rotation 为单位四元数
PASS  R-032  assemblies[apple_ii]       scale 各分量 > 0
PASS  R-033  assemblies[apple_ii]       scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[case]           translation 为 3 个有限实数
PASS  R-031  assemblies[case]           rotation 为单位四元数
PASS  R-032  assemblies[case]           scale 各分量 > 0
PASS  R-033  assemblies[case]           scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[lid]            translation 为 3 个有限实数
PASS  R-031  assemblies[lid]            rotation 为单位四元数
PASS  R-032  assemblies[lid]            scale 各分量 > 0
PASS  R-033  assemblies[lid]            scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[bottom]         translation 为 3 个有限实数
PASS  R-031  assemblies[bottom]         rotation 为单位四元数
PASS  R-032  assemblies[bottom]         scale 各分量 > 0
PASS  R-033  assemblies[bottom]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[badge]          translation 为 3 个有限实数
PASS  R-031  assemblies[badge]          rotation 为单位四元数
PASS  R-032  assemblies[badge]          scale 各分量 > 0
PASS  R-033  assemblies[badge]          scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[handle]         translation 为 3 个有限实数
PASS  R-031  assemblies[handle]         rotation 为单位四元数
PASS  R-032  assemblies[handle]         scale 各分量 > 0
PASS  R-033  assemblies[handle]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[vent_grille]    translation 为 3 个有限实数
PASS  R-031  assemblies[vent_grille]    rotation 为单位四元数
PASS  R-032  assemblies[vent_grille]    scale 各分量 > 0
PASS  R-033  assemblies[vent_grille]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_supply]   translation 为 3 个有限实数
PASS  R-031  assemblies[power_supply]   rotation 为单位四元数
PASS  R-032  assemblies[power_supply]   scale 各分量 > 0
PASS  R-033  assemblies[power_supply]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[psu_case]       translation 为 3 个有限实数
PASS  R-031  assemblies[psu_case]       rotation 为单位四元数
PASS  R-032  assemblies[psu_case]       scale 各分量 > 0
PASS  R-033  assemblies[psu_case]       scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_switch]   translation 为 3 个有限实数
PASS  R-031  assemblies[power_switch]   rotation 为单位四元数
PASS  R-032  assemblies[power_switch]   scale 各分量 > 0
PASS  R-033  assemblies[power_switch]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[psu_board]      translation 为 3 个有限实数
PASS  R-031  assemblies[psu_board]      rotation 为单位四元数
PASS  R-032  assemblies[psu_board]      scale 各分量 > 0
PASS  R-033  assemblies[psu_board]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_cord]     translation 为 3 个有限实数
PASS  R-031  assemblies[power_cord]     rotation 为单位四元数
PASS  R-032  assemblies[power_cord]     scale 各分量 > 0
PASS  R-033  assemblies[power_cord]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[transformer]    translation 为 3 个有限实数
PASS  R-031  assemblies[transformer]    rotation 为单位四元数
PASS  R-032  assemblies[transformer]    scale 各分量 > 0
PASS  R-033  assemblies[transformer]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[rectifier]      translation 为 3 个有限实数
PASS  R-031  assemblies[rectifier]      rotation 为单位四元数
PASS  R-032  assemblies[rectifier]      scale 各分量 > 0
PASS  R-033  assemblies[rectifier]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[regulator]      translation 为 3 个有限实数
PASS  R-031  assemblies[regulator]      rotation 为单位四元数
PASS  R-032  assemblies[regulator]      scale 各分量 > 0
PASS  R-033  assemblies[regulator]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[output_harness] translation 为 3 个有限实数
PASS  R-031  assemblies[output_harness] rotation 为单位四元数
PASS  R-032  assemblies[output_harness] scale 各分量 > 0
PASS  R-033  assemblies[output_harness] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[keyboard]       translation 为 3 个有限实数
PASS  R-031  assemblies[keyboard]       rotation 为单位四元数
PASS  R-032  assemblies[keyboard]       scale 各分量 > 0
PASS  R-033  assemblies[keyboard]       scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[keycap_array]   translation 为 3 个有限实数
PASS  R-031  assemblies[keycap_array]   rotation 为单位四元数
PASS  R-032  assemblies[keycap_array]   scale 各分量 > 0
PASS  R-033  assemblies[keycap_array]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[keyswitch_array] translation 为 3 个有限实数
PASS  R-031  assemblies[keyswitch_array] rotation 为单位四元数
PASS  R-032  assemblies[keyswitch_array] scale 各分量 > 0
PASS  R-033  assemblies[keyswitch_array] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[keyboard_pcb]   translation 为 3 个有限实数
PASS  R-031  assemblies[keyboard_pcb]   rotation 为单位四元数
PASS  R-032  assemblies[keyboard_pcb]   scale 各分量 > 0
PASS  R-033  assemblies[keyboard_pcb]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[key_encoder]    translation 为 3 个有限实数
PASS  R-031  assemblies[key_encoder]    rotation 为单位四元数
PASS  R-032  assemblies[key_encoder]    scale 各分量 > 0
PASS  R-033  assemblies[key_encoder]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[mainboard]      translation 为 3 个有限实数
PASS  R-031  assemblies[mainboard]      rotation 为单位四元数
PASS  R-032  assemblies[mainboard]      scale 各分量 > 0
PASS  R-033  assemblies[mainboard]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[rom_section]    translation 为 3 个有限实数
PASS  R-031  assemblies[rom_section]    rotation 为单位四元数
PASS  R-032  assemblies[rom_section]    scale 各分量 > 0
PASS  R-033  assemblies[rom_section]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[ram_section]    translation 为 3 个有限实数
PASS  R-031  assemblies[ram_section]    rotation 为单位四元数
PASS  R-032  assemblies[ram_section]    scale 各分量 > 0
PASS  R-033  assemblies[ram_section]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[ram_row_c]      translation 为 3 个有限实数
PASS  R-031  assemblies[ram_row_c]      rotation 为单位四元数
PASS  R-032  assemblies[ram_row_c]      scale 各分量 > 0
PASS  R-033  assemblies[ram_row_c]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[ram_row_d]      translation 为 3 个有限实数
PASS  R-031  assemblies[ram_row_d]      rotation 为单位四元数
PASS  R-032  assemblies[ram_row_d]      scale 各分量 > 0
PASS  R-033  assemblies[ram_row_d]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[ram_row_e]      translation 为 3 个有限实数
PASS  R-031  assemblies[ram_row_e]      rotation 为单位四元数
PASS  R-032  assemblies[ram_row_e]      scale 各分量 > 0
PASS  R-033  assemblies[ram_row_e]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[clock_circuit]  translation 为 3 个有限实数
PASS  R-031  assemblies[clock_circuit]  rotation 为单位四元数
PASS  R-032  assemblies[clock_circuit]  scale 各分量 > 0
PASS  R-033  assemblies[clock_circuit]  scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[video_section]  translation 为 3 个有限实数
PASS  R-031  assemblies[video_section]  rotation 为单位四元数
PASS  R-032  assemblies[video_section]  scale 各分量 > 0
PASS  R-033  assemblies[video_section]  scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[video_ttl_group] translation 为 3 个有限实数
PASS  R-031  assemblies[video_ttl_group] rotation 为单位四元数
PASS  R-032  assemblies[video_ttl_group] scale 各分量 > 0
PASS  R-033  assemblies[video_ttl_group] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[video_connector] translation 为 3 个有限实数
PASS  R-031  assemblies[video_connector] rotation 为单位四元数
PASS  R-032  assemblies[video_connector] scale 各分量 > 0
PASS  R-033  assemblies[video_connector] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[io_section]     translation 为 3 个有限实数
PASS  R-031  assemblies[io_section]     rotation 为单位四元数
PASS  R-032  assemblies[io_section]     scale 各分量 > 0
PASS  R-033  assemblies[io_section]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[cassette_ports] translation 为 3 个有限实数
PASS  R-031  assemblies[cassette_ports] rotation 为单位四元数
PASS  R-032  assemblies[cassette_ports] scale 各分量 > 0
PASS  R-033  assemblies[cassette_ports] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[game_port]      translation 为 3 个有限实数
PASS  R-031  assemblies[game_port]      rotation 为单位四元数
PASS  R-032  assemblies[game_port]      scale 各分量 > 0
PASS  R-033  assemblies[game_port]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_connector] translation 为 3 个有限实数
PASS  R-031  assemblies[power_connector] rotation 为单位四元数
PASS  R-032  assemblies[power_connector] scale 各分量 > 0
PASS  R-033  assemblies[power_connector] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_array]     translation 为 3 个有限实数
PASS  R-031  assemblies[slot_array]     rotation 为单位四元数
PASS  R-032  assemblies[slot_array]     scale 各分量 > 0
PASS  R-033  assemblies[slot_array]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[bus_logic]      translation 为 3 个有限实数
PASS  R-031  assemblies[bus_logic]      rotation 为单位四元数
PASS  R-032  assemblies[bus_logic]      scale 各分量 > 0
PASS  R-033  assemblies[bus_logic]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[decoupling_group] translation 为 3 个有限实数
PASS  R-031  assemblies[decoupling_group] rotation 为单位四元数
PASS  R-032  assemblies[decoupling_group] scale 各分量 > 0
PASS  R-033  assemblies[decoupling_group] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[speaker]        translation 为 3 个有限实数
PASS  R-031  assemblies[speaker]        rotation 为单位四元数
PASS  R-032  assemblies[speaker]        scale 各分量 > 0
PASS  R-033  assemblies[speaker]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[disk_ii]        translation 为 3 个有限实数
PASS  R-031  assemblies[disk_ii]        rotation 为单位四元数
PASS  R-032  assemblies[disk_ii]        scale 各分量 > 0
PASS  R-033  assemblies[disk_ii]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[disk_mech]      translation 为 3 个有限实数
PASS  R-031  assemblies[disk_mech]      rotation 为单位四元数
PASS  R-032  assemblies[disk_mech]      scale 各分量 > 0
PASS  R-033  assemblies[disk_mech]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[disk_platter]   translation 为 3 个有限实数
PASS  R-031  assemblies[disk_platter]   rotation 为单位四元数
PASS  R-032  assemblies[disk_platter]   scale 各分量 > 0
PASS  R-033  assemblies[disk_platter]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[spindle]        translation 为 3 个有限实数
PASS  R-031  assemblies[spindle]        rotation 为单位四元数
PASS  R-032  assemblies[spindle]        scale 各分量 > 0
PASS  R-033  assemblies[spindle]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[read_write_head] translation 为 3 个有限实数
PASS  R-031  assemblies[read_write_head] rotation 为单位四元数
PASS  R-032  assemblies[read_write_head] scale 各分量 > 0
PASS  R-033  assemblies[read_write_head] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[head_coil]      translation 为 3 个有限实数
PASS  R-031  assemblies[head_coil]      rotation 为单位四元数
PASS  R-032  assemblies[head_coil]      scale 各分量 > 0
PASS  R-033  assemblies[head_coil]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[drive_motor]    translation 为 3 个有限实数
PASS  R-031  assemblies[drive_motor]    rotation 为单位四元数
PASS  R-032  assemblies[drive_motor]    scale 各分量 > 0
PASS  R-033  assemblies[drive_motor]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[disk_door]      translation 为 3 个有限实数
PASS  R-031  assemblies[disk_door]      rotation 为单位四元数
PASS  R-032  assemblies[disk_door]      scale 各分量 > 0
PASS  R-033  assemblies[disk_door]      scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_0]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_0]         rotation 为单位四元数
PASS  R-032  assemblies[slot_0]         scale 各分量 > 0
PASS  R-033  assemblies[slot_0]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_1]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_1]         rotation 为单位四元数
PASS  R-032  assemblies[slot_1]         scale 各分量 > 0
PASS  R-033  assemblies[slot_1]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_2]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_2]         rotation 为单位四元数
PASS  R-032  assemblies[slot_2]         scale 各分量 > 0
PASS  R-033  assemblies[slot_2]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_3]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_3]         rotation 为单位四元数
PASS  R-032  assemblies[slot_3]         scale 各分量 > 0
PASS  R-033  assemblies[slot_3]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_4]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_4]         rotation 为单位四元数
PASS  R-032  assemblies[slot_4]         scale 各分量 > 0
PASS  R-033  assemblies[slot_4]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_5]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_5]         rotation 为单位四元数
PASS  R-032  assemblies[slot_5]         scale 各分量 > 0
PASS  R-033  assemblies[slot_5]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_6]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_6]         rotation 为单位四元数
PASS  R-032  assemblies[slot_6]         scale 各分量 > 0
PASS  R-033  assemblies[slot_6]         scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[slot_7]         translation 为 3 个有限实数
PASS  R-031  assemblies[slot_7]         rotation 为单位四元数
PASS  R-032  assemblies[slot_7]         scale 各分量 > 0
PASS  R-033  assemblies[slot_7]         scale 各分量在 [1e-6, 1e6]
PASS  R-040  meta.precision_level       precision_level=L2 合法
PASS  R-041  assemblies[case]           glTF 可解析（version=2.0）
PASS  R-042  assemblies[case]           预算统计（v0.1 降级）：nodes=1, triangles=1；超限由 budget_check.py 报告，不阻塞（预算数字可调）
PASS  R-041  assemblies[keyboard]       glTF 可解析（version=2.0）
PASS  R-042  assemblies[keyboard]       预算统计（v0.1 降级）：nodes=1, triangles=1；超限由 budget_check.py 报告，不阻塞（预算数字可调）
PASS  R-041  assemblies[mainboard]      glTF 可解析（version=2.0）
PASS  R-042  assemblies[mainboard]      预算统计（v0.1 降级）：nodes=1, triangles=1；超限由 budget_check.py 报告，不阻塞（预算数字可调）
PASS  R-041  assemblies[disk_ii]        glTF 可解析（version=2.0）
PASS  R-042  assemblies[disk_ii]        预算统计（v0.1 降级）：nodes=1, triangles=1；超限由 budget_check.py 报告，不阻塞（预算数字可调）
PASS  R-050  THIRD_PARTY.md             THIRD_PARTY.md 存在
PASS  R-051  THIRD_PARTY.md             第三方资产行均含来源 URL 与获取日期
PASS  R-052  meta.sources               所有 source.url 为 http/https
PASS  R-053  meta.sources               所有 source.license 为四档枚举
PASS  R-054  meta.sources               所有 source.accessed_at 为 YYYY-MM-DD
PASS  R-060  annotations                标注文本不含未定标记
PASS  R-061  role                       role 文案均含「在整机」
PASS  R-062  annotations                role 标注字数 20-200
PASS  R-063  annotations                标注 sources URL 合法
PASS  R-070  meta.version               version='1.0.0' 为合法 semver
PASS  R-071  meta.spec_version          spec_version='0.1' 为 0.1
PASS  R-072  meta.engine_min_version    engine_min_version='0.1.0' 为合法 semver
------------------------------------------------------------------------------
总计 258 条：PASS 258，FAIL 0
```

---

## 三、定稿决策摘要

**版本**：选定 **Apple II（1977 原版）** 为垂直切片物理模型，运行档 `apple2`（Integer BASIC）为主、`apple2p`（Applesoft）为备。理由：与设计文档 §2.1 一致、一份资产同时覆盖 II/II Plus 两个 ROM 档、机箱曲面最易 1:1 还原、MAME/AppleWin 双模拟器成熟支持。不选 IIe 是为范围控制与叙事纯度，IIe 留待个人机厅阶段复用同一流水线。

**模拟器**：选定 **MAME `apple2`** 为主、AppleWin 为备选与交叉验证/调试工具。决定性因素为跨平台（首发 Win/Linux/macOS）、可脚本化进程控制（与现有 `gw` 网关 stdio 协议同构）、许可同为 GPL-2.0（走 ADR D1 进程隔离）。

**授权**：游戏**绝不内置**任何 ROM/固件/磁盘镜像/商业软件；仅提供合法获取渠道说明与引导文案，并把"我已持有合法文件"设为继续的显式确认。依据 Apple v. Franklin（1983）判例确立的 ROM 版权，及 CHM 获 Apple 授权公开 DOS 源码（非商业）的既有事实。

---

## 四、与 TASK-05 底稿的差异清单

| # | TASK-05 底稿结论 | TASK-10 定稿 | 差异性质 |
|---|---|---|---|
| 1 | 模拟器"建议 MAME + [TBD]" | 明确推荐 MAME，8 维逐维论述 | 细化/强化 |
| 2 | 运行档"apple2 主/apple2p 备" | 保留，并补"一份资产双版本"零成本理由 | 细化 |
| 3 | ROM 授权标"需核实" | 以判例 + CHM 授权公开固化"绝不内置、仅引导" | 推翻"需核实"→ 定稿 |
| 4 | DeviceSpec 草稿按"附录 A"（设计文档示例） | 按《内容包规范 v0.1》正式 Schema + validate 0 FAIL | 升级对齐 |
| 5 | 装配树 46 装配体 + 6 元器件 | 55 装配体 + 12 元器件（67 节点、5 层） | 扩充 |
| 6 | input_map 草案 57 项 | 57 项逻辑动作 + 物理路径格式（keyboard.*/joystick.*）对齐 PROTOCOL.md v1 | 细化/对齐 |
| 7 | transform 用六元组占位 `[0,0,0,0,0,0]` | 按规范改为 `{translation, rotation(四元数), scale}` 对象 | 修正（底稿六元组不符合规范） |

---

## 五、开放问题与「需核实」清单

1. **input_map 键名枚举**：规范 v0.1 §7.3 键名为自定，PROTOCOL.md v1 键名亦为自由字符串；需在规范升版时把通用键名收敛为正式枚举。
2. **运行档默认 ROM**：`apple2` vs `apple2p` 最终取值 `[TBD]` 作者拍板。
3. **商标呈现策略**：历史引用 vs 去商标化，`[TBD 需法律意见]`（FR-J2）。
4. **整机尺寸定值**：两源（S12 15.25×4.25×17.5 in vs S13 38.7×45.7×11.3 cm）宽/深命名与小数位有出入，需实测定值。
5. **键盘编码器型号**：A1026 是否准确待查 S03 原理图。
6. **主板修订**：Rev 0/1 vs Rev 4/7 选定 `[TBD]`。
7. **FCC OET 内部照片**：Apple II 具体 FCC ID 未检索到，需补查。
8. **自备份权利**：各司法辖区"格式转换/备份"例外不一，需按发行辖区核实。
9. **媒体目录约定**：导入目录与文件名规范待 TASK-02 规范媒体目录后对齐。

以上"需核实"项一律未混入 content 正式文案（R-060 校验通过）。

---

## 六、转交输入说明

**转交 01 线（接线/网关）**：
- 新增 `gw/emulators/apple2.py` 后端，遵循 PROTOCOL.md §5 设备通道协议（stdio JSON 行）。
- 复用本包 `runtime.json` 的 `emulator/system/media_hint/bios_required/input_map` 作为启动配置与输入翻译契约。
- 帧回传 `rgb8`、音频 `s16le`，与 TASK-01 彩条帧链路一致，内屏 CRT 投放零改动复用。
- ROM/媒体缺失时上报"未就绪"，前端转入运行向导（对接 E2/E3，测试用例 TC-040~TC-045）。

**转交 09 线（交互）**：
- 运行向导五步界面文案已备齐（12 号文档），可直接落地 UI。
- input_map 57 个逻辑动作作为"输入映射可视化"（测试用例 TC-025/TC-026）的设备侧键位清单。
- 拆解层级/爆炸图展开主轴约定（11 号文档末尾）作为拆解交互（FR-D）的资产坐标依据。

**转交建模生产**：
- `11_建模生产brief.md` 的 67 行条目表 + 详解 + 总则，是资产生产的直接 brief；`content/apple-ii/meshes/` 4 个占位可直接被正式网格同名替换。
