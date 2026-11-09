# THIRD_PARTY.md — 第三方资产许可清册

> TRS-80 Model I 设备包（TASK-78A 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — TRS-80 | 文档（索引） | cc | https://en.wikipedia.org/wiki/TRS-80 | 2026-11-04 | 综合参数参考，仅转述未复制 |
| Wikipedia — Zilog Z80 | 文档（索引） | cc | https://en.wikipedia.org/wiki/Zilog_Z80 | 2026-11-04 | CPU 参数参考 |
| trs80gp 模拟器 | 软件 | licensed | https://48k.ca/trs80gp.html | 2026-11-04 | 运行方案参考（预留），未内嵌二进制，许可【需核实】 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **ROM/系统红线**：TRS-80 Model I 的 Level I/Level II BASIC ROM 与软件磁带镜像属受版权保护固件/软件，本包**未下载、未提供任何 ROM 或镜像**；真跑时获取与授权单独走合规流程。
- **模拟器预留接线说明**：trs80gp（Freeware【需核实】）与 MAME trs80 驱动（GPL）为 TRS-80 的真跑候选后端，二选一暂不落地；`runtime.emulator` 当前为 `"none"`（demo_mode 起步），槽位走 dedicated 预留（详见 `docs/research/trs80-model1_简报.md`）。
