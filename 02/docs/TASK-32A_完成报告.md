# TASK-32A 完成报告 — 建模校验接入门禁与全包索引 v3

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本报告与配套代码按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-32A（02 线 1/2）：建模校验接入门禁与全包索引 v3 |
| 状态 | 完成 |
| 日期 | 2026-11-03 |
| 前置 | TASK-27（model_check + 反例全绿 + v0.3 定稿） |

---

## 1. 交付物

| 路径 | 变更 | 说明 |
|---|---|---|
| `tools/regress/regress_all.py` | 升级（219→283 行） | 新增 `--with-model` 档位，汇总表加 MR-01..04 FAIL/WARN 列 |
| `tools/index/collect_index.py` | 升级 | 索引表加 MR-FAIL/MR-WARN 双结果列 |
| `docs/全包索引.md` | 重生成（v3） | 12 device-id 去重 / 13 包目录 |
| `docs/全包索引_v2归档.md` | 新增 | v2 归档 |
| `docs/TASK-32A_完成报告.md` | 新增 | 本报告 |

## 2. 门禁接入 diff（regress_all 升级要点）

- 新增 `--with-model`：每步先 `validate.py` 再 `model_check.py --json`，汇总表由
  「总计/PASS/FAIL/耗时/退出码」扩为「总计/FAIL/**MR-01~04(F/W)**/耗时/结论」。
- `--json` 输出 `with_model:true` 时 `packages[].model` 内嵌 `mr`（逐规则 fail/warn）+ `mr_fail`/`mr_warn` 汇总。
- collect_index.py 同步：索引表加 `MR-FAIL`/`MR-WARN` 两列（由 model_check.py 实测）。

## 3. 逐包表格（10 规范包 + 新增，--with-model 实测）

| 序号 | 包 | 总计 | FAIL | MR-01 | MR-02 | MR-03 | MR-04 | 结论 |
|---|---|---|---|---|---|---|---|---|
| 1 | manchester-baby（03） | 128 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| 2 | eniac | 92 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| 3 | edsac | 132 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| 4 | edvac | 126 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| 5 | pdp8 | 72 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| 6 | system360 | 78 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| 7 | pdp11 | 78 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| 8 | apple-ii | 272 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| 9 | atari-2600 | 128 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| 10 | famicom | 100 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| — | test-device（夹具） | 54 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |
| — | vax11（执行期新增） | 78 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | PASS |

> 双套反例回归全绿：`run_tests.py` PASS 21 / FAIL 0；`run_model_tests.py` PASS 7 / FAIL 0。
> 占位盒阶段 MR 全过、无 WARN；正式建模开产后 MR-02 预算门禁才真正生效。

## 4. 与 01 线 verify_all 的衔接说明

- **01 线 `verify_all.py`** 是"一键验收门禁"（m0→m1→m1b + 硬编码 5 包 validate）。
- **02 线 `regress_all.py --with-model`** 是"包级全量双校验门禁"（动态扫描 + validate + model_check）。
- 衔接方式（供 01 线未来调用）：01 线 verify_all 可在其 `pkg` 步骤里改为调用
  `python tools/regress/regress_all.py --with-model --content-dir <d>`，即获得"validate 0 FAIL +
  MR 0 FAIL"的双重门禁，取代其硬编码 5 包清单与硬编码 validator 路径（消除 `D:\work\02\...`
  跨机脆弱性）。

## 5. 开放问题

1. **包数持续增长**：任务写"10 规范包"，执行期 03 线又新增 vax11（现 12 device-id / 13 包目录）。
   索引按实际状态生成，报告如实记录。
2. **MR 门禁触发**：当前占位盒 MR 全过；正式网格开产后若 MR-02 出现 WARN/FAIL，需区分
   "合理高模（走 §10.4 豁免）"vs"超预算失控"，门禁只卡后者。
3. **verify_all 硬编码**：01 线 verify_all 的 validator 绝对路径 + 5 包清单仍未改，建议 01 线改用
   regress_all（见 §4），本线不改他线文件。
