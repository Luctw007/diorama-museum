# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `edsac`（EDSAC，电子延迟存储自动计算器）设备内容包中所有资产的来源与许可信息。

> 许可分档四档（见《内容包规范 v0.1》第八章）：`公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；自产/原创资产标注为 `原创`。第三方资产**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| whole.gltf / console.gltf / delay_line_bank.gltf / crt_display_unit.gltf | 网格 | 原创 | - | - | TASK-12-A 自产占位盒几何（单位盒，仅作装配占位） |
| encyclopedia.md / meta.json / runtime.json / annotations.json 中的全部中文文案 | 文案 | 原创 | - | - | 依据 03 线 hall-dawn 调研转述撰写，未照搬原文 |
| QEdsac（模拟器，C++/Qt5） | 软件依赖 | 授权许可 | https://github.com/qedsac/qedsac | 2026-10-31 | 运行时 `emulator` 声明的候选模拟器；仅登记接入，未下载源码/二进制；许可证与版本需在正式接线前核实 |
| Warwick 大学 EDSAC 模拟器（Martin Campbell-Kelly） | 软件/文档 | 仅视觉参考 | http://www.dcs.warwick.ac.uk/~edsac/ | 2026-10-31 | 免费闭源，仅作外链/界面参考 |
| TNMOC — EDSAC 复刻项目 | 文档/网页 | 仅视觉参考 | https://www.tnmoc.org/edsac | 2026-10-31 | 机架划分与复刻进度的文字转述来源 |
| An Ultrasonic Memory Unit for the EDSAC（Wilkes & Renwick） | 文档 | 公共领域 | http://www.cs.man.ac.uk/CCS/Archive/misc/EDSAC/ElectronicEngineeringRawTifs.pdf | 2026-10-31 | 水银延迟线原理的文字转述依据（1940s 原始论文） |
| EDSAC Order Code（David Wheeler，剑桥） | 文档/网页 | 仅视觉参考 | https://www.cl.cam.ac.uk/relics/orders.notes.html | 2026-10-31 | 17 位指令集定义的转述来源 |
| Wikipedia — EDSAC | 文档/网页 | CC | https://en.wikipedia.org/wiki/EDSAC | 2026-10-31 | 仅作索引，事实均转述 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-12-A 自产内容，不包含任何真实设备的扫描、照片或受版权保护的材料。
- 「授权许可」条目（QEdsac）为软件依赖登记，本包**未下载、未嵌入**其任何源码或二进制；其许可证与版本需在正式接线前核实。
- 「仅视觉参考」条目仅作事实转述与参数依据，未使用其原始图片/文本资产。
