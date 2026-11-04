# TASK-17B 完成报告 — 规范 v0.2.1 勘误与键名全集定稿（含 TASK-17 两份总收尾）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本报告与配套文档按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-17B（02 线 第 2/2 份）：规范 v0.2.1 勘误与键名全集定稿 |
| 状态 | 完成 |
| 日期 | 2026-11-02 |
| 前置 | TASK-17A 完成（迁移助手） |

---

## 0. TASK-17 两份总收尾 + 02 线本轮完成标注

- **17-A**：`tools/migrate/migrate_package.py`（460 行，纯 stdlib）+ `tools/migrate/README.md` +
  四包演练 `tools/migrate/demo/` + `docs/TASK-17A_完成报告.md`（含 edsac R-090 定位）。
- **17-B**：`docs/内容包规范_v0.2.1.md`（全文）+ `docs/勘误记录_v0.2.1.md` + 一致性自检证据。
- **02 线本轮（TASK-17）完成**：迁移工具链落地 + 规范首个勘误版发布 + 键名全集定稿，
  两份目标均达成。schema/validate 无需变更，R-086 行为未回退。

---

## 1. 变更清单全表（v0.2.1，7 条）

| # | 位置 | 旧文 | 新文 | 缘由 |
|---|---|---|---|---|
| 1 | §11.2 input_map 形态 | 「两种形态」并列、legacy「继续接受」 | 对象格式为**推荐唯一新格式**；legacy 为 deprecated 兼容窗口（含移除触发条件） | DEFECT-M1B-KEYMAP-01 方案 A |
| 2 | §11.2 键名全集 | keyboard「`^KEY_[A-Z0-9_]+$`（见校验器正则）」 | keyboard Godot `KEY_*` 全集（字母序）+ 项目扩展 3 键；joystick/mouse 全集 | 键名全集定稿 |
| 3 | §11.3 对齐差异表 | 「PROTOCOL.md（v1）」「sink 路由 v1 未实现」 | 更新到网关 v2 现状（proto=2、§10、多 sink 已实现） | 网关已 v2 |
| 4 | 附录 C 迁移表 | name_en「保留但 deprecated」、input_map「结构化迁移」 | name_en 并入后删除；input_map 不在 migrate 工具机械范围 | 与 migrate 工具一致化 |
| 5 | §1.2 版本规则 | （无说明） | v0.2.1 为文档勘误，`spec_version` 仍 `"0.2"` | 澄清版本语义 |
| 6 | §11.1 surface 注释 | 「v0.1 存量包使用兼容项」 | 补充 03 线四包已迁移清零现状 | 与 TASK-18A 一致 |
| 7 | 附录 B 开放问题 2 | 「input_map 与网关 v2 对齐」 | 已裁决（方案 A），转 legacy 移除触发条件跟踪点 | DEFECT 已裁决关闭 |

## 2. 运行日志（原文）

### 2.1 run_tests.py（全绿）

```text
======================================================================
TASK-07 校验器测试（v0.2）
======================================================================
[PASS] 正例：content/test-device 全绿  — exit=0, 汇总「FAIL 0」
[PASS] 反例01：缺引用（component.assembly 悬空）→ R-014  — exit=1, 命中 R-014
[PASS] 反例02：循环父子（装配树成环）→ R-012  — exit=1, 命中 R-012
[PASS] 反例03：命名违规（节点 id 非 snake_case）→ R-021  — exit=1, 命中 R-021
[PASS] 反例04：缺 THIRD_PARTY.md → R-050  — exit=1, 命中 R-050
[PASS] 反例05：含未定标记文案（标注 text）→ R-060  — exit=1, 命中 R-060
[PASS] 反例06：transform 越界（scale 分量 = 0）→ R-032  — exit=1, 命中 R-032
[PASS] 反例07：materials 引用文件不存在 → R-017  — exit=1, 命中 R-017
[PASS] 反例08：timeline 结构非法（t 起止倒置）→ R-080  — exit=1, 命中 R-080
[PASS] 反例09：timeline 总时长超预算 → R-081  — exit=1, 命中 R-081
[PASS] 反例10：C4 级 anim 缺 caption → R-082  — exit=1, 命中 R-082
[PASS] 反例11：caption 含未定标记 → R-083  — exit=1, 命中 R-083
[PASS] 反例12：sink surface 非法枚举 → R-084  — exit=1, 命中 R-084
[PASS] 反例13：annotation.surface 未声明 → R-085  — exit=1, 命中 R-085
[PASS] 反例14：input_map 键名非法（key 非 KEY_*）→ R-086  — exit=1, 命中 R-086
[PASS] 反例20：legacy 令牌非法（大写点分）→ R-086  — exit=1, 命中 R-086
[PASS] 反例15：localized 缺 zh → R-087  — exit=1, 命中 R-087
[PASS] 反例16：name_en 与 name.en 不一致 → R-088  — exit=1, 命中 R-088
[PASS] 反例17：era 越界 → R-089  — exit=1, 命中 R-089
[PASS] 反例18：glTF 网格节点名与 node_id 不符 → R-090  — exit=1, 命中 R-090
[PASS] 反例19：THIRD_PARTY 行 URL 非法 → R-091  — exit=1, 命中 R-091
----------------------------------------------------------------------
结果：PASS 21，FAIL 0
（退出码 0）
```

### 2.2 validate.py（test-device 全绿）

```text
$ python tools/validate/validate.py content/test-device
...
PASS  R-091  THIRD_PARTY.md             THIRD_PARTY 行三件套（分档+URL+日期）合法
------------------------------------------------------------------------------
总计 54 条：PASS 54，FAIL 0
```

> **schema/validate 未改的说明**：本次勘误为条文/裁决层，schema 的
> `input_map.anyOf[input_descriptor, 字符串令牌]` 与 R-086 双形态逻辑已正确表达方案 A，无需改动；
> 上表为本次复跑证据，证明 R-086 行为无回退（反例 14/20 仍命中 R-086）。

## 3. 裁决记录

| DEFECT | 裁决 | 说明 |
|---|---|---|
| DEFECT-M1B-KEYMAP-01 | 方案 A | 对象格式为唯一新格式；legacy 兼容窗口；移除触发条件=全部量产包对象化+评审通过 |
| DEFECT-M1-ROLLBACK-01 | 归 01 线后端 | 运行时竞态，非内容契约，规范不改 |

## 4. 开放问题（legacy 移除触发条件的跟踪点）

1. **legacy 字符串移除触发点**（§11.2.2 / 附录 B 第 2 项）：待「03/05 线全部量产内容包
   input_map 对象化完成 + 项目评审通过」后，从 schema/校验器移除 legacy 字符串令牌，
   届时 R-086 仅接受 `{map,key}`。**当前不得收紧**。
   - 现状盘点：05 线 apple-ii 已对象化（57 键）；03 线 manchester-baby/eniac/edsac/edvac
     仍为 legacy 字符串（迁移归 03 线后续任务 / 或 02 线后续提供 input_map 迁移工具）。
2. **项目扩展键规范化**：`KEY_POWER`/`KEY_RESET`/`KEY_REPEAT` 为设备语义动作扩展（非 Godot
   枚举），后续可考虑在网关翻译层定义统一映射表，或收敛为更语义化的键名。
3. **键名全集与校验器正则会合**：规范全集为权威、校验器正则（`btn[0-9]+` 等）为宽松兜底，
   后续若需严格对齐，可在 schema 增加枚举（需先完成存量包对象化，避免回退）。
4. **media_hint 多介质 / 资产预算数字 / accuracy_level 归一**：沿用 v0.2 遗留开放问题（附录 B）。

---

## 附：本轮全部交付物

| 文件 | 说明 |
|---|---|
| `tools/migrate/migrate_package.py` | 迁移助手（460 行） |
| `tools/migrate/README.md` | 用法/对照表/边界 |
| `tools/migrate/demo/` | 四包演练副本（apply 后 v0.2 全绿） |
| `docs/TASK-17A_完成报告.md` | 17-A 完成报告（含 edsac R-090 定位） |
| `docs/内容包规范_v0.2.1.md` | 规范勘误版（全文） |
| `docs/勘误记录_v0.2.1.md` | 裁决结论 + 勘误理由 + 受影响文件清单 |
| `docs/TASK-17B_完成报告.md` | 本报告（两份总收尾） |
