# godot/content/ — 设备内容包登记

多设备加载器（`scripts/device_loader.gd` v2）枚举本目录下每个子文件夹为一个设备包。
下表由 `scripts/sync_content.py`（TASK-16B）自动生成；`meshes` 数据为 glTF 文件数。

## 包清单与校验

| device-id | 名称 | 来源（原位） | validate |
|---|---|---|---|
| apple-ii | ? | `D:\work\05\repo\content\apple-ii` | FAIL 0（通过） |
| atari-2600 | ? | `D:\work\05\repo\content\atari-2600` | FAIL 0（通过） |
| bbcmicro | ? | `D:\work\03\repo\content\bbcmicro` | FAIL 0（通过） |
| commodore64 | ? | `D:\work\03\repo\content\commodore64` | FAIL 0（通过） |
| edsac | ? | `D:\work\03\repo\content\edsac` | FAIL 0（通过） |
| edvac | ? | `D:\work\03\repo\content\edvac` | FAIL 0（通过） |
| eniac | ? | `D:\work\03\repo\content\eniac` | FAIL 0（通过） |
| famicom | ? | `D:\work\05\repo\content\famicom` | FAIL 0（通过） |
| ibm5150 | ? | `D:\work\03\repo\content\ibm5150` | FAIL 0（通过） |
| macintosh128k | ? | `D:\work\03\repo\content\macintosh128k` | FAIL 0（通过） |
| manchester-baby | ? | `D:\work\03\repo\content\manchester-baby` | FAIL 0（通过） |
| neo-geo-mvs | ? | `D:\work\05\repo\content\neo-geo-mvs` | FAIL 0（通过） |
| pdp11 | ? | `D:\work\03\repo\content\pdp11` | FAIL 0（通过） |
| pdp8 | ? | `D:\work\03\repo\content\pdp8` | FAIL 0（通过） |
| sega-md | ? | `D:\work\05\repo\content\sega-md` | FAIL 0（通过） |
| system360 | ? | `D:\work\03\repo\content\system360` | FAIL 0（通过） |
| vax11 | ? | `D:\work\03\repo\content\vax11` | FAIL 0（通过） |

## 目录包（catalog bundle，61-A 流水线自动再生）

- 目录行数 1484 / 分片 28 / 生成 2026-11-04T01:55:01（`res://content/catalog/`）


## 字段齐备性自查表（loader 视角，自动探测）

| device-id | meta.json | runtime | annotations.json | glTF | encyclopedia.md | input_profile.json | 备注 |
|---|---|---|---|---|---|---|---|
| apple-ii | ✓ | runtime.json | ✓ | 4 | ✗ | ✓ |  |
| atari-2600 | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| bbcmicro | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| commodore64 | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| edsac | ✓ | runtime.json | ✓ | 4 | ✓ | ✓ |  |
| edvac | ✓ | runtime.json | ✓ | 3 | ✓ | ✓ |  |
| eniac | ✓ | runtime.json | ✓ | 4 | ✓ | ✓ |  |
| famicom | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| ibm5150 | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| macintosh128k | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| manchester-baby | ✓ | runtime.json | ✓ | 4 | ✗ | ✓ |  |
| neo-geo-mvs | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| pdp11 | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| pdp8 | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| sega-md | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| system360 | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |
| vax11 | ✓ | runtime.json | ✓ | 0 | ✓ | ✗ |  |

## 人工备注区

<!-- 以下备注不参与自动生成，请人工维护 -->

- `test-device` 为 02 线示例包，不参与内容线同步；
- 正式 3D 资产到达前 glTF 均为占位盒；loader 加载失败时降级占位盒。

## 待验证清单（引擎侧，Godot 实机安装后逐项核对）

| # | 项 | 核对方式 |
|---|---|---|
| 1 | `device_loader.gd`：场景装载、Pack dScene→占位盒降级路径 | 运行工程任一设备包 |
| 2 | `inspect_controller.gd`：悬停高亮/点选/文案弹层 | 进入 Inspect 交互 |
| 3 | `explode_controller.gd`：CLOSED/OPENED/EXPLODED 状态机与位移公式 | 拆解交互 |
| 4 | `gateway_client.gd`：分片重组、画面投放内屏 CRT | 网关起 fake + 投放 |
| 5 | `exhibit_host.gd`（TASK-21B 静态交付）：load_layout/spawn_devices/get_tour_order/find_audience/acquire_run 全流程 | 装 Godot 后加载 exhibit_dawn.json |
| 6 | `input_profile.gd`：读取各包 input_profile.json 并渲染 unbound 清单 | 绑定设置原型 |

> 布局文件（exhibit_dawn.json 等）位于本目录但**不是设备包**，device_loader 扫描时按目录过滤。
