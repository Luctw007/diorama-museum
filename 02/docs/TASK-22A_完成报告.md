# TASK-22A 完成报告 — 全包索引与回归聚合工具

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本报告与配套代码按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-22A（02 线 1/2）：全包索引与回归聚合工具 |
| 状态 | 完成 |
| 日期 | 2026-11-02 |
| 前置 | TASK-17（migrate 工具 + v0.2.1 规范） |

---

## 1. 交付物与行数

| 路径 | 行数 | 说明 |
|---|---|---|
| `tools/index/collect_index.py` | 341 | 全包索引生成器（纯 stdlib，`--json`） |
| `tools/regress/regress_all.py` | 219 | 全包回归聚合（纯 stdlib，`--fail-fast`/`--json`） |
| `docs/全包索引.md` | — | 自动生成产物（本工具输出） |
| `docs/TASK-22A_完成报告.md` | — | 本报告 |

两工具 `py_compile` 全过；无第三方依赖。

## 2. 运行日志原文

### 2.1 collect_index.py（生成索引）

```text
$ python tools/index/collect_index.py
已生成索引：\\DESKTOP-2IDAL09\work\02\repo\docs\全包索引.md
共 6 个 device-id（去重后），扫描包目录 7 个
  apple-ii           个人计算机厅           272 条 FAIL 0
  edsac              计算机黎明厅           132 条 FAIL 0
  edvac              计算机黎明厅           126 条 FAIL 0
  eniac              计算机黎明厅           92 条 FAIL 0
  manchester-baby    计算机黎明厅           128 条 FAIL 0
  test-device        （校验夹具 · 非展项）     54 条 FAIL 0
  [同名] manchester-baby 在其它仓库有同名副本：02/repo/content/manchester-baby
```

### 2.2 regress_all.py（全量回归）

```text
$ python tools/regress/regress_all.py
| 序号 | 包 | 总计 | PASS | FAIL | 耗时(ms) | 退出码 | 结论 |
|---|---|---|---|---|---|---|---|
| 1 | `02/repo/content/manchester-baby` | 48 | 48 | 0 | 2696.8 | 0 | PASS |
| 2 | `02/repo/content/test-device` | 54 | 54 | 0 | 2433.4 | 0 | PASS |
| 3 | `03/repo/content/edsac` | 132 | 132 | 0 | 2947.7 | 0 | PASS |
| 4 | `03/repo/content/edvac` | 126 | 126 | 0 | 2936.6 | 0 | PASS |
| 5 | `03/repo/content/eniac` | 92 | 92 | 0 | 2546.3 | 0 | PASS |
| 6 | `03/repo/content/manchester-baby` | 128 | 128 | 0 | 2819.9 | 0 | PASS |
| 7 | `05/repo/content/apple-ii` | 272 | 272 | 0 | 2977.5 | 0 | PASS |
汇总：7 包，PASS 7，FAIL 0
（退出码 0）
```

## 3. 索引样例（docs/全包索引.md 全文）

| # | device-id | 名称 | 门类 Hall 归属 | 仓库路径 | 总计 | PASS | FAIL | 字段齐备 |
|---|---|---|---|---|---|---|---|---|
| 1 | apple-ii | Apple II | 个人计算机厅 | `05/repo/content/apple-ii` | 272 | 272 | 0 | 齐备 |
| 2 | edsac | EDSAC（…） | 计算机黎明厅 | `03/repo/content/edsac` | 132 | 132 | 0 | 缺 intro、era、manufacturer |
| 3 | edvac | EDVAC（…） | 计算机黎明厅 | `03/repo/content/edvac` | 126 | 126 | 0 | 缺 intro、era、manufacturer |
| 4 | eniac | ENIAC（…） | 计算机黎明厅 | `03/repo/content/eniac` | 92 | 92 | 0 | 缺 intro、era、manufacturer |
| 5 | manchester-baby | 曼彻斯特 Baby（SSEM） | 计算机黎明厅 | `03/repo/content/manchester-baby` | 128 | 128 | 0 | 缺 intro、era、manufacturer |
| 6 | test-device ⚠夹具 | 验证方块机 | （校验夹具 · 非展项） | `02/repo/content/test-device` | 54 | 54 | 0 | 齐备 |

> 同名副本：`manchester-baby` 在 `02/repo/content/manchester-baby` 有脚手架骨架副本（48 条），
> 索引按 device-id 去重，保留 03 生产包为 canonical。

## 4. 与 01 线 verify_all 的职责边界

| 维度 | 01 线 `scripts/verify_all.py` | 02 线 `tools/regress/regress_all.py` | 02 线 `tools/index/collect_index.py` |
|---|---|---|---|
| 定位 | 01 线**一键验收门禁** | 02 线**包级全量回归** | 02 线**静态总目索引** |
| 内容 | m0→m1→m1b 网关/运行时验收 + 5 个硬编码生产包校验 | 动态扫描 01/02/03/05 content，逐包跑 validate | 静态画像：device-id/名称/门类/路径/字段齐备 |
| 包清单 | 硬编码 5 包（不含 02 夹具、不含同名骨架） | 扫描发现 7 包目录（含夹具与骨架） | 扫描发现 6 个 device-id（去重） |
| 输出 | 门禁通过/失败 + 退出码 | 序号/总计/FAIL/耗时/退出码 + `--fail-fast`/`--json` | 索引表 + `--json` |
| 依赖 | 硬编码 `D:\work\02\...` 绝对路径（脆） | 相对脚本定位（可移植） | 相对脚本定位（可移植） |

**结论**：01 线 verify_all 管"自己线验收"（m0/m1/m1b 网关链路）；02 线 regress_all 管"包级全量"（动态扫描、
给耗时与退出码），collect_index 管"总目"（一页看全所有包的状态与门类）。三者互补，不冲突。

## 5. 目录核对结果（对照 01/03/05 content 实际目录）

| 仓库 | content 实际目录 | 工具识别 | 说明 |
|---|---|---|---|
| 01 | `repo/content`（仅 README.md） | 0 包 | 空（内容包在 01 线为运行时导入，见下） |
| 02 | `repo/content` | 2 包 | manchester-baby（骨架夹具）、test-device（校验夹具）；`schema/` 非包被跳过 |
| 03 | `repo/content` | 4 包 | edsac、edvac、eniac、manchester-baby（生产） |
| 04 | `repo/content` | 不扫描 | 设计线，无量产包（按任务排除） |
| 05 | `repo/content` | 1 包 | apple-ii（生产） |

> 附注：`01/repo/godot/content` 下有 6 个包，属 Godot 运行时导入副本（非 `<repo>/content` 清单，
> 且与 03/05 生产包同名），按任务范围不纳入；如需纳入可在后续用 `--content-dir` 显式追加。

## 6. 开放问题

1. **01 线 verify_all 的硬编码路径**：`VALIDATOR = D:\work\02\...` 与 5 个包路径硬编码，跨机器/路径迁移会失效；建议后续改为相对定位或复用 02 线 regress_all 的扫描逻辑。
2. **Hall 归属映射**：当前由 `meta.category → 厅` 映射表推导（early-computer→黎明厅 等）；未来厅名/厅数定稿后应以显式字段或独立映射文件为准，避免硬编码漂移。
3. **同名包来源裁决**：`manchester-baby` 在 02（骨架）与 03（生产）并存，索引以"非夹具 + 规则数多者"为 canonical；正式合并单一树时需做权威来源裁决（已在 TASK-07 遗留问题中跟踪）。
4. **`01/repo/godot/content` 运行时副本**：与生产包同名、易混淆，建议明确其定位（运行时导入 vs 源包）并在索引中标注，或纳入统一清单。
