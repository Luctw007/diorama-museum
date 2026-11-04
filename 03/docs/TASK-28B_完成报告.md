# TASK-28B 完成报告：PDP-11 设备包 + 大型机/小型机厅导语 v1

> 任务：28-B（03 线 2/2）。产出 `content/pdp11/` 完整设备包（PDP-11/70 定档）与 `docs/research/hall-mainframe/08_展厅导语_v1.md`。
> 落盘于 `\\DESKTOP-2IDAL09\work\03\repo\`。
> 依据：hall-mainframe/03_PDP11.md（预研）；衔接 04 线"黎明厅台本"体例。

## 0. 规范版本说明

同 28-A：02 线 v0.3 仅为草案（未定稿），本任务**按 v0.2.1 执行**，`meta.spec_version` 取 `"0.2"`。

## 1. 交付物清单与校验结果

### 1.1 `content/pdp11/` 设备包

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | `meta.json` | spec_version 0.2、era=1975、manufacturer、intro/description/category 齐备 | ✅ |
| 2 | `runtime.json` | emulator="none"（demo_mode）、output_sinks（terminal + indicator_lamps）、input_map 6 动作 | ✅ |
| 3 | `assemblies/*.gltf`（5 件） | console/cpu_cabinet/disk_rk05/tape_tu10/unibus_rack，节点名=node_id | ✅ |
| 4 | `assemblies/MESHES.md` | 占位盒说明 + 真实尺寸依据 | ✅ |
| 5 | `annotations/annotations.json` | 39 条（≥30，操作台旋钮/灯组 + Unibus 等） | ✅ |
| 6 | `encyclopedia.md` | **2,579 汉字**（≥2500，Unibus/RSX-11/Unix 渊源） | ✅ |
| 7 | `THIRD_PARTY.md` | 三件套齐全 | ✅ |

**校验结果（02 线 validate.py）**：

```text
总计 78 条：PASS 78，FAIL 0   （退出码 0）
```

### 1.2 `docs/research/hall-mainframe/08_展厅导语_v1.md`

**3,067 汉字**（≥3000）。含：展厅总导语（"服务规模化"主线，5 段）· 四台设备引言 · 时间线（1964–1978）· 给玩家的三个问题 · 结语 · 叙事主线与参观动线（供运营）· 给 04 线台本化移交说明。

## 2. 定档理由（PDP-11/70）

1. **PDP-11 家族的性能与内存顶峰**：/70 引入内存管理单元（MMU），把地址从 16 位 64K 扩展到 22 位 4M，代表 PDP-11"向上生长"的成熟形态，技术故事完整（Unibus + MMU）。
2. **外设构成丰富、展陈性强**：操作台 + CPU 柜 + RK05 磁盘组 + TU10/TS11 磁带机 + Unibus 扩展架，完整呈现"内存与设备统一编址"的物理形态。
3. **era=1975 与任务书一致**：PDP-11/70 于 1975 年推出，`meta.era` 取 1975。

## 3. 尺寸对照表（占位盒 vs 03_PDP11.md 档案）

| 占位盒 | 占位盒实际（单位盒） | 档案/真实尺寸（「需核实」） | 结论 |
|---|---|---|---|
| console.gltf | 1 m³（半长 0.5） | 操作台约 0.6 m 宽 × 0.3 m 高 | 占位几何 |
| cpu_cabinet.gltf | 同上 | CPU 柜单机架约 0.6 m 宽 × 1.6 m 高 | 占位几何 |
| disk_rk05.gltf | 同上 | RK05 磁盘约 0.48 m 宽 × 0.26 m 高（19 英寸机架） | 占位几何 |
| tape_tu10.gltf | 同上 | TU10/TS11 磁带机约 0.48 m 宽 × 0.66 m 高 | 占位几何 |
| unibus_rack.gltf | 同上 | Unibus 扩展架约 0.48 m 宽 × 0.6 m 高 | 占位几何 |

## 4. 与 04 线台本化的移交清单

| # | 移交项 | 说明 |
|---|---|---|
| 1 | 厅导语 v1 成品文案 | `08_展厅导语_v1.md`，口语化可转配音，已按"总导语/逐台引言/时间线/问题/结语"分层 |
| 2 | 事实溯源 | 编号 [Sxx] 指向 `06_证据包索引.md`（S27 起），台本化时隐去编号 |
| 3 | 与黎明厅台本衔接点 | 本厅开场承接黎明厅"存储程序"收尾；建议台本首句"上一站机器证明自己能算，这一站机器开始真正服务人" |
| 4 | 每台可玩点（待 04 线定互动文案） | System/360（Hercules 近亲演示）、PDP-8（前面板交互）、PDP-11（跑 Unix）、VAX（跑 VMS/BSD） |
| 5 | 出口过渡 | "出口衔接个人计算机厅"过渡文案待 04 线定 |

## 5. TASK-28 两份总收尾

- **28-A（System/360 设备包）**：完整产出并 **0 FAIL**（78 PASS），定档 Model 30，Hercules 真跑仅写预留接线说明，详见 `docs/TASK-28A_完成报告.md`。
- **28-B（PDP-11 设备包 + 厅导语）**：完整产出并 **0 FAIL**（78 PASS），厅导语 3,067 字，为 04 线台本化备料完成。

## 6. 开放问题

1. **display/fps 字段未落地**（沿用 23-A 阻塞结论）：PDP-11 terminal+indicator_lamps 的真实画面参数无法写入 runtime，待 02 线规范新增后回填。
2. **surface 命名**：本包用 `terminal` + `indicator_lamps`（任务书指定）；规范 §11.1 建议新包灯组用 `led`，属轻微命名不一致，可全馆统一清理时收敛。
3. **PDP-11/70 控制台精确布局**：本包按"终端 + 灯组 + 控制开关"通用配置建模，具体以 DEC PDP-11/70 手册为准（「需核实」）。
4. **Ancient UNIX License / VMS 授权**：PDP-11 跑 Unix、VAX 跑 VMS 的真跑涉及软件授权，商用分发前需逐项核实（本包 demo_mode 起步，未下载任何系统镜像）。
5. **v0.3 草案的对齐**：02 线《规范 v0.3 建模网格章草案》已明确"一装配体一文件 + 根节点名=node_id + 占位盒替换协议"，本包已对齐；待 v0.3 定稿后按新预算/材质条款复检正式网格。
