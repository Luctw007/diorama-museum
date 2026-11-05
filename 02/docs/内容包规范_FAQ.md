# 内容包规范 FAQ 汇编

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。
>
> 任务：TASK-129（02 线）。定位：把散落在多版规范文档里的高频问答汇编成 FAQ，每条标注出处
> （规范版本 + 章节/条文号），供内容线与贡献者快速查阅。答案只转述现有规范结论，不新增规则。

## 一、目录键名与 id

**Q1 目录条目用英文键还是中文键？**
A：统一英文定稿键 13 个（id/name/aliases/manufacturer/origin/era/taxonomy_path/status/device_id/
influence/verify/sources/research_doc）；05 线中文字段列为"非规范写法"，新贡献一律英文键。
出处：`内容包与目录规范_v0.6.md` §一、§1.3。

**Q2 05 线中文键怎么迁移？**
A：11 键对照表直接改名（名称→name、别名→aliases、厂商→manufacturer、分类路径→taxonomy_path、
影响力理由→influence、状态→status、关联包→device_id 等），值不变可脚本化批量完成。
出处：`内容包与目录规范_v0.6.md` §1.3。

**Q3 目录 id 格式是什么？**
A：`大类码-中分类码-6 位序号`，如 `C-PC-000123`；大类码 C/G/M/A/P/E/X，中分类码 2~4 字符，
正则 `^[CGMPAEX]-[A-Z]{2,4}-\d{6}$`。出处：`内容包与目录规范_v0.6.md` §七、`catalog_check.py` CC-02。

**Q4 新 id 怎么申请？**
A：走 `id_registry.py allocate <大类码> <数量> [中分类码]` 正式分配，严禁手编。
出处：`id_registry.py`、`内容包与目录规范_v0.6.md` §七。

## 二、分类与 media_class

**Q5 分类路径必须写满三级吗？**
A：不必。三级推荐、两级允许；两级时第三级视为「未细分」（如 `["家电影音","影音播放机"]`）。
出处：`内容包与目录规范_v0.6.md` §二。

**Q6 分类路径能不能自由发明层级？**
A：不能，必须整条落在 `taxonomy.json` 官方树内（大分类 7 类硬约束），否则 catalog_check CC-03 拦截。
出处：`catalog_check.py` CC-03、`taxonomy.json`。

**Q7 media_class 有哪几类？**
A：cartridge / disk / tape / cd / dvd / card / firmware / app_package / 无（无介质，是合法值非缺失）。
出处：`规范增补_v0.6.1.md`、v0.5 槽位契约 §3.3。

**Q8 media_class 怎么定？**
A：用 `media_infer.py` 按「分类路径 + 关键词」规则推定（R01~R60 + 关键词 K01~K10），输出建议表供回填；
置信度 <0.6 须人工复核。出处：`media_infer.py`、`规范增补_v0.6.1.md`。

## 三、THIRD_PARTY 与许可

**Q9 第三方资产要登记什么（三件套）？**
A：「许可分档 + 来源 URL + 获取日期」三件套，缺一不可；非原创条目必须填 URL 与日期。
出处：`内容包规范_v0.1.md` 第八章、各包 `THIRD_PARTY.md`。

**Q10 许可分档有哪几档？**
A：`原创` / `公共领域` / `CC` / `授权许可` / `仅视觉参考` 五档。
出处：`内容包规范_v0.1.md` 第八章。

**Q11 ROM/二进制能进仓吗？**
A：不能，红线——ROM/固件/磁盘镜像/模拟器二进制永不进仓、不自动下载；只在 THIRD_PARTY 登记来源。
出处：`licenses/MAME.md` FR-E3、`CONTRIBUTING.md` 红线章。

## 四、反链与规则

**Q12 完工包为什么必须回填目录 device_id？**
A：反链义务——完工过闸 ready 的内容包必须在其目录条目回填 device_id 且 status=done，使包↔目录双向可溯；
缺失由 catalog_ref_check REF-02 拦截。出处：`规范增补_v0.6.2.md` §六。

**Q13 CC 规则和 REF 规则有什么区别？**
A：CC（CC-01~08）是目录单表校验（字段/格式/分类/状态/年代/理由/别名/device_id）；REF（REF-01~04）
是跨"目录↔内容包"引用一致性（悬空引用/反链缺失/台账漂移/形态非法）。出处：`catalog_check.py`、
`catalog_ref_check.py`。

## 五、gd 脚本与生成物

**Q14 gd 方法名能和 Godot 原生方法重名吗？**
A：不能。get_index/get_meta/get_name/get_parent/get_class/get_path 等 Object/Node 原生方法名黑名单，
命名前自查，冲突即改名。出处：`规范增补_v0.6.3.md` v0.6.3-01（反例 DEFECT-RUN-01）。

**Q15 `:=` 推断类型要注意什么？**
A：凡结果可能为 Variant（三元两分支不收敛、动态调用返回值），必须显式标注类型（`: String` 等），
不得裸 `:=` 推断 Variant（项目 warning-as-error）。出处：`规范增补_v0.6.3.md` v0.6.3-02（RUN-01/02）。

**Q16 改了 class_name 为什么还报"类名未注册"？**
A：须删除 `.godot/` 缓存目录后重开引擎（Reload），否则 Godot 沿用旧类表。
出处：`规范增补_v0.6.3.md` v0.6.3-03（RUN-03）。

**Q17 哪些生成物不入库？**
A：`.godot/`、`demo_out*/`、`slots/_drill/`、`__pycache__/`、`*.pyc` 等缓存/帧/临时产物一律进 `.gitignore`。
出处：`规范增补_v0.6.3.md` v0.6.3-08、`.gitignore`。

**Q18 白模占位网格无材质，高亮怎么保证可见？**
A：高亮系统须对无材质网格现建 StandardMaterial3D override，不得以 material_override is
StandardMaterial3D 为前置条件。出处：`规范增补_v0.6.3.md` v0.6.3-04（RUN-07）。

## 六、模拟器与错误码

**Q19 模拟器怎么登记？**
A：单一真相源——一切模拟器经 `slots/emulators/<id>/manifest.json` 声明，网关内置 EMULATORS 仅兜底、
须与同名槽位语义一致，新后端必须走槽位。出处：`规范增补_v0.6.2.md` §一。

**Q20 EMULATOR_BINARY_MISSING 和 EMULATOR_BACKEND_MISSING 区别？**
A：前者"有模块、无二进制"（给安装指引）；后者"无模块、预留槽位"（指引待后端实现）——两条独立路径。
出处：`规范增补_v0.6.2.md` §二。

**Q21 模拟器许可未核实怎么办？**
A：如实标「需核实」，不做新查证、不升级结论；许可未核实不得擅自把 reserved/researched 升为可接入。
出处：`许可台账_v1.md`、`规范增补_v0.6.2.md`。

## 七、贡献与流程

**Q22 贡献内容包交包前要过什么？**
A：validate 0 FAIL + catalog_ref 四查 + THIRD_PARTY 三件套 + 史实需核实标注；AI 产出须人确认。
出处：`CONTRIBUTING.md` §四、`github_templates/PULL_REQUEST_TEMPLATE.md`。

**Q23 内容包有哪些必备文件？**
A：meta.json / runtime.json / glTF（assemblies 或 meshes）/ MESHES.md / annotations/annotations.json /
THIRD_PARTY.md（encyclopedia.md 部分包有）。出处：`CONTRIBUTING.md` §二。

**Q24 规范版本这么多，以哪个为准？**
A：以《内容包与目录规范 v0.6》正文（§一~§七）为准绳，增补 v0.6.1/v0.6.2/v0.6.3 在正文之上追加条文
（不升主版本）。出处：`内容包与目录规范_v0.6.md` §八。

---

> 覆盖清单：目录键名（Q1/2）· 分类两层（Q5/6）· id（Q3/4）· media_class（Q7/8）· THIRD_PARTY（Q9/10）·
> 许可（Q11/21）· 反链（Q12）· CC/REF（Q13）· gd 命名与 `:=`（Q14/15）· class_name/缓存（Q16）·
> 生成物（Q17）· 白模材质（Q18）· 模拟器单一真相源（Q19）· 错误码（Q20）· 贡献流程（Q22/23）· 版本（Q24）。
> 共 **24 条**，≥20 达标。
