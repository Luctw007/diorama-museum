# THIRD_PARTY.md — 第三方资产许可清册

本文件记录 `manchester-baby`（曼彻斯特 Baby / SSEM）设备内容包中所有资产的来源与许可信息。

> 说明：许可分档四档（见《内容包规范 v0.1》第八章）：
> `公共领域`（public_domain）、`CC`（cc）、`授权许可`（licensed）、`仅视觉参考`（visual_reference_only）；
> 自产/原创资产标注为 `原创`。第三方资产**必须**填写「来源 URL」与「获取日期」。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| whole.gltf / cabinet.gltf / store_crt_unit.gltf / switch_panel_unit.gltf | 网格 | 原创 | - | - | TASK-08 自产占位盒几何（单位盒，仅作装配占位，非真实设备模型） |
| meta.json / runtime.json / annotations.json 中的全部中文文案 | 文案 | 原创 | - | - | 依据 03 线 hall-dawn 调研转述撰写，未照搬任何原文 |
| davidpsharp/baby（模拟器，GPL-3.0） | 软件依赖 | 授权许可 | https://github.com/davidpsharp/baby | 2026-10-31 | 运行时 `emulator` 声明的目标模拟器；仅登记接入，未下载源码/二进制 |
| Manchester Baby 在线模拟 | 文档/网页 | 仅视觉参考 | https://manchesterbaby.com | 2026-10-31 | 仅作接入与界面参考，未使用其任何资产 |
| The Baby: The World's First Stored-Program Computer (billp.org) | 文档 | 仅视觉参考 | http://www.billp.org/baby.pdf | 2026-10-31 | 技术参数与 CRT 存储结构的文字转述来源，未下载粘贴 |
| History of Information — Baby 首程序 | 文档/网页 | 仅视觉参考 | https://www.historyofinformation.com/detail.php?id=672 | 2026-10-31 | 首程序事实（17 指令/52 分钟）的转述来源 |
| Wikipedia — Manchester Baby | 文档/网页 | CC | https://en.wikipedia.org/wiki/Manchester_Baby | 2026-10-31 | 仅作索引，未整段引用；事实均转述 |

## 声明

- 本包内所有几何、文案、运行时配置均为 TASK-08 自产内容，不包含任何真实设备的扫描、照片或受版权保护的材料。
- 上表「授权许可」条目（davidpsharp/baby）为软件依赖登记，本包**未下载、未嵌入**其任何源码或二进制；接入方式见 runtime.json 的 `emulator` 字段与完成报告。
- 「仅视觉参考」条目仅作事实转述与参数依据，未使用其原始图片/文本资产。
