# TASK-221-B 完成报告（真跑矩阵 dry-run 终检 + need_verify 分布终版）

## 交付物清单
1. dry-run 终检：三台真跑 + 第二批 SIMH 三台逐台 `launch_device --dry-run` 全链复测（七台口径：apple-ii / pdp8 / atari-2600 / hp-2100 / data-general-nova / altair-8800，pdp8 兼属两组），逐台贴输出与 rc——全部 rc=0、无异常分支。
2. `docs/realrun_launch_param_check.md` §五更新为「TASK-221-B 终版」：need_verify 分布定稿（核销 5 / 续挂 6）+ 第二批 SIMH 待核项合并口径（3×3 并入 SIMH 组不重复计数）+ **用户侧待办清单三件**（放介质真跑 / 补 Stella DLL / 编译第二批 SIMH 二进制）+ 七台终检结论 + R2 口径。
3. `docs/TASK-221-B_完成报告.md`。

## 验收日志（原样）
1. hard 门禁：首跑 46/48（他线并发写瞬时 2 FAIL）→ 干净重跑 **48/48 通过** rc=0（41 完工包+7 步）
2. dry-run 七台自证（均 rc=0）：
```text
apple-ii   决策: 槽位 mame-apple2 二进制就位（…third_party\mame\mame.exe）→ 真实后端
pdp8       决策: 槽位 simh-pdp8 二进制就位（…third_party\simh\pdp8.exe）→ 真实后端
atari-2600 决策: 槽位 stella 二进制就位（…third_party\stella\stella.exe）→ 真实后端
hp-2100    决策: 二进制未就位 → EMULATOR_BINARY_MISSING + …third_party/simh/hp2100 或 SIMH_HP2100_BIN
data-general-nova 决策: 二进制未就位 → …third_party/simh/nova 或 SIMH_NOVA_BIN
altair-8800 决策: 二进制未就位 → …third_party/simh/altair8800 或 SIMH_ALTAIR_BIN
```
3. `release_check.py` → `汇总：硬断言 FAIL 0 处 → rc=0`

## 与任务书的漂移（如实）
1. 任务书列「七台 = 三台真跑 + 四台 SIMH（含 pdp8 重复）」：pdp8 同一设备兼属两组，实测以 6 个唯一设备 id 覆盖 7 口径（报告中已注明）；atari-2600 决策链显示「二进制就位」为决策层判定（stella.exe 存在），**其 0xC0000135 缺 DLL 问题为运行层环境缺陷**（presmoke 已记录），终检不覆盖运行层——如实标注、未臆造「真跑就绪」；
2. need_verify 终版分布与任务书一致（核销 5 / 续挂 6，无新增）；
3. 门禁一次瞬时 46/48（他线并发写）→ 干净重跑 48/48 收敛；未下载/未编译/未启动真实模拟器、未改 02/03/05 线、未做 git（统筹收口）。