# THIRD_PARTY.md — 第三方资产许可清册

> Apple iPhone（初代）设备包（TASK-108A 生产）。本包全部网格资产（`assemblies/*.gltf`）为**原创占位盒**，不包含任何第三方二进制资产。
> 下列行登记本包**引用为参考来源**的第三方资料（用于文案与技术参数，非再分发资产）。

| 资产 | 类型 | 许可分档 | 来源 URL | 获取日期 | 说明 |
|---|---|---|---|---|---|
| Wikipedia — iPhone (first generation) | 文档（索引） | cc | https://en.wikipedia.org/wiki/IPhone_(first_generation) | 2026-11-05 | 综合参数参考，仅转述未复制 |
| Wikipedia — Multi-touch | 文档（索引） | cc | https://en.wikipedia.org/wiki/Multi-touch | 2026-11-05 | 多点触控原理参考 |
| Wikipedia — iOS | 文档（索引） | cc | https://en.wikipedia.org/wiki/IOS | 2026-11-05 | iPhone OS / iOS 脉络参考 |

## 声明
- 本包未包含任何无授权或版权不明的第三方资产；`assemblies/*.gltf` 均为原创占位盒（8 顶点 / 12 三角面）。
- 上表第三方条目仅作**清单级引用**（文字转述 + 出处），未下载、未再分发任何受版权保护的图片、文本全文或二进制。
- **模拟器行**：**无成熟模拟器 → 演示向。** iPhone 初代无可用模拟器（iOS 闭源 + 专有固件 + 硬件加密），`runtime.emulator` 为 `"none"`（demo 通道起步）。演示走「静态展陈 + 多点触控原理动画 + 铃声/解锁交互合成」；**触屏仿真预留**：未来若接入触屏仿真后端再回填 emulator 字段。
- **iOS/固件红线**：iPhone 的 iPhone OS（iOS）系统镜像与基带固件属苹果专有版权，本包**未下载、未提供任何系统镜像或固件**；真跑/仿真时获取与授权单独走合规流程（详见 `docs/research/hall-phone/03_iPhone初代.md` 调研）。
