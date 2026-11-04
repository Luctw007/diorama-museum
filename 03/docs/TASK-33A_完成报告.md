# TASK-33A 完成报告：VAX-11 设备包生产（大型机厅首轮收官）

> 任务：33-A（03 线 1/2）。产出 `content/vax11/` 完整设备包（VAX-11/780）。
> 落盘于 `\\DESKTOP-2IDAL09\work\03\repo\content\vax11\`。
> 依据：hall-mainframe/04_VAX11.md（预研）。至此大型机/小型机厅四台（S/360、PDP-8、PDP-11、VAX-11）首轮全部成包。

## 0. 规范版本说明

同 28-A/28-B：02 线 v0.3 仅为草案（未定稿），本任务**按 v0.2.1 执行**，`meta.spec_version` 取 `"0.2"`。

## 1. 交付物清单与校验结果

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | `meta.json` | spec_version 0.2、era=1977、manufacturer、intro/description/category 齐备 | ✅ |
| 2 | `runtime.json` | emulator="none"（demo_mode）、output_sinks（terminal + indicator_lamps）、input_map 6 动作 | ✅ |
| 3 | `assemblies/*.gltf`（5 件） | console(VT100)/cpu_cabinet/tape_tu78/disk_ra81/unibus_light_panel，节点名=node_id | ✅ |
| 4 | `assemblies/MESHES.md` | 占位盒说明 + 真实尺寸依据 | ✅ |
| 5 | `annotations/annotations.json` | 38 条（≥30，含虚拟寻址流程、boot 流程讲解锚点） | ✅ |
| 6 | `encyclopedia.md` | **2,539 汉字**（≥2500，VAX 架构/虚拟地址空间/BSD 渊源/DEC 兴衰） | ✅ |
| 7 | `THIRD_PARTY.md` | 三件套齐全 | ✅ |

**校验结果（02 线 validate.py）**：

```text
总计 78 条：PASS 78，FAIL 0   （退出码 0）
```

## 2. 尺寸对照表（占位盒 vs 04_VAX11.md 档案）

| 占位盒 | 占位盒实际（单位盒） | 档案/真实尺寸（「需核实」） | 结论 |
|---|---|---|---|
| console.gltf | 1 m³（半长 0.5） | VT100 操作台约 0.5 m 宽 × 0.3 m 高 | 占位几何 |
| cpu_cabinet.gltf | 同上 | CPU 柜（11/780）约 0.7 m 宽 × 1.5 m 高 | 占位几何 |
| tape_tu78.gltf | 同上 | TU78 磁带机约 0.6 m 宽 × 0.8 m 高 | 占位几何 |
| disk_ra81.gltf | 同上 | RA81 磁盘约 0.48 m 宽 × 0.26 m 高（19 英寸机架） | 占位几何 |
| unibus_light_panel.gltf | 同上 | 灯板约 0.48 m 宽 × 0.3 m 高 | 占位几何 |

## 3. 大型机/小型机厅四台展呈并列关系建议（动线雏形）

| 序 | 设备 | 一句话定位 | 展呈侧重 | 可玩出口 |
|---|---|---|---|---|
| 1 | IBM System/360 | 兼容家族 · 一套语言 | 通道 + 微程序 + 批处理流水 | Hercules 近亲演示（预留） |
| 2 | DEC PDP-8 | 小型化 · 下放 | 磁芯 + 前面板拨键 | SIMH + 前面板交互 |
| 3 | DEC PDP-11 | 优雅架构 · 软件生态 | Unibus + 正交指令集 | SIMH 跑 Unix/RT-11 |
| 4 | DEC VAX-11 | 虚拟寻址 · 服务规模化 | 分页/虚拟内存/VAX MIPS | SIMH 跑 VMS/BSD |

**动线雏形**：入口总导语（"服务规模化"）→ System/360（大）→ PDP-8（小）→ PDP-11（优雅）→ VAX-11（虚）→ 出口衔接个人计算机厅。四台构成"从大到小、从硬到软、从实到虚"的完整演进弧线。

## 4. SIMH VAX 真跑衔接说明（仅预留，未下载）

| 项 | 说明 |
|---|---|
| 本包 emulator | `"none"`（demo_mode 起步）——SIMH VAX 二进制未就位、01 线未注册 vax 模拟器 |
| SIMH 许可 | MIT-style（Classic 3.x / Open SIMH），主站 `https://simh.trailing-edge.com/` |
| VMS 授权 | 业余/社区许可（Hobbyist/Community License）仅限非商业，商用分发前「需核实」 |
| 预留接线 | 未来真跑：01 线注册 `simh-vax` 模拟器 → 03 线把 `runtime.emulator` 改为 "simh-vax"（本报告记录，不落地改动） |

## 5. 开放问题

1. **display/fps 字段未落地**（沿用 23-A 阻塞结论）：terminal+indicator_lamps 真实画面参数无法写入 runtime，待 02 线规范新增后回填。
2. **surface 命名**：用 `terminal` + `indicator_lamps`（任务书指定）；规范建议新包灯组用 `led`，可全馆统一清理时收敛。
3. **VAX-11/780 各部件精确尺寸**：CPU 柜/TU78/RA81 等以 DEC 手册为准（「需核实」）。
4. **VMS/BSD 软件授权**：真跑涉及系统镜像授权，商用分发前需逐项核实（本包 demo_mode 起步，未下载镜像）。
