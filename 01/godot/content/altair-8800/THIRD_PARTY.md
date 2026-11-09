# THIRD_PARTY.md — 第三方资产许可清册

> MITS Altair 8800 设备包（TASK-178-A 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Open SIMH Altair 8800 模拟器 | 软件 | licensed | https://github.com/open-simh/simh | 2026-11-10 | 运行方案参考（`runtime.emulator` 预留），未内嵌二进制，许可【需核实】 |
| Wikipedia — Altair 8800 | 文档（索引） | cc | https://en.wikipedia.org/wiki/Altair_8800 | 2026-11-10 | 史实底稿与百科文案，仅转述未复制 |
| Wikipedia — S-100 bus | 文档（索引） | cc | https://en.wikipedia.org/wiki/S-100_bus | 2026-11-10 | S-100 总线史实参考 |
| Wikipedia — Altair BASIC | 文档（索引） | cc | https://en.wikipedia.org/wiki/Altair_BASIC | 2026-11-10 | 微软首款产品史实参考 |
| Computer History Museum — Altair 8800 | 文档（索引） | visual_reference_only | https://www.computerhistory.org/ | 2026-11-10 | 史实交叉核对，仅视觉参考 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **Altair BASIC 版权红线**：Altair BASIC 是微软的首款产品，版权受保护，本包**未下载、未提供任何 Altair BASIC 磁带/纸带镜像或固件**。
- **未下载任何 ROM / 固件 / 二进制**：`runtime.emulator="simh-altair8800"` 仅为槽位预留字符串，本包不携带 SIMH 二进制。
- **模拟器预留接线说明**：Open SIMH Altair 8800（许可【需核实】）为 Altair 8800 的真跑候选后端，槽位走 `reserved` 预留；「可玩」建议用自研复刻程序（拨键装小程序 + 跑灯反馈）承载，不依赖原机固件（详见 `docs/research/hall-personal-batch2/09_Altair8800.md`）。
