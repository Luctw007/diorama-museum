# TASK-34A 完成报告（04 线 1/2 · 大型机厅导览台本 v1）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。
> 完成日期：2026-11-03 ｜ 执行线：04 线（未修改 01/03 线任何文件）

## 1. 交付物与字数统计

| 文件 | 字数（去空白） |
|---|---|
| `docs/design/22_大型机厅导览台本_v1.md` | 全文 9,560；§3 解说词区段 2,958（含 trigger 标记，纯口播 ≈2,320）≥2200 达标 |
| 其中 §8 测试用例 | T-200~T-219 共 20 条 ≥18 达标（手工 14/待实机 4/自动化 2） |

迭代口径：v1.0 第 1 轮；§8 用例反查（T-203 对 §2 站 2 C3、T-204 对站 3 可玩点、T-216 对 §5）为第 2 轮。

## 2. 与 03 线导语/四包 annotations 的衔接表

| 台本站 | 03 线依据 | 引用条目 | 缺口 |
|---|---|---|---|
| 站 1 总导语 | 08_展厅导语_v1 §一 5 段 | —（文案改写为口播） | bgm_hall_mainframe（M7） |
| 站 2 S/360 | 导语 §二 S/360 + 01_System360.md | console/cpu_cabinet/tape_drive/card_reader/printer/`ipl_flow`/`card_feed_flow`/microprogram_rom/lamp 组 18 条 | 灯组演示驱动（M3）、anim 无（M2） |
| 站 3 PDP-8 | 导语 §二 PDP-8 + 02_PDP8.md | panel/core_memory_rack/core_stack/`manual_program_flow`/sw_data_00~11 | 操机小程序（M4）、anim 无（M2） |
| 站 4 PDP-11 | 导语 §二 PDP-11 + 03_PDP11.md | cpu_cabinet/disk_rk05/tape_tu10/unibus_rack/`unibus_flow`/`boot_flow`/mmu/unibus_backplane | 终端演示（M5）、anim 无（M2） |
| 站 5 VAX-11 | 导语 §二 VAX-11 + 04_VAX11.md | （无包——白模+名牌占位） | **包全缺（M1）**、概念动画（M6） |
| 站 6 出口 | 导语 §三时间线/§四三问 | — | 招牌（M9） |

## 3. 需补清单（22 号 §6 全文，M1~M9）

M1 VAX-11 包未生产（最高优先）；M2 三包全无 anim 条目；M3 灯组驱动数据；M4 PDP-8 操机小程序；M5 PDP-11 终端演示；M6 VAX 页表搬页动画；M7 bgm_hall_mainframe；M8 narr 六条配音；M9 占位资产与招牌。

## 4. 事件 id 与 20 号音频表对齐记录（22 号 §4 摘要）

既有 id 复用 8 类（sfx_enter_hall/exit_hall/page/slider_tick/badge/power_on/key_single/key_repeat、amb_cabinet、bgm_exit）；新增 8 条（bgm_hall_mainframe 1 + narr_mf_* 6 + 站 4 命令雨无音特效标注）——全部在 22 号 §4 逐行登记，新增项回填 20 号需补章节由 29-B 后置处理。

## 5. 开放问题

1. VAX-11 包未产前，站 5 是否以「预挂牌 + 白模」先上（台本已按可先上设计）；
2. PDP-8/PDP-11「可玩点」的交互实现依赖 34-B 绑定同源逻辑，两任务并行交付时的联调节奏；
3. 大机柜仰角 −15° 的取值与讲解板 3 m/0.8 m 位置待实机校准；
4. 站 4 命令雨走带 [需实机核对] 的视觉密度（防眩）；
5. 「个人计算机厅」未定名，出口招牌文案随 03 线后续展馆定名联升；
6. bgm_hall_mainframe 未进 20 号正文（本报告登记），待 29-B 音频规格升版时并入。