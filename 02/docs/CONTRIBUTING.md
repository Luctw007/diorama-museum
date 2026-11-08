# CONTRIBUTING.md — 箱庭电子博物馆贡献指南（v1）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 本文档是开源准备三件套的第一件，面向**从零开始的社区贡献者**：告诉你仓库长什么样、能贡献什么、
> 每类贡献要交哪些文件、交之前怎么自测、哪些事是绝对红线。跟着做即可提交第一条合规的贡献。

箱庭电子博物馆（Hako Electronic Museum）是一个以"可拆装、可运行、可导览"为目标的电子设备数字
博物馆：每一台展品既是三维模型，也是能真正跑起来的模拟器，配目录、百科、标注与音频解说。这个
仓库承担的是"内容与规范"这一半——设备目录、内容包、模拟器槽位，以及让这一切可被机器校验的规范
与门禁。作为社区贡献者，你的最小贡献可以只是一行目录条目，最大贡献可以是一台完整设备的全部内容
包。无论大小，流程一致：认领 → 申请 id → 造物 → 自测 → 提交。

**如何选择贡献路径**：只想补充/纠错一台设备的目录信息，走路径一（一行 jsonl，最快）；想把一台
尚未收录的设备做进博物馆，走路径二（内容包，最完整）；想让某台设备"真跑起来"，在已有内容包的
基础上补模拟器槽位，走路径三（manifest，最偏工程）。三条路径共享同一套自测与红线，交之前都要过。

---

## 〇、90 秒看懂仓库

项目根目录下按「线」划分五个仓库目录，各司其职：

| 线 | 目录 | 职责 | 你在这里能贡献什么 |
|---|---|---|---|
| 01 | `01/repo/` | 网关、模拟器插槽、门禁脚本 | 模拟器槽位（manifest） |
| 02 | `02/repo/` | 规范、校验器、索引工具 | 规范条文、校验器（需走规范流程） |
| 03 | `03/repo/` | 计算机类内容包 + 目录普查 | 内容包、目录条目 |
| 04 | `04/repo/` | 设计、音频工程、验收用例 | 设计/验收文档 |
| 05 | `05/repo/` | 游戏机/家电类内容包 + 目录普查 | 内容包、目录条目 |

**三个"在哪"**（新手最常问）：

- **内容包在哪**：`03/repo/content/<device-id>/`、`05/repo/content/<device-id>/`（如
  `03/repo/content/pdp8/`、`05/repo/content/apple-ii/`）。
- **规范在哪**：`02/repo/docs/`，核心是 `内容包与目录规范_v0.6.md`（目录/分类/键名定稿）、
  `内容包规范_v0.4.md`（内容包本体规范）、`规范v0.5_槽位契约章草案.md`（槽位契约），以及
  增补 `规范增补_v0.6.1.md`、`规范增补_v0.6.2.md`、`规范增补_v0.6.3.md`（gd 脚本交互域条文，
  附 `gd_naming_check` 需求 GN-01~03）。
- **门禁在哪**：每日门禁 `01/repo/01/scripts/verify_all.py`（`--daily --cache`，日常基线 37 步全绿）；
  v0.1 发布闸 `01/repo/01/scripts/release_check.py`（R1 验收基线 / R2 三槽位三许可 / R3 完工包 ≥30，
  rc=0 方可封版）；各专项校验器在 `02/repo/tools/validate/`（`validate.py` / `model_check.py` /
  `audio_check.py` / `slot_check.py` / `catalog_check.py` / `catalog_ref_check.py`）；id 分配走
  `02/repo/tools/index/id_registry.py`。

> 分类树的机器可读权威在 `02/repo/docs/taxonomy.json`，模拟器登记母表在
> `02/repo/docs/emulators_registry.json`。这两个 json 是"单一真相源"，其 md 是渲染视图，手改无效。

---

## 一、贡献路径一：目录条目贡献（最轻量，一条 jsonl 行）

设备目录是"全库设备的可读清单"，每台设备一行 JSONL。文件位于 `03/repo/docs/catalog/*.jsonl`
与 `05/repo/docs/catalog/*.jsonl`。你只需**在对应大类的 jsonl 末尾追加一行**。

### 1.1 一条目录行的字段表（14 键，定稿英文键）

| 键 | 类型 | 必需 | 说明 |
|---|---|---|---|
| `id` | string | 是 | 全库唯一 id（大类码-中分类码-6 位序号，如 `C-PC-000123`），须向 `id_registry` 申请 |
| `name` | string | 是 | 主名 |
| `aliases` | array | 否 | 别名数组 |
| `manufacturer` | string | 否 | 厂商 |
| `origin` | string | 否 | 产地 |
| `era` | int | 否 | 年代（发布年） |
| `taxonomy_path` | array | 是 | 分类路径 `[大, 中, (子)]`，须落在 `taxonomy.json` 树内 |
| `status` | string | 是 | planned / researching / package / wip / done |
| `device_id` | string | 条件 | 关联包 device_id（done/package/wip 必填，见 §六·反链义务） |
| `influence` | string | 是 | 影响力理由（非空，≤60 字） |
| `verify` | bool | 否 | 需核实标记（false=已核，true=需核实） |
| `sources` | array | 否 | 来源编号[] |
| `research_doc` | string | 否 | 调研文档路径 |
| `media_class` | string | 否 | 介质类目（v0.6.1 新增可选字段，`cartridge/disk/tape/cd/dvd/card/firmware/app_package/无`；与 CC-10 覆盖率校验相关，见 `规范增补_v0.6.1` §二） |

### 1.2 可复制样例（照抄结构）

```json
{"id": "C-PC-000999", "name": "某个人电脑", "aliases": ["别名"], "manufacturer": "某厂",
 "origin": "某国", "era": 1985, "taxonomy_path": ["计算机", "个人机", "PC 兼容"],
 "influence": "一句话说明为何值得收录。", "status": "done", "device_id": "some-device",
 "verify": true, "sources": ["S99X"], "research_doc": null}
```

> 中文键是**非规范写法**（05 线存量遗留），新贡献一律用上表英文键。

---

## 二、贡献路径二：设备内容包贡献（核心路径）

一个内容包 = 一个 `content/<device-id>/` 目录，逐件清单如下（以 `03/repo/content/pdp8/`、
`05/repo/content/apple-ii/` 为样例）：

| 件 | 文件名 | 必需 | 样例路径 | 说明 |
|---|---|---|---|---|
| 元数据 | `meta.json` | 是 | `03/repo/content/pdp8/meta.json` | meta + assemblies + components + runtime |
| 运行时 | `runtime.json` | 是 | `03/repo/content/pdp8/runtime.json` | emulator/system/input_map/output_sinks 等 |
| 网格 | `assemblies/*.gltf` 或 `meshes/*.gltf` | 是 | `05/repo/content/apple-ii/meshes/case.gltf` | 装配体网格（v0.5 起两目录并存） |
| 网格说明 | `MESHES.md` | 是 | `05/repo/content/apple-ii/meshes/MESHES.md` | 网格命名/节点说明 |
| 标注 | `annotations/annotations.json` | 是 | `03/repo/content/pdp8/annotations/annotations.json` | 拆装/交互标注 |
| 百科 | `encyclopedia.md` | 部分 | `03/repo/content/pdp8/encyclopedia.md` | 百科条目（多数包有） |
| 第三方许可 | `THIRD_PARTY.md` | 是 | `03/repo/content/pdp8/THIRD_PARTY.md` | 外部资产的许可三件套 |

`meta.json` 的关键字段：`meta.id`（= device_id，kebab-case）、`spec_version`（跟随规范最新版）、
`meta.category`、`meta.precision_level`；`runtime.json` 关键字段：`emulator`、`system`、
`input_map`（对象格式 + 键名全集，见 `内容包规范_v0.4.md`）。

---

## 三、贡献路径三：模拟器槽位贡献

模拟器一律经槽位 manifest 声明（单一真相源，见 `规范增补_v0.6.2` §一）。槽位目录
`01/repo/slots/emulators/<slot_id>/manifest.json`，可照抄样例：

```json
{
  "slot_id": "fake-slot",
  "device_class": "console",
  "backend_type": "native",
  "description": "样例槽位：演示 manifest → 网关自动注册",
  "license": "MIT（本仓库自带）",
  "media_classes": ["cartridge"],
  "keymap": null
}
```

完整 schema（binary 多架构、license 三件套对象、capabilities 四能力位）见
`规范v0.5_槽位契约章草案` §二；`backend_type` 枚举与 `media_classes` 全集以该章为准。真实
二进制与 ROM **永不进仓**（见 §六红线），放置位置与哈希清单按 v0.5 §三执行。

---

## 四、自测口径（交包前必做，缺一不可）

1. **内容包校验 0 FAIL**：`python 02/repo/tools/validate/validate.py <包目录>`，末行须
   `FAIL 0`；建模/音频/槽位专项分别跑 `model_check.py` / `audio_check.py` / `slot_check.py`。
2. **REF 四查自检**：`python 02/repo/tools/validate/catalog_ref_check.py`，确认
   REF-01 悬空引用 0、REF-02 反链缺失 0（反链义务，原「CC-10 语义」口语已作废）、REF-04 形态
   非法 0（REF-03 台账漂移应 0）。目录规则编号现状：CC-01~08 已定稿、CC-09 为 **reserved**
   （空缺裁决）、CC-10 定义为 media_class 覆盖率、后续从 **CC-11** 起编（见 `编号与路径_封版收口_v1.md`）。
3. **目录条目自检**：`python 02/repo/tools/validate/catalog_check.py <你的 jsonl>`，逐规则 0 FAIL。
4. **id 唯一**：新 id 先 `python 02/repo/tools/index/id_registry.py allocate ...` 申请，勿手编。
5. **gd 脚本自测**（若贡献 GDScript）：`python 01/repo/01/scripts/gd_naming_check.py <godot目录>`，
   GN-01（方法名与 Object/Node 原生冲突）/ GN-02（裸 `:=` 推断 Variant）/ GN-03（class_name 未注册）
   全 0；01 线已实现该检查并纳入门禁（见 `规范增补_v0.6.3` 附录 A）。

**AI 辅助贡献者允许**：AI 产出的**史实、年代、许可**一律标 `verify: true`（目录）或写
「需核实」（THIRD_PARTY），**最终由人工确认**后才能转 `verify: false`。AI 不得替你拍板红线条目。

> **贡献者自测包**：02 线校验器可分发给贡献者打包自测，其内容清单与命令口径见
> `02/repo/docs/贡献者自测包说明_v1.2.md`（内容清单由 `02/repo/tools/contrib_kit/build_content_manifest.py`
> 脚本化生成），与本节自测口径交叉一致。

---

## 五、红线章（一票否决，触犯即退回）

1. **ROM / 二进制永不进仓**：任何固件镜像、ROM、模拟器二进制不得提交；只存 manifest 的
   哈希清单与来源，实体放外部并登记。
2. **许可三件套必需**：外部资产（音频/纹理/模型/字体）须在 `THIRD_PARTY.md` 有
   「许可分档 + 来源 URL + 获取日期」三件套，缺一不可。
3. **id 唯一性**：目录 `id` 全库唯一，由 `id_registry` 分配，严禁手编或复用。
4. **各线目录边界**：改 01 线脚本、02 线规范/校验器、03/05 内容包须对应线主权；跨线引用只读。
5. **反链义务**：完工过闸的内容包必须回填目录 `device_id` 且 `status=done`（`规范增补_v0.6.2` §六）。

---

## 六、与 01 线 git 工作流的衔接

本项目 git 化的操作卡由 01 线 81-B 产出 `01/repo/docs/git_workflow.md`，提交时遵循其约定：

- **忽略清单**：`__pycache__/`、`*.pyc`、`third_party/`（整个目录）、`slots/_drill/`、
  `demo_out/`、`docs/doctor_log_*.txt` 等临时产物一律进 `.gitignore`，二进制与 ROM 固化进 ignore。
- **提交 message**：按"类型（feat/fix/docs/chore）+ 范围 + 简述"写，分阶段 add（代码 → 文档 →
  内容树），避免大杂烩。
- **红线固化**：任何二进制与 ROM 不进版本库，是 git_workflow 的禁入清单首条。

---

## 七、贡献流程 Step-by-Step 与常见问题（FAQ）

### 7.1 从零到第一条贡献，五步走

1. **认领**：先看 `taxonomy.json` 与目录，确认设备是否已收录；未收录再动手，避免重复。
2. **申请 id**：`python 02/repo/tools/index/id_registry.py allocate <大类码> <数量> <中分类码>`，
   拿到正式 id 再写目录行或内容包，绝不手编。
3. **按路径造物**：目录贡献写一行 jsonl；内容包贡献按 §二 逐件清单补文件；槽位贡献照抄 manifest。
4. **自测**：按 §四 跑 validate + REF 四查 + catalog_check，直到全 0 FAIL。
5. **提交**：按 §六 的 git message 约定分阶段 add，红线项（二进制/ROM）一律不进库。

### 7.2 常见问题

**Q：我怎么知道一台设备该归哪个大分类？**
A：先查 `02/repo/docs/taxonomy.json`，七个大分类（计算机/游戏机/通讯与移动/家电影音/办公与
计算外设/嵌入式与工业/其他）是硬约束；中分类、子分类在树内选，找不到的路径先提 issue 讨论，
不要自由发明新层级（否则会被 catalog_check 的 CC-03 拦下）。

**Q：目录行的 `status` 该怎么填？**
A：只调研未动工写 `researching`，已开始写内容包写 `package` 或 `wip`，完工过闸写 `done`。
`done/package/wip` 三态都必须带真实 `device_id`（CC-04/CC-08 校验），且完工后按反链义务回填。

**Q：内容包的 `spec_version` 写多少？**
A：跟随 `02/repo/docs/` 下最新内容包规范版本（当前 `内容包规范_v0.4.md`）；字段格式以最新版为准，
旧包由 `tools/migrate` 迁移，新包直接按新版写。

**Q：我提交的史实/年代不确定怎么办？**
A：如实标 `verify: true`（目录）或写「需核实」（THIRD_PARTY），并尽量附 `sources` 来源编号。
不要为了"看起来完整"而编造年份或厂商，这正是红线章第 2 条的精神——宁可标需核实，不可伪造。

**Q：AI 能帮我写内容包吗？**
A：能。但 AI 产出的史实与许可一律标「需核实」，最终由人确认后才可转已核。AI 不得替你决定
红线条目（如 ROM 是否进库、许可是否够用）。

**Q：我改了别人的文件会不会被拒？**
A：各线目录有主权边界（红线第 4 条）。改 01 脚本、02 规范/校验器、03/05 内容包，须对应线
主权；跨线引用只读。想改公共资产（schema/校验器/规范），走规范变更流程，不直接改。

**Q：门禁 `FAIL n` 那行是什么意思？**
A：`catalog_ref_check.py` 统一输出 `FAIL n` 供 `verify_all` 解析，n 是 REF-01 + REF-02 + REF-04
的合计；n>0 即不合规，逐条看 `[REF-xx]` 前缀样例定位。

### 7.3 贡献礼仪与沟通

- 动工前先看目录与 `taxonomy.json`，确认没有撞车；拿不准的分类与 id，先在 issue 里问，别闷头造。
- 提交说明写清楚"改了什么、为什么"，引用的来源与出处随行附上，方便他人复核。
- 被门禁打回时，逐条看 `[CC-xx]` / `[REF-xx]` / `[R-xxx]` 前缀定位问题，修到全 0 再重新提交，
  不要把半成品留给下一个人。
- 尊重各线主权与红线章，宁可多问一句，不越界改公共资产。

### 7.4 为什么有这些规矩（设计原理）

这些规矩不是给新人添堵，而是项目从"零散手工整理"走向"万级目录可机器裁判"的必然：

- **单一真相源**（taxonomy.json / emulators_registry.json / manifest）：避免"目录说它是计算机、
  槽位说它是游戏机"的分叉，机器只认一个权威文件。
- **id 唯一 + id_registry 分配**：万级目录靠"大类码-中分类码-6 位序号"保证全库不重，手编必撞号。
- **许可三件套**：开源合规的底线，避免上游版权纠纷；这也是"开源准备"而非"内部整理"的关键差异。
- **反链义务**：只造包不回链，检索与展陈会断链；双向可溯是"目录↔内容包引用一致性"的门禁前提。

---

## 附录：路径速查

- 规范：`02/repo/docs/内容包与目录规范_v0.6.md`、`内容包规范_v0.4.md`、`规范v0.5_槽位契约章草案.md`、`规范增补_v0.6.1.md`、`规范增补_v0.6.2.md`、`规范增补_v0.6.3.md`
- 门禁：`01/repo/01/scripts/verify_all.py`、`01/repo/01/scripts/release_check.py`、`01/repo/01/scripts/gd_naming_check.py`、`02/repo/tools/validate/*.py`、`02/repo/tools/index/id_registry.py`
- 贡献者自测包：`02/repo/docs/贡献者自测包说明_v1.2.md`、`02/repo/docs/自测包内容清单_v1.2.md`
- 单一真相源：`02/repo/docs/taxonomy.json`、`02/repo/docs/emulators_registry.json`
- 样例：`03/repo/content/pdp8/`、`05/repo/content/apple-ii/`、`01/repo/slots/emulators/fake-slot/manifest.json`、`03/repo/docs/catalog/计算机大类_目录_v2.jsonl`
