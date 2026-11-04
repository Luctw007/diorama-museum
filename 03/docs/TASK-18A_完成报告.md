# TASK-18A 完成报告：四包 v0.2 迁移清零（03 线）

> 任务：把 03 线 content 下四个包（manchester-baby / eniac / edsac / edvac）全部迁移到 v0.2，
> 在 02 线 v0.2 校验器下 **FAIL 0**。结果：四包全部 **0 FAIL**，校验器退出码均为 0。

## 0. 结论一览

| 包 | 迁移前 FAIL | 迁移后 总计 | PASS | FAIL | 退出码 |
|---|---|---|---|---|---|
| manchester-baby | 12 | 128 | 128 | **0** | 0 |
| eniac | 12 | 92 | 92 | **0** | 0 |
| edsac | 15 | 132 | 132 | **0** | 0 |
| edvac | 12 | 126 | 126 | **0** | 0 |

## 1. 四包 validate 日志（原文）

校验命令：`python <02线>tools/validate/validate.py <包>`（每包以 `content/<device-id>` 为参数）。

### 1.1 manchester-baby

```
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
PASS  R-017  -                          所有 materials 文件存在
PASS  R-018  -                          所有 annotations 引用存在
PASS  R-020  meta.id                    device-id 'manchester-baby' 符合 kebab-case
PASS  R-021  nodes                      所有节点 id 符合 snake_case
PASS  R-022  annotations/output_sinks   annotation/sink id 符合 snake_case
PASS  R-023  nodes                      节点 id 全局唯一
PASS  R-030  assemblies[whole]          translation 为 3 个有限实数
PASS  R-031  assemblies[whole]          rotation 为单位四元数
PASS  R-032  assemblies[whole]          scale 各分量 > 0
PASS  R-033  assemblies[whole]          scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[cabinet]        translation 为 3 个有限实数
PASS  R-031  assemblies[cabinet]        rotation 为单位四元数
PASS  R-032  assemblies[cabinet]        scale 各分量 > 0
PASS  R-033  assemblies[cabinet]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[storage_unit]   translation 为 3 个有限实数
PASS  R-031  assemblies[storage_unit]   rotation 为单位四元数
PASS  R-032  assemblies[storage_unit]   scale 各分量 > 0
PASS  R-033  assemblies[storage_unit]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[control_unit]   translation 为 3 个有限实数
PASS  R-031  assemblies[control_unit]   rotation 为单位四元数
PASS  R-032  assemblies[control_unit]   scale 各分量 > 0
PASS  R-033  assemblies[control_unit]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[arithmetic_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[arithmetic_unit] rotation 为单位四元数
PASS  R-032  assemblies[arithmetic_unit] scale 各分量 > 0
PASS  R-033  assemblies[arithmetic_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[io_unit]        translation 为 3 个有限实数
PASS  R-031  assemblies[io_unit]        rotation 为单位四元数
PASS  R-032  assemblies[io_unit]        scale 各分量 > 0
PASS  R-033  assemblies[io_unit]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_unit]     translation 为 3 个有限实数
PASS  R-031  assemblies[power_unit]     rotation 为单位四元数
PASS  R-032  assemblies[power_unit]     scale 各分量 > 0
PASS  R-033  assemblies[power_unit]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[store_crt_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[store_crt_unit] rotation 为单位四元数
PASS  R-032  assemblies[store_crt_unit] scale 各分量 > 0
PASS  R-033  assemblies[store_crt_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[control_crt_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[control_crt_unit] rotation 为单位四元数
PASS  R-032  assemblies[control_crt_unit] scale 各分量 > 0
PASS  R-033  assemblies[control_crt_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[accumulator_crt_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[accumulator_crt_unit] rotation 为单位四元数
PASS  R-032  assemblies[accumulator_crt_unit] scale 各分量 > 0
PASS  R-033  assemblies[accumulator_crt_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[clock_unit]     translation 为 3 个有限实数
PASS  R-031  assemblies[clock_unit]     rotation 为单位四元数
PASS  R-032  assemblies[clock_unit]     scale 各分量 > 0
PASS  R-033  assemblies[clock_unit]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[sequencer_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[sequencer_unit] rotation 为单位四元数
PASS  R-032  assemblies[sequencer_unit] scale 各分量 > 0
PASS  R-033  assemblies[sequencer_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[subtractor_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[subtractor_unit] rotation 为单位四元数
PASS  R-032  assemblies[subtractor_unit] scale 各分量 > 0
PASS  R-033  assemblies[subtractor_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[switch_panel_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[switch_panel_unit] rotation 为单位四元数
PASS  R-032  assemblies[switch_panel_unit] scale 各分量 > 0
PASS  R-033  assemblies[switch_panel_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[store_crt_board] translation 为 3 个有限实数
PASS  R-031  assemblies[store_crt_board] rotation 为单位四元数
PASS  R-032  assemblies[store_crt_board] scale 各分量 > 0
PASS  R-033  assemblies[store_crt_board] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[control_crt_board] translation 为 3 个有限实数
PASS  R-031  assemblies[control_crt_board] rotation 为单位四元数
PASS  R-032  assemblies[control_crt_board] scale 各分量 > 0
PASS  R-033  assemblies[control_crt_board] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[accumulator_crt_board] translation 为 3 个有限实数
PASS  R-031  assemblies[accumulator_crt_board] rotation 为单位四元数
PASS  R-032  assemblies[accumulator_crt_board] scale 各分量 > 0
PASS  R-033  assemblies[accumulator_crt_board] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[subtractor_board] translation 为 3 个有限实数
PASS  R-031  assemblies[subtractor_board] rotation 为单位四元数
PASS  R-032  assemblies[subtractor_board] scale 各分量 > 0
PASS  R-033  assemblies[subtractor_board] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[switch_board]   translation 为 3 个有限实数
PASS  R-031  assemblies[switch_board]   rotation 为单位四元数
PASS  R-032  assemblies[switch_board]   scale 各分量 > 0
PASS  R-033  assemblies[switch_board]   scale 各分量在 [1e-6, 1e6]
PASS  R-040  meta.precision_level       precision_level=L2 合法
PASS  R-041  assemblies[whole]          glTF 可解析（version=2.0）
PASS  R-042  assemblies[whole]          预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[cabinet]        glTF 可解析（version=2.0）
PASS  R-042  assemblies[cabinet]        预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[store_crt_unit] glTF 可解析（version=2.0）
PASS  R-042  assemblies[store_crt_unit] 预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[switch_panel_unit] glTF 可解析（version=2.0）
PASS  R-042  assemblies[switch_panel_unit] 预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-050  THIRD_PARTY.md             THIRD_PARTY.md 存在
PASS  R-051  THIRD_PARTY.md             第三方资产行均含来源 URL 与获取日期
PASS  R-052  meta.sources               所有 source.url 为 http/https
PASS  R-053  meta.sources               所有 source.license 为四档枚举
PASS  R-054  meta.sources               所有 source.accessed_at 为 YYYY-MM-DD
PASS  R-060  annotations                标注文本不含未定标记
PASS  R-061  role                       role 文案均含「在整机」
PASS  R-062  annotations                role 标注字数 20-200
PASS  R-063  annotations                标注 sources URL 合法
PASS  R-070  meta.version               version='1.1.0' 为合法 semver
PASS  R-071  meta.spec_version          spec_version='0.2' 为 0.2
PASS  R-072  meta.engine_min_version    engine_min_version='0.1.0' 为合法 semver
PASS  R-080  annotations.timeline       timeline 结构合法
PASS  R-080  annotations.timeline       timeline highlight 引用存在
PASS  R-081  annotations.timeline       timeline 总时长≤预算(180s)
PASS  R-082  annotations.timeline       C4 级 anim 每镜头 caption 齐全
PASS  R-083  annotations.timeline       caption 无未定标记
PASS  R-084  runtime.output_sinks       sink surface 为命名枚举
PASS  R-085  annotations                annotation.surface 均已声明
PASS  R-086  runtime.input_map          input_map 键名合法；legacy 字符串形式 36 项（建议迁移结构化）
PASS  R-087  localized                  localized 结构完整；警告：以下字段缺 en（回退 zh）：['assembly.whole.role', 'assembly.cabinet.role', 'assembly.storage_unit.role', 'assembly.control_unit.role', 'assembly.arithmetic_unit.role', 'assembly.io_unit.role', 'assembly.power_unit.role', 'assembly.store_crt_unit.role', 'assembly.control_crt_unit.role', 'assembly.accumulator_crt_unit.role', 'assembly.clock_unit.role', 'assembly.sequencer_unit.role', 'assembly.subtractor_unit.role', 'assembly.switch_panel_unit.role', 'assembly.store_crt_board.role', 'assembly.control_crt_board.role', 'assembly.accumulator_crt_board.role', 'assembly.subtractor_board.role', 'assembly.switch_board.role', 'component.williams_tube.role', 'component.store_crt_screen.role', 'component.store_electron_gun.role', 'component.control_crt_screen.role', 'component.accumulator_crt_screen.role', 'component.subtractor_valve.role', 'component.clock_oscillator.role', 'component.sequencer_relay.role', 'component.toggle_switch.role', 'component.push_button.role', 'component.power_transformer.role']
PASS  R-088  meta.name_en               无 deprecated name_en（已迁移）
PASS  R-089  meta.era                   未填 era（可选）
PASS  R-090  gltf                       glTF 网格节点名与 node_id 对应
PASS  R-091  THIRD_PARTY.md             THIRD_PARTY 行三件套（分档+URL+日期）合法
------------------------------------------------------------------------------
总计 128 条：PASS 128，FAIL 0

```

### 1.2 eniac

```
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
PASS  R-017  -                          所有 materials 文件存在
PASS  R-018  -                          所有 annotations 引用存在
PASS  R-020  meta.id                    device-id 'eniac' 符合 kebab-case
PASS  R-021  nodes                      所有节点 id 符合 snake_case
PASS  R-022  annotations/output_sinks   annotation/sink id 符合 snake_case
PASS  R-023  nodes                      节点 id 全局唯一
PASS  R-030  assemblies[whole]          translation 为 3 个有限实数
PASS  R-031  assemblies[whole]          rotation 为单位四元数
PASS  R-032  assemblies[whole]          scale 各分量 > 0
PASS  R-033  assemblies[whole]          scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[cabinet]        translation 为 3 个有限实数
PASS  R-031  assemblies[cabinet]        rotation 为单位四元数
PASS  R-032  assemblies[cabinet]        scale 各分量 > 0
PASS  R-033  assemblies[cabinet]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_unit]     translation 为 3 个有限实数
PASS  R-031  assemblies[power_unit]     rotation 为单位四元数
PASS  R-032  assemblies[power_unit]     scale 各分量 > 0
PASS  R-033  assemblies[power_unit]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[accumulator_bank] translation 为 3 个有限实数
PASS  R-031  assemblies[accumulator_bank] rotation 为单位四元数
PASS  R-032  assemblies[accumulator_bank] scale 各分量 > 0
PASS  R-033  assemblies[accumulator_bank] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[accumulator_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[accumulator_unit] rotation 为单位四元数
PASS  R-032  assemblies[accumulator_unit] scale 各分量 > 0
PASS  R-033  assemblies[accumulator_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[function_table_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[function_table_unit] rotation 为单位四元数
PASS  R-032  assemblies[function_table_unit] scale 各分量 > 0
PASS  R-033  assemblies[function_table_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[multiplier_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[multiplier_unit] rotation 为单位四元数
PASS  R-032  assemblies[multiplier_unit] scale 各分量 > 0
PASS  R-033  assemblies[multiplier_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[divider_unit]   translation 为 3 个有限实数
PASS  R-031  assemblies[divider_unit]   rotation 为单位四元数
PASS  R-032  assemblies[divider_unit]   scale 各分量 > 0
PASS  R-033  assemblies[divider_unit]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[master_programmer_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[master_programmer_unit] rotation 为单位四元数
PASS  R-032  assemblies[master_programmer_unit] scale 各分量 > 0
PASS  R-033  assemblies[master_programmer_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[io_unit]        translation 为 3 个有限实数
PASS  R-031  assemblies[io_unit]        rotation 为单位四元数
PASS  R-032  assemblies[io_unit]        scale 各分量 > 0
PASS  R-033  assemblies[io_unit]        scale 各分量在 [1e-6, 1e6]
PASS  R-040  meta.precision_level       precision_level=L2 合法
PASS  R-041  assemblies[whole]          glTF 可解析（version=2.0）
PASS  R-042  assemblies[whole]          预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[accumulator_unit] glTF 可解析（version=2.0）
PASS  R-042  assemblies[accumulator_unit] 预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[function_table_unit] glTF 可解析（version=2.0）
PASS  R-042  assemblies[function_table_unit] 预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[master_programmer_unit] glTF 可解析（version=2.0）
PASS  R-042  assemblies[master_programmer_unit] 预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-050  THIRD_PARTY.md             THIRD_PARTY.md 存在
PASS  R-051  THIRD_PARTY.md             第三方资产行均含来源 URL 与获取日期
PASS  R-052  meta.sources               所有 source.url 为 http/https
PASS  R-053  meta.sources               所有 source.license 为四档枚举
PASS  R-054  meta.sources               所有 source.accessed_at 为 YYYY-MM-DD
PASS  R-060  annotations                标注文本不含未定标记
PASS  R-061  role                       role 文案均含「在整机」
PASS  R-062  annotations                role 标注字数 20-200
PASS  R-063  annotations                标注 sources URL 合法
PASS  R-070  meta.version               version='1.1.0' 为合法 semver
PASS  R-071  meta.spec_version          spec_version='0.2' 为 0.2
PASS  R-072  meta.engine_min_version    engine_min_version='0.1.0' 为合法 semver
PASS  R-080  annotations.timeline       timeline 结构合法
PASS  R-080  annotations.timeline       timeline highlight 引用存在
PASS  R-081  annotations.timeline       timeline 总时长≤预算(180s)
PASS  R-082  annotations.timeline       C4 级 anim 每镜头 caption 齐全
PASS  R-083  annotations.timeline       caption 无未定标记
PASS  R-084  runtime.output_sinks       sink surface 为命名枚举
PASS  R-085  annotations                annotation.surface 均已声明
PASS  R-086  runtime.input_map          input_map 键名合法；legacy 字符串形式 4 项（建议迁移结构化）
PASS  R-087  localized                  localized 结构完整；警告：以下字段缺 en（回退 zh）：['assembly.whole.role', 'assembly.cabinet.role', 'assembly.power_unit.role', 'assembly.accumulator_bank.role', 'assembly.accumulator_unit.role', 'assembly.function_table_unit.role', 'assembly.multiplier_unit.role', 'assembly.divider_unit.role', 'assembly.master_programmer_unit.role', 'assembly.io_unit.role', 'component.decade_ring.role', 'component.pulse_circuit.role', 'component.neon_lamp.role', 'component.tube_socket.role']
PASS  R-088  meta.name_en               无 deprecated name_en（已迁移）
PASS  R-089  meta.era                   未填 era（可选）
PASS  R-090  gltf                       glTF 网格节点名与 node_id 对应
PASS  R-091  THIRD_PARTY.md             THIRD_PARTY 行三件套（分档+URL+日期）合法
------------------------------------------------------------------------------
总计 92 条：PASS 92，FAIL 0

```

### 1.3 edsac

```
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
PASS  R-017  -                          所有 materials 文件存在
PASS  R-018  -                          所有 annotations 引用存在
PASS  R-020  meta.id                    device-id 'edsac' 符合 kebab-case
PASS  R-021  nodes                      所有节点 id 符合 snake_case
PASS  R-022  annotations/output_sinks   annotation/sink id 符合 snake_case
PASS  R-023  nodes                      节点 id 全局唯一
PASS  R-030  assemblies[whole]          translation 为 3 个有限实数
PASS  R-031  assemblies[whole]          rotation 为单位四元数
PASS  R-032  assemblies[whole]          scale 各分量 > 0
PASS  R-033  assemblies[whole]          scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[cabinet]        translation 为 3 个有限实数
PASS  R-031  assemblies[cabinet]        rotation 为单位四元数
PASS  R-032  assemblies[cabinet]        scale 各分量 > 0
PASS  R-033  assemblies[cabinet]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[memory_subsystem] translation 为 3 个有限实数
PASS  R-031  assemblies[memory_subsystem] rotation 为单位四元数
PASS  R-032  assemblies[memory_subsystem] scale 各分量 > 0
PASS  R-033  assemblies[memory_subsystem] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[control_subsystem] translation 为 3 个有限实数
PASS  R-031  assemblies[control_subsystem] rotation 为单位四元数
PASS  R-032  assemblies[control_subsystem] scale 各分量 > 0
PASS  R-033  assemblies[control_subsystem] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[arithmetic_subsystem] translation 为 3 个有限实数
PASS  R-031  assemblies[arithmetic_subsystem] rotation 为单位四元数
PASS  R-032  assemblies[arithmetic_subsystem] scale 各分量 > 0
PASS  R-033  assemblies[arithmetic_subsystem] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[io_subsystem]   translation 为 3 个有限实数
PASS  R-031  assemblies[io_subsystem]   rotation 为单位四元数
PASS  R-032  assemblies[io_subsystem]   scale 各分量 > 0
PASS  R-033  assemblies[io_subsystem]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[display_subsystem] translation 为 3 个有限实数
PASS  R-031  assemblies[display_subsystem] rotation 为单位四元数
PASS  R-032  assemblies[display_subsystem] scale 各分量 > 0
PASS  R-033  assemblies[display_subsystem] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_unit]     translation 为 3 个有限实数
PASS  R-031  assemblies[power_unit]     rotation 为单位四元数
PASS  R-032  assemblies[power_unit]     scale 各分量 > 0
PASS  R-033  assemblies[power_unit]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[delay_line_bank] translation 为 3 个有限实数
PASS  R-031  assemblies[delay_line_bank] rotation 为单位四元数
PASS  R-032  assemblies[delay_line_bank] scale 各分量 > 0
PASS  R-033  assemblies[delay_line_bank] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[recirculation_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[recirculation_unit] rotation 为单位四元数
PASS  R-032  assemblies[recirculation_unit] scale 各分量 > 0
PASS  R-033  assemblies[recirculation_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[clock_unit]     translation 为 3 个有限实数
PASS  R-031  assemblies[clock_unit]     rotation 为单位四元数
PASS  R-032  assemblies[clock_unit]     scale 各分量 > 0
PASS  R-033  assemblies[clock_unit]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[sequence_unit]  translation 为 3 个有限实数
PASS  R-031  assemblies[sequence_unit]  rotation 为单位四元数
PASS  R-032  assemblies[sequence_unit]  scale 各分量 > 0
PASS  R-033  assemblies[sequence_unit]  scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[decoder_unit]   translation 为 3 个有限实数
PASS  R-031  assemblies[decoder_unit]   rotation 为单位四元数
PASS  R-032  assemblies[decoder_unit]   scale 各分量 > 0
PASS  R-033  assemblies[decoder_unit]   scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[accumulator_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[accumulator_unit] rotation 为单位四元数
PASS  R-032  assemblies[accumulator_unit] scale 各分量 > 0
PASS  R-033  assemblies[accumulator_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[multiplier_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[multiplier_unit] rotation 为单位四元数
PASS  R-032  assemblies[multiplier_unit] scale 各分量 > 0
PASS  R-033  assemblies[multiplier_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[tape_reader_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[tape_reader_unit] rotation 为单位四元数
PASS  R-032  assemblies[tape_reader_unit] scale 各分量 > 0
PASS  R-033  assemblies[tape_reader_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[teleprinter_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[teleprinter_unit] rotation 为单位四元数
PASS  R-032  assemblies[teleprinter_unit] scale 各分量 > 0
PASS  R-033  assemblies[teleprinter_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[crt_display_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[crt_display_unit] rotation 为单位四元数
PASS  R-032  assemblies[crt_display_unit] scale 各分量 > 0
PASS  R-033  assemblies[crt_display_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[delay_tank_board] translation 为 3 个有限实数
PASS  R-031  assemblies[delay_tank_board] rotation 为单位四元数
PASS  R-032  assemblies[delay_tank_board] scale 各分量 > 0
PASS  R-033  assemblies[delay_tank_board] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[adder_board]    translation 为 3 个有限实数
PASS  R-031  assemblies[adder_board]    rotation 为单位四元数
PASS  R-032  assemblies[adder_board]    scale 各分量 > 0
PASS  R-033  assemblies[adder_board]    scale 各分量在 [1e-6, 1e6]
PASS  R-040  meta.precision_level       precision_level=L2 合法
PASS  R-041  assemblies[whole]          glTF 可解析（version=2.0）
PASS  R-042  assemblies[whole]          预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[control_subsystem] glTF 可解析（version=2.0）
PASS  R-042  assemblies[control_subsystem] 预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[delay_line_bank] glTF 可解析（version=2.0）
PASS  R-042  assemblies[delay_line_bank] 预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[crt_display_unit] glTF 可解析（version=2.0）
PASS  R-042  assemblies[crt_display_unit] 预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-050  THIRD_PARTY.md             THIRD_PARTY.md 存在
PASS  R-051  THIRD_PARTY.md             第三方资产行均含来源 URL 与获取日期
PASS  R-052  meta.sources               所有 source.url 为 http/https
PASS  R-053  meta.sources               所有 source.license 为四档枚举
PASS  R-054  meta.sources               所有 source.accessed_at 为 YYYY-MM-DD
PASS  R-060  annotations                标注文本不含未定标记
PASS  R-061  role                       role 文案均含「在整机」
PASS  R-062  annotations                role 标注字数 20-200
PASS  R-063  annotations                标注 sources URL 合法
PASS  R-070  meta.version               version='1.1.0' 为合法 semver
PASS  R-071  meta.spec_version          spec_version='0.2' 为 0.2
PASS  R-072  meta.engine_min_version    engine_min_version='0.1.0' 为合法 semver
PASS  R-080  annotations.timeline       timeline 结构合法
PASS  R-080  annotations.timeline       timeline highlight 引用存在
PASS  R-081  annotations.timeline       timeline 总时长≤预算(180s)
PASS  R-082  annotations.timeline       C4 级 anim 每镜头 caption 齐全
PASS  R-083  annotations.timeline       caption 无未定标记
PASS  R-084  runtime.output_sinks       sink surface 为命名枚举
PASS  R-085  annotations                annotation.surface 均已声明
PASS  R-086  runtime.input_map          input_map 键名合法；legacy 字符串形式 16 项（建议迁移结构化）
PASS  R-087  localized                  localized 结构完整；警告：以下字段缺 en（回退 zh）：['assembly.whole.role', 'assembly.cabinet.role', 'assembly.memory_subsystem.role', 'assembly.control_subsystem.role', 'assembly.arithmetic_subsystem.role', 'assembly.io_subsystem.role', 'assembly.display_subsystem.role', 'assembly.power_unit.role', 'assembly.delay_line_bank.role', 'assembly.recirculation_unit.role', 'assembly.clock_unit.role', 'assembly.sequence_unit.role', 'assembly.decoder_unit.role', 'assembly.accumulator_unit.role', 'assembly.multiplier_unit.role', 'assembly.tape_reader_unit.role', 'assembly.teleprinter_unit.role', 'assembly.crt_display_unit.role', 'assembly.delay_tank_board.role', 'assembly.adder_board.role', 'component.mercury_delay_tank.role', 'component.transducer.role', 'component.accumulator_register.role', 'component.paper_tape_reader.role', 'component.teleprinter.role', 'component.crt_screen.role', 'component.neon_indicator.role']
PASS  R-088  meta.name_en               无 deprecated name_en（已迁移）
PASS  R-089  meta.era                   未填 era（可选）
PASS  R-090  gltf                       glTF 网格节点名与 node_id 对应
PASS  R-091  THIRD_PARTY.md             THIRD_PARTY 行三件套（分档+URL+日期）合法
------------------------------------------------------------------------------
总计 132 条：PASS 132，FAIL 0

```

### 1.4 edvac

```
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
PASS  R-017  -                          所有 materials 文件存在
PASS  R-018  -                          所有 annotations 引用存在
PASS  R-020  meta.id                    device-id 'edvac' 符合 kebab-case
PASS  R-021  nodes                      所有节点 id 符合 snake_case
PASS  R-022  annotations/output_sinks   annotation/sink id 符合 snake_case
PASS  R-023  nodes                      节点 id 全局唯一
PASS  R-030  assemblies[whole]          translation 为 3 个有限实数
PASS  R-031  assemblies[whole]          rotation 为单位四元数
PASS  R-032  assemblies[whole]          scale 各分量 > 0
PASS  R-033  assemblies[whole]          scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[cabinet]        translation 为 3 个有限实数
PASS  R-031  assemblies[cabinet]        rotation 为单位四元数
PASS  R-032  assemblies[cabinet]        scale 各分量 > 0
PASS  R-033  assemblies[cabinet]        scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[central_arithmetic] translation 为 3 个有限实数
PASS  R-031  assemblies[central_arithmetic] rotation 为单位四元数
PASS  R-032  assemblies[central_arithmetic] scale 各分量 > 0
PASS  R-033  assemblies[central_arithmetic] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[central_control] translation 为 3 个有限实数
PASS  R-031  assemblies[central_control] rotation 为单位四元数
PASS  R-032  assemblies[central_control] scale 各分量 > 0
PASS  R-033  assemblies[central_control] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[memory_unit]    translation 为 3 个有限实数
PASS  R-031  assemblies[memory_unit]    rotation 为单位四元数
PASS  R-032  assemblies[memory_unit]    scale 各分量 > 0
PASS  R-033  assemblies[memory_unit]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[input_unit]     translation 为 3 个有限实数
PASS  R-031  assemblies[input_unit]     rotation 为单位四元数
PASS  R-032  assemblies[input_unit]     scale 各分量 > 0
PASS  R-033  assemblies[input_unit]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[output_unit]    translation 为 3 个有限实数
PASS  R-031  assemblies[output_unit]    rotation 为单位四元数
PASS  R-032  assemblies[output_unit]    scale 各分量 > 0
PASS  R-033  assemblies[output_unit]    scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[power_unit]     translation 为 3 个有限实数
PASS  R-031  assemblies[power_unit]     rotation 为单位四元数
PASS  R-032  assemblies[power_unit]     scale 各分量 > 0
PASS  R-033  assemblies[power_unit]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[adder_unit]     translation 为 3 个有限实数
PASS  R-031  assemblies[adder_unit]     rotation 为单位四元数
PASS  R-032  assemblies[adder_unit]     scale 各分量 > 0
PASS  R-033  assemblies[adder_unit]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[multiplier_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[multiplier_unit] rotation 为单位四元数
PASS  R-032  assemblies[multiplier_unit] scale 各分量 > 0
PASS  R-033  assemblies[multiplier_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[clock_unit]     translation 为 3 个有限实数
PASS  R-031  assemblies[clock_unit]     rotation 为单位四元数
PASS  R-032  assemblies[clock_unit]     scale 各分量 > 0
PASS  R-033  assemblies[clock_unit]     scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[sequence_unit]  translation 为 3 个有限实数
PASS  R-031  assemblies[sequence_unit]  rotation 为单位四元数
PASS  R-032  assemblies[sequence_unit]  scale 各分量 > 0
PASS  R-033  assemblies[sequence_unit]  scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[dispatch_unit]  translation 为 3 个有限实数
PASS  R-031  assemblies[dispatch_unit]  rotation 为单位四元数
PASS  R-032  assemblies[dispatch_unit]  scale 各分量 > 0
PASS  R-033  assemblies[dispatch_unit]  scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[delay_line_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[delay_line_unit] rotation 为单位四元数
PASS  R-032  assemblies[delay_line_unit] scale 各分量 > 0
PASS  R-033  assemblies[delay_line_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[recirculation_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[recirculation_unit] rotation 为单位四元数
PASS  R-032  assemblies[recirculation_unit] scale 各分量 > 0
PASS  R-033  assemblies[recirculation_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[tape_input_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[tape_input_unit] rotation 为单位四元数
PASS  R-032  assemblies[tape_input_unit] scale 各分量 > 0
PASS  R-033  assemblies[tape_input_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[scope_output_unit] translation 为 3 个有限实数
PASS  R-031  assemblies[scope_output_unit] rotation 为单位四元数
PASS  R-032  assemblies[scope_output_unit] scale 各分量 > 0
PASS  R-033  assemblies[scope_output_unit] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[delay_tank_board] translation 为 3 个有限实数
PASS  R-031  assemblies[delay_tank_board] rotation 为单位四元数
PASS  R-032  assemblies[delay_tank_board] scale 各分量 > 0
PASS  R-033  assemblies[delay_tank_board] scale 各分量在 [1e-6, 1e6]
PASS  R-030  assemblies[adder_board]    translation 为 3 个有限实数
PASS  R-031  assemblies[adder_board]    rotation 为单位四元数
PASS  R-032  assemblies[adder_board]    scale 各分量 > 0
PASS  R-033  assemblies[adder_board]    scale 各分量在 [1e-6, 1e6]
PASS  R-040  meta.precision_level       precision_level=L2 合法
PASS  R-041  assemblies[whole]          glTF 可解析（version=2.0）
PASS  R-042  assemblies[whole]          预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[memory_unit]    glTF 可解析（version=2.0）
PASS  R-042  assemblies[memory_unit]    预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-041  assemblies[adder_unit]     glTF 可解析（version=2.0）
PASS  R-042  assemblies[adder_unit]     预算统计：nodes=1, triangles=12；超限由 budget_check.py 报告，不阻塞（可调）
PASS  R-050  THIRD_PARTY.md             THIRD_PARTY.md 存在
PASS  R-051  THIRD_PARTY.md             第三方资产行均含来源 URL 与获取日期
PASS  R-052  meta.sources               所有 source.url 为 http/https
PASS  R-053  meta.sources               所有 source.license 为四档枚举
PASS  R-054  meta.sources               所有 source.accessed_at 为 YYYY-MM-DD
PASS  R-060  annotations                标注文本不含未定标记
PASS  R-061  role                       role 文案均含「在整机」
PASS  R-062  annotations                role 标注字数 20-200
PASS  R-063  annotations                标注 sources URL 合法
PASS  R-070  meta.version               version='1.1.0' 为合法 semver
PASS  R-071  meta.spec_version          spec_version='0.2' 为 0.2
PASS  R-072  meta.engine_min_version    engine_min_version='0.1.0' 为合法 semver
PASS  R-080  annotations.timeline       timeline 结构合法
PASS  R-080  annotations.timeline       timeline highlight 引用存在
PASS  R-081  annotations.timeline       timeline 总时长≤预算(180s)
PASS  R-082  annotations.timeline       C4 级 anim 每镜头 caption 齐全
PASS  R-083  annotations.timeline       caption 无未定标记
PASS  R-084  runtime.output_sinks       sink surface 为命名枚举
PASS  R-085  annotations                annotation.surface 均已声明
PASS  R-086  runtime.input_map          input_map 键名合法；legacy 字符串形式 4 项（建议迁移结构化）
PASS  R-087  localized                  localized 结构完整；警告：以下字段缺 en（回退 zh）：['assembly.whole.role', 'assembly.cabinet.role', 'assembly.central_arithmetic.role', 'assembly.central_control.role', 'assembly.memory_unit.role', 'assembly.input_unit.role', 'assembly.output_unit.role', 'assembly.power_unit.role', 'assembly.adder_unit.role', 'assembly.multiplier_unit.role', 'assembly.clock_unit.role', 'assembly.sequence_unit.role', 'assembly.dispatch_unit.role', 'assembly.delay_line_unit.role', 'assembly.recirculation_unit.role', 'assembly.tape_input_unit.role', 'assembly.scope_output_unit.role', 'assembly.delay_tank_board.role', 'assembly.adder_board.role', 'component.mercury_delay_tank.role', 'component.transducer.role', 'component.accumulator_register.role', 'component.instruction_register.role', 'component.program_counter.role']
PASS  R-088  meta.name_en               无 deprecated name_en（已迁移）
PASS  R-089  meta.era                   未填 era（可选）
PASS  R-090  gltf                       glTF 网格节点名与 node_id 对应
PASS  R-091  THIRD_PARTY.md             THIRD_PARTY 行三件套（分档+URL+日期）合法
------------------------------------------------------------------------------
总计 126 条：PASS 126，FAIL 0

```


## 2. 逐文件 diff 摘要表

迁移项为纯结构与版本字段，**未改动任何文案本体**（role.zh / name.zh 均原样搬入）。

| 包 | 文件 | 变更摘要 |
|---|---|---|
| manchester-baby | meta.json | `meta.name` string → `{zh,en}`；`meta.name_en` 删除（并入 name.en）；`spec_version` 0.1→0.2；`version` 1.0.0→1.1.0；`assemblies[].role` 19 处 → `{zh}`；`components[].role` 11 处 → `{zh}` |
| manchester-baby | runtime.json | 由 meta.runtime 重生成（内容等价，未变） |
| eniac | meta.json | `meta.name` → `{zh,en}`；`name_en` 删除；`spec_version` → 0.2；`version` → 1.1.0；`assemblies[].role` 10 处、`components[].role` 4 处 → `{zh}` |
| eniac | runtime.json | 由 meta.runtime 重生成（内容等价，未变） |
| edsac | meta.json | `meta.name` → `{zh,en}`；`name_en` 删除；`spec_version` → 0.2；`version` → 1.1.0；`assemblies[].role` 20 处、`components[].role` 7 处 → `{zh}`；`runtime.output_sinks[1].surface` `indicator_led` → `led` |
| edsac | runtime.json | 同上 surface 修正（`indicator_led` → `led`），由 meta.runtime 重生成 |
| edsac | meshes/console.gltf | 节点 `name` `console` → `control_subsystem`；网格 `name` `console_mesh` → `control_subsystem_mesh` |
| edsac | meshes/MESHES.md | console.gltf 行 node 名同步为 `control_subsystem` |
| edvac | meta.json | `meta.name` → `{zh,en}`；`name_en` 删除；`spec_version` → 0.2；`version` → 1.1.0；`assemblies[].role` 19 处、`components[].role` 5 处 → `{zh}` |
| edvac | runtime.json | 由 meta.runtime 重生成（内容等价，未变） |

## 3. edsac 专项修复详情

### 3.1 R-084 —— 非法 surface 枚举

- 现场：`runtime.output_sinks[1].surface = "indicator_led"`，不在 v0.2 八枚举内（R-003/R-084 双失败）。
- 修复：改为兼容枚举 `led`（LED 显示），`meta.json` 内嵌 runtime 与 `runtime.json` 同步修改，R-004 逐字节等价性保持（脚本已用 `meta.runtime == runtime.json` 复核为 True）。

### 3.2 R-090 —— glTF 节点名与 assembly.id 不对齐

- 现场：`assemblies[].id = "control_subsystem"`，其 `mesh_ref` 指向 `meshes/console.gltf`，但该 glTF 场景根节点名为 `console`、网格名为 `console_mesh`，R-090 判定「节点/网格名未见 control_subsystem」。
- 修复（修改前 → 修改后）：

| 位置 | 修改前 | 修改后 |
|---|---|---|
| console.gltf `nodes[0].name` | `console` | `control_subsystem` |
| console.gltf `meshes[0].name` | `console_mesh` | `control_subsystem_mesh` |
| MESHES.md 表格 node 名列 | `console（control_subsystem）` | `control_subsystem` |

## 4. 与 02 线工具 / 规范版本采用说明

- **规范版本**：采用 `内容包规范_v0.2.md`（02 线 TASK-07 产出）。执行时 02 线尚未产出 v0.2.1 / migrate 工具（02 线 `tools/` 下仅 `validate/`，无 `migrate/`），故按规范第十二章迁移表**手工迁移**，本报告据此记录。
- **校验器版本**：`tools/validate/validate.py`（v0.2，2026-10-31 复跑修订版），schema 为 `content/schema/device_spec.schema.json`（draft 2020-12）。
- **迁移后版本号**：`meta.version` 由 1.0.0 升 1.1.0（迁移性小版本，规范校验报告 §2 建议值）；`engine_min_version` 保持 0.1.0 不动。

## 5. 备份快照清单

迁移前快照存于 `docs/migrate_backup/`：

| 文件 | 说明 |
|---|---|
| manchester-baby.meta.json / .runtime.json | 迁移前 meta / runtime 副本 |
| eniac.meta.json / .runtime.json | 迁移前 meta / runtime 副本 |
| edsac.meta.json / .runtime.json | 迁移前 meta / runtime 副本 |
| edvac.meta.json / .runtime.json | 迁移前 meta / runtime 副本 |
| validate_*.log × 4 | 迁移后四包完整校验日志 |

## 6. 开放问题

1. **role.en 缺失（R-087 警告，非阻塞）**：四包全部 `role` 仅迁移为 `{zh}`，未补 `en`。规范允许 en 缺失回退 zh（警告不阻塞）。若后续要求全量英文文案，需逐条补译（manchester-baby 30 条、eniac 14 条、edsac 27 条、edvac 24 条 role 文案）。
2. **input_map legacy 字符串形式**：四包 `input_map` 仍为 v0.1 legacy 字符串令牌（baby 36 项、eniac 4 项、edsac 16 项、edvac 4 项），R-086 通过但提示「建议迁移结构化 {map,key}」。按任务要求本轮只做迁移类清零、不改语义，结构化迁移留待后续。
3. **meta.era / manufacturer 未补**：v0.2 新增可选字段 `era`/`manufacturer` 未回填（R-089 显示「未填 era（可选）」）。如需档案完整性，可在后续内容生产轮次补录（edsac 1949、edvac 1951 交付 / 1952 运行、eniac 1946、baby 1948）。
4. **占位网格仍为 unit box**：四包 `meshes/*.gltf` 仍是 TASK-08/12 的 8 顶点占位盒（nodes=1, triangles=12），R-041/R-042 通过但预算为占位值；真实网格替换在后续设备内容生产阶段完成。
