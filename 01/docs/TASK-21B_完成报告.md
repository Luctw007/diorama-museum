# TASK-21B 完成报告（docs/TASK-21B_完成报告.md）

> 01 线 · 2026-11-02 · 任务：多设备展厅调度层（展陈布局 + Godot 宿主 + 校验工具）。
> 本报告含 TASK-21 两份总收尾，01 线本轮（任务 21-A/B）完成。

## 1. 交付物与规模

| 文件 | 行数 | 说明 |
|---|---|---|
| `godot/scripts/exhibit_host.gd` | 300 | 展厅宿主：布局加载/多设备放置/运行配额(默认1)/围观圈/导览推进/高亮与调试圈 |
| `scripts/layout_check.py` | 107 | 布局 JSON 校验（L-01~L-04），正负用例实测 |
| `godot/content/exhibit_dawn.json` | — | 样例布局：黎明厅 4 台（slot 1-4，20×12 大厅） |
| `docs/exhibit_layout_spec.md` | ≥1500 字 | L1 schema、04 线坐标系对照、运行预算、导览衔接 |
| `scripts/sync_content.py` + `godot/content/README.md` | — | README 模板新增"待验证清单（引擎侧）"节（同步时不丢失） |

## 2. 运行日志（layout_check 正/负用例）

```text
$ python scripts/layout_check.py godot/content/exhibit_dawn.json
布局合法：黎明厅（Dawn Hall），设备 4 台（大厅 20.0×12.0，包清单 6 个）   → rc=0

$ python scripts/layout_check.py <负例：id=not-exist>
  [FAIL] L-02 devices[0].id=not-exist 不在 godot/content（现有: apple-ii, edsac,
         edvac, eniac, manchester-baby, test-device）
布局校验失败：1 条                                     → rc=1
```

## 3. 迭代记录（2 轮）

1. **轮 1**：负例文件用 PowerShell Out-File 产生 UTF-8 BOM → json.load 炸在读取层 → 校验器改用 `utf-8-sig` 读取（记事本保存的布局也能过）；
2. **轮 2（静态自查）**：捕获笔误 `ImmediateGeometry`（Godot 3 遗留类）→ 改为 Godot 4.x 的 `ImmediateMesh`；补 `_ready` 调试圈自动开关逻辑。

## 4. 静态自查清单（Godot 实机前的逐项打勾）

| # | 项 | 结果 |
|---|---|---|
| 1 | 类名/类型存在性：Node3D/Quaternion/BoxMesh/StandardMaterial3D/MeshInstance3D/ImmediateMesh/BaseMaterial3D/FileAccess | ✓ 均为 Godot 4.x 内置 |
| 2 | `preload("res://scripts/device_loader.gd")` 路径 | ✓（与现有工程脚本同址） |
| 3 | 依赖 API 与 device_loader.gd 实际签名一致（load_device/get_index/get_meta/get_runtime/get_assembly_nodes） | ✓（grep 逐项核对） |
| 4 | 语法要点：类型化 Dict/Array、sort_custom lambda、maxi/TAU/deg_to_rad | ✓ 均 Godot 4 合法 |
| 5 | 布局 JSON 字段与 layout_check 规则一致（L-01~L-04） | ✓ 正例实测通过 |
| 6 | 缩进统一（4 空格）、无 Tab 混用 | ✓ |

## 5. 与 04 线坐标系的对照结论

布局采用"米制、+Y 上、-Z 进深"；与 04 线 03 号俯视网格的换算（横向→+X、纵向→-Z、
朝向角→`rotation.y` 逆时针）已写入 spec §2 并**收敛到单点函数**（`_apply_entry_transform`）——
04 线若改网格原点，只需改这一处 + layout_check 边界判断（spec §2 已标注）。

## 6. 开放问题

1. exhibit_host 全部为静态交付：`load_device` 的占位盒降级、导览高亮、围观圈判定待 Godot 实机（README 待验证清单 #5）；
2. 运行配额 acquire_run 目前是纯内存纪律——将来"多机同屏演示"需要网关侧并发测试（m1 已有多设备并发能力，接入时为每台设备独立画面投放即可复用）；
3. exhibit_dawn.json 的站位坐标是初稿（按 04 线 03 号动线粗放），待 04 线 24-B 导览台本 v2 落地后回填精调。

## 7. TASK-21 两份总收尾 + 01 线本轮完成标注

- 21-A：m2a_check.py 双轨（fake 10/10 全绿；mame 轨二进制缺失 1 PASS + 5 SKIP、rc=0 不误红），
  过程中对齐协议字段（frame_ready/audio_chunk/save_state_ack）并加固 recv 洪水防护；
- 21-B：展厅调度层三层件（宿主脚本/布局规格/校验工具）+ 样例布局 + README 待验证清单常驻化；
- 01 线本轮（任务 21）完成。