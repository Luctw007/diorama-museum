# TASK-168-B 完成报告（annotations 深度补强 · 9 台 flow 补齐）

## 交付物

对 9 台老包各追加 flow 讲解至 ≥10（**只增不改，0 修改 0 删除**）：

| 包 | 增补前 flow | +新增 | 增补后 flow |
|---|---|---|---|
| eniac | 2 | 8 | 10 |
| edsac | 3 | 7 | 10 |
| edvac | 1（任务书标 0，实为 1） | 9 | 10 |
| bbcmicro | 2 | 8 | 10 |
| commodore64 | 2 | 8 | 10 |
| ibm5150 | 2 | 8 | 10 |
| pdp8 | 9 | 1 | 10 |
| amiga500 | 9 | 1 | 10 |
| atari-st | 9 | 1 | 10 |

新增 flow 覆盖定案「为何镇馆」锚点：ENIAC 首台通用机+女性程序员、EDSAC 首台实用+首个游戏、EDVAC 冯·诺依曼报告、PDP-8 首台商用小型机、BBC Micro ARM 摇篮、C64 史上最畅销+SID、IBM 5150 开放架构、Amiga 500 欧洲游戏、Atari ST 音乐人工具。

## 验收日志

1. **逐包门禁（9 台全 0 FAIL）**：eniac 92 / edsac 132 / edvac 126 / bbcmicro 78 / commodore64 78 / ibm5150 84 / pdp8 72 / amiga500 78 / atari-st 78（全 PASS、FAIL 0）。
2. **只增不改**：新增 id 全局唯一，既有条目 id 与 text 一字未动；target 复用 `whole` 或已证实存在的 role 节点。
3. **目录版本唯一性复查**：本任务不碰目录 jsonl；`catalog_check`「跨文件重复」0 条，活跃版本「计算机 v2 + 通讯 v3」唯一。

> 注：edvac 任务书标现状 flow=0，实际为 1（此前 134 轮已加过 1 条），故增补 +9 至 10，已在表注明。
