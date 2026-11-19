# THIRD_PARTY.md — 第三方资产许可清册

> Commodore Amiga 1000 设备包（TASK-208-A 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| UAE / FS-UAE 模拟器 | 软件 | licensed | https://fs-uae.net/ | 2026-11-15 | 运行方案参考（`runtime.emulator="uae"` 预留），GPL 进程隔离，未内嵌二进制 |
| Wikipedia — Amiga 1000 | 文档（索引） | cc | https://en.wikipedia.org/wiki/Amiga_1000 | 2026-11-15 | 史实底稿与百科文案，仅转述未复制 |
| Wikipedia — Amiga | 文档（索引） | cc | https://en.wikipedia.org/wiki/Amiga | 2026-11-15 | Amiga 家族史与三芯片组参考 |
| Computer History Museum — Amiga | 文档（索引） | visual_reference_only | https://www.computerhistory.org/ | 2026-11-15 | 史实交叉核对，仅视觉参考 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **UAE GPL 隔离声明**：UAE 为 GPL 许可，集成走「独立进程 + 协议通信隔离」（不链接、不派生），运行不构成本项目代码的许可传染；**随仓库分发 UAE 二进制须另行法律评估，故本仓库不随附**（二进制由用户自备进 slots）。
- **Kickstart ROM 红线**：Amiga 的 Kickstart ROM 受版权保护，**不入库、不下载、不提供、不再分发**，只做清单级引用；真跑时 Kickstart ROM 与磁盘镜像由用户按合规渠道自备（详见 `docs/research/hall-personal-batch2/12_Amiga1000产包口径卡.md`）。
