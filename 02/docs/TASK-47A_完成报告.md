# TASK-47A 完成报告（02 线 1/2）：槽位契约规范章 v0.5

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-47A（02 线 1/2）：槽位契约规范章 v0.5（manifest 与媒体组织立法） |
| 前置 | TASK-42（音频校验器 + 13 包复验）；与 01 线 46-A 并行 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `docs/规范v0.5_槽位契约章草案.md` | 槽位契约章草案（含全量 schema） | **8075 汉字**（≥8000 达标）、715 行 |
| `docs/TASK-47A_完成报告.md` | 本报告 | — |

## 二、规范内容覆盖核对（对照 47-A 任务逐项）

| 任务要求 | 落点 | 达成 |
|---|---|---|
| manifest.json schema 逐字段定义 | §2.2 字段总表 + §2.3~2.11 逐字段 | ✅ |
| slot_id | §2.3 | ✅ |
| device_class 枚举（7 项） | §3.1 | ✅ |
| backend_type 枚举 | §3.2 | ✅ |
| binary（相对路径 + 多架构允许表） | §2.6 | ✅ |
| binary_env | §2.7 | ✅ |
| media_class 支持表（每类 1-2 行示例 + 扩展名约定） | §3.3（8 类全表） | ✅ |
| license 三件套（槽位级，挂钩 licenses/） | §2.9 | ✅ |
| capabilities（frame/audio/input/save 四能力位） | §2.10 | ✅ |
| 媒体目录组织 + 嵌套规则 + 空槽位 README 模板 | §4.1 / §4.2 | ✅ |
| 安全与红线（不下载、哈希清单、来源三件套介质级） | §5 | ✅ |
| 与 EMULATORS 注册表、keymap 注册衔接条款 | §6 | ✅ |
| 15 包 slot 回填建议表 | §7 + §7.1（分批建议） | ✅ |

额外增补：§1.4 设计原理、§1.5 与既有规范关系、§1.6 术语、§八 三场景演练、§九 常见错误对照、
§十 FAQ、附录 C 术语表、附录 D 设计决策记录、结语。

## 三、与 01 线 46-A 实现的对齐核对表（46-A 已交付）

| # | 项 | 46-A 实现 | 本规范 | 结论 |
|---|---|---|---|---|
| 1 | backend_type 枚举 | native/mame/simh/stella/mesen/mobile/dedicated（7 项） | 同 7 项（吸收 native） | 采纳一致 |
| 2 | device_class 枚举 | computer/console/handheld/phone/pda/dedicated_av/other | 同 | 采纳一致 |
| 3 | media 目录第三级 | `<slot_id>`（media_dirs 实现） | `<slot_id>` | 采纳（46-A 任务文 `<device_id>` 记为笔误） |
| 4 | license 字段 | 字符串（对拷 entry.license） | 三件套对象 + 简写字符串 | 需 46-A 补对象→字符串序列化 |
| 5 | binary 多架构 | 单 string + .exe 变体探测 | string 或 object 多架构表 | 需 46-A 补 object 分支 |
| 6 | capabilities | 未实现 | 四能力位 | 需 46-A/46-B 补读 |
| 7 | media 目录嵌套 | 三层 media/class/dc/slot | 同 | 一致 |

**关键裁决（写入规范附录 D）**：
- **D1** 吸收 `native`（6→7 项）：fake/demo 槽位需要"仓库自带、零二进制"语义；
- **D2** 介质第三级定为 `slot_id` 而非 `device_id`：介质挂靠"哪个槽位"而非"哪个设备包"；
- **D3** 许可双形态（三件套对象 + 简写字符串）：样例轻、生产严；
- **D4** 专用后端统一 `dedicated`：避免枚举随专用模拟器数量无限膨胀；
- **D5** capabilities 缺省全 false：宁可保守少承诺。

## 四、15 包 slot 回填建议表（交 03/05 线，不改他线文件）

| # | device-id | 当前 emulator | 建议 backend_type | device_class | 建议 media_class | 建议 slot_id |
|---|---|---|---|---|---|---|
| 1 | manchester-baby | davidpsharp-baby | dedicated | computer | （无） | manchester-baby |
| 2 | edsac | qedsac | dedicated | computer | tape | edsac |
| 3 | edvac | none | （不声明） | computer | （无） | — |
| 4 | eniac | none | （不声明） | computer | （无） | — |
| 5 | pdp8 | simh-pdp8 | simh | computer | tape | pdp8 |
| 6 | pdp11 | none | simh（预留） | computer | disk | pdp11 |
| 7 | vax11 | none | simh（预留） | computer | disk | vax11 |
| 8 | system360 | none | dedicated（预留） | computer | tape | system360 |
| 9 | apple-ii | mame | mame | computer | disk | apple-ii |
| 10 | ibm5150 | pc86box | dedicated | computer | disk | ibm5150 |
| 11 | commodore64 | vice | dedicated | computer | tape | commodore64 |
| 12 | bbcmicro | beebem | dedicated | computer | tape | bbcmicro |
| 13 | famicom | mesen | mesen | console | cartridge | famicom |
| 14 | sega-md | blastem | dedicated | console | cartridge | sega-md |
| 15 | atari-2600 | stella | stella | console | cartridge | atari-2600 |

回填分批建议（§7.1）：第一批 4 包（apple-ii/pdp8/famicom/atari-2600，规范后端已就位）、
第二批 6 包（专用后端待模块化）、第三批 5 包（静态/预留）。

## 五、消耗条款核对

| 条款 | 达成 |
|---|---|
| schema 全量逐字段表 | §2.2 字段总表 + 逐字段展开 ✅ |
| 媒体类目 + 设备类目两大枚举表齐全 | §3.1/§3.2/§3.3 ✅ |
| 字数统计 | 8075 汉字（≥8000）✅ |
| 迭代 ≥2 轮 | 初稿 → 补设计原理/术语/演练/FAQ → 补术语表/决策记录/结语，多轮扩写 ✅ |

## 六、开放问题

1. **backend_type 的 `dedicated` 是否拆分**（VICE/BeebEm/BlastEm/PC-86 逐一命名 vs 统一 dedicated）。
2. **license 简写字符串的存废**（正式版是否强制三件套对象）。
3. **capabilities 与 demo_mode 的关系**（需 46-B 落地后对齐）。
4. **多架构表的运行时选择**（loader 按宿主平台选 binary 变体，46-A 未实现）。
5. **介质来源三件套登记位置**（README.md vs 独立 SOURCES.md）。
6. **`runtime.slot` 回填触发点**（15 包回填 + 评审后，`runtime.emulator` 是否退役）。
7. **46-A 三处规范超前项**（license 对象序列化 / binary 多架构 / capabilities 读取）已写入回写建议，待 01 线后续迭代补齐。
