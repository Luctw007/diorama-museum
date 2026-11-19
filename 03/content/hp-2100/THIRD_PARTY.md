# THIRD_PARTY.md — 第三方资产许可清册

> HP 2100 设备包（TASK-188-A 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Open SIMH HP 2100 模拟器 | 软件 | licensed | https://github.com/open-simh/simh | 2026-11-13 | 运行方案参考（`runtime.emulator` 预留），未内嵌二进制，许可【需核实】 |
| Wikipedia — HP 2100 | 文档（索引） | cc | https://en.wikipedia.org/wiki/HP_2100 | 2026-11-13 | 史实底稿与百科文案，仅转述未复制 |
| Wikipedia — HP 2116A | 文档（索引） | cc | https://en.wikipedia.org/wiki/HP_2116A | 2026-11-13 | HP 2116A 谱系史实参考 |
| Computer History Museum — HP 2100 | 文档（索引） | visual_reference_only | https://www.computerhistory.org/ | 2026-11-13 | 史实交叉核对，仅视觉参考 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **未下载任何 ROM / 纸带 / 固件 / 二进制**：`runtime.emulator="simh-hp2100"` 仅为槽位预留字符串，本包不携带 SIMH 二进制。
- **模拟器预留接线说明**：Open SIMH HP 2100（许可【需核实】）为 HP 2100 的真跑候选后端，槽位走 `reserved` 预留；「可玩」建议用自研复刻程序（拨键装小程序 + 指示灯反馈）承载，不依赖原机固件（详见 `docs/research/hall-mainframe/10_HP2100.md`）。
