# TASK-38A 完成报告：Commodore 64 设备包生产（个人机厅首台）

> 任务：38-A（03 线 1/2）。产出 `content/commodore64/` 完整设备包。
> 落盘于 `\\DESKTOP-2IDAL09\work\03\repo\content\commodore64\`。
> 依据：hall-personal/01_Commodore64.md（预研）。

## 0. 与 02 线规范版本的合规说明

- 任务书要求"与 02 线 v0.4（若已定稿则采用）的合规说明"。经核实，02 线当前 **v0.4 仅为《规范v0.4_音频章草案.md》（草案，未定稿）**；已定稿的最新规范为 **v0.3**（`内容包规范_v0.3.md`，TASK-27B，并入「建模与网格」第十三章）。
- 故本包**按 v0.3 执行**：`meta.spec_version` 仍为 `"0.2"`（v0.3 未引入字段结构级变更）；并按 v0.3 第十三章跑 **`model_check.py`（MR-001~004）**（27-A 已产出）。

## 1. 交付物清单与校验结果

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | `meta.json` | spec_version 0.2、era=1982、manufacturer、intro/description/category 齐备 | ✅ |
| 2 | `runtime.json` | emulator="vice"（预留真跑）、output_sinks（external_crt+speaker+led）、input_map 7 动作对象格式 | ✅ |
| 3 | `assemblies/*.gltf`（5 件） | case（breadbin）/keyboard/motherboard/power/datasette，节点名=node_id | ✅ |
| 4 | `assemblies/MESHES.md` | 占位盒说明 + 真实尺寸依据 | ✅ |
| 5 | `annotations/annotations.json` | 31 条（≥30，含 SID 声芯片、磁带装载流程讲解锚点） | ✅ |
| 6 | `encyclopedia.md` | **2,532 汉字**（≥2500，家用市场/6502 系/SID/游戏文化） | ✅ |
| 7 | `THIRD_PARTY.md` | 三件套齐全 + ROM 红线声明 | ✅ |

**校验结果**：

```text
validate.py  总计 78 条：PASS 78，FAIL 0   （退出码 0）
model_check  MR-01 节点命名 / MR-02 三角面 / MR-03 贴图 / MR-04 扩展 —— 全 PASS（5/5 网格）
```

## 2. 尺寸对照表（占位盒 vs 01_Commodore64.md 档案）

| 占位盒 | 占位盒实际（单位盒） | 档案/真实尺寸（「需核实」） | 结论 |
|---|---|---|---|
| case.gltf | 1 m³（半长 0.5） | 主机壳（breadbin）约 40×20×8 cm | 占位几何 |
| keyboard.gltf | 同上 | 键盘约 40×15 cm | 占位几何 |
| motherboard.gltf | 同上 | 主板约 30×20 cm | 占位几何 |
| power.gltf | 同上 | 外置电源砖约 15×10×6 cm | 占位几何 |
| datasette.gltf | 同上 | Datasette 约 20×10×5 cm | 占位几何 |

## 3. VICE 真跑衔接说明（仅预留，未下载）

| 项 | 说明 |
|---|---|
| 本包 emulator | `"vice"`（预填，预留真跑）——VICE 二进制未就位、01 线未注册 vice 模拟器 |
| VICE 许可 | GPLv2，主站 `http://vice-emu.sourceforge.io` |
| ROM 红线 | C64 BASIC/KERNAL ROM 受版权保护，VICE 不含 ROM，需用户提供合法镜像；本包未下载、未提供 ROM |
| 预留接线 | 未来真跑：01 线注册 `vice` 模拟器 → 二进制就位 → 引导用户提供 ROM 即可真跑（本报告记录，不落地改动） |

## 4. 开放问题

1. **display/fps 字段未落地**（沿用 23-A 阻塞结论）：external_crt 等真实画面参数无法写入 runtime，待 02 线规范新增后回填。
2. **ROM 授权流程**：C64 真跑依赖受版权保护的 BASIC/KERNAL ROM，需建立统一的"固件授权"流程。
3. **"世界最畅销单一计算机型号"口径**：销量 1,250 万 vs 1,700 万两说（Bergström 等不同来源），已在百科卡采用保守表述"超过一千万台"。
4. **各部件精确尺寸**：breadbin 机身/主板/电源等尺寸「需核实」，正式建模以存世实机为准。
5. **input_map 键位绑定**：run_stop→KEY_ESCAPE、return→KEY_ENTER 等为占位建议，需 04 线绑定设置界面最终确认玩家层键位。
