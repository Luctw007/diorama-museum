# THIRD_PARTY.md — 第三方资产许可清册

> Macintosh 128K 设备包（TASK-58B 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — Macintosh 128K | 文档（索引） | cc | https://en.wikipedia.org/wiki/Macintosh_128K | 2026-11-04 | 综合参数参考，仅转述未复制 |
| Wikipedia — Motorola 68000 | 文档（索引） | cc | https://en.wikipedia.org/wiki/Motorola_68000 | 2026-11-04 | CPU 参数参考 |
| Mini vMac 模拟器 | 软件 | licensed | https://www.gryphel.com/c/minivmac/ | 2026-11-04 | 运行方案参考（预留），未内嵌二进制，许可分档【需核实】 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **ROM/系统红线**：Macintosh 128K 的 64KB 系统 ROM 与 System 1.0/MacWrite/MacPaint 等系统软件属受版权保护固件/软件，本包**未下载、未提供任何 ROM 或系统镜像**；真跑时获取与授权单独走合规流程。
- **Mini vMac 预留接线说明**：Mini vMac（GPL 许可【需核实】）为 Macintosh 128K 的真跑预留后端，`runtime.emulator` 当前为 `"none"`（demo_mode 起步）；待 01 线注册 Mini vMac 后端并完成 ROM 合规后，再回填 `runtime.emulator` 并接线真跑（见 TASK-58B 报告）。
