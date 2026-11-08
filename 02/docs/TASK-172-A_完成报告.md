# TASK-172-A 完成报告：v0.1 发布收尾——开源社区化配套

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。

## 一、交付物清单

| # | 路径 | 状态 | 说明 |
|---|---|---|---|
| 1 | `docs/CONTRIBUTING.md` | 终版修订 | 82-A v1 → 终版，5 修订点落地，2748 汉字 |
| 2 | `tools/contrib_kit/build_content_manifest.py` | 新建 | 183 行，纯 stdlib，只读扫描 + 黑名单自检 |
| 3 | `docs/贡献者自测包说明_v1.2.md` | 新建 | 1299 汉字，gd_naming_check 转"已落地" + 清单脚本化 |
| 4 | `docs/自测包内容清单_v1.2.md` | 脚本生成 | 10 条目，违规 0（由交付物 2 生成） |

## 二、CONTRIBUTING 修订点 1~5 逐条落点

1. **发布门禁入口**：§〇「门禁在哪」补 `01/repo/01/scripts/release_check.py`（发布闸，R1 验收基线 /
   R2 三槽位三许可 / R3 完工包 ≥30，rc=0 方可封版），保留 `verify_all.py`（每日门禁 37 步）。
2. **目录行字段表**：§一「1.1 字段表」13 键 → **14 键**，新增 `media_class`（v0.6.1 可选字段，
   说明与 CC-10 覆盖率校验关系）。
3. **REF 四查更正**：§四第 2 条明确「REF-02 反链义务（原"CC-10 语义"口语已作废）」，补「CC-09
   reserved、CC-10 = media_class 覆盖率、后续 CC-11 起编」。
4. **gd 脚本自测**：§四新增第 5 条 `gd_naming_check.py`（GN-01/02/03，01 线已实现）。
5. **规范清单升至 v0.6.3 + 自测包入口**：§〇「规范在哪」与附录路径速查补 `规范增补_v0.6.3.md`；
   §四末尾补「贡献者自测包」分发入口（引用说明 v1.2 + 清单脚本）。

### 2.1 8 关键字抽查（Select-String 等价）

```
release_check      2
media_class        4
REF-02             2
CC-09              1
gd_naming_check    3
GN-01              2
v0.6.3             3
贡献者自测包       3
```

## 三、自测包内容清单脚本（§四.2 实跑输出）

```
自测包内容清单生成（版本 v1.2）
repo 根：\\DESKTOP-2IDAL09\work\02\repo
  [OK] tools/validate/audio_check.py  17482 B  06b2847f8d8718b9b64312f4314a1ad8
  [OK] tools/validate/budget_check.py  11350 B  de147c58de561988949393e14e48bac7
  [OK] tools/validate/catalog_check.py  20232 B  7f0b19f73fa6cec2ea654880180daf73
  [OK] tools/validate/catalog_ref_check.py  10005 B  315e9da98f6ca5d24411d7dc225ace05
  [OK] tools/validate/model_check.py  14486 B  c4fba47214eddfcbda12aa1e42a0d5f7
  [OK] tools/validate/scaffold_device.py  11054 B  4c7f08899a97906ea3a6c7d3d3987940
  [OK] tools/validate/slot_check.py  19474 B  72fc0257ffa5c6d504a4f1512bec7622
  [OK] tools/validate/validate.py  50886 B  8a08f34f11851d1bc9a7d4dcc7a37eb3
  [OK] content/schema/device_spec.schema.json  14568 B  975da7e8d4e9b9c019a46b53d60fa222
  [OK] docs/贡献者自测包说明_v1.2.md  7559 B  d2c2e87c21d550b4c38e972dd7e89bf5
汇总：条目 10 / 总字节 177096 / 违规 0
已写入：\\DESKTOP-2IDAL09\work\02\repo\docs\自测包内容清单_v1.2.md
```

- 末行汇总 **违规 0**、**条目 10**（8 校验器 + 1 schema + 1 说明），退出码 0。

### 3.1 清单文件非空核对（Get-Item 等价）

```
-rw-r--r-- 1 Luctw 197121 1568 Nov  8 23:20 docs/自测包内容清单_v1.2.md
```
`Length = 1568 > 0` ✓；清单条目 10 与收录范围一致；说明 v1.2 引用"内容清单路径 =
`docs/自测包内容清单_v1.2.md`"，gd_naming_check 标注"已由 01 线实现"（非 v1.1 的"预计新增"）。

## 四、门禁只读复测（§四.4）

```
结果：36/37 通过
```

**留底说明（偏差如实记录）**：任务文档写"当前基线 37/37"，但执行时实际基线为 **36/37**——唯一
失败步骤 `catalog`（rc=1，摄取 8 文件 2313 行、错误 306）。根因：monorepo 镜像
`01/repo/03/docs/catalog/` 同时残留 `通讯与移动大类_目录_v2.jsonl` 与 `_v3.jsonl`（`sync_monorepo.py`
用 robocopy `/E` 只增不删，v3 上线时未删 v2），导致 306 条重复 id；共享盘 03 目录仅 v3（干净）。
**此失败与本任务无关**（本任务只改 `02/repo/docs/` 与新增 `02/repo/tools/contrib_kit/`，不进任何
门禁步骤），执行前后均 36/37，零回归。

## 五、红线自查结论

1. **不下载 ROM/二进制/版权文件** ✓：纯文档修订 + 纯文本扫描脚本，脚本不联网、不写二进制，
   黑名单命中即判违规（本次 0 命中）。
2. **不编造史实** ✓：仅对齐既有规范/实测现状，未新增任何未经核实的史实/年代/许可断言。
3. **只改 02 线目录** ✓：改动仅 `02/repo/docs/`（CONTRIBUTING / 说明 v1.2 / 清单 v1.2）与
   `02/repo/tools/contrib_kit/`（新脚本）；01 线 `make_contrib_kit.py` / `contrib_kit_src/` / `dist/` /
   `release_check.py` / `gd_*check.py` 一律只读未动。
4. **对齐不改语义** ✓：黑名单 `BLOCK_EXTS` / `BLOCK_SUBSTR` 与 `make_contrib_kit.py` 逐项一致；
   未改任何校验规则、编号语义或门禁行为。
5. **禁止低质产出** ✓：CONTRIBUTING 终版 2748 汉字（≥2600）、说明 v1.2 1299 汉字（≥1200），
   全部贴真实命令与真实输出。

## 六、开放问题

- 01 线 `make_contrib_kit.py` 重新打包时，应把本任务的 `build_content_manifest.py` 与
  `贡献者自测包说明_v1.2.md`、`自测包内容清单_v1.2.md` 纳入 contrib_kit 源材料范围（当前打包器
  尚未引用，属 01 线侧后续动作）。
- monorepo 镜像 `catalog` 步骤 306 重复 id（v2/v3 并存）需 01 线 `sync_monorepo.py` 改 `/MIR` 或
  删旧版后收口，属镜像数据新鲜度问题，非本线责任。
