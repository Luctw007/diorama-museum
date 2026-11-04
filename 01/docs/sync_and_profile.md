# 内容同步与输入映射规则（docs/sync_and_profile.md）

> TASK-16B 交付。两个可运行工具：`scripts/sync_content.py`（03/05 线 → Godot 工程内容同步+
> 校验+登记）与 `scripts/gen_input_profile.py`（runtime.input_map → 玩家层 input_profile.json 骨架）。

## 1. 同步规则（sync_content.py）

| 项 | 规则 |
|---|---|
| 源 | 固定清单 `SOURCES`（03 线 4 包 + 05 线 apple-ii；新增包在此登记） |
| 目标 | `godot/content/<device-id>`，全量覆盖（`dirs_exist_ok`），排除 `__pycache__` |
| 校验 | 复制后对目标跑 02 线校验器；FAIL>0 → 该包标记失败并计入退出码 |
| 登记 | 重写 `godot/content/README.md`：包清单+validate 结果表、字段齐备性自动探测表（meta/runtime/annotations/glTF 数/encyclopedia/input_profile） |
| 保留 | 目标目录中源不存在的文件（如生成的 input_profile.json）不删除（copytree 合并语义） |
| 预览 | `--dry-run` 仅打印计划；退出码 0 |

## 2. 默认宿主绑定规则（gen_input_profile.py，两层键名模型 §5 落地）

| input_map 形态 | 推导 | 区段 |
|---|---|---|
| 对象 `{map:keyboard, key:KEY_A}` | `key_a`（KEY_ 剥除转小写） | keyboard |
| 对象 `{map:joystick, key:axis_x}` | `joy_axis_x` | actions |
| 对象 `{map:joystick, key:btn0}` | `joy_button_0` | actions |
| 对象 `{map:mouse, key:…}` | `mouse_button_left` 等 | mouse |
| legacy 令牌 `keyboard.key_a` | `key_a`（leaf 已是 key_ 形原样保留） | keyboard |
| legacy 令牌 `panel.*` / `panel.switch.*` | 空字符串 → unbound 清单 | actions |
| 其余无法推导 | 空字符串 → unbound 清单 | actions |

## 3. 与 04 线输入可视化（07 号文档）的衔接

- `unbound` 清单即"需要在设置界面给玩家自定键的动作集"——04 线的绑定设置界面对接
  `input_profile.json` 时，先渲染 unbound 顶部置顶；baby（36 个 store_bit_xx 面板开关）
  应引导玩家用"整面板快捷切换"而不是逐键绑定（04 线 01 号文档依赖的交互语义）。
- `input_profile.gd` 的 `actions/keyboard/mouse` 三表结构与产物完全一致；额外顶层键
  （unbound/note）对 loader 安全（load_from_json 只取三表）。

## 4. 给玩家的默认键位表模板（示例，apple-ii）

- 字母/数字：键名同字符（`key_a`…`key_0`）；
- 转盘（paddle_axis_0/1）：手柄左摇杆 X/Y；双人 paddle_axis_2/3 复用同一摇杆（待玩家设置界面分流）；
- 按钮（paddle_btn_N）：手柄按钮 0/1/2；
- 早期面板机（baby/eniac/edsac/edvac）：全部 unbound，进设置界面按面板分区绑定。

## 5. 红线与收尾

- 两工具均不写 03/05 源仓（gen 默认目标为 godot/content 副本；sync 只读源）；
- 生成物 input_profile.json 属于**玩家层配置**，不入内容包 v0.2 规范（02 线 R 规则
  判定为包外文件，校验器不受影响——已实测 5 包 0 FAIL）。