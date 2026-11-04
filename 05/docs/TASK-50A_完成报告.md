# TASK-50A 完成报告（手机/手持/家电模拟器生态调研）

> 任务：TASK-50A（05 线 1/2）· 里程碑 M1 · 前置：任务 45 完成。
> 完成日期：2026-11-04 · 类型：清单级调研（零下载）。

---

## 一、交付物与字数统计（实测 CJK）

| 文件 | 内容 | 字数 |
|---|---|---|
| `emu-eco/00_手机手持家电_模拟器生态_v1.md` | 三大类生态调研 + 接入难度分级 + media_class 建议 | 6003（≥6000 达标） |

## 二、生态结论表（类目 × 可运行性）

| 类目 | 可运行性 | 模拟器 | 许可 | 后端 | 接入量级 |
|---|---|---|---|---|---|
| Symbian / N-Gage | 可运行（有限） | EKA2L1 | GPL-3.0 | custom | 需自定义 |
| 旧 Nokia S30/S40 | 展示向 | 无 | — | 无 | 不可行 |
| Game & Watch | 可运行 | MAME 手持驱动 + MADrigal sim | GPL-2.0+/`[需核实]` | mame/custom | 现成协议/需自定义 |
| Palm OS | 可运行 | CloudpilotEmu（POSE 后继） | GPL-3.0 | custom | 需自定义 |
| iPhone OS 早期 | 展示向 | 无（QEMU 实验） | — | 无 | 不可行 |
| VCD/DVD 播放器 | 展示向 | 无 | — | 无 | 不可行（合成演示） |

## 三、给 01/02 线槽位实现的分级输入

建议 media_class 采用**三级**（而非两级）：

| media_class | 适用 | 后端 |
|---|---|---|
| `runnable_mame` | Game & Watch（MAME 驱动） | mame |
| `runnable_custom` | Symbian（EKA2L1）、Palm OS（CloudpilotEmu）、G&W 网页 sim | custom |
| `static_anim` | iPhone 早期、旧 Nokia、VCD/DVD | 无 |

接入优先级：P0 Game & Watch（现成协议）、P1 Palm OS（CLI 有进程对接潜力）、P2 Symbian（无 headless，视 spike 定去留）。

## 四、开放问题（对应调研 §七 E1–E6）

1. EKA2L1 是否有 headless 接口（接入可行性）。
2. 旧 Nokia S30/S40 是否有小众开源模拟器。
3. QEMU 早期 iOS 启动成熟度。
4. MADrigal 等 G&W sim 的许可与维护状态。
5. CloudpilotEmu CLI 进程级接入可行性。
6. MAME G&W 手持驱动覆盖机型清单。

> 以上均记入调研 §七「需核实」集中列表，正式接入前逐条核验（含对 EKA2L1/CloudpilotEmu 的技术 spike，同 13 号模式）。

## 五、TASK-50 两份收尾标注

本份（50-A）完成；50-B（G&W 建模卡）见 `console-batch2/09_GW_建模任务卡.md` 与 `TASK-50B_完成报告.md` 的总收尾。
