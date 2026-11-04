# 缺陷跟踪索引（defects/INDEX.md）

> 维护：04 线。追更：01/05 线修复完成后回填状态并附修复说明。

| 编号 | 用例/断言 | 摘要 | 状态 | 归口线 | 贴证路径 |
|---|---|---|---|---|---|
| DEFECT-M1-ROLLBACK-01 | T-061 / m1_check 第 8 项 | fake 后端 load_state 与产帧线程无锁竞态：回滚后第一帧 frame_id==保存点（期望 ≥保存点+1），确定性复现 2/2 | **closed**（round_2 : m0 23/23 + m1 42/42 连续 2 轮，回滚首帧 == 保存点+1 精确命中；01 线 _frame_lock 修复） | 01 | defects/DEFECT-M1-ROLLBACK-01.md |
| DEFECT-M1B-KEYMAP-01 | T-025/026 前置 / m1b_check | apple-ii input_map 已升对象格式 {"map","key"}，run_profile 仍按字符串校验 → 57 键全判未知（契约漂移） | **closed**（round_2 : m1b 19/19；apple-ii 57 键 unknown=0、首键 {keyboard: KEY_A}；五包 --json 双形态无漂移；run_profile 已支持对象形态） | 05+01 | defects/DEFECT-M1B-KEYMAP-01.md |