# godot/content/ — 设备内容包登记

多设备加载器（`scripts/device_loader.gd` v2）枚举本目录下每个子文件夹为一个设备包。
下表由 `scripts/sync_content.py`（TASK-16B）自动生成；`meshes` 数据为 glTF 文件数。

## 包清单与校验

| device-id | 名称 | 来源（原位） | validate |
|---|---|---|---|
| altair-8800 | ? | `D:\work\03\repo\content\altair-8800` | FAIL 0（通过） |
| amiga500 | ? | `D:\work\03\repo\content\amiga500` | FAIL 0（通过） |
| apple-ii | ? | `D:\work\05\repo\content\apple-ii` | FAIL 0（通过） |
| atari-2600 | ? | `D:\work\05\repo\content\atari-2600` | FAIL 0（通过） |
| atari-st | ? | `D:\work\03\repo\content\atari-st` | FAIL 0（通过） |
| bbcmicro | ? | `D:\work\03\repo\content\bbcmicro` | FAIL 0（通过） |
| commodore64 | ? | `D:\work\03\repo\content\commodore64` | FAIL 0（通过） |
| dynatac-8000x | ? | `D:\work\03\repo\content\dynatac-8000x` | FAIL 0（通过） |
| edsac | ? | `D:\work\03\repo\content\edsac` | FAIL 0（通过） |
| edvac | ? | `D:\work\03\repo\content\edvac` | FAIL 0（通过） |
| eniac | ? | `D:\work\03\repo\content\eniac` | FAIL 0（通过） |
| famicom | ? | `D:\work\05\repo\content\famicom` | FAIL 0（通过） |
| game-boy | ? | `D:\work\05\repo\content\game-boy` | FAIL 0（通过） |
| ibm5150 | ? | `D:\work\03\repo\content\ibm5150` | FAIL 0（通过） |
| iphone | ? | `D:\work\03\repo\content\iphone` | FAIL 0（通过） |
| macintosh128k | ? | `D:\work\03\repo\content\macintosh128k` | FAIL 0（通过） |
| manchester-baby | ? | `D:\work\03\repo\content\manchester-baby` | FAIL 0（通过） |
| neo-geo-mvs | ? | `D:\work\05\repo\content\neo-geo-mvs` | FAIL 0（通过） |
| next | ? | `D:\work\03\repo\content\next` | FAIL 0（通过） |
| nokia-3310 | ? | `D:\work\03\repo\content\nokia-3310` | FAIL 0（通过） |
| palm-pilot | ? | `D:\work\03\repo\content\palm-pilot` | FAIL 0（通过） |
| pdp11 | ? | `D:\work\03\repo\content\pdp11` | FAIL 0（通过） |
| pdp8 | ? | `D:\work\03\repo\content\pdp8` | FAIL 0（通过） |
| pet2001 | ? | `D:\work\03\repo\content\pet2001` | FAIL 0（通过） |
| sega-md | ? | `D:\work\05\repo\content\sega-md` | FAIL 0（通过） |
| sfc | ? | `D:\work\05\repo\content\sfc` | FAIL 0（通过） |
| system360 | ? | `D:\work\03\repo\content\system360` | FAIL 0（通过） |
| trs80-model1 | ? | `D:\work\03\repo\content\trs80-model1` | FAIL 0（通过） |
| vax11 | ? | `D:\work\03\repo\content\vax11` | FAIL 0（通过） |
| vic20 | ? | `D:\work\03\repo\content\vic20` | FAIL 0（通过） |
| x68000 | ? | `D:\work\03\repo\content\x68000` | FAIL 0（通过） |
| zx-spectrum | ? | `D:\work\03\repo\content\zx-spectrum` | FAIL 0（通过） |

## 目录包（catalog bundle，61-A 流水线自动再生）

- 目录行数 1582 / 分片 24 / 生成 2026-11-10T01:24:41（`res://content/catalog/`）


## 字段齐备性自查表（loader 视角，自动探测）

| device-id | meta.json | runtime | annotations.json | glTF | encyclopedia.md | input_profile.json | 备注 |
|---|---|---|---|---|---|---|---|
| altair-8800 | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| amiga500 | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |
| apple-ii | ✓ | runtime.json | ✓ | 4 | ✗ | ✓ |  |
| atari-2600 | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| atari-st | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |
| bbcmicro | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |
| commodore64 | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |
| dynatac-8000x | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| edsac | ✓ | runtime.json | ✓ | 4 | ✓ | ✓ |  |
| edvac | ✓ | runtime.json | ✓ | 3 | ✓ | ✓ |  |
| eniac | ✓ | runtime.json | ✓ | 4 | ✓ | ✓ |  |
| famicom | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| game-boy | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| ibm5150 | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| iphone | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |
| macintosh128k | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| manchester-baby | ✓ | runtime.json | ✓ | 4 | ✗ | ✓ |  |
| neo-geo-mvs | ✓ | runtime.json | ✓ | 7 | ✓ | ✗ |  |
| next | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| nokia-3310 | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| palm-pilot | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| pdp11 | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |
| pdp8 | ✓ | runtime.json | ✓ | 4 | ✓ | ✗ |  |
| pet2001 | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| sega-md | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| sfc | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| system360 | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |
| trs80-model1 | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |
| vax11 | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |
| vic20 | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| x68000 | ✓ | runtime.json | ✓ | 6 | ✓ | ✗ |  |
| zx-spectrum | ✓ | runtime.json | ✓ | 5 | ✓ | ✗ |  |

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
