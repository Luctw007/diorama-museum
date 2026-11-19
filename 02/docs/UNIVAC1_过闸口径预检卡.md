# UNIVAC I 过闸口径预检卡（无成熟模拟器形态）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-192-A（02 线）。对象：第二批第 5 台 UNIVAC I（目录 `C-MF-000050`，S 档，1951 首台商用
> 电子计算机）。性质：**口径预检**——只给 03 线产包用的过闸口径，不产包、不改校验器代码。

## 〇、一句话结论（三问三答）

| 问题 | 结论 |
|---|---|
| `emulator` 字段怎么写 | **`emulator="none"`**（否决 `null` 与 `simh-univac`） |
| S/A/B 档判定 | **允许 S 档过闸**，件清单全规格 + 静态+原理动画，模拟器作 NOTE 级提示 |
| 校验器放行 | **已放行 `emulator="none"`，无需改校验器**；`null` 会 FAIL（schema required string） |

## 一、`emulator` 字段「无成熟模拟器」怎么写

### 1.1 三选一裁决

| 候选 | 裁决 | 理由 |
|---|---|---|
| `emulator="none"` | **采纳（推荐）** | ① 既有先例一致（eniac / edvac / nokia-3310 均用 `"none"` 静态展示，validate 0 FAIL 已证放行）；② 语义明确——"静态展示、无模拟器"的显式声明，不是"没做完" |
| `emulator=null` | **否决** | schema `runtime.emulator` 是 **required + type=string + pattern `^[a-z][a-z0-9_-]*$`**（`device_spec.schema.json` L263-266），`null` 不满足 string、且 required 字段不能 null，会 FAIL R-003 |
| `simh-univac`（需核实） | **否决** | 研究卡明说"无成熟模拟器，SIMH 候选需核实"；写 `simh-univac` 会声称一个 SIMH 里并不存在的后端，重蹈 apple-ii"槽位未建立"的误导 |

### 1.2 建议写法（供 03 线照抄）

```json
{
  "emulator": "none",
  "version": "0.0.0",
  "system": "UNIVAC I（静态展示）",
  "media_hint": "tape",
  "bios_required": false,
  "bios_guide_url": null,
  "output_sinks": [ ... ],
  "input_map": { ... }
}
```

- `system` 写「UNIVAC I（静态展示）」，与 eniac/edvac 先例一致。
- `media_hint="tape"`（UNIVAC I 是首批用磁带作主存储的计算机之一，研究卡 §一）。
- 模拟器候选（SIMH 需核实）**不进 `emulator` 字段**，改记在 `THIRD_PARTY.md` 与 `encyclopedia.md`
  的「模拟器可行性」段（"SIMH 候选需核实、槽位 dedicated 预留、不下发二进制"），供后续接入。

## 二、S/A/B 档判定归属

UNIVAC I 是 **S 档**（第二批第 5 台、镇馆级、"首台商用电子计算机"的叙事锚点）。「无成熟模拟器」不影响
它作为 S 档的**建模/标注/百科全规格**——只影响"运行"这一件：

- **件清单**：照 S 档全规格——meta/runtime + assemblies 全（中央处理机柜/内存/磁带机/控制台/打印机
  五部件，研究卡 §三）+ annotations 含 flow（大选预测、磁带读写、真空管开关原理）+ encyclopedia
  （2548 字量级）+ THIRD_PARTY 三件套。
- **模拟器**：`emulator="none"`（静态 + 原理动画），模拟器缺失作 **NOTE 级提示**（不是 FAIL、不算 WIP
  缺口）——与 S 档口径"无 bone 不算缺口"一致，只是 UNIVAC I 是"连候选都需核实"的更强形态。
- **反链 / 门禁**：照 S 档——目录 `device_id` + `status=done`，`pkg:*` 进 ready 全绿。

## 三、校验器放行口径（实测依据）

- **`emulator="none"` 已放行**：schema `runtime.emulator` 的 pattern `^[a-z][a-z0-9_-]*$` 匹配 `none`
  （全小写字母）；既有 eniac / edvac / nokia-3310 三包均 `emulator="none"` 且 validate 84 PASS / 0 FAIL，
  实证放行。
- **`emulator=null` 不放行**：schema required + type=string，`null` 触发 R-003 FAIL。
- **结论**：**无需改校验器**，口径层写 `emulator="none"` 即可；若未来确有"待核实模拟器"需要新枚举值
  （如 `pending`），属**改校验器（另开任务）**，本预检不预占。

## 四、给 03 线产包的落地清单

1. `runtime.emulator="none"`、`system="UNIVAC I（静态展示）"`、`media_hint="tape"`；
2. S 档件清单全规格（五部件 assemblies + flow 标注 + 百科 + THIRD_PARTY 三件套）；
3. 模拟器候选（SIMH 需核实）记入 THIRD_PARTY.md / encyclopedia.md，不进 emulator 字段；
4. 过闸自测：`validate.py` 0 FAIL + `catalog_ref_check` REF 四查 0 + 反链 done。

## 五、与任务书的漂移（如实）

- 分档口径文件实际名为 `第二批分档验收口径_v1.md`（标题已是 v2），任务书写 `_v2.md`，本预检按实际
  文件名追加条款。
- 校验器放行结论以 schema（`device_spec.schema.json` L263-266）与既有包实测为准，非凭经验。
