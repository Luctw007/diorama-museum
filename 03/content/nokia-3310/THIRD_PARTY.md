# THIRD_PARTY.md — 第三方资产许可清册

> Nokia 3310 设备包（TASK-173-B 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — Nokia 3310 | 文档（索引） | cc | https://en.wikipedia.org/wiki/Nokia_3310 | 2026-11-08 | 综合参数参考，仅转述未复制 |
| Wikipedia — Nokia | 文档（索引） | cc | https://en.wikipedia.org/wiki/Nokia | 2026-11-08 | 诺基亚公司脉络参考 |
| Wikipedia — SMS | 文档（索引） | cc | https://en.wikipedia.org/wiki/SMS | 2026-11-08 | 短信（SMS）技术参考 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **模拟器行**：**静态 + 原理动画（演示向）。** Nokia 3310 为功能机（非 Symbian），无成熟专用模拟器；Symbian/MAME 手持等候选许可一律【需核实】，`runtime.emulator` 为 `"none"`（demo 通道起步），槽位 **reserved 预留**，不下载二进制。
- **固件红线**：Nokia 手机固件受版权保护，本包**未下载、未提供任何固件或 ROM**；「贪吃蛇 II」可玩建议用自研复刻小游戏承载（不依赖原机固件），真跑/仿真时获取与授权单独走合规流程（详见 `docs/research/hall-phone/02_Nokia8110_3310.md` 研究卡）。
