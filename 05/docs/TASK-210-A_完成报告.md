# TASK-210-A 完成报告（第二批第 8 台 Apple IIe 设备包）

> 任务 210-A（05 线）· 完成日期：2026-11-14。

## 交付
`content/apple-iie/`（meta.json + runtime.json + assemblies/ 6 件 gltf + MESHES.md + annotations/annotations.json + encyclopedia.md + THIRD_PARTY.md）；目录 `计算机大类_目录_v2.jsonl` + `_v2.md` 新建 Apple IIe 条目（id=C-PC-000208）；本报告。

## 核对清单自查（对应任务第 4 章）

**1. validate.py → 全 PASS / 0 FAIL**：
```
总计 80 条：PASS 80，FAIL 0   → rc=0
```
**2. model_check.py → MR-01~04 全过**：6 件 gltf 均 `MR-01 根节点 name=node_id 一致 / MR-02 三角面 156–168 ≤20000 / MR-03 无贴图合规 / MR-04 扩展白名单内`，`FAIL 0`，rc=0 ✅。
**3. verify_all.py --only pkg:apple-iie → 全 PASS**：
```
== [pkg:apple-iie] validate.py ...apple-iie
   总计 80 条：PASS 80，FAIL 0
   pkg:apple-iie  PASS  FAIL 0  → 结果 1/1 通过，rc=0
```
**4. 目录新建+回填后复测**：
```
catalog_ingest.py --from-work --gate → [catalog] 摄取 5 文件 1583 行，错误 0，rc=0
catalog_ref_check → REF-01 悬空 0 / REF-02 反链缺失 0 / REF-04 形态非法 0；FAIL 0
```
新条目 jsonl 原文（id=C-PC-000208 无重复，grep 计数=1）：
```json
{"id": "C-PC-000208", "name": "Apple IIe", "aliases": ["Apple //e"], "manufacturer": "Apple", "origin": "美国", "era": 1983, "taxonomy_path": ["计算机", "个人机", "8 位家用"], "influence": "Apple II 系列增强型，长寿产品线中坚。", "status": "done", "device_id": "apple-iie", "verify": false, "sources": ["S58A"], "research_doc": "docs/research/hall-personal-batch2/11_AppleIIe.md"}
```

## 六件 gltf 顶点数自检
whole 112 / case 112 / keyboard 112 / monitor 104 / floppy 104 / power_supply 104（均 >100 且 <4000）；节点名 = node_id；baseColorFactor 纯色无贴图。

## 「需核实」清单
- 尺寸（主机约 40×12×40 cm）、主频（约 1 MHz）、内存（64/128 KB）沿用研究卡 [S116] 标「需核实」，只进 encyclopedia/MESHES，不进 role/flow。
- MAME apple2e 驱动许可「需核实」（runtime 保守写 `mame`）。
- Apple IIe ROM（Monitor ROM + Applesoft BASIC）红线：不入库、不下载、只清单级引用。

## 红线遵守
不下载 ROM/磁盘镜像/二进制/固件；尺寸/主频无源标「需核实」；只改 05 线 `content/apple-iie/` + 报告 + 03 线目录 v2 两个文件；未碰 01/02/04 线；目录版本唯一治理（只在活跃「计算机 v2」新增，未新建版本文件）。
