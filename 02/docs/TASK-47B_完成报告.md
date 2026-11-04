# TASK-47B 完成报告（02 线 2/2）：槽位与介质校验器 slot_check.py

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码均按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-47B（02 线 2/2）：槽位与介质校验器 slot_check.py |
| 前置 | TASK-47A（槽位契约章 v0.5） |
| 目标 | 槽位契约的可运行裁判——manifest 与介质目录放错即刻报错 |
| 状态 | 完成 |

---

## 一、交付物清单

| 文件 | 说明 | 规模 |
|---|---|---|
| `tools/validate/slot_check.py` | 槽位与介质校验器（纯 stdlib） | 470 行（≥260 达标） |
| `tools/validate/tests/run_slot_tests.py` | 反例测试（6 反例 + 1 正例） | 7/7 全绿 |
| `docs/TASK-47B_完成报告.md` | 本报告 | — |

## 二、规则↔规范条号对照表

| 规则 | 规范条号 | 落地判定 | 级别 |
|---|---|---|---|
| SV-01 manifest 存在且 JSON 合法 | v0.5 §2（manifest schema） | `manifest.json` 存在 + json.load 成功 | FAIL |
| SV-02 schema 关键字段类型/枚举 | v0.5 §2.4/2.5/2.8 + §3.1/3.2/3.3 | slot_id kebab + 目录名一致；device_class/backend_type/media_classes 全枚举；binary 多架构键白名单；capabilities 布尔 | FAIL/WARN |
| SV-03 二进制路径存在 + 介质扩展名 | v0.5 §2.6/2.7 + §3.3/§4.1 | 二进制（含 .exe 变体）在槽位目录；介质文件扩展名命中 media_class 约定 | FAIL |
| SV-04 许可三件套字段齐全 | v0.5 §2.9 + §5.3 | license 对象须 tier+url+date；字符串非空 PASS；介质来源三件套 WARN | FAIL/WARN |
| SV-05 哈希清单行格式 | v0.5 §5.2 | `SHA256SUMS` 每行 `64hex + 空格 + 文件名` | FAIL |

## 三、样例槽位 + 反例命中表

### 3.1 样例槽位（01 线 fake-slot）实跑

```
== 槽位系统（槽位 1 个，介质目录 0 个，FAIL 0，WARN 0）==
  fake-slot
    PASS SV-01  manifest 存在且 JSON 合法
    PASS SV-02  slot_id fake-slot 合法
    PASS SV-02  device_class console 合法
    PASS SV-02  backend_type native 合法
    PASS SV-02  media_classes ['cartridge'] 合法
    PASS SV-03  无 binary（native/零二进制后端）
    PASS SV-04  许可简写字符串非空（MIT（本仓库自带））
  [media/]
    PASS SV-03  media/: 介质扩展名均符合类目约定（或无介质文件）
    PASS SV-05  media/: 无 SHA256SUMS（可选，跳过）
    PASS SV-04  media/: 介质来源登记齐备（或无介质文件）
```

fake-slot 样例全 PASS（FAIL 0），验证了与 46-A 样例的契约一致性。

### 3.2 反例命中表（7/7 全绿）

```
[PASS] 反例01：缺 manifest → SV-01 FAIL
[PASS] 反例02：枚举非法（device_class）→ SV-02 FAIL
[PASS] 反例03：二进制缺失 → SV-03 FAIL
[PASS] 反例04：介质扩展名错 → SV-03 FAIL
[PASS] 反例05：三件套缺（license 对象）→ SV-04 FAIL
[PASS] 反例06：哈希行坏 → SV-05 FAIL
[PASS] 正例07：全合法（三件套对象 + 介质）→ 无 FAIL（exit 0）
```

反例覆盖任务要求的 6 类（缺 manifest/枚举非法/二进制缺失/扩展名错/三件套缺/哈希行坏）全命中。

## 四、15 包 slot 回填基线（v0）

用 47-A 建议表对现有 15 包做"当前声明状态"扫描，结果**全部未声明**（`runtime.slot` 为空）：

```
bbcmicro/commodore64/edsac/edvac/eniac/ibm5150/manchester-baby/pdp11/pdp8/
system360/vax11/apple-ii/atari-2600/famicom/sega-md  →  全部 slot=None（未声明）
汇总：15 包，已声明 0，未声明 15（基线 v0：全空）
```

- 基线 v0 已如实记录：15 包无一声明 `slot` 字段。
- 待 03/05 线按 47-A §7.1 分批回填后，基线推进到 v1（可据此做"未声明 vs 已声明"统计）。

## 五、四套测试全绿自检

```
run_tests        结果：PASS 21，FAIL 0
run_model_tests  结果：PASS 7，FAIL 0
run_audio_tests  结果：PASS 7，FAIL 0
run_slot_tests   结果：PASS 7，FAIL 0
```

## 六、消耗条款核对

| 条款 | 达成 |
|---|---|
| slot_check.py ≥260 行纯 stdlib | 470 行 ✅ |
| 反例 ≥6 全绿 | 6 反例 + 1 正例，7/7 ✅ |
| 样例槽位 pass + 6 反例命中表 | §3.1/§3.2 ✅ |
| 迭代 ≥2 轮 | 介质路径双写 bug 修复 1 轮 + 正例补三件套对象 1 轮 ✅ |
| 不下载不放置真实介质 | 全程仅临时目录合成最小文件（bytes b"x"），无真实介质 ✅ |

## 七、TASK-47 两份总收尾

- **47-A**：`规范v0.5_槽位契约章草案.md`（8075 汉字，含全量 schema + 三大枚举 + 15 包回填建议 + 5 条设计裁决）。
- **47-B**：`slot_check.py`（470 行，SV-01~05）+ 反例 7/7 全绿 + fake-slot 样例 pass + 15 包基线 v0。

## 八、开放问题

1. **backend_type `dedicated` 是否拆分**（VICE/BeebEm/BlastEm/PC-86 逐一命名 vs 统一 dedicated）。
2. **license 简写字符串存废**（正式版是否强制三件套对象）。
3. **capabilities 与 demo_mode**（需 46-B 落地后对齐）。
4. **多架构表运行时选择**（loader 按宿主平台选 binary 变体，46-A 未实现）。
5. **介质来源三件套登记位置**（README.md vs SOURCES.md）。
6. **`runtime.slot` 回填触发点**（15 包回填 + 评审后，`runtime.emulator` 是否退役）。
7. **slot_check 与门禁集成**：当前 slot_check 为独立工具，尚未接入 regress_all/collect_index；待 46-B 门禁落地后，可加 `--with-slot` 档位与索引 slot 列。
