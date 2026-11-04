# THIRD_PARTY.md — 第三方资产许可清册

> Amiga 500 设备包（TASK-68B 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — Amiga 500 | 文档（索引） | cc | https://en.wikipedia.org/wiki/Amiga_500 | 2026-11-04 | 综合参数参考，仅转述未复制 |
| Wikipedia — Original Chip Set | 文档（索引） | cc | https://en.wikipedia.org/wiki/Original_Chip_Set | 2026-11-04 | 三芯片组架构参考 |
| FS-UAE 模拟器 | 软件 | licensed | https://fs-uae.net/ | 2026-11-04 | 运行方案参考（预留），未内嵌二进制，GPLv2 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **ROM/系统红线**：Amiga 500 的 Kickstart ROM 与 Workbench 系统盘属受版权保护固件/软件，本包**未下载、未提供任何 ROM 或系统镜像**；真跑时获取与授权（如经 Amiga Forever 等授权渠道）单独走合规流程。
- **FS-UAE 预留接线说明**：FS-UAE（GPLv2，本次已核实）为 Amiga 500 的真跑预留后端，`runtime.emulator` 当前为 `"none"`（demo_mode 起步）；待 01 线注册 UAE 后端并完成 Kickstart ROM 合规后，再回填 `runtime.emulator` 并接线真跑（见 TASK-68B 报告）。
