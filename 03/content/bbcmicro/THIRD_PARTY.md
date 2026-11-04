# THIRD_PARTY.md — 第三方资产许可清册

> BBC Micro 设备包（TASK-43A 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — BBC Micro | 文档（索引） | cc | https://en.wikipedia.org/wiki/BBC_Micro | 2026-11-04 | 综合参数参考，仅转述未复制 |
| Wikipedia — MOS Technology 6502 | 文档（索引） | cc | https://en.wikipedia.org/wiki/MOS_Technology_6502 | 2026-11-04 | CPU 参数参考 |
| BeebEm 模拟器 | 软件 | licensed | http://www.mkw.me.uk/beebem/ | 2026-11-04 | 运行方案参考，未内嵌二进制 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **ROM 红线**：BBC Micro 的 BBC BASIC/MOS ROM 属受版权保护固件，本包**未下载、未提供任何 ROM**；真跑时 ROM 获取与授权单独走合规流程。BeebEm 真跑仅作预留接线说明（见 TASK-43A 报告）。
