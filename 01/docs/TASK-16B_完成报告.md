# TASK-16B 完成报告（docs/TASK-16B_完成报告.md）

> 01 线 · 2026-11-02 · 任务：内容同步与输入映射生成（见 任务16-B 文档）。
> 本报告含"TASK-16 两份总收尾"（16-A 见 docs/TASK-16A_完成报告.md），01 线本轮（任务 16-A/B）完成。

## 1. 交付物与规模

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/sync_content.py` | 156 | 五包同步到 godot/content + 02 线校验 + README 登记表自动重写；`--dry-run`；失败退出码 |
| `scripts/gen_input_profile.py` | 148 | input_map → 玩家层 input_profile.json 骨架（对象/legacy 双形态；unbound 清单） |
| `docs/sync_and_profile.md` | — | 同步/绑定规则表、04 线衔接、默认键位模板 |
| `godot/content/README.md`（重写） | — | 包清单+validate 全通过表、字段齐备性自动探测表（含新 input_profile.json 列） |
| `godot/content/{五包}/input_profile.json` | — | 五份玩家层映射骨架（生成物） |

## 2. 运行日志（原文关键段）

```text
$ python scripts/sync_content.py
  manchester-baby  复制完成；validate 结果: FAIL 0（通过）
  eniac            复制完成；validate 结果: FAIL 0（通过）
  edsac            复制完成；validate 结果: FAIL 0（通过）
  edvac            复制完成；validate 结果: FAIL 0（通过）
  apple-ii         复制完成；validate 结果: FAIL 0（通过）
README 已重写: …\godot\content\README.md
同步汇总：5 包，失败 0

$ python scripts/gen_input_profile.py --all
  baby      动作 36；可自动绑定 0；unbound 36   （panel.* 面板开关，正确判为待绑定）
  eniac     动作 4； unbound 4
  edsac     动作 16；unbound 16
  edvac     动作 4； unbound 4
  apple-ii  动作 57；可自动绑定 57；unbound 0   （KEY_* 全量小写化 + 摇杆 joy_*）
```

apple-ii 产物样例（input_profile.json 头部）：

```json
{ "actions": { "paddle_axis_0": "joy_axis_x", "paddle_axis_1": "joy_axis_y",
    "paddle_btn_0": "joy_button_0" },
  "keyboard": { "key_a": "key_a", "key_b": "key_b", … } }
```

## 3. 迭代记录（≥2 轮）

1. **轮 1（dry-run）**：发现 legacy 令牌 `keyboard.key_a` 会生成 `key_key_a`（重复前缀）→ 补 leaf 前缀判断修复；
2. **轮 2（实跑前）**：gen 的目标目录原指向 03/05 源仓，恐跨线污染 → 改为 godot/content 副本，并在 sync 之后运行（先同步、后生成、再复核同步一次确认 input_profile.json 不会在后续同步被删）。

## 4. 复核结论

- 生成 input_profile.json 后重新 sync：五包 validate 仍然 **FAIL 0**（02 线校验器将 input_profile.json 视为包外文件，不受影响）；
- `godot/content/README.md` 登记表为五包全列 + validate 全通过（见该文件）。

## 5. 待验证清单 / 开放问题

1. Godot 实机仍未装——input_profile.gd 对生成 JSON 的加载路径待实机核对（README 中"待验证清单"沿用）；
2. 双人 paddle_axis_2/3 与单人 paddle_axis_0/1 共用同一摇杆的问题，需 04 线在绑定设置界面做"玩家槽位切换"（已写入 sync_and_profile.md §4）；
3. baby 36 个 store_bit 开关建议"面板区批量绑定"而非逐键——转 04 线下一轮输入可视化迭代。

## 6. TASK-16 两份总收尾

- 16-A：verify_all.py 全链路门禁（m0/m1/m1b/pkg/daily 全绿）；mame_apple2.py 骨架 + 注册表 + 许可/放置文档；m2_assert_draft.md 三里程碑断言（fake 先行双轨）；网关回归无回归。
- 16-B：sync_content.py / gen_input_profile.py 两个可运行工具 + 五包同步登记 + 五份玩家层映射骨架。
- 01 线本轮（任务 16）完成。