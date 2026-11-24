# release_check 现状盘点 v1（docs/release_check现状盘点_v1.md · TASK-301-C）

> TASK-301-C 交付。F-16 封版预检第①步：逐条盘点 release_check.py R1~R4 + --smoke/--snapshot 现状，
> 为 301-D 扩展口径设计打底。只改 01 目录，纯文档盘点，**不改 release_check.py**。

## ① 逐条盘点表（现状 + 结论）

| 断言 | 内容 | 现状（源码 + 最新日志 296-A 轮） | 结论 |
|---|---|---|---|
| R1（硬） | docs/verify_last.json 存在且 passed == total（先跑 verify_all --daily --cache） | 2026-11-25 日志：R1 验收基线 59/59 通过 | 全绿 |
| R2（硬） | 三台真跑槽位 mame-apple2/simh-pdp8/stella 均存在且 module 非空（非「预留」）、desc 不含「预留」、run_status ∈ {live, dry-run}；licenses/MAME.md、SIMH.md、Stella.md 三份许可记录存在 | 三台 run_status=live；第二批 simh-hp2100/nova/altair-8800 已转正 dry-run（预留态 missing 合法不 FAIL）；三份许可存在 | 全绿 |
| R3（硬） | 完工内容包 ≥ 30（pkg_registry.discover_packages_full；wip 只打印） | 完工包 51 ≥ 30 | 全绿 |
| R4（信息） | 源码残留扫描（TODO/FIXME/XXX/预留/占位）——只暴露不计 rc | 命中 1 处（gw\emulators\mame_apple2.py「占位」×1） | 信息项，无碍 |
| --smoke（可选） | demo_frames.py --frames 5 --html（失败计入 rc） | 本轮未启用（任务书不要求） | 可选开关 |
| --snapshot（可选） | verify_last.json → verify_baseline_v0.1.json 冻结基线 | 本轮未启用 | 可选开关 |

## ② 硬断言计数现状

- **硬断言 FAIL 0 处 → rc=0**（R1/R2/R3 全硬断言全绿；R4 信息项 1 处命中不计 rc）。
- 备注：third_party/（第三方软件）使 R4 遍历变慢（约数分钟），属正常现象不计 FAIL（用户 2026-11-24 确认）。

## ③ 扩展前需先定口径的缺口识别

1. **F-1~F-15 销账/实装状态校验缺断言**：release_check 现只守工程底线（基线/槽位/包数），无 F 系列销账行与待实机条数的一致性校验——候选 R5（301-D 设计）。
2. **待实机清单条数一致性无断言**：F系列待实机清单汇总（68 项/格）与各母本条数无机器核对——候选 R5。
3. **封版文档齐备性无断言**：README/RELEASE/台账/验收单等必查文件无存在性校验——候选 R5。
4. 现状结论：**扩展前必须先定口径**（哪些转硬、哪些保持信息），由 301-D 出设计、301-H 汇总后由后续任务实装。
