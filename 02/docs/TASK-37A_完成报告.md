# TASK-37A 完成报告 — 音频规范 v0.4 定稿

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本报告与配套文档按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-37A（02 线 1/2）：音频规范 v0.4 定稿 |
| 状态 | 完成 |
| 日期 | 2026-11-03 |
| 前置 | TASK-32（v0.4 音频章草案 + 建模校验进索引） |

---

## 1. 交付物

| 路径 | 说明 |
|---|---|
| `docs/内容包规范_v0.4.md` | 全文定稿（v0.3 + 第十四章音频资产，变更清单 12 条） |
| `docs/TASK-37A_完成报告.md` | 本报告 |

## 2. 变更清单全表（v0.3 → v0.4，12 条）

| # | 位置 | 旧文 | 新文 | 缘由 |
|---|---|---|---|---|
| 1 | 第十四章（新增） | 无 | 音频资产章全文 | 32-B 草案定稿 |
| 2 | §2 目录 | `sounds/` | `audio/`（bgm/sfx/vo 三层） | 音频落位约定 |
| 3 | §4 命名 | 无音频前缀 | bgm_/sfx_/vo_/amb_/run_ | 命名即契约 |
| 4 | §8 THIRD_PARTY | 音频未单列 | 三件套延伸 + SYNTH.md 升格 | 授权先行 |
| 5 | §9 校验 | 无音频规则 | A-01~04（本轮不实现） | 预研转正 |
| 6 | 第十四章 §2 | 无响度规范 | vo−16/sfx−18/bgm−24/amb−30 LUFS + dBFS 峰值 | 杜绝音量不一 |
| 7 | 第十四章 §3 | narr_ | vo_ + 厅/站/句 | 裁决 |
| 8 | 第十四章 §3 | bgm_hall_dawn | bgm_dawn_01 | 裁决 |
| 9 | 第十四章 §3 | sfx_lid_open | sfx_apple_ii_lid_open | 裁决 |
| 10 | 第十四章 §2 | dBFS/RMS/LUFS 混用 | LUFS+dBFS 双层 | 裁决 |
| 11 | 附录 B | 无音频项 | 新增 TTS/响度工具/遮挡 | 开放问题并入 |
| 12 | 卷首工具 | 无 audio_check | 标注本轮不实现 | 只定义不实现 |

## 3. 裁决记录表（吸收 04 线 20 号，12 条 ≥10）

| # | 参数 | 04 线 20 号 | 本章 | 裁决 |
|---|---|---|---|---|
| 1 | 采样率 | 48 kHz | 48 kHz | 采纳 |
| 2 | 位深 | 24bit WAV | 24bit WAV | 采纳 |
| 3 | 交付格式 | OGG q5/q6 | OGG q5/q6 | 采纳 |
| 4 | 响度单位 | dBFS/RMS/LUFS 混用 | LUFS+dBFS 双层 | 调整 |
| 5 | 解说响度 | LUFS −16 | vo −16 | 采纳 |
| 6 | 效果音响度 | 峰值−12/RMS−20 | sfx LUFS −18 + 峰值 −12 | 调整 |
| 7 | BGM 响度 | 增益 −18 dB | BGM LUFS −24 | 调整 |
| 8 | 解说前缀 | narr_ | vo_ | 调整 |
| 9 | BGM 命名 | bgm_hall_dawn | bgm_dawn_01 | 调整 |
| 10 | 效果音命名 | sfx_lid_open | sfx_apple_ii_lid_open | 调整 |
| 11 | SYNTH.md | [TBD] 建议 | 升格规范要求 | 调整 |
| 12 | 授权四档 | 四档+原创+合成 | 同 | 采纳 |

## 4. 一致性自检日志原文（三段）

### 4.1 run_tests 全绿

```text
$ python tools/validate/tests/run_tests.py
结果：PASS 21，FAIL 0
```

### 4.2 run_model_tests 全绿

```text
$ python tools/validate/tests/run_model_tests.py
结果：PASS 7，FAIL 0
```

### 4.3 全包 validate 全 0 FAIL

```text
$ python tools/regress/regress_all.py
| 1 | 02/repo/content/manchester-baby | 48 | 48 | 0 | PASS |
| 2 | 02/repo/content/test-device | 54 | 54 | 0 | PASS |
| 3 | 03/repo/content/commodore64 | 78 | 78 | 0 | PASS |
| 4 | 03/repo/content/edsac | 132 | 132 | 0 | PASS |
| 5 | 03/repo/content/edvac | 126 | 126 | 0 | PASS |
| 6 | 03/repo/content/eniac | 92 | 92 | 0 | PASS |
| 7 | 03/repo/content/manchester-baby | 128 | 128 | 0 | PASS |
| 8 | 03/repo/content/pdp11 | 78 | 78 | 0 | PASS |
| 9 | 03/repo/content/pdp8 | 72 | 72 | 0 | PASS |
| 10 | 03/repo/content/system360 | 78 | 78 | 0 | PASS |
| 11 | 03/repo/content/vax11 | 78 | 78 | 0 | PASS |
| 12 | 05/repo/content/apple-ii | 272 | 272 | 0 | PASS |
| 13 | 05/repo/content/atari-2600 | 128 | 128 | 0 | PASS |
| 14 | 05/repo/content/famicom | 100 | 100 | 0 | PASS |
汇总：14 包，PASS 14，FAIL 0
```

> **包数说明**：任务写"10 内容包（含 vax11）"，执行期 03 线又新增 commodore64，现共 14 包目录
> （12 生产 device-id + test-device 夹具 + 02 骨架副本），全 0 FAIL。规范文本无破坏。

## 5. 与 04 线参数分歧点（裁决已闭环）

| 分歧 | 裁决 | 状态 |
|---|---|---|
| 响度单位混用 vs LUFS 双层 | LUFS 目标 + dBFS 峰值 | 已闭环（§14.2） |
| narr_ vs vo_ | vo_ + 厅/站/句 | 已闭环（§14.3） |
| bgm_hall_dawn vs bgm_dawn_01 | bgm_厅_序号 | 已闭环（§14.3） |
| sfx 无设备前缀 | 补设备前缀 | 已闭环（§14.3） |
| sounds/ vs audio/ | audio/ 三层 | 已闭环（§2） |

## 6. 开放问题

1. A-01~04 实现（留 v0.4.x 工具任务）：推荐独立 `audio_check.py`，`regress_all` 加 `--with-audio`。
2. TTS 与真人配音取舍（预算门）；响度测量工具选型（纯 stdlib 浅校验 vs CI 侧 ffmpeg 真计量）。
3. 遮挡 −6dB/层射线判定载体；run_* bed 化与 04/05 线对齐。
