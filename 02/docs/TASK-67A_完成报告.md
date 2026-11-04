# TASK-67A 完成报告（02 线 1/2）：v0.6.1 增补（media_class 规则章 + catalog_check CC-08）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-67A（02 线 1/2）：v0.6.1 增补 |
| 前置 | TASK-62（media_infer 回填建议 + taxonomy 治理） |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `docs/规范增补_v0.6.1.md` | media_class 推定规则章 + CC-08 规则 + 衔接条款 | 全文 |
| `tools/validate/catalog_check.py` | 增 CC-08（device_id 存在性 rigid 判定） | 已更新 |
| `tools/validate/tests/run_catalog_tests.py` | 反例 +1（CC-08） | 8/8 全绿 |
| `docs/TASK-67A_完成报告.md` | 本报告 | — |

## 二、规则同步证明（与 62-B 建议表）

规范增补 §1.2/§1.3 的规则表（R01~R53 + K01~K10）与 `media_infer.py` 的 `RULES`/`REFINE` 常量
**逐条一一对应**：38 条基础规则 + 10 条关键词精化，字段（匹配条件/输出/依据）完全一致。
同步约定已写入增补 §1.2 注（"任何一侧增删规则须同步另一侧"）。

## 三、CC-08 规则落地

| 规则 | 判定 | 级别 |
|---|---|---|
| CC-08 | status ∈ {package, wip, done} 必须带非空 device_id 且存在于 03/05/02 content | FAIL（rigid） |

实现要点：`discover_device_ids()` 扫描 03/05/02 `repo/content` 的 meta.id 构建存在性集合；
`check_entry` 增 CC-08 判定；CLI 增 `--content-dir` 可覆盖默认 content 目录。

## 四、反例测试（8/8 全绿）

```
结果：PASS 8，FAIL 0
（反例07 新增：device_id 不存在 → CC-08 FAIL；其余 6 反例 + 1 正例不变）
```

## 五、CC-08 全量实跑（1562 条最新版目录）

```
== 目录校验（文件 4 个，条目 1562 行，唯一 id 1562，FAIL 0，WARN 0）==
  CC-04  FAIL 0 / PASS 1562
  CC-08  FAIL 0 / PASS 17
```

17 条 `done/package/wip` 条目 device_id 全部命中（**0 冲突**），无悬空引用。

## 六、开放问题

1. 目录 `media_class` 回填时机（03/05 线人工复核排期）；
2. "无"是否入 media_class 枚举（v0.5.x 裁决）；
3. CC-08 device_id 存在性检查范围配置化（新增内容线时同步）；
4. 目录仍存在 v1/v2 并存重复（同 62 开放问题，待 03/05 清理）。
