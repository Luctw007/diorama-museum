# TASK-30B 完成报告（Apple II 分批建模任务卡 · 第一批：外壳+键盘）

> 任务：TASK-30B（05 线 2/2）· 里程碑 M1 · 与 30-A 共同构成 TASK-30 两份。
> 依据：19/20 号冻结表、11 号 brief、02 线 v0.3 草案。
> 完成日期：2026-11-02。

---

## 一、字数统计（实测 CJK 字符数）

| 文件 | 字数（中文字符，实测） |
|---|---|
| `docs/research/apple-ii/21_建模任务卡_第一批.md` | 6031（≥6000 达标，卡片为主） |
| `docs/research/apple-ii/22_建模验收清单_第一批.md` | 775（人工核对表，以勾选项为主） |

> 21 号为"卡片为主"文档，除 CJK 外含大量数字、英文 node_id 与预算表。字数以正则统计 CJK 字符为准。

## 二、任务卡清单表

| 卡片 | 目标文件 | LOD1 预算 | 关键约束 |
|---|---|---|---|
| 卡片 1 case | `meshes/case.gltf` | ≤800 | 圆润曲面、面板卡口、含 badge/handle/vent_grille 子节点 |
| 卡片 2 lid | `meshes/lid.gltf` | ≤500 | **开盖铰链轴 Y=+108.0mm/Z=−222.5mm 沿 +X** |
| 卡片 3 bottom | `meshes/bottom.gltf` | ≤500 | 机脚独立子节点、铭牌只做凹槽 |
| 卡片 4 keyboard | `meshes/keyboard.gltf` | ≤400 | 卡口干涉检查、+Z 展开主轴 |
| 卡片 5 keycap_array | `meshes/keycap_array.gltf` | ≤600 | 键帽内凹弧面、字符自绘、实例化 |
| 卡片 6 keyswitch_array | `meshes/keyswitch_array.gltf` | ≤300 | 键杆导槽、实例化 |
| 卡片 7 keyboard_pcb | `meshes/keyboard_pcb.gltf` | ≤150 | 焊盘对应、走线丝印表达 |

每卡字段完整（目标文件/三档 LOD 预算/贴图清单/枢轴铰链/命名表/验收核对行/错误vs正确示例），并附附录 A（逐件建模要点详解）、C（v0.3 规则转述）、D（返工点清单）。

## 三、给建模执行方的一句话交付契约（模板）

> "本批交付 7 件 glTF（case/lid/bottom/keyboard/keycap_array/keyswitch_array/keyboard_pcb），节点名=文件名=node_id，米制 Y-up 右手系，LOD1 观察档面数 ≤ 各卡预算，贴图 `_basecolor/_metallic_roughness/_normal` 后缀、2048 为 2 的幂，开盖铰链轴 Y=+108.0mm/Z=−222.5mm 沿 +X。以 19 号冻结表 + 20 号材质表 + 21 号任务卡为唯一依据，超预算或命名不符即退回。"

## 四、开放问题

1. **27-A model_check 未产出**：本批验收核对行按 27-A 任务文档定义的 MR-01~04 规则写"将如何通过"，但 model_check.py 尚在 02 线本轮任务中；待其产出后，22 号清单的自动校验命令从 budget_check.py 切换为 model_check.py。
2. **MR-02 的 LOD 命名笔误**：27-A 任务文档写"LOD0 高模/LOD1 观察/LOD2 特写"，与 v0.3 草案 §3.1"LOD0 特写/LOD1 观察/LOD2 远景"冲突（LOD2 不应是"特写"）。本批以 v0.3 §3.1 为准，已在 21 号 §〇 注明。
3. **整机三围/键帽弧面/编码器型号**：仍"待实测/待核实"，本批沿用 19 号冻结的近似值（延续 25-B 开放问题）。
4. **第二批范围**：内部结构（mainboard/power/disk_ii/元器件）留待第二批任务卡，复用本批模板。

## 五、TASK-30 两份总收尾

- **30-A（FC/NES 设备包生产）**：产出 `content/famicom/` 完整内容包（meta/runtime/6 件 glTF/30 条标注/2532 字百科/THIRD_PARTY），**validate.py 100 PASS / 0 FAIL**，定档 1983 红白机，给出与 atari-2600 的"奠基区—复苏区"动线雏形。
- **30-B（Apple II 分批建模任务卡）**：产出 `21_建模任务卡_第一批.md`（6031 字）+ `22_建模验收清单_第一批.md`，把 19 号冻结表翻译成可交付执行方的逐件任务卡。
- **05 线本轮收尾**：游戏机厅第二台（Famicom）已开产并通过校验；Apple II 正式建模第一批（外壳+键盘）的任务卡与验收清单就绪，具备交给外包或生成器的完备度。同时完成 19 号冻结表向 v0.3 草案三档 LOD 口径的对齐。
