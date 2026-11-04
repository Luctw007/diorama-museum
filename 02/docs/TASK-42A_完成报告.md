# TASK-42A 完成报告（02 线 1/2）：音频规则校验器实现（A-01~A-04 落地）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-42A（02 线 1/2）：音频规则校验器实现 |
| 前置 | TASK-37（规范 v0.4 定稿 + 协作契约 v2） |
| 目标 | 把 v0.4 音频章 A-01~A-04 从"规则定义"做成可运行校验器（模式同 model_check） |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `tools/validate/audio_check.py` | 音频规则校验器（纯 stdlib） | 460 行（≥260 达标） |
| `tools/validate/tests/run_audio_tests.py` | 反例测试（6 反例 + 1 正例） | 全绿 |
| `docs/TASK-42A_完成报告.md` | 本报告 | — |

## 二、规则实现对照（v0.4 §14.5 / §9 A-01~04 → 代码）

| 规则 | v0.4 定义 | audio_check.py 落地 | 违规级别 |
|---|---|---|---|
| A-01 命名 | audio/ 文件名匹配 `^(bgm\|sfx\|vo\|amb\|run)_[a-z0-9_]+$` | 三层子目录（bgm/sfx/vo）层级校验 + 基础正则 + 前缀-目录一致 + 结构正则（bgm_厅_序号 / sfx_设备_动作 / vo_厅_站_句） | FAIL |
| A-02 格式元数据 | 采样率 48k / 声道匹配 | WAV 头解析（RIFF/fmt，struct）采样率=48000、位深 16 或 24；OGG 仅登记大小并 WARN（[需实测]） | WARN（解析失败 FAIL） |
| A-03 时长与响度 | sfx ≤4s、LUFS 分层 | WAV 时长对照类别上限（bgm≤180s/sfx≤30s/vo≤600s/amb≤120s/run≤30s）；响度无计量库 → [需实测] WARN（不作 FAIL） | WARN |
| A-04 来源三件套 | THIRD_PARTY 音频行 + SYNTH.md | 外部音频须 THIRD_PARTY.md「分档+URL+日期」三件套行；合成件须 audio/SYNTH.md 配方 | FAIL（无登记）/ WARN（合成件无配方） |

### 2.1 与 v0.4 §9 口径差异（裁决记录）

TASK-42A 任务文档给出的 A-03 时长上限为 **bgm≤180s、sfx≤30s、vo≤10min(600s)**，与
v0.4 §9 速查表的 "sfx ≤4s（amb 60–120s 例外）" 不一致。按"任务文档 > 既有规范"原则，本实现
**以任务文档口径为准**（bgm 180 / sfx 30 / vo 600），并额外沿用 v0.4 §2.3 的 amb 60–120s、run 同
sfx。此差异列入开放问题，待 v0.4.x 规范勘误统一（sfx 4s vs 30s 需正式裁决）。

### 2.2 [需实测] 项目清单（纯 stdlib 无法完成，如实 WARN）

| 项 | 原因 | 处理 |
|---|---|---|
| OGG 采样率/位深 | 纯 stdlib 不解析 Vorbis 头 | WARN + 登记文件大小 |
| OGG 时长 | 同上 | WARN [需实测] |
| 响度（LUFS/峰值 dBFS） | 需 K 加权滤波 + 积分计量（EBU R128），非纯 stdlib 可做 | WARN [需实测]，不作 FAIL |
| WAV 无 data chunk 时长 | 数据区缺失 | WARN [需实测] |

## 三、反例测试运行日志（7/7 全绿）

```
======================================================================
TASK-42A 音频规则校验器反例测试（audio_check.py）
======================================================================
[PASS] 反例01：命名非法（大写）→ A-01 FAIL  — exit=1, 命中 A-01 FAIL
[PASS] 反例02：采样率错（44.1kHz）→ A-02 WARN  — exit=1, 命中 A-02 WARN
[PASS] 反例03：时长超限（sfx 31s）→ A-03 WARN  — exit=1, 命中 A-03 WARN
[PASS] 反例04：三件套缺（无 THIRD_PARTY）→ A-04 FAIL  — exit=1, 命中 A-04 FAIL
[PASS] 反例05：位深非法（8bit）→ A-02 WARN  — exit=1, 命中 A-02 WARN
[PASS] 反例06：层级错放（sfx 在 bgm 目录）→ A-01 FAIL  — exit=1, 命中 A-01 FAIL
[PASS] 正例07：全合法三件套齐备 → 无 FAIL  — exit=0
----------------------------------------------------------------------
结果：PASS 7，FAIL 0
```

反例覆盖：命名非法 / 采样率错 / 时长超限 / 三件套缺 / 位深非法 / 层级错放（任务要求的 6 类全命中），
另加 1 条全合法正例做回归护栏。

## 四、15 包全量实跑（全"跳过"，如实记录）

当前全部规范包尚无 `audio/` 目录，audio_check 对每包报告「跳过」并如实记录（非静默跳过）：

```
bbcmicro       == bbcmicro（audio/ 文件 0 个，FAIL 0，WARN 0）==
commodore64    == commodore64（audio/ 文件 0 个，FAIL 0，WARN 0）==
edsac          == edsac（audio/ 文件 0 个，FAIL 0，WARN 0）==
edvac          == edvac（audio/ 文件 0 个，FAIL 0，WARN 0）==
eniac          == eniac（audio/ 文件 0 个，FAIL 0，WARN 0）==
ibm5150        == ibm5150（audio/ 文件 0 个，FAIL 0，WARN 0）==
manchester-baby == manchester-baby（audio/ 文件 0 个，FAIL 0，WARN 0）==
pdp11          == pdp11（audio/ 文件 0 个，FAIL 0，WARN 0）==
pdp8           == pdp8（audio/ 文件 0 个，FAIL 0，WARN 0）==
system360      == system360（audio/ 文件 0 个，FAIL 0，WARN 0）==
vax11          == vax11（audio/ 文件 0 个，FAIL 0，WARN 0）==
apple-ii       == apple-ii（audio/ 文件 0 个，FAIL 0，WARN 0）==
atari-2600     == atari-2600（audio/ 文件 0 个，FAIL 0，WARN 0）==
famicom        == famicom（audio/ 文件 0 个，FAIL 0，WARN 0）==
sega-md        == sega-md（audio/ 文件 0 个，FAIL 0，WARN 0）==
```

> 注：任务文档写"13 个规范包"，但执行期间 03/05 线并行又新增了 bbcmicro、sega-md 两包，
> 现共 **15 个规范包**（03 线 11 + 05 线 4），全部 0 音频文件、全「跳过」。本报告按实际 15 包记录。

## 五、消耗条款核对

| 条款 | 达成情况 |
|---|---|
| audio_check.py ≥260 行纯 stdlib | 460 行，仅 struct/json/re/os/subprocess（stdlib） |
| 反例 ≥6 全绿 | 6 反例 + 1 正例，7/7 PASS |
| 13 包实跑 | 实际 15 包全跑，全「跳过」如实记录 |
| WAV 头解析纯 struct | 是（RIFF/fmt/data chunk 解析） |
| 迭代 ≥2 轮 | 命名正则/结构正则/A-04 判定在反例验证后各调 1 轮 |

## 六、开放问题

1. **A-03 时长口径分歧**：任务文档 sfx≤30s 与 v0.4 §9 "sfx ≤4s" 不一致，需 v0.4.x 勘误统一（本实现取任务口径）。
2. **A-02 声道匹配未落地**：任务文档仅要求采样率+位深；v0.4 §9 还有"声道数与类别匹配（vo 单声道、amb/bgm 立体声）"，未实现，留待后续（需读 WAV channels 字段，成本 S）。
3. **A-04 外部 vs 合成件的自动判定**：当前靠文件名是否出现在 SYNTH.md 判定；无法从文件名自动区分"自录原创"与"外部采购"，THIRD_PARTY 三件套行需人工保证含文件名。后续可约定"原创件也写 THIRD_PARTY 标原创"以简化判定。
4. **响度计量工具选型**：若需真 LUFS/峰值计量，须引入 ffmpeg loudnorm 或轻量库（仅 CI 侧，不入运行时），与 v0.4 附录 B 开放问题 3 对齐。
