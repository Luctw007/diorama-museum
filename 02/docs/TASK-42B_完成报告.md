# TASK-42B 完成报告（02 线 2/2）：13 包全量复验与全包索引 v5

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-42B（02 线 2/2）：13 包全量复验与全包索引 v5 |
| 前置 | TASK-42A（audio_check 落地） |
| 背景 | 新入 C64/IBM5150 两包 + v0.4 生效后，一次全量复验与索引刷新 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `tools/regress/regress_all.py` | 新增 `--with-audio` 档位（三连复验） | 283 → 340 行 |
| `tools/index/collect_index.py` | 新增 A-FAIL/A-WARN 结果列 | 411 行 |
| `docs/全包索引.md` | v5（13 包×三列 + 字段齐备 + 厅归属） | 16 device-id |
| `docs/全包索引_v3归档.md` | 上一代索引归档（防丢失） | — |
| `docs/TASK-42B_完成报告.md` | 本报告 | — |

## 二、三连复验逐包表（regress_all.py --with-model --with-audio）

```
全包回归聚合（regress_all.py）

| 序号 | 包 | 总计 | FAIL | MR-01 | MR-02 | MR-03 | MR-04 | A-01 | A-02 | A-03 | A-04 | 耗时(ms) | 结论 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 02/repo/content/manchester-baby | 48 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2048.4 | PASS |
| 2 | 02/repo/content/test-device | 54 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 1701.5 | PASS |
| 3 | 03/repo/content/bbcmicro | 78 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2205.8 | PASS |
| 4 | 03/repo/content/commodore64 | 78 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2644.6 | PASS |
| 5 | 03/repo/content/edsac | 132 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2045.7 | PASS |
| 6 | 03/repo/content/edvac | 126 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2025.3 | PASS |
| 7 | 03/repo/content/eniac | 92 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 1734.2 | PASS |
| 8 | 03/repo/content/ibm5150 | 84 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2504.7 | PASS |
| 9 | 03/repo/content/manchester-baby | 128 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2520.2 | PASS |
| 10 | 03/repo/content/pdp11 | 78 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2104.0 | PASS |
| 11 | 03/repo/content/pdp8 | 72 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2127.4 | PASS |
| 12 | 03/repo/content/system360 | 78 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2146.9 | PASS |
| 13 | 03/repo/content/vax11 | 78 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2070.1 | PASS |
| 14 | 05/repo/content/apple-ii | 272 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 1995.7 | PASS |
| 15 | 05/repo/content/atari-2600 | 128 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2333.2 | PASS |
| 16 | 05/repo/content/famicom | 100 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2240.8 | PASS |
| 17 | 05/repo/content/sega-md | 96 | 0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2738.5 | PASS |

汇总：17 包，PASS 17，FAIL 0
建模校验汇总：MR FAIL 合计 0，MR WARN 合计 0
音频校验汇总：A FAIL 合计 0，A WARN 合计 0
```

> 17 个包目录 = 02 线夹具/骨架 2（manchester-baby 骨架 + test-device）+ 03 线 11 + 05 线 4。
> 按 device-id 去重后 16（含 test-device 夹具），**规范包（展项）15 个**。

## 三、复验发现清单（新两包在 v0.4 下的差异）

新入 **commodore64（C64）** 与 **ibm5150（IBM PC 5150）** 两包，v0.4 三连复验结果：

| 包 | validate | model_check | audio_check | 结论 |
|---|---|---|---|---|
| commodore64 | 78 条 FAIL 0 | MR FAIL 0 / WARN 0 | 0 音频文件（跳过） | **0 差异** |
| ibm5150 | 84 条 FAIL 0 | MR FAIL 0 / WARN 0 | 0 音频文件（跳过） | **0 差异** |

两包均无 `audio/` 目录（v0.4 音频章为可选，历史包不涉及迁移），在 v0.4 下无任何差异。

### [需实测] 项目汇总（音频响度类）

- 生产包侧：**0 条**（全部 15 规范包无 `audio/` 目录，audio_check 对每包报告「跳过」而非静默通过）。
- 潜在项（正式录音开产后才触发，见 42-A §2.2）：OGG 采样率/位深/时长、WAV 响度（LUFS/峰值 dBFS）
  计量需引入 CI 侧工具（ffmpeg loudnorm），运行时仍零第三方依赖。

## 四、与 01 线门禁（pkg_registry）的衔接说明

01 线 TASK-41A 已产出 `scripts/pkg_registry.py`（数据驱动门禁，扫描 03/05 content，`EXCLUDES`
剔除 fixture，WIP 判据 = 缺 THIRD_PARTY/annotations/双网格目录合计 0 gltf 或 `.wip` 标记）。
其验证记录与本次复验**同口径对齐**：

| 项 | 01 线 pkg_registry | 02 线 regress_all/collect_index |
|---|---|---|
| 扫描源 | 03/05 `repo/content` | 01/02/03/05 `repo/content` |
| 包数 | 15 ready / 0 wip | 16 device-id（15 生产 + test-device） |
| 职责 | 包清单发现 + WIP 判据 + 单包过滤 | 校验回归三连（validate+model+audio）+ 索引总目 |

二者互补不冲突：registry 管「哪些包、是否完工」，regress_all 管「完工包三连校验是否全绿」。
本线全量复验 15 规范包 **FAIL 0**，与 01 线 `verify_all --daily` 的 17/17 结论一致。

## 五、消耗条款核对

| 条款 | 达成情况 |
|---|---|
| 三连复验逐包表格 | 是（§二 17 包表） |
| 索引 v5 全文生成 | 是（16 device-id，三列结果 + 字段齐备 + 厅归属） |
| 迭代 ≥2 轮 | regress_all 表头动态拼装调 1 轮；collect_index 列对齐调 1 轮 |

## 六、TASK-42 两份总收尾

- **42-A**：`audio_check.py`（460 行）落地 A-01~A-04，反例 6+1 全绿，15 包全「跳过」如实记录。
- **42-B**：`regress_all.py` 加 `--with-audio`、`collect_index.py` 加 A 列，三连复验 17 目录全 PASS、
  索引 v5 生成（16 device-id 全 0 FAIL），新两包 0 差异。

## 七、开放问题

1. **包数持续增长**：任务写"13 规范包"，执行期间 03/05 线并行新增 bbcmicro、sega-md，现
   **15 规范包**（16 device-id 含夹具）；后续任务文档的包数口径需按实际扫描对齐。
2. **A-03 时长口径**：任务文档 sfx≤30s vs v0.4 §9 "sfx ≤4s"，需 v0.4.x 勘误统一（见 42-A §六）。
3. **legacy input_map 移除触发点**：仍跟踪中（03 线黎明厅四包 input_map 未对象化），与 v0.2.1
   附录 B 对齐。
4. **字段齐备缺口**：黎明厅四包（edsac/edvac/eniac/manchester-baby）仍缺 `intro/era/manufacturer`，
   pdp8 缺 `intro`——内容线文案待补，非校验 FAIL。
