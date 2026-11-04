# TASK-23B 完成报告：PDP-8 设备包生产（大厅主机首台开产）

> 任务：23-B（03 线 2/2）。把"大型机/小型机厅"第一台（DEC PDP-8）正式做成内容包。
> 落盘于 `\\DESKTOP-2IDAL09\work\03\repo\content\pdp8\`。
> 依据：hall-mainframe/02_PDP8.md（预研）+ 01 线 SIMH 网关登记（`simh-pdp8` 已注册）。

## 1. 交付物清单与校验结果

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | `meta.json` | spec_version 0.2、era=1965、manufacturer、localized name/role | ✅ |
| 2 | `runtime.json` | emulator=simh-pdp8、output_sinks、input_map 对象格式 | ✅ |
| 3 | `assemblies/*.gltf`（4 个占位盒） | panel/chassis/core_memory_rack/io_expansion_rack，节点名=node_id | ✅ |
| 4 | `assemblies/MESHES.md` | 占位盒说明 + 真实尺寸依据 | ✅ |
| 5 | `annotations/annotations.json` | 44 条（面板开关/灯 Inspect 文案 33 条 + 装配体 role 5 条 + flow 1 条 + 其余 5 条） | ✅ |
| 6 | `encyclopedia.md` | C1 百科卡，**2,546 汉字**（≥2500） | ✅ |
| 7 | `THIRD_PARTY.md` | 三件套齐全（原创占位盒声明 + 引用来源登记） | ✅ |

**校验结果（02 线 validate.py，v0.2）**：

```text
总计 72 条：PASS 72，FAIL 0   （退出码 0）
```

关键规则全绿：R-002/R-003/R-004/R-005（结构）、R-060/R-061/R-062（文案）、R-070/R-071/R-089（版本/规范/年代）、R-086（input_map 对象格式键名合法）、R-090（glTF 节点名=node_id）。

## 2. 迭代记录（≥2 轮）

- **迭代 1（结构）**：首验 68 PASS / 6 FAIL——缺 4 条装配体 role 标注（panel/chassis/core_memory_rack/io_expansion_rack 的 `annotations` 引用了不存在的 `*_role`）+ 缺 `THIRD_PARTY.md`（R-018 ×4、R-050、R-091）。→ 补 4 条 role 标注 + 写 THIRD_PARTY.md → 复验 72 PASS / 0 FAIL。
- **迭代 2（字数）**：encyclopedia.md 首版 1,572 汉字 → 增补「深度解读五~八」（八条指令 / 型号谱系 / FOCAL-PAL-OS8 / 遗产意义）+「在展厅里怎么看它」+「一句话总结」→ 2,546 汉字（≥2500）。
- **迭代 3（input_map 格式）**：按 v0.2.1 裁决，input_map 全部采用**对象格式 `{map,key}`**（非 legacy 字符串），键名取 Godot `KEY_*` 全集与项目扩展键（KEY_POWER/KEY_CLEAR 等），R-086 全绿。

## 3. 占位盒尺寸与 02_PDP8.md 档案表对照

| 占位盒（glTF） | 占位盒实际（单位盒） | 02_PDP8.md 档案表 / 真实尺寸 | 结论 |
|---|---|---|---|
| panel.gltf | 1 m × 1 m × 1 m（半长 0.5） | 前面板约 48 cm 宽 × 27 cm 高（19 英寸机架面板）「需核实」 | 占位几何，待真实网格替换 |
| chassis.gltf | 同上 | 机体约 48 × 27 × 50 cm（机架/台式）「需核实」 | 占位几何 |
| core_memory_rack.gltf | 同上 | 核心内存机架（"3.2KW"功耗口径「需核实」） | 占位几何 |
| io_expansion_rack.gltf | 同上 | I/O 扩展架（视配置）「需核实」 | 占位几何 |

> 说明：占位盒仅为几何占位（保证 R-016/R-041/R-090 通过），**真实尺寸按资料写入 `assemblies/MESHES.md` 注释**，逐条目对照如上。正式建模时按 DEC PDP-8 Handbook 与复刻机实测替换。

## 4. 与 SIMH 真跑路径的衔接说明

| 步骤 | 状态 | 说明 |
|---|---|---|
| 1. 网关登记 `simh-pdp8` | ✅ 已完成（01 线 gateway.py `EMULATORS["simh-pdp8"]`） | 本包 `runtime.emulator="simh-pdp8"` 已对齐 |
| 2. 本包 input_map 对象化 | ✅ 已完成（8 动作：load_addr/exam/dep/start/continue/stop/clear/power） | 键名全部合法，R-086 通过 |
| 3. **等待 SIMH 二进制就位** | ⏳ 待办（**这是唯一等待点**） | 01 线当前缺 `third_party/simh/pdp8` 二进制，网关返回 `EMULATOR_BINARY_MISSING`；二进制就位后 `simh-pdp8` 即可真跑 |
| 4. 后端 `simh_pdp8.py` | ⏳ 待办（01 线） | 需新增后端，把 SIMH 终端文本流映射为设备通道消息（见 01 线 `licenses/SIMH.md`） |
| 5. 真跑验证 | ⏳ 待办 | 二进制 + 后端就位后，用 input_map 的 exam/dep/start 等做面板操作真跑验收 |

**结论**：本包已按 v0.2 完整生产并 0 FAIL，与 01 线 `simh-pdp8` 登记对齐；真跑唯一阻塞是 **SIMH 二进制未安装**（01 线 `licenses/SIMH.md` 已登记该依赖），本线无需再改。

## 5. TASK-23 两份总收尾

- **23-A（四包 runtime display/fps 补全）**：**前置未满足，已阻塞并如实记录**（详见 `docs/TASK-23A_完成报告.md`）。核实结论：02 线 v0.2.1 是文档勘误版，**未新增 display/fps 字段**，schema `additionalProperties:false` 会拒绝任何 display 字段 → 无法写入而不破坏校验。已完成的替代产出：四包真实画面参数研究 + 与 01 线缺省表核对，四包保持 0 FAIL。
- **23-B（PDP-8 设备包生产）**：完整产出并 **0 FAIL**，是"大型机/小型机厅"第一台正式内容包。

## 6. 开放问题

1. **23-A 阻塞点**：display/fps 字段需 02 线在规范/schema 中先行新增（升任务或勘误 v0.2.2），03 线随后回填四包真实画面参数（Baby 32×32 点阵等）。
2. **"核心内存机架 3.2KW"口径**：任务书中的"3.2KW"含义待核（功耗 3.2 kW 还是内存 3.2K 字），已按功耗口径写入注释并标「需核实」。
3. **PDP-8 面板开关/灯的精确命名**：本包按 DEC 手册常见的"12 数据开关 + 7 控制开关 + 12 累加器灯 + 链接/运行灯"建模；不同型号（8/S、8/I、8/E）面板有差异，正式建模以目标型号（建议 PDP-8/I）为准。
4. **input_map 键位绑定**：当前 8 个动作的键盘绑定为占位建议（exam→E、dep→D 等），需 01 线 `input_profile.gd` / 04 线绑定设置界面最终确认玩家层键位。
5. **SIMH 二进制与后端**：真跑依赖 01 线安装 SIMH 二进制并实现 `simh_pdp8.py` 后端（见 §4），属跨线依赖，需项目排期协调。
