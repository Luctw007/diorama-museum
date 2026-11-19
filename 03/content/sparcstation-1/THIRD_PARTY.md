# THIRD_PARTY.md — 第三方资产许可清册

> Sun SPARCstation 1 设备包（TASK-213-A 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — SPARCstation | 文档（索引） | cc | https://en.wikipedia.org/wiki/SPARCstation | 2026-11-16 | 史实底稿与百科文案，仅转述未复制 |
| Wikipedia — Sun Microsystems | 文档（索引） | cc | https://en.wikipedia.org/wiki/Sun_Microsystems | 2026-11-16 | Sun 公司史参考 |
| Computer History Museum — SPARCstation | 文档（索引） | visual_reference_only | https://www.computerhistory.org/ | 2026-11-16 | 史实交叉核对，仅视觉参考 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **QEMU sparc 需核实声明**：QEMU 的 sparc 目标为 SPARCstation 的候选后端，但许可与成熟度「需核实」，且 01 线无 qemu 槽位，故本包 `runtime.emulator="none"`（静态 + 动画演示，不写 qemu 后端）。
- **SunOS/Solaris 镜像红线**：SunOS/Solaris 系统镜像受版权保护，**不入库、不下载、不提供、不再分发**，只做清单级引用；真跑时镜像由用户按合规渠道自备（详见 `docs/research/hall-workstation/03_SPARCstation1产包口径卡.md`）。
