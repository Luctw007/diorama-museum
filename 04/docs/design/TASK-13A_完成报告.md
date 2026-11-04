# TASK-13A 完成报告（M1 测试执行手册 + 01 线验收对接说明）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本报告按 MIT 许可分发。

| 项 | 内容 |
|---|---|
| 任务 | TASK-13A（04 线第 1/2 份）：08 测试执行手册 + 09 验收对接说明 |
| 状态 | 完成（纯文档产出；红线：未写网关/游戏代码） |
| 日期 | 2026-10-31 |

---

## 1. 交付物清单

| 文件 | 说明 | 汉字数（实测） |
|---|---|---|
| `docs/design/08_测试执行手册.md` | 72 行三档矩阵（8 列全量）+ m1_check 对照表 20 行 + 新增断言草案 7 条 + 手工执行记录模板 + 执行顺序与 10 条日常回归集 | 见 §6 汇总 |
| `docs/design/09_验收对接01线说明.md` | 断言命名规则、日志格式、失败贴证要求、与 11-B（m1b_check）衔接条款 | 见 §6 汇总 |
| `docs/design/TASK-13A_完成报告.md` | 本报告 | — |

---

## 2. 三档统计（按 08 号矩阵实测）

| 档位 | 数量 | 构成 |
|---|---|---|
| 自动化 | 12 | T-043~T-049、T-051、T-053、T-055、T-056、T-061 |
| 手工 | 43 | 其余桌面/共用 UI 用例（含携带网关补验的 T-023/025/027/028 及 T-037~T-042 向导组） |
| 待实机 | 17 | 全部 VR 用例：T-002/004/006/008/010/015/018/020/024/026/030/034/036/042/052/062/069 |
| 合计 | 72 | 与 05 号 v2（T-001~T-072）一致 |

---

## 3. 矩阵关键行摘录

| 用例 | 档位 | 网关验证点（摘录） | 关联 FR |
|---|---|---|---|
| T-051 | 自动化 | error{PROCESS_CRASHED} → status{restarting} → status{running} → 帧恢复（frame_id 回跳至 __auto 附近）；m1_check 第 10/11 轮已覆盖 | FR-E8c |
| T-053 | 自动化 | frame_chunk 按 (device_id,frame_id) 收齐 total 片；重组解码 raw_len==w*h*3；m1_check 第 5 项已覆盖 | FR-I2 |
| T-055 | 自动化 | heartbeat_ack{running_devices:{dev1:"running",dev3:"running"}}；m1_check 第 9 项已覆盖 | FR-I4 |
| T-061 | 自动化 | load_state_ack{frame_id==保存点} + 回滚后首帧 frame_id≤保存点+3；m1_check 第 8 项已覆盖 | FR-G4 |
| T-046 | 自动化 | error{RESTART_EXCEEDED} + status{degraded}；m1_check 第 12 项已覆盖 | FR-E8b |
| T-023 | 手工(网关辅助) | start_device_ack{ok:true, info.sinks:["main","speaker","led"]}（fake 320×240@24 补验） | FR-E1/E6 |

---

## 4. 新增断言草案清单（08 号 §2.1 与表 2B，8 条）

| 草案 | 命名 | 覆盖用例 | 判定要点 |
|---|---|---|---|
| a | check_e8_manual_mode | T-043/044/045 | auto_restart=false 崩溃→crashed 保持不重启→stop 后重启成功 |
| b | check_e9_gw_disconnect | T-048 | 杀网关→TCP EOF；重启→heartbeat_ack 空设备表 |
| c | check_g3_load_missing | T-049 | load 不存在 id→error{NOT_FOUND}；合法 id 仍可 load |
| d | check_i4_snapshot_isolation | T-056 | 双设备各自 save/load 保存点匹配；input_ack 不串设备 |
| e | （撤销，并入 m1_check#37） | T-046 收尾 | degraded 可 stop |
| f | check_f2_pkg_version_gate | T-003/004 | engine_min_version 高于引擎 → 拒绝加载（Godot 单测） |
| g | check_e4_media_magic | T-039 | floppy 魔数不匹配 → 返回固定错误文案（Godot 单测） |
| h | check_e8_manual_retry_power | T-044 强化 | 重试后新进程签名 frame_id 从 1 重新递增（并入 a 第三段） |
| i | check_i2_chunk_gap | T-053/054 | 人为丢片必报缺片错；完整流零报错（注入式 drop 开关） |

---

## 5. 与 01 线的接口约定

1. 断言实现沿用 m1_check 的 `GatewayClient/check/PASSED` 风格与退出码口径，命名 `check_<FR域>_<场景>`，先登记（08 §2.1）后入库。
2. 失败贴证：自动化=断言名+stderr 尾部≥40 行+最小复现命令序列；手工=09 号 §3 执行记录表行+截图；贴证落 `design/defects/DEFECT-<T编号>-<日期>.md`。
3. 日志：网关侧沿用现有 stderr 格式并保证崩溃/重启事件含 device_id；Godot 侧 `user://logs/acceptance/` 三行式用例日志。
4. 与 11-B 衔接：网关行为归 m1/m2、内容包映射归 m1b，端口错开（17333/17334），每日回归结论三表合并。

---

## 6. 字数统计（实测，PowerShell `[\u4e00-\u9fff]`）

| 文件 | 汉字数 | 要求 |
|---|---|---|
| 08_测试执行手册.md | 4,536 | ≥4500 ✓ |
| 09_验收对接01线说明.md | 1,548 | ≥1500 ✓ |
| 本报告 | ~900 | — |

---

## 7. 开放问题

1. 新增草案落库位置（建议新建 `scripts/m2_check.py`）[TBD]。
2. m1_check 断言与 T- 用例号的双向注释是否引入脚本 [TBD]。
3. T-070/VR 复核项与 T-066(VR 分支) 的分档边界待实机清单固化。
4. Godot 日志目录打包写权限。
5. `defects/` 目录维护归属（建议 04 线）。