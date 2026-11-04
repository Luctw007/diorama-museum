# DEFECT-M1B-KEYMAP-01 （m1b_check apple-ii 键名契约漂移 · 归 05/01 线）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 编号 | DEFECT-M1B-KEYMAP-01（用例 T-025/026 前置 · m1b_check 第 1 组断言） |
| 轮次 | round_1（2026-10-31）→ round_2（2026-11-02，04 线独立复测闭环） |
| 档位 | 自动化（m1b_check） |
| 状态 | closed（round_2 复测通过，契约对齐已验证） |
| 归口 | 05 线（apple-ii 内容包 input_map 新格式）+ 01 线（scripts/run_profile.py 映射桥）双线裁决 |

## 1. 失败断言描述

```
M1b 验收失败 ✘  ->  apple-ii：57 键全部合法（未知 57）
```

断言：`len(m_apple["keys"]["unknown"]) == 0`（m1b_check.py L208）——实际 57/57 判未知。

## 2. 现场事实

`run_profile.py` 对 apple-ii 的输出：

```text
设备 apple-ii（apple2）  模式: 可运行（接线候选 mame）
  键名: 共 57 个，未知 57
    [未知键] key_a -> {'map': 'keyboard', 'key': 'KEY_A'}
    [未知键] key_b -> {'map': 'keyboard', 'key': 'KEY_B'}
    ...
```

## 3. 根因（已确证，读取共享盘当前文件）

apple-ii 内容包（05 线，并行会话已更新）的 `input_map` 值已从**字符串点分格式**升级为**对象格式**：

```json
"key_a": { "map": "keyboard", "key": "KEY_A" }      // 当前（新）
"key_a": "keyboard.key_a"                            // 此前（旧，manchester-baby 仍为此格式）
```

而 01 线 `scripts/run_profile.py` 的校验仍是字符串规则：

```python
LOGICAL_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$")
token = str(v)   # dict 被 str() 成 "{'map': 'keyboard', 'key': 'KEY_A'}" → 不匹配
```

- manchester-baby（36 键旧格式）通过，apple-ii（57 键新格式）全判未知——**契约漂移局部发生**。
- 联动影响：08 号 T-025/026（输入映射可视化）、T-037~040（向导）、06 号 §3.2 映射规则表、09 号 §6 消息字段核对表均以旧字符串格式为基准，需随裁决结果同步升版。

## 4. 裁决建议（供两线拍板，本线不改任一侧）

- 方案 A（推荐）：02 线规范 v0.2 明确 input_map 对象格式为唯一格式 → 01 线 run_profile 支持 `{"map","key"}`（并保留旧字符串兼容窗口）→ 03 线 baby 包同步升本格式。
- 方案 B：05 线回退字符串格式，规范 v0.2 再定。成本低但放弃 MAME 键名映射的真实诉求（大写 MAME 键名 KEY_A 更贴近真实模拟器）。
- 无论何案：m1b_check apple 断言（首键 token "keyboard.key_a" 期望）与 T-025/026 用例文本需同轮更新。

## 5. 贴证物与备注

- 完整输出：`design/rounds/m1b_round_1.log`。
- 依据 09 号 §4：m1b 失败归 02/03/05 线内容包与 run_profile；本轮 m1b 红灯，按漏斗规则其关联手工档（T-009/025/026/037~042 内容包依赖组）执行前必须先解决本缺陷。

## 6. round_2 复测结果（2026-11-02 · 04 线独立复测）

### 6.1 复测结论

**通过（PASS）** —— 方案 A 裁决已落地为 01 线实现 + 05 线包态不变：apple-ii 57 键 unknown==0，首键断言 `key_a -> {keyboard: KEY_A}`（对象形态）通过；对象/legacy 双形态在五包全量校验中无漂移。

### 6.2 通过证据

| 证据 | 值 | 日志 |
|---|---|---|
| m1b_check（17334） | **19/19 断言全过** | `design/rounds/m1b_round_2.log` |
| apple-ii 键名 | 57 键全部合法（未知 0）；首键 `key_a -> {keyboard: KEY_A}`（对象形态） | 同上 |
| baby 键名 | 36 键全部合法；首键 `power -> panel.power`（legacy 形态，兼容窗口生效） | 同上 |
| eniac | demo_mode 判定正确；indicator_lamps → led | 同上 |
| 五包 `--json` 键名校验 | baby 36 / eniac 4 / edsac 16 / edvac 4 / apple-ii 57，**unknown 全部为 0**，无漂移 | `design/rounds/run_profile_round_2.log`（全文） |
| m1_check ×2（17333，同轮旁证） | 42/42 连续 2 轮 | `design/rounds/m1_round_2_run{1,2}.log` |

### 6.3 关闭说明

1. **01 线映射桥已实现对象形态**（方案 A 落地）：`scripts/run_profile.py` 新增 `MAP_KEY_RE` 全类键名规则（L35-40）与 `_key_entry` 对象分支（L84-89）——`{map:"keyboard", key:"KEY_A"}` 按 keyboard 正则 `^KEY_[A-Z0-9_]+$` 校验；legacy 字符串令牌走 `LOGICAL_KEY_RE` 兼容窗口，两个窗口并存且互不影响（五包实测佐证）。
2. **m1b_check apple 断言已随裁决更新**：未知键断言保持 `unknown==0`（L208-210），首键断言改为对象形态期望 `key_a -> {keyboard: KEY_A}`（L211-214），与 02 线 v0.2 R-086 双形态语义一致（02 线《真实包校验报告》§3 同证三包双形态全过）。
3. **用例文本同轮升版（04 线职责）**：08 号 T-025/026 操作步骤与验证点已按对象形态重写（见 08 号 v2.0 变更清单）。
4. **漏斗解锁**：本缺陷闭环后，T-009/025/026/037~042 内容包依赖组按 08 号 §4.1 恢复执行资格。
5. 处置方式：无需提级（09 号 §4 提级路径未触发）；04 线未修改 01/05 线任何文件。

### 6.4 状态

**open → closed**（INDEX 同步更新）。