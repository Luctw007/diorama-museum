# TASK-76A 完成报告（docs/TASK-76A_完成报告.md）

> 01 线 · 2026-11-04 · 任务：网关注册表与槽位扫描区折叠为单一真相源（解决 71-B 开放问题 1）。

## 1. 交付物

| 文件 | 改动 |
|---|---|
| `slots/emulators/mame-apple2/manifest.json` | 新建：mame 后端声明（binary_env=MAME_BIN、media_classes=[disk]、keymap 引用） |
| `slots/emulators/simh-pdp8/manifest.json` | 新建：simh 后端声明（binary_env=SIMH_PDP8_BIN、media_classes=[firmware]） |
| `scripts/slot_loader.py` | +ALIASES/canonical()（mame→mame-apple2、simh→simh-pdp8）；+builtin_entries()（延迟导入网关注册表）；slots_available() 重写为合并视图（内置优先、补缺字段不覆盖）；--list 标注"（后端模块预留）" |
| `scripts/launch_lib.py` | decision_chain 统一走合并视图：三态判定（未建立 / 后端预留 / 二进制就位或未就位） |
| `scripts/emulator_doctor.py` | 槽位检查行标注后端预留；guide 复用 binary_hint/binary_env |
| `slots/README.md` | 新增"单一真相源（TASK-76A）"一节 |

## 2. 验收日志（原文）

```text
$ python scripts/slot_loader.py --list
fake-slot          OK(native,无二进制要求)          样例槽位…  [MIT（本仓库自带）]
mame-apple2        MISSING(无二进制)              MAME apple2 驱动骨架…  [MAME 上游 GPLv2+/BSD-3…]
fake               OK(native,无二进制要求)          测试用假模拟器…  [MIT（本仓库自带）]
simh-pdp8          MISSING(无二进制)（后端模块预留）      SIMH PDP-8…  [SIMH 许可（需核实…）]
介质目录 0 个

$ python scripts/launch_device.py --device apple-ii --dry-run
  emulator=mame  demo_mode=False  category=computer
  slot 提示: mame → mame-apple2（media_class=? bios_hint=?）
  决策: 二进制未就位 → EMULATOR_BINARY_MISSING + doctor 指引: 把二进制放入 third_party\mame\mame 或设环境变量 MAME_BIN
  （不再出现"槽位未建立" ✔）

$ python scripts/launch_device.py --device pdp8 --dry-run
  决策: 后端模块未实现（预留槽位）→ 暂不可真跑；可选 demo 预览（--force-demo）或等待后端

$ $env:MAME_BIN=…mame_drill.bat; launch_device --device apple-ii --dry-run
  决策: 槽位 mame-apple2 二进制就位（D:\work\01\repo\slots\_drill\mame\mame_drill.bat）→ 真实后端（管线待后端实现）

$ python scripts/verify_all.py --daily --cache
结果：27/27 通过（含 slot_consistency_check PASS：完工包 22，SC-01 违规 0）
```

## 3. 迭代记录

- 轮 1：builtin_entries 直接 `from gw import gateway` 失败（scripts 运行时 sys.path 无 repo 根）→
  加 `sys.path.insert(0, REPO)` 修复；该轮曾出现 mame-apple2 被标"OK(native)"的误判，修复后归位 MISSING。

## 4. 开放问题

- 合并视图内内置 "fake" 与槽位 "fake-slot" 并存（一个测试后端两个 id），无害但可在规范里明确二者关系；
- pdp8 运行时 emulator=simh-pdp8 直接命中规范名，无需 alias；未來内容包统一写语义名（mame/simh）后 alias 才生效——建议 02 线在 v0.6.2 增补中规定运行时 emulator 字段的规范写法。