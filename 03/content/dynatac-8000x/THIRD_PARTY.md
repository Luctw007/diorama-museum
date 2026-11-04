# THIRD_PARTY.md — 第三方资产许可清册

> Motorola DynaTAC 8000X 设备包（TASK-98A 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — Motorola DynaTAC | 文档（索引） | cc | https://en.wikipedia.org/wiki/Motorola_DynaTAC | 2026-11-05 | 综合参数参考，仅转述未复制 |
| Wikipedia — Martin Cooper (inventor) | 文档（索引） | cc | https://en.wikipedia.org/wiki/Martin_Cooper_(inventor) | 2026-11-05 | 1973 首通电话史实参考 |
| Computer History Museum — Timeline | 文档（索引） | visual_reference_only | https://www.computerhistory.org/timeline/ | 2026-11-05 | 年代定位参考，仅查阅未复制 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **模拟器行**：**无成熟模拟器 → 演示向。** DynaTAC 8000X 无任何可用模拟器（1G 模拟 AMPS 网络 + 专有固件，生态空白）。演示方案走「芯片级原理示意 + 铃声/按键合成交互」，引用 04 线 29 号通用设备互动规格的合成方案；真跑不可行，不做真跑预留。
- **固件红线**：DynaTAC 的基带固件与射频参数属专有版权，本包**未下载、未提供任何固件或镜像**；`runtime.emulator` 为 `"none"`（演示向起步），槽位无模拟器预留（详见 `docs/research/hall-phone/01_DynaTAC8000X.md` 研究卡）。
