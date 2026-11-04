# TASK-11A 完成报告：三台真实设备包集成到 Godot

> 01 线 · 2026-10-31 · 执行位置 `D:\work\01\repo`

## 1. 交付物清单（路径 + 行数）

| 文件 | 行数 | 说明 |
|---|---|---|
| `godot/content/manchester-baby/`、`eniac/`、`apple-ii/` | — | 从 03/05 线复制（原文不动）；登记表见下 |
| `godot/content/README.md` | 25 | 包清单 + 字段齐备性自查表 + 结构要点 + 内容线需修清单 |
| `godot/scripts/device_loader.gd`（v2 重写） | 231 | 多设备索引 / object 形 transform 兼容 / 内联 role / components 挂载 / 降级表 |
| `godot/scripts/device_picker.gd` | 116 | HUD 设备选择面板（图鉴条目态、自动绑定 DeviceRoot） |
| `godot/README.md`（更新） | — | 新节点图、操作说明 |

## 2. 复制与字段自查（摘要，全表见 content/README.md）

| device-id | meta | runtime | annotations | meshes | encyclopedia.md |
|---|---|---|---|---|---|
| manchester-baby | ✓ | ✓（双写，一致） | ✓ | 4 glTF | ✗（缺，报内容线） |
| eniac | ✓ | ✓（runtime.json） | ✓ | 4 glTF | ✓ |
| apple-ii | ✓（顶层 $schema 忽略） | ✓ | ✓ | 4 glTF | ✗（缺，报内容线） |

抽查 `manchester-baby/meshes/whole.gltf`：nodes[0].name == "whole"，与装配体 id 对应 ✓（占位盒阶段）。

## 3. 关键设计决策（device_loader v2）

1. **transform 双形态兼容**：内容线实际产出为对象形 `{translation,rotation,scale}`（非旧扁平数组）——v2 主读对象形，同时保留扁平数组旧兼容；rotation 以 Quaternion(w,x,y,z) 解读；
2. **role 内联优先**：`assemblies[].role` / `components[].role` 直接携带"在整机"文案，逐一写入 `_role_by_node`（InspectController 悬停显示）；annotations.json 为 flow/anim 内容层；
3. **components 物理挂载**：component 节点按 `.assembly` 引用挂到所属装配体下（零件清单/未来点选可达）；
4. **降级表**：缺 meta → 索引置灰不可加载；缺 mesh_ref 或 glTF 未导入 → 占位盒 + push_warning；缺 annotations → 软跳过；
5. **不硬编码设备 id**：索引全部来自目录枚举，字段按规范名读取。

## 4. 内容线需修清单（不改他线文件，交 03/05 线）

1. `manchester-baby`、`apple-ii` 缺 `encyclopedia.md`（eniac 有）→ 统一约定：建议内容线补齐或 02 线规范明确该文件必/可选；
2. runtime 未声明画面宽高/帧率（01 线已用缺省表过渡，见 11-B 报告）；
3. apple-ii meta.json 顶层 `$schema` 相对路径在包内无 schema 文件（校验在 02 线侧执行，引擎无影响，供知悉）。

## 5. 待实机验证清单（安装 Godot 后逐项）

- [ ] 索引枚举：4 包均入图鉴且 test-device/manchester-baby/eniac/apple-ii loadable=true；
- [ ] Tab 图鉴选择装载各设备、置灰逻辑；
- [ ] 占位盒树与悬停点选 role 文案显示；
- [ ] glTF 正式资产到达后 PackedScene 路径替换无需改代码。

## 6. 开放问题

1. 多包切换时旧节点树即时释放策略（当前 queue_free 下一帧生效，切换瞬间两树并存一帧）；
2. 根装配体 `parent:null` 直接挂 DeviceRoot 下——未来展厅摆放需要"设备台座"包装层（与 04 线 03 号布局文档衔接）。