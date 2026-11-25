# 27 · Apple II 目录 planned 巡检卡

> 任务：TASK-320-Q（apple-ii 27 号）· 完成日期：2026-11-26
> 性质：**纯巡检**——只对家电外设目录与 Apple II 线相关的 planned 候选分组做只读巡检（条目号 / 名称 / 状态 / 挂接关系 / 是否已产包 / 候选建议），**不回填、不改 jsonl、不产包、不下载任何 ROM/BIOS/二进制/贴图**。
> 体例母本：`10_定稿决策.md`（外设口径母本）；`25_扩展卡与软件卡清单级预研卡.md`（巡检卡体例与红线）。
> 只读来源：`../../catalog/家电影音与外设大类_目录_v2.jsonl`（实测扫描，条目号/名称/状态以实扫为准）；`../../content/apple-ii/meta.json`（`disk_ii` / `game_port` / `cassette_ports` / `video_section` 现状）。

---

## 一、红线总则（本卡全程生效）

1. **纯巡检、不回填、不改 jsonl**：本文件只做目录条目的只读巡检与候选建议，不修改任何 jsonl，不回填 `device_id` 或 `status`。
2. **清单实测、不臆造**：所有条目号、名称、`status`、`device_id` 均以 jsonl 实扫结果为准，未扫描到的条目一律不写入。
3. **不下载任何 ROM / BIOS / 二进制 / 贴图**：本卡不涉及任何固件获取。
4. **已产包与候选项严格区分**：`disk_ii` 已作为 assembly 落在 apple-ii 包内（meta.json），须与目录中的"通用软驱"候选项明确区分，避免重复登记。

---

## 二、巡检范围与只读现状

### 2.1 巡检对象

本卡只巡检四组、共 7 条 `status = planned` 的目录条目（实扫确认，全部 `device_id = null`）：

| 分组 | 条目号 | 名称 | 实扫 status |
|---|---|---|---|
| ① 存储外设 | P-ST-000001 | 软盘驱动器 | planned |
| ① 存储外设 | P-ST-000002 | 5.25 英寸软驱 | planned |
| ② 输入外设 | P-IN-000013 | 摇杆 | planned |
| ② 输入外设 | P-IN-000008 | 游戏手柄 | planned |
| ③ 显示外设 | P-MO-000001 | CRT 显示器 | planned |
| ③ 显示外设 | P-MO-000002 | 单色显示器 | planned |
| ④ 打印外设 | P-PR-000001 | 点阵打印机 | planned |

### 2.2 Apple II 包内现状（只读，来自 meta.json）

- **存储**：`disk_ii` 软驱 assembly 已存在（整机 `apple_ii` 的 children 含 `disk_ii`，读 5.25 英寸软盘、140 KB），`slot_6` 挂载 `disk_controller` 组件（`part_no: "341-0027"`，Disk II 控制器引导 ROM）。即 **Apple 专属 Disk II 软驱已在包内**。
- **输入**：`game_port`（游戏接口）已存在，role 明确"连接摇杆与手柄，接收模拟轴与按钮的输入信号"；`cassette_ports`（磁带接口，1200 波特）已存在。`runtime.input_map` 含 `paddle_axis_0~3`（PDL0–PDL3 四路摇杆模拟轴）与 `paddle_btn_0~2`（PB0–PB2 三按钮）。
- **显示**：`video_section` / `video_connector` 已存在，输出 NTSC 复合视频（RCA），供外接监视器或电视显示；`runtime.output_sinks` 含 `crt_internal`（内屏 CRT 投放，`surface: internal_crt`）。
- **打印**：无原生打印机接口；打印需经八扩展槽插卡（如 SSC 串行卡或并行接口卡）挂接（见 25 号卡 SSC 串行卡）。

---

## 三、四组候选分组逐项巡检

### ① 存储外设（P-ST-000001 软盘驱动器 / P-ST-000002 5.25 英寸软驱）

| 条目号 | 名称 | 实扫 status | device_id | 厂商 / 年代 | 与 Apple II 挂接关系 | 是否已产包 | 候选建议 |
|---|---|---|---|---|---|---|---|
| P-ST-000001 | 软盘驱动器 | planned | null | Shugart/IBM · 1976 | 目录"通用软驱"条目；Apple II 经槽 6 `disk_controller`（341-0027）挂接 **Apple 专属 Disk II** 软驱（5.25 英寸、140 KB） | **disk_ii 已在 apple-ii 包内**，条目本身未产包 | 通用软驱条目与已产包的 Disk II 是"通用 vs 专属型号"关系，非重复登记；建议不回填 `device_id`，保持 planned |
| P-ST-000002 | 5.25 英寸软驱 | planned | null | Shugart · 1976 | 同左；5.25 英寸软驱口径（Shugart SA-400 系）是 Disk II 的介质/规格母型，但 Disk II 为 Apple 自研控制器方案 | **disk_ii 已在包内**（读 5.25 软盘），条目未产包 | 建议与 P-ST-000001 同口径处理：作为"通用 5.25 软驱"候选保留，不与包内 Disk II 合并 |

> 巡检要点：`meta.json` 中 `disk_ii`（assembly）与 `slot_6.disk_controller`（组件 341-0027）已覆盖"Apple II 存储外设"的物理呈现；目录这两条是**通用外设目录条目**，属"办公与计算外设"大类，与 Apple II 专属 Disk II **分属不同登记体系**，本卡仅做对照，不改动任何一侧。

### ② 输入外设（P-IN-000013 摇杆 / P-IN-000008 游戏手柄）

| 条目号 | 名称 | 实扫 status | device_id | 厂商 / 年代 | 与 Apple II 挂接关系 | 是否已产包 | 候选建议 |
|---|---|---|---|---|---|---|---|
| P-IN-000013 | 摇杆 | planned | null | Atari/多家 · 1977 | 经 `game_port`（游戏接口）挂接；`input_map` 已预留 PDL0–PDL3 模拟轴 + PB0–PB2 按钮 | 接口已产包（`game_port`），**摇杆实物未产包** | 强候选：接口与输入映射已就绪，仅缺摇杆实物 assembly |
| P-IN-000008 | 游戏手柄 | planned | null | 多家厂商 · 1980 | 同左，经 `game_port` 挂接（按钮输入 PB0–PB2） | 接口已产包，**手柄实物未产包** | 候选：接口已就绪，手柄为摇杆的替代形态，可择一登记 |

> 巡检要点：Apple II 原版无独立鼠标/键盘外设（键盘内建），游戏输入统一走 `game_port`。目录两条输入候选的"挂接点"已在包内（`game_port` + `input_map` 的摇杆轴/按钮），但**实物设备未建模**，属后续配套候选。

### ③ 显示外设（P-MO-000001 CRT 显示器 / P-MO-000002 单色显示器）

| 条目号 | 名称 | 实扫 status | device_id | 厂商 / 年代 | 与 Apple II 挂接关系 | 是否已产包 | 候选建议 |
|---|---|---|---|---|---|---|---|
| P-MO-000001 | CRT 显示器 | planned | null | 多家厂商 · 1976 | 经 `video_connector`（RCA）接 NTSC 复合视频；Apple II 输出可接 CRT 电视 / 监视器 | 视频输出接口已产包（`video_section`/`video_connector`），**显示器实物未产包** | 候选：内屏 CRT 投放（`crt_internal`）已覆盖，外接 CRT 显示器可作配套候选 |
| P-MO-000002 | 单色显示器 | planned | null | IBM/Apple · 1981 | 同左，NTSC 复合视频兼容单色监视器（绿/琥珀单色）；Apple 官方 Monitor II 属单色/彩色监视器系 | 接口已产包，**显示器实物未产包** | 候选：单色监视器是 Apple II 时代文字处理标配，可作显示候选 |

> 巡检要点：Apple II 的显示挂接点是 RCA 复合视频（NTSC），非数字 RGB。目录两条显示候选的"信号源"已在包内（`video_section` + `video_connector` + `crt_internal` 内屏），但**外部显示器实物未建模**。

### ④ 打印外设（P-PR-000001 点阵打印机）

| 条目号 | 名称 | 实扫 status | device_id | 厂商 / 年代 | 与 Apple II 挂接关系 | 是否已产包 | 候选建议 |
|---|---|---|---|---|---|---|---|
| P-PR-000001 | 点阵打印机 | planned | null | Epson · 1978 | Apple II 原版**无原生打印机接口**；需经八扩展槽插卡（SSC 串行卡接串行打印机，或并行接口卡接并行点阵打印机）挂接 | **未产包**（无接口、无实物） | 弱候选 / 需前置：Epson MX-80 类是 Apple II 时代经典配对，但挂接依赖扩展卡（SSC/并行卡），优先度低于前三组 |

> 巡检要点：与前三组不同，打印外设在 Apple II 包内**既无接口、也无实物**，需额外扩展卡（25 号卡已列 SSC 串行卡为候选）。因此打印候选的挂接成本最高，建议排为最低优先级。

---

## 四、汇总对照表

| 分组 | 条目（实扫） | status | 包内挂接点 | 已产包情况 | 候选优先度 |
|---|---|---|---|---|---|
| ① 存储 | P-ST-000001 / P-ST-000002 | planned | 槽 6 `disk_controller` + `disk_ii` | **disk_ii 已产包**（条目为通用软驱，未产包） | 已产包对照，条目保留 planned |
| ② 输入 | P-IN-000013 / P-IN-000008 | planned | `game_port` + `input_map`（PDL/PB） | 接口已产包，实物未产包 | 高 |
| ③ 显示 | P-MO-000001 / P-MO-000002 | planned | `video_connector`（RCA/NTSC） | 输出接口已产包，实物未产包 | 中高 |
| ④ 打印 | P-PR-000001 | planned | 无原生接口（需 SSC/并行卡） | 接口与实物均未产包 | 低 |

---

## 五、一句话结论

四组 7 条候选均为 jsonl 实扫 `status = planned`（`device_id = null`）；其中存储组的 Apple 专属 `disk_ii` **已在 apple-ii 包内**（与目录"通用软驱"条目属不同登记体系，不合并），输入组（`game_port`）、显示组（`video_connector`）的**挂接接口已产包、仅实物未建模**，打印组**接口与实物均缺、需扩展卡前置**。本卡纯巡检，**不回填、不改 jsonl、不产包**。
