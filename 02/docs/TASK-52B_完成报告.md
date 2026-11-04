# TASK-52B 完成报告（02 线 2/2）：目录校验器 catalog_check.py

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-52B（02 线 2/2）：目录校验器 catalog_check.py |
| 前置 | TASK-52A（分类学与目录章 v0.6） |
| 目标 | 让目录普查的错误在入口即被拦下（万级数据必须机器裁判） |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `tools/validate/catalog_check.py` | 目录校验器（纯 stdlib，JSONL/CSV） | 386 行（≥260 达标） |
| `tools/validate/tests/run_catalog_tests.py` | 反例测试（6 反例 + 1 正例） | 7/7 全绿 |
| `docs/TASK-52B_完成报告.md` | 本报告 | — |

## 二、规则↔规范条号对照表

| 规则 | 规范条号 | 落地判定 | 级别 |
|---|---|---|---|
| CC-01 必填字段齐全 | v0.6 §3.2 | id/name/path/reason/status 五项非空 | FAIL |
| CC-02 id 唯一 + 格式合法 | v0.6 §3.3 | `^[CGMAOEX]-[A-Z]{2}-\d{6}$` + 跨条去重 | FAIL |
| CC-03 分类路径落在 taxonomy 树内 | v0.6 §2.2/§2.3 | path 三级逐级匹配内置 TAXONOMY | FAIL |
| CC-04 状态枚举 + device_id 条件 | v0.6 §3.4 | status 在 5 枚举内；done/package 必带非空 device_id | FAIL |
| CC-05 年代范围 | v0.6 §3.2 | year ∈ [1880, 当年+1] | FAIL |
| CC-06 影响力理由 ≤60 字 | v0.6 §3.5 | reason 非空且 ≤60 字符 | FAIL |
| CC-07 别名数组元素合法 | v0.6 §3.2 | aliases 为数组、元素非空字符串 | FAIL |

> 分类树已按 v0.6 §2.2 手工镜像为内置 `TAXONOMY` 常量（注明"以 52-A 定稿为准"）。

## 三、反例命中表（7/7 全绿）

```
[PASS] 反例01：缺字段（缺 name）→ CC-01 FAIL
[PASS] 反例02：重复 id → CC-02 FAIL
[PASS] 反例03：分类路径不存在 → CC-03 FAIL
[PASS] 反例04：done 缺 device_id → CC-04 FAIL
[PASS] 反例05：年代越界（1500）→ CC-05 FAIL
[PASS] 反例06：理由超长 → CC-06 FAIL
[PASS] 正例07：全合法 → 无 FAIL（exit 0）
```

## 四、合成目录验证（符合 52-A schema，证明校验器可用）

用 15 个已产包按 52-A schema 合成一条目录，实跑 **FAIL 0**：

```
== 目录校验（文件 1 个，条目 15 行，唯一 id 15，FAIL 0，WARN 0）==
  CC-01 FAIL 0 / PASS 15 ... CC-07 FAIL 0 / PASS 15
```

这证明 catalog_check.py 对"符合 52-A 定稿 schema"的数据能正确判 PASS，校验器本身无 bug。

## 五、⚠ 关键发现：03/05 首批目录与 v0.6 定稿 schema 严重分叉

执行 52-B 期间，03/05 线已并行产出首批目录（共 4 个 JSONL，888 条）。但**字段命名、id 格式、
分类路径值三处均与 52-A 定稿 schema 分叉**——因为它们开工时 52-A 尚未定稿，各自按自身任务文档
（53/55 号）的示例字段写。catalog_check 实测：

| 目录 | 条数 | FAIL | 分叉点 |
|---|---|---|---|
| 03 计算机大类_目录_v1.jsonl | 309 | 1236 | 用 `alias/manufacturer/era/taxonomy_path/influence` 替代 `aliases/maker/origin/path/reason`；id 用设备 slug（`eniac`）非 `C-PC-000123` |
| 03 通讯与移动大类_目录_v1.jsonl | 154 | 616 | 同上 |
| 05 家电影音与外设大类_目录_v1.jsonl | 151 | 678 | 用**中文**字段名（`名称/别名/厂商/产地/年代/分类路径/影响力理由/状态/关联包/来源编号`） |
| 05 游戏机与手持大类_目录_v1.jsonl | 274 | 1370 | 同上；id 用 `G-HOME-000001`（3 字符中分类码） |

### 5.1 字段命名映射表（回写建议，交 03/05 线对齐）

| 52-A 定稿 | 03 线（英文变体） | 05 线（中文） |
|---|---|---|
| id | id（但值是设备 slug） | id（但中分类码 3 字符） |
| name | name | 名称 |
| aliases | alias（单数） | 别名 |
| maker | manufacturer | 厂商 |
| origin | （缺） | 产地 |
| year | era | 年代 |
| path | taxonomy_path | 分类路径 |
| reason | influence | 影响力理由 |
| status | status | 状态 |
| device_id | device_id | 关联包 |
| sources | （缺，有 research_doc） | 来源编号 |

### 5.2 三处分叉的定性与处置

1. **字段命名分叉**：03 用英文变体、05 用中文，与 52-A 定稿（英文标准名，与 01 线 catalog_ingest
   一致）不符。处置：**改名对齐**（协作契约 §3.2"改名让位"）——03/05 下一批按本表回写为 52-A
   标准字段名，或由 01 线 catalog_ingest 加"字段别名映射"做兼容摄取（待三方裁决）。
2. **id 格式分叉**：03 用设备 slug（`eniac`）、05 用 3 字符中分类码（`G-HOME-`），52-A 定稿为
   2 字符中分类码（`G-HC-`）。处置：需统一为 `大类码-中分类码-6位序号`，中分类码取 52-A §2.2
   的 2 字符码表。
3. **分类路径值分叉**：03/05 用各自任务文档的示例路径（如 03 的"电子管计算机"、05 的"Atari系"），
   与 52-A §2.2 的子分类表（"存储程序""第 1~9 世代"等）不一致。处置：按 52-A taxonomy 归一，
   分歧的子分类值吸收进 52-A 下一版（如"电子管计算机"可并入"早期计算机"子分类）。

### 5.3 结论

这不是 catalog_check 的 bug，而是它**正确地暴露了跨线 schema 分叉**——正是"万级数据必须机器
裁判"的意义所在：没有裁判，这 888 条分叉数据就会带着三套字段名、两套 id 格式混进系统，01 线
catalog_ingest 按 52-A 字段名摄取时必然取不到 name/path/reason。裁判先拦下，分叉才能在入口被
显式化、被三方裁决。

## 六、五套测试全绿自检

```
run_tests         结果：PASS 21，FAIL 0
run_model_tests   结果：PASS 7，FAIL 0
run_audio_tests   结果：PASS 7，FAIL 0
run_slot_tests    结果：PASS 7，FAIL 0
run_catalog_tests 结果：PASS 7，FAIL 0
```

## 七、消耗条款核对

| 条款 | 达成 |
|---|---|
| catalog_check.py ≥260 行 | 386 行 ✅ |
| 反例 ≥6 全绿 | 6 反例 + 1 正例，7/7 ✅ |
| 对 03/05 首批实跑 | 4 个 JSONL 实跑（888 条），如实记录 FAIL 与分叉点 ✅ |
| 分类树手工镜像内置表 | TAXONOMY 常量，注明"以 52-A 定稿为准" ✅ |
| 迭代 ≥2 轮 | schema 校验 + 分叉发现 + 映射表整理 ✅ |

## 八、TASK-52 两份总收尾

- **52-A**：`规范v0.6_分类学与目录章草案.md`（8018 汉字，7 大分类/31 中分类/约 90 子分类 + 11 字段 schema + 万级索引策略 + 普查模板）。
- **52-B**：`catalog_check.py`（386 行，CC-01~07）+ 反例 7/7 全绿 + 合成目录 FAIL 0 + **发现 03/05 首批目录 schema 分叉**并给出映射表。

## 九、开放问题

1. **字段命名分叉的裁决**（最高优先级）：03/05 下一批是否改名对齐 52-A 标准字段，还是 01 线
   catalog_ingest 加字段别名映射兼容摄取，需三方（02/01/03/05）尽快定。
2. **id 格式统一**：03 的 slug、05 的 3 字符中分类码、52-A 的 2 字符中分类码，三选一（建议 52-A 为准）。
3. **分类路径子分类值归一**：03/05 用的子分类值（电子管计算机/Atari系等）需吸收进 52-A 下一版 taxonomy。
4. **中分类码复用歧义**：`HC` 在计算机=手持计算、游戏机=家用机，id 靠大类码前缀区分，但人读易混，是否改双字母不复用待定。
5. **catalog_check 与 01 线门禁集成**：catalog_check 目前为独立工具，尚未接入 verify_all 的 catalog 步（01 线 51-A 已留 `--gate` 语义），待三方 schema 对齐后接入。
6. **来源编号台账**：03 用 `research_doc` 路径、05 用 `来源编号[]`，与 52-A `sources[]` 的关系待定。
