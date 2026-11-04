# TASK-28A 完成报告：IBM System/360 设备包生产（大型机厅第二台）

> 任务：28-A（03 线 1/2）。产出 `content/system360/` 完整设备包，代表机型 S/360 Model 30。
> 落盘于 `\\DESKTOP-2IDAL09\work\03\repo\content\system360\`。
> 依据：hall-mainframe/01_System360.md（预研）。

## 0. 规范版本与工具采用说明

- **规范版本**：02 线《内容包规范 v0.2.1》。任务书提及"02 线 v0.3 规范（27-B 若同轮定稿则以 v0.3；未定稿按 v0.2.1）"——经核实，02 线当前 v0.3 仅产出 `规范v0.3_建模网格章草案.md`（**草案，未定稿**，明文"不取代现行 v0.2.1"），故**按 v0.2.1 执行**，`meta.spec_version` 取 `"0.2"`。
- **model_check**：任务书"若 27-A 已产出"——经核实 02 线 `tools/` 下**无 model_check 工具**（27-A 未产出），故跳过，本报告注明。

## 1. 定档理由（S/360 Model 30）

1. **体积适中**：Model 30 为入门商用机型，8 位数据通路、单机柜为主，建模与展陈体量可控，符合"占位盒起步"阶段的实际投入。
2. **资料足**：Model 30 是 System/360 家族产量最大的机型之一，手册与档案相对完整（Wikipedia 独立条目 + bitsavers 手册）。
3. **技术故事性强**：Model 30 靠**微程序控制**以 8 位数据通路演绎 32 位指令集，是讲清"兼容家族如何实现"的最佳样本；其读卡机/磁带机/打印机外设构成完整的"批处理流水"展陈。

## 2. 交付物清单与校验结果

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | `meta.json` | spec_version 0.2、era=1964、manufacturer、intro/description/category 齐备 | ✅ |
| 2 | `runtime.json` | emulator="none"（demo_mode 起步）、output_sinks（indicator_lamps + internal_crt）、input_map 7 动作 | ✅ |
| 3 | `assemblies/*.gltf`（5 件） | console/cpu_cabinet/tape_drive/card_reader/printer，节点名=node_id | ✅ |
| 4 | `assemblies/MESHES.md` | 占位盒说明 + 真实尺寸依据 | ✅ |
| 5 | `annotations/annotations.json` | 50 条（控制台旋钮/灯组 Inspect 34 条 + 读卡机送卡 3 条 + 装配体 role + flow） | ✅ |
| 6 | `encyclopedia.md` | **2,501 汉字**（≥2500，兼容家族史/微程序/OS/360） | ✅ |
| 7 | `THIRD_PARTY.md` | 三件套齐全 | ✅ |

**校验结果（02 线 validate.py）**：

```text
总计 78 条：PASS 78，FAIL 0   （退出码 0）
```

关键规则全绿：R-002/R-003/R-004/R-005、R-060/R-061/R-062、R-070/R-071/R-089（era=1964）、R-086（input_map 对象格式）、R-090（glTF 节点名=node_id）。

## 3. 尺寸对照表（占位盒 vs 01_System360.md 档案）

| 占位盒 | 占位盒实际（单位盒） | 档案/真实尺寸（「需核实」） | 结论 |
|---|---|---|---|
| console.gltf | 1 m³（半长 0.5） | 双 CRT 操作台约 1.2 m 宽 × 1.0 m 高 | 占位几何，待替换 |
| cpu_cabinet.gltf | 同上 | 单机架约 0.6 m 宽 × 2 m 高 | 占位几何 |
| tape_drive.gltf | 同上 | IBM 2415 磁带机 ×2，单台约 1.5 m 高 × 0.8 m 宽 | 占位几何 |
| card_reader.gltf | 同上 | 读卡机约 1.0 m 宽 × 0.6 m 深 | 占位几何 |
| printer.gltf | 同上 | 行式打印机约 1.5 m 宽 × 1.2 m 高 | 占位几何 |

> 说明：占位盒仅几何占位；真实尺寸按资料写入 `assemblies/MESHES.md` 注释。IBM 2415 磁带机为 Model 30 典型外设（"2415 机型档案值"），正式建模以 IBM 各设备规格书为准。

## 4. Hercules 真跑衔接说明（仅预留接线，未下载）

| 项 | 说明 |
|---|---|
| 本包 emulator 取值 | `"none"`（demo_mode 起步）——因 Hercules 二进制未就位、且 01 线网关未注册 hercules，本包先以静态展示起步 |
| Hercules 许可 | QPL（OSI 认证，非 GPL），主站 `https://www.hercules-390.eu/` |
| 关键差异 | Hercules 原生模拟 S/370+，非逐周期仿真 System/360；用其跑 360 时代软件属"近亲演示"，须明示差异 |
| IBM OS 授权 | OS/360、MVS 等属 IBM Licensed Program，展陈须规避；建议用自由许可系统（z/Linux）或公共领域软件 |
| 预留接线 | 未来真跑路径：01 线注册 `hercules` 模拟器 → 03 线把 `runtime.emulator` 从 "none" 改为 "hercules" 并补 media 配置（本报告记录，不落地改动） |

## 5. 开放问题

1. **display/fps 字段仍未落地**（沿用 23-A 阻塞结论）：System/360 控制台灯组 + 双 CRT 的真实画面参数无法写入 runtime（schema 无 display 字段），待 02 线规范新增后回填。
2. **surface 命名**：本包灯组用 `indicator_lamps`（任务书指定），CRT 用 `internal_crt`；规范 §11.1 建议新包灯组用 `led`，属轻微命名不一致，可在全馆统一清理时收敛。
3. **"2415 机型"尺寸**：IBM 2415 磁带机精确尺寸与"×2 阵列"配置方式「需核实」，正式建模以 IBM 档案为准。
4. **Model 30 控制台精确布局**：本包按"双 CRT + 灯组 + 旋钮开关"通用配置建模，具体旋钮/灯位以 IBM 2150/1052 控制台档案为准（「需核实」）。
5. **Hercules 近亲演示的合规口径**：S/370≠S/360、IBM OS 授权两处红线，正式接入真跑前需法务确认（本包未下载、未内嵌任何 Hercules 二进制）。
