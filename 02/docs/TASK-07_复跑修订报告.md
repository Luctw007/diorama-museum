# TASK-07 复跑修订报告（docs/TASK-07_复跑修订报告.md）

> 01 线代执行 · 2026-10-31 · 动机：用户指示"02 任务运行失败，重新运行"。
> 本报告记录对 02 线 TASK-07 产出的**复核、缺陷修复与补交付**，与原《TASK-07_完成报告》共同构成 07 任务完整记录。

## 1. 修改文件清单

| 文件 | 修改 |
|---|---|
| `tools/validate/validate.py` | ① `SINK_SURFACES` 增 `crt_display`/`indicator_lamps`；② 新增 `DEVICE_TOKEN_RE`；③ R-086 改为双形态（结构化 {map,key} + legacy 字符串令牌），legacy 通过时给出迁移提示 |
| `content/schema/device_spec.schema.json` | ① output_sink.surface 枚举扩为八项；② input_map 值 `anyOf[input_descriptor, 字符串令牌 pattern]` |
| `docs/内容包规范_v0.2.md` | §11.1 枚举表加兼容两项并注明 deprecated；§11.2 增"两种形态"与两层键名模型决策段；§12.2 迁移表两行更新 |
| `tools/validate/tests/run_tests.py` | 新增反例20（legacy 令牌非法 → R-086） |
| `docs/设计/`（目录卫生） | 删除误拷入的 04 线 design 文档副本 |

## 2. 修复根因说明

1. **R-086 冲突**：v0.2 原要求 input_map 值一律结构化 `{map,key}`，与 03/05 线全部量产包（legacy 字符串令牌）以及 01 线 runtime_mapping §5"两层键名模型"结论冲突 → 改为双形态兼容（legacy 不阻断，提示迁移）；
2. **R-084 冲突**：v0.2 枚举漏掉 v0.1 实际使用的 `crt_display`（Baby 三显屏）与 `indicator_lamps`（ENIAC 灯组）→ 增为兼容枚举。

## 3. 复跑日志（原文关键段）

```text
$ python tools/validate/tests/run_tests.py
  … 结果：PASS 21，FAIL 0（含新反例20）

$ python tools/validate/validate.py content/test-device
  总计 54 条：PASS 54，FAIL 0

$ python tools/validate/validate.py D:\work\03\repo\content\manchester-baby
  总计 137 条：PASS 125，FAIL 12   （= R-002×10 + R-088 + R-071，localize 迁移类）

$ python tools/validate/validate.py D:\work\03\repo\content\eniac
  总计 101 条：PASS 89，FAIL 12   （同上）

$ python tools/validate/validate.py D:\work\05\repo\content\apple-ii
  总计 272 条：PASS 272，FAIL 0   （已完全符合 v0.2）
```

修订前对比：baby 24 FAIL / eniac 19 FAIL / apple-ii 23 FAIL（R-086、R-084 为冲突主因），
修订后 R-084/R-086 在三个包上全部通过。

## 4. 补交付物

- `docs/规则矩阵_v0.2.md`（原任务 §五 要求独立文档；此前折叠在报告中）；
- `docs/真实包校验报告.md`（原任务对三个真实包的校验与修复建议；此前缺交付）。

## 5. 遗留事项与开放问题

1. **localize 迁移（R-002/R-071/R-088）**：manchester-baby、eniac 剩余 12 条失败为 v0.1→v0.2 迁移证据，修复清单见《真实包校验报告》§2，责任交 03 线（建议并入其下一轮任务）；
2. edsac/edvac 仍为空目录（03 线 12-A/B 未执行），不回本线；
3. `scaffold_device.py` 生成的是新版结构化 input_map，如需 legacy 演示可在后续加 `--legacy` 选项（未做，不阻塞）；
4. `content/manchester-baby` fixture 与 03 线同名包分别位于各自 repo，合并入单一树时需做来源裁决（当前不冲突）。

## 6. 结论

TASK-07 经复跑修订后：工具链自测全绿（21 用例 / 54 规则），与全部存量真实包的冲突点已消除；
剩余失败均为有清单、可执行的 localize 迁移项。**07 任务判定为完成（含修订）**。