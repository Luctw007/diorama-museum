# TASK-19A 完成报告（04 线第 1/2 份 · round_2 复测与缺陷闭环）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。按 MIT 许可分发。
> 完成日期：2026-11-02 ｜ 执行线：04 线（独立复测；全程未修改 01/02/03/05 线任何文件）

## 1. round_2 结论表

| 脚本/校验 | 断言/包数 | 结果 | 关键断言实值 | 完整日志 |
|---|---|---|---|---|
| m0_check（17331） | 23/23 | **PASS** | 回滚后第一帧 frame_id=6 == 保存点 5+1 | `design/rounds/m0_round_2.log` |
| m1_check 第 1 轮（17333） | 42/42 | **PASS** | **回滚后第一帧 frame_id=11 == 保存点 10+1（精确命中）**；崩溃恢复 ×2 轮、RESTART_EXCEEDED→degraded 全过 | `design/rounds/m1_round_2_run1.log` |
| m1_check 第 2 轮（17333，连续复跑） | 42/42 | **PASS** | 同上，回滚断言连续第 2 次精确命中（竞态修复统计性复核 2/2） | `design/rounds/m1_round_2_run2.log` |
| m1b_check（17334） | 19/19 | **PASS** | apple-ii：57 键全部合法（未知 0）；首键 `key_a -> {keyboard: KEY_A}`（对象形态）；baby 首键 `power -> panel.power`（legacy） | `design/rounds/m1b_round_2.log` |
| run_profile --json ×5 | 5 包 | **PASS** | baby 36 / eniac 4 / edsac 16 / edvac 4 / apple-ii 57；unknown 全 0；对象/legacy 双形态无漂移；profile_warning 全 null | `design/rounds/run_profile_round_2.log` |

环境卫生：执行前独立清空 `%TEMP%\diorama_*.json`（实查 0 残留）；netstat 复核 17331-17334 无占用。环境 Python 3.7.3（`C:\Program Files\Python37\python.exe`），四脚本 py_compile 全过（exit=0）。

**round_2 总判定：绿灯。** 结论归档 `design/rounds/round_2_结论.md`。

## 2. DEFECT 处置状态

| 编号 | round_1 | round_2 | 处置 |
|---|---|---|---|
| DEFECT-M1-ROLLBACK-01 | open | **closed** | 报告新增 §7「round_2 复测结果」：PASS 证据 3 行（m0 23/23 + m1 连续两轮 42/42，回滚首帧 == 保存点+1 精确命中）；关闭说明核验 01 线 `fake_emulator.py` `_frame_lock`（L68/L133-136/L215-234）+ `m1_check.py` TEMP 入口自清（L186-191）；无需提级 |
| DEFECT-M1B-KEYMAP-01 | open | **closed** | 报告新增 §6「round_2 复测结果」：PASS 证据（m1b 19/19、apple-ii 57 键 unknown=0、首键对象形态、五包双形态无漂移）；关闭说明核验 `run_profile.py` `MAP_KEY_RE`（L35-40）与 `_key_entry` 对象分支（L84-89）、m1b 首键断言（L211-214）；无需提级 |

- `defects/INDEX.md` 两行状态同步 open → closed 并附修复说明。
- 两条闭环均依据「复测通过」路径，未触发 09 号 §4.5 提级模板；漏斗搁置（T-023/027/028/061、T-009/025/026/037~042 等）随红灯消除解锁。

## 3. 手册 v2 变更清单

### 3.1 08 号《测试执行手册》v1.0 → v2.0

| # | 位置 | 变更 |
|---|---|---|
| 1 | 表头 | 版本升 v2.0（2026-11-02），注明 TASK-19A 依据 |
| 2 | §1 矩阵 T-025/026 | 文本按 input_map 对象形态重写：apple-ii 注入键 = device action 名 `key_a`（非 KEY_A）；KEY_A 为 MAME 侧绑定名，只在 input_map 与映射可视化右图呈现；legacy 包（baby/eniac/edsac/edvac）显示点分令牌 |
| 3 | §2.2 新增 | 「m2 草案 a~i 落位」表：逐条落位载体/端口/状态；核验 01 线 `docs/m2_assert_draft.md` 与 `scripts/m2_check.py` 均未产出（"若已产出"条件不成立），全部标「已登记，待实现」，未产出前本手册 §2.1 为草案唯一现行文本 |
| 4 | §4.2 | 每日回归最小集改为 **m0+m1b+内容包校验** 自动化三件套（带命令与判据）；原 10 条混合清单废止——m1 全量改每周/深查，手工 10 条改发版前由 01 线执行 |
| 5 | §6.4 | 五包对照表：apple-ii 补对象形态表述（57 键）；新增 edsac（qedsac，16 键）/edvac（demo_mode，4 键）行 |
| 6 | §11 新增 | 修订记录表 |

### 3.2 09 号《验收对接 01 线说明》v1.0 → v2.0

| # | 位置 | 变更 |
|---|---|---|
| 1 | 表头 | 版本升 v2.0 |
| 2 | §4.4 | 每日口径同步 08 号 v2.0 §4.2（m0+m1b+内容包校验） |
| 3 | §4.5 新增 | **缺陷提级模板**（仍失败时填写：轮次链/漏斗影响逐条/复测最小集/处置权限）；注明闭环时无需提级 |
| 4 | §5.1 新增 | **round_3 标准执行入口**：verify_all.py 预留（01 线 16-A 未产出，实查 `scripts/` 无此文件）+ 现行序贯回退双轨；上线需附 01 线回归证据、04 线复测确认后移除回退行 |
| 5 | §6 | input_event 行按键名契约 v0.2 R-086 升版（`key`=action 名；绑定名 KEY_A 不过网关） |
| 6 | §14 新增 | 修订记录表 |

## 4. round_3 建议入口

1. **首选（条件触发）**：01 线 16-A 交付 `verify_all.py` 后，round_3 以此为标准执行入口（09 号 v2.0 §5.1 双轨表上轨）。
2. **现行回退**：verify_all.py 未交付前，按 08 号 §6.1 序贯执行 `m0 → m1（全量）→ m1b → run_profile --json ×5`，日志按 09 号 §12 命名归档 `design/rounds/`。
3. 每日回归口径：08 号 v2.0 §4.2 三件套（m0 + m1b + 内容包校验），仅当 verify_all.py 上线后由其内部自动编排。
4. 追踪点：m2 草案 a~i 实现（依赖 01 线 m2_check.py）、01 线 docs/m2_assert_draft.md 产出后回填 08 号 §2.2。

## 5. 消耗条款自检

- [x] 复测日志全文存档：三脚本（m0×1、m1×2、m1b×1）+ 五包 --json 各轮完整输出均在 `design/rounds/`；
- [x] DEFECT 两份 round_2 节成稿 + INDEX 更新；
- [x] 手册 v2 变更点清单（本报告 §3）；
- [x] 迭代 ≥2 轮要求：本轮 m1 断言连续 2 次复跑（19-A §三.1 要求），且 round_1→round_2 为跨轮迭代；复测全过，未触发"发现新问题再迭代"分支；
- [x] 红线遵守：未替 01 线改任何代码（对 01 线文件仅读取与运行）。

## 6. 附：本轮产出文件清单（04 线）

| 文件 | 动作 |
|---|---|
| `docs/design/rounds/m0_round_2.log` | 新增（复测日志） |
| `docs/design/rounds/m1_round_2_run1.log`、`m1_round_2_run2.log` | 新增（复测日志，连续 2 轮） |
| `docs/design/rounds/m1b_round_2.log` | 新增（复测日志） |
| `docs/design/rounds/run_profile_round_2.log` | 新增（五包键名校验全文） |
| `docs/design/rounds/round_2_结论.md` | 新增（轮次结论，08 号 §7 模板） |
| `docs/design/defects/DEFECT-M1-ROLLBACK-01.md` | 修改（§7 round_2 节 + 状态 closed） |
| `docs/design/defects/DEFECT-M1B-KEYMAP-01.md` | 修改（§6 round_2 节 + 状态 closed） |
| `docs/design/defects/INDEX.md` | 修改（两行 closed + 修复说明） |
| `docs/design/08_测试执行手册.md` | 修改（v2.0，§3.1 清单） |
| `docs/design/09_验收对接01线说明.md` | 修改（v2.0，§3.2 清单） |
| `docs/design/TASK-19A_完成报告.md` | 新增（本文件） |