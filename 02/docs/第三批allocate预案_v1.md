# 第三批 allocate 预案 v1（id 分配预案，待用户点头后执行）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-267-A（02 线）。定位：第三批定案四步中「02 复核已完成（262-B，结论维持 242-A 顺序，待用户
> 点头 3 项）」，本任务**先行产出 allocate 预案**——10 台目录 id 分配预案 + 目录归属 + 执行清单 + 依赖声明。
> **只改 02 目录，纯文档预案，不 allocate、不改任何目录 jsonl。**
>
> 母本：`第三批产包顺序02侧复核_v1.md`（262-B）；验收清单：`第三批产包验收清单_v1.md`（252-B）；
> id 规则：`id_registry.py`（57-B，id = 大类码-中分类码(2~4 大写)-6 位序号）。

## 一、10 台 device_id + 目录 id 分配预案表

| # | 顺序（242-A） | device_id 建议（包 id） | 目录 id 占位 | allocate 分组 | 续接序号（预案） | 目录归属 |
|---|---|---|---|---|---|---|
| 1 | IBM System/370 | ibm-system370 | C-MF-0000xx | C MF 1 | C-MF-000085 | 计算机大类 v2 |
| 2 | MSX2（Panasonic FS-A1） | msx2 | C-PC-0000xx | C PC 6 | C-PC-000209 | 计算机大类 v2 |
| 3 | Macintosh Plus | macintosh-plus | C-PC-0000xx | C PC 6 | C-PC-000210 | 计算机大类 v2 |
| 4 | IBM PC XT | ibm-pc-xt | C-PC-0000xx | C PC 6 | C-PC-000211 | 计算机大类 v2 |
| 5 | Acorn Archimedes | acorn-archimedes | C-PC-0000xx | C PC 6 | C-PC-000212 | 计算机大类 v2 |
| 6 | Sinclair ZX81 | sinclair-zx81 | C-PC-0000xx | C PC 6 | C-PC-000213 | 计算机大类 v2 |
| 7 | SGI Indigo | sgi-indigo | C-WS-0000xx | C WS 1 | C-WS-000055 | 计算机大类 v2 |
| 8 | Compaq Portable | compaq-portable | C-PC-0000xx | C PC 6 | C-PC-000214 | 计算机大类 v2 |
| 9 | Whirlwind | whirlwind | C-EC-0000xx | C EC 1 | C-EC-000014 | 计算机大类 v2 |
| 10 | Apple Newton MessagePad | apple-newton | M-PD-0000xx | M PD 1 | M-PD-000070 | 通讯与移动 v3 |

> 续接序号依据：registry.jsonl 各前缀当前最大序号——C-MF=84 / C-PC=208 / C-WS=54 / C-EC=13 / M-PD=69，
> 预案续接 = 最大值 + 1 起顺序分配。**实际序号以 allocate 执行时 id_registry 计算为准**（续号纳入
> 「台账 ∪ 目录已用 id」，若目录已用 id 超出本预案序号，allocate 会自动跳过，不撞号）。

## 二、id 命名规则核对 + 无冲突核对

1. **device_id 命名（kebab-case slug）**：10 个建议 id 均符合 `^[a-z0-9]+(-[a-z0-9]+)*$`，与 03 线研究卡/
   口径卡建议 id 对齐（252-B §一「包 id 建议」列原文沿用）。
2. **与现有 47 包无冲突**：10 个 device_id（ibm-system370 / msx2 / macintosh-plus / ibm-pc-xt /
   acorn-archimedes / sinclair-zx81 / sgi-indigo / compaq-portable / whirlwind / apple-newton）逐一与门禁
   47 个 ready 包 device_id 对账，**无重复**。注意区分：现有 `system360`（IBM System/360）≠ 新 `ibm-system370`、
   现有 `macintosh128k` ≠ 新 `macintosh-plus`、现有 `ibm5150` ≠ 新 `ibm-pc-xt`，均不撞号。
3. **目录 id 不撞号**：10 台续接序号落在各自前缀最大号之后，与 registry 现有 1583 条不重。

## 三、目录归属预案（只列方案，不落 jsonl）

| 归属文件 | 台数 | 设备 |
|---|---|---|
| `03/repo/docs/catalog/计算机大类_目录_v2.jsonl` | 9 | System/370（C-MF）、MSX2/Macintosh Plus/IBM PC XT/Archimedes/ZX81/Compaq Portable（C-PC ×6）、SGI Indigo（C-WS）、Whirlwind（C-EC） |
| `03/repo/docs/catalog/通讯与移动大类_目录_v3.jsonl` | 1 | Apple Newton（M-PD） |

> 说明：10 台全入 03 线活跃目录（计算机 v2 + 通讯 v3），与第二批/第三批口径一致；产包后目录条目
> `device_id=<包 id>` + `status=done` 由 03 线回填（反链责任=产包线，252-A 口径）。

## 四、allocate 执行清单（用户点头后逐条执行，本任务不执行）

> 前置条件：定案四步「用户点头 → 01 线登记」两步完成后，才轮到本清单的 02 线 allocate。

1. **用户点头**：确认 262-B 待点头 3 项（顺序维持 / 模拟器合规路径 / BIOS-ROM 红线）。
2. **01 线登记**：第三批 10 台正式定案登记（定案四步第三步，01 线）。
3. **02 线 allocate**（按中分类码分 5 组，共 10 号）：
   ```
   python tools/index/id_registry.py allocate C MF 1   # System/370
   python tools/index/id_registry.py allocate C PC 6   # MSX2/MacPlus/PCXT/Archimedes/ZX81/CompaqPortable
   python tools/index/id_registry.py allocate C WS 1   # SGI Indigo
   python tools/index/id_registry.py allocate C EC 1   # Whirlwind
   python tools/index/id_registry.py allocate M PD 1   # Apple Newton
   ```
4. **03 线回填目录**：把 allocate 返回的 10 个真实目录 id 填入 9 台计算机大类 + 1 台通讯大类目录条目。
5. **03 线逐台产包**：按 242-A 顺序领办，每台产包完成即回填 `device_id` + `status=done`（反链义务，252-A）。
6. **门禁复测**：全部产包 + 反链后，`verify_all --daily --cache` 预期升至 64/64 级（10 个新 `pkg:*` 入 ready），
   `catalog_ref` REF 四查 0 冲突。

## 五、与 262-B 待点头 3 项的依赖声明

**点头前不执行**：本预案仅为「待用户点头」后的执行蓝图，不 allocate、不改目录 jsonl、不产包。用户点头前，
allocate 分组/续接序号/目录归属均为预案（序号以 allocate 实算为准）。若用户对 262-B 顺序或模拟器合规路径
提出调整，本预案的 device_id/分组随之修订后再落地。

## 六、红线自查

零联网、零下载（纯文档预案）；id 命名以仓库规范（id_registry ID_RE + 47 包实账）为准，未臆造；只改 02
目录、未 allocate、未改任何目录 jsonl、未改 01/03/04/05 线、未产包。
