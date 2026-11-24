# TASK-270-A 完成报告

> 任务：Nintendo 64 低模样板 gltf（按 26 号预研卡）· 完成日期：2026-11-21。

## 一、交付物

新增 `content/nintendo-64/assemblies/` 下 8 件低模 gltf + `MESHES.md`，节点名 = node_id，baseColorFactor 纯色无贴图（全 0–1），均 >100 且 <4000 顶点。

| 文件 | node_id | 顶点数 | 材质数 |
|---|---|---|---|
| chassis.gltf | chassis | 120 | 5 |
| cartridge_slot.gltf | cartridge_slot | 104 | 5 |
| cartridge.gltf | cartridge | 104 | 5 |
| mainboard.gltf | mainboard | 104 | 5 |
| power_supply.gltf | power_supply | 104 | 6 |
| controller_port.gltf | controller_port | 104 | 6 |
| expansion_slot.gltf | expansion_slot | 104 | 5 |
| controller.gltf | controller | 104 | 5 |

## 二、第 4 章验收日志

1. **门禁只读复测**：`verify_all.py --daily --no-ref-hard` → **55/55 通过、rc=0** ✅（本机无 py -3.7，用 python 3.13；--cache 写网络盘被拒，以只读复测为准）。
2. **顶点数自检**：POSITION accessor count 为 120 / 104 / 104 / 104 / 104 / 104 / 104 / 104，均 >100 且 <4000 ✅。
3. **baseColorFactor 自检**：每件 ≥1 条且数值 0–1。配色沿用 26 号预研卡——chassis 深灰(0.20,0.20,0.22)、panel 深灰(0.30,0.30,0.32)、black 黑(0.05,0.05,0.06)、controller 深灰(0.30,0.30,0.32)、stick 摇杆灰(0.40,0.40,0.42)、red_led 红(0.90,0.20,0.10)、green 绿 PCB(0.08,0.25,0.12)、chip 芯片黑(0.05,0.05,0.05)、psu 银灰(0.60,0.62,0.65)、metal 银(0.72,0.74,0.78) ✅。
4. **改动清单自证**：本任务只新增 `nintendo-64\assemblies\` 8 件 gltf + MESHES.md + 本报告，无其它文件改动 ✅。

## 三、与任务书的漂移

1. **8 件拆分**：按 26 号预研卡拆分方案建 8 件（chassis/cartridge_slot/cartridge/mainboard/power_supply/controller_port/expansion_slot/controller），与任务书第 3 章完全一致；与 Saturn/PS 的「6 件 whole+5」口径不同，是 N64 拆分方案所致，非漂移。
2. **本机无 py -3.7**：改用 python 3.13（前述多轮已记录的环境事实）。

## 四、红线自检

未下载 ROM/BIOS/二进制/贴图（N64 BIOS/ROM 红线只清单级引用）；尺寸/配色沿用 26 号预研卡、无源处标 [需核实]；只改 05 目录；**未建** meta.json / annotations / 目录 jsonl（低模样板待产包轮次入链）；8 件 gltf JSON 解析 + base64 解码字节数 == byteLength 全 OK；cartridge/cartridge_slot（插拔）与 controller（模拟摇杆）已在 MESHES.md 标注识别件。

## 五、结论

Nintendo 64 低模样板 8 件 gltf 完成，为游戏机线第三台回归建模备好低模，全部验收通过。
