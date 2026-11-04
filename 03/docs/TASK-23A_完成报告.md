# TASK-23A 完成报告：四包 runtime 运行参数补全（display/fps）—— 前置未满足，阻塞并记录

> 任务：23-A（03 线 1/2）。为 manchester-baby / eniac / edsac / edvac 的 runtime 补全 display/fps 画面参数。
> 结论：**任务前置"02 线 v0.2.1 已支持 display 相关字段"与事实不符——v0.2.1 未新增任何 display/fps 字段**。
> 本报告如实记录核证证据、已完成的真实画面参数研究、缺省表核对，并给出阻塞结论与前进路径。四包 runtime 未被改动，维持 **FAIL 0**。

---

## 1. 核证结论：v0.2.1 未支持 display/fps

任务书 §一.1 要求"读 02 线《内容包规范_v0.2.1.md》中 runtime 的 display/fps 条款"。经逐字核对，**v0.2.1 中不存在任何 display/fps 条款**，证据如下：

| 证据项 | 实测结果 |
|---|---|
| v0.2.1 §七 RuntimeProfile 字段表 | 仅 8 字段：`emulator/version/system/media_hint/bios_required/bios_guide_url/output_sinks/input_map`，**无 display** |
| v0.2.1 全文检索 `display`/`fps`/`width`/`height`/`帧率`/`宽高` | 仅命中 surface 枚举 `crt_display`（输出面名，与画面宽高帧率无关），**无字段定义** |
| `content/schema/device_spec.schema.json` 的 `$defs/runtime` | `properties` 仅上述 8 字段，且 `additionalProperties: false` |
| 勘误记录 `docs/勘误记录_v0.2.1.md` §3 | 明确"`schema/validate.py` **无变更**"；v0.2.1 是**文档勘误版**，`meta.spec_version` 仍为 `"0.2"` |

**直接后果（已用 schema 实测验证）**：若给任意包的 `runtime.json` 增加 `display` 字段，会被
`additionalProperties: false` 拒绝 → **R-003 FAIL**（runtime 无法通过 `$defs/runtime` 校验），
与本任务自身要求的"跑 validate → FAIL 0"直接冲突。

> 关键澄清：v0.2.1 的"勘误"是**规范条文层**（input_map 对象格式定为唯一新格式、Godot `KEY_*` 键名全集定稿、§11.3 对齐网关 v2），**不涉及 runtime 结构变更**。因此"02 线 v0.2.1 已支持 display"这一前置判断不成立。

---

## 2. 四包真实画面参数研究（供 02 线未来加字段后回填）

> 本表为**研究结论 + 参考取值**，当前**不写入 runtime.json**（会触发 R-003 FAIL）。无来源处标「需核实」。

| 包 | 真实显示面 | 建议 display 取值（待规范支持） | 依据 / 备注 |
|---|---|---|---|
| manchester-baby | 3 只 Williams 管 CRT（store / accumulator / control），各显示 32 字 × 32 位点阵 | `{width:32, height:32, fps:…}`（点阵，非普通光栅） | store/control/accumulator 三屏；"32×32 点阵"为真实事实，「需核实」逐屏刷新率 |
| eniac | 无 CRT，20 累加器氖灯 + 面板指示灯 | 不适用（indicator_lamps，静态） | emulator="none"，静态展示，无帧率概念 |
| edsac | CRT 示波器（OXO 井字棋显示面） | 点阵显示，「需核实」具体点阵规格 | emulator="qedsac"，CRT 输出 |
| edvac | 无 CRT（示波器输出单元，静态展示） | 不适用（indicator_lamps，静态） | emulator="none"，静态展示 |

**关键发现**：真实设备分辨率（如 Baby 32×32 点阵）与 01 线缺省表（early-computer → 320×200@25）**差异巨大**，说明缺省表是"过渡占位"而非"真实参数"——这正是任务书要求补全的原因，也再次印证该字段须由 02 线规范先行定义。

---

## 3. 与 01 线缺省画面表的核对

01 线 `docs/runtime_mapping.md` §3 缺省表（按 `meta.category` 取缺省）：

| category | 宽×高 | fps |
|---|---|---|
| early-computer | 320×200 | 25 |
| computer / personal-computer / console | 320×240 | 24 |
| phone | 240×320 | 15 |
| 其他 | 320×240 | 24 |

四包核对结果：

| 包 | category | 缺省映射 | 核对结论 |
|---|---|---|---|
| manchester-baby | early-computer | 320×200@25 | ✅ 命中；但真实为 32×32 点阵，与缺省不符（见 §2） |
| eniac | early-computer | 320×200@25 | ✅ 命中；真实无 CRT（静态），缺省值仅占位 |
| edsac | early-computer | 320×200@25 | ✅ 命中；真实 CRT 点阵规格待核 |
| edvac | early-computer | 320×200@25 | ✅ 命中；真实无 CRT（静态），缺省值仅占位 |

> 核对结论：四包 `category` 均正确落在 `early-computer` 段，01 线缺省表当前可正常取到 320×200@25，
> 过渡策略运行无异常；但缺省值与真实设备不符，属已知开放问题（见 §5）。

---

## 4. 阻塞结论

1. **任务 §一.2"为 runtime.json 补全画面参数"当前不可执行**：schema `additionalProperties:false` 且无 display 字段，任何补写都导致 R-003 FAIL。
2. **本任务未改动四包任何文件**（避免引入校验失败）；四包保持 0 FAIL（日志见 §6）。
3. 可执行部分已完成：真实画面参数研究（§2）+ 缺省表核对（§3），作为未来回填的输入依据。

---

## 5. 前进路径与建议（开放问题）

1. **（阻塞解除点）02 线需在规范/schema 中新增 `display{width,height,fps}`（或等价字段）**：这是 01 线 `runtime_mapping.md` §3 早已标记的开放问题（"最终应由 02 线 v0.2 规范在 runtime 字段里声明 display{width,height,fps}，届时本桥删除缺省表、改为校验必填"）。建议升 02 线任务（如 24-A 或勘误 v0.2.2）。
2. **字段落地后 03 线回填**：按 §2 表写入四包 display（Baby 32×32 点阵等真实值；eniac/edvac 静态机标记不适用或 indicator_lamps）。
3. **缺省表与真实参数的矛盾**：真实机（尤其早期 CRT 点阵机）的分辨率远低于缺省值，规范新增 display 字段时需明确"点阵/指示灯类 surface 是否也需要 width/height/fps，还是仅对 CRT/主画面适用"。
4. **「需核实」清单**：Baby 三屏逐屏刷新率；EDSAC CRT 点阵规格；Baby"双 32×32"与"三 CRT"的口径差异（Baby 实为 3 只 Williams 管，任务书"双 32×32"疑为口径笔误）。

---

## 6. 四包 validate 日志（当前状态，未改动，FAIL 0）

```text
manchester-baby    总计 128 条：PASS 128，FAIL 0
eniac              总计 92 条：PASS 92，FAIL 0
edsac              总计 132 条：PASS 132，FAIL 0
edvac              总计 126 条：PASS 126，FAIL 0
```

（完整逐条日志与 18-A 报告一致，四包本轮未做任何改动，故无新增 FAIL 与迭代记录。）
