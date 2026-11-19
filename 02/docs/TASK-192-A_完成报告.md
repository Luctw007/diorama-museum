# TASK-192-A 完成报告：UNIVAC I 产包过闸口径预检（无成熟模拟器形态）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。

## 交付物清单

1. 新增 `docs/UNIVAC1_过闸口径预检卡.md`（738 汉字）：三问三答 + 建议写法 + 03 线落地清单。
2. 改 `docs/第二批分档验收口径_v1.md`：§二 追加「S 档无成熟模拟器形态」跨档条款。

## 无模拟器形态口径结论表

| 问题 | 结论 | 依据 |
|---|---|---|
| `emulator` 字段怎么写 | **`emulator="none"`**（否决 null / simh-univac） | schema required string + 既有 eniac/edvac/nokia-3310 先例 0 FAIL |
| S/A/B 档归属 | **S 档过闸**，件清单全规格 + 静态+原理动画，模拟器作 NOTE 级提示 | S 档口径"无 bone 不算缺口" + UNIVAC I 镇馆级叙事锚点不降档 |
| 校验器放行 | **已放行 `"none"`，无需改校验器**；`null` 会 FAIL R-003 | schema pattern `^[a-z][a-z0-9_-]*$` 匹配 none、不匹配 null |

## 验收日志（原文 + 退出码）

```
# 1) 预检卡关键字自检（Select-String 命中数）
emulator 14 · 分档 1 · 放行 7 · NOTE 2

# 2) 校验器放行实测（verify_all --only catalog_ref）
===== 验收汇总（1 项）=====
  catalog_ref          PASS  FAIL 0
结果：1/1 通过   （退出码 0）

# 3) 门禁只读复测（verify_all --daily --cache）
结果：41/41 通过   （退出码 0）
```

## 与任务书的漂移（如实）

1. **分档口径文件名**：任务书写 `第二批分档验收口径_v2.md`，实际文件名为 `第二批分档验收口径_v1.md`
   （标题已 v2，187-A 只改了标题未改文件名），本任务按实际文件名追加条款。
2. **`emulator=null` 否决依据**：实测 schema `device_spec.schema.json` L263-266 `emulator` 为
   required + type=string，`null` 必 FAIL R-003；非凭经验。
3. **`simh-univac` 否决依据**：研究卡 `11_UNIVAC1.md` §五 明说"无成熟模拟器，SIMH 候选需核实"，写
   `simh-univac` 会声称不存在的后端。
4. 未改校验器代码（放行无需改码）、未产包、未动 03/05 线、零下载零联网。

## 红线自查

1. 不下载 ROM/二进制 ✓；2. 不编造史实 ✓（口径基于研究卡/规范/schema）；3. 只改 02 目录 ✓；
4. 不改校验器代码逻辑 ✓；5. 口径有理由有实测依据 ✓；6. 无 git/代理/PAT ✓。
