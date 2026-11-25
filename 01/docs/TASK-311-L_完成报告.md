# TASK-311-L 完成报告

> 任务 311-L（01 线）：第二批 SIMH 三槽转 live 预检卡 v1。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\第二批SIMH转live预检卡_v1.md`（新增，2026 字节 ≥1200）：①三槽逐台转 live 核对表（slot_id/当前 run_status/二进制就位待办/转 live 后 R2 口径）；②转 live 判定（二进制就位即 live，仍缺则保持 dry-run）；③用户动作清单（编译/放置二进制，01 线不代做）；④声明「不下载、不代编译二进制」。
- `D:\work\01\repo\01\docs\TASK-311-L_完成报告.md`（本报告）。

## 预检卡自证

- 字节数：2026（>1200 达标）。
- 三槽核对表：simh-hp2100/simh-nova/simh-altair-8800 均 dry-run（MISSING 无二进制），binary_hint 路径成文（third_party/simh/hp2100|nova|altair8800，altair 名标 [需核实]）。
- 转 live 判定成文：run_status_of 口径（module 非空 + binary_path 命中即 live），转 live 不涉及 release_check 改码。
- 用户动作清单三条 + 「不下载不代编译」声明成文。

## 与任务书的漂移

1. altair 二进制名 `altair8800` 保留 201-B 推定口径并标 [需核实]（301-O 清单同口径），不臆造定名。
2. slot_loader --list 复跑三槽均 MISSING(无二进制) 与核对表一致（dry-run 语义 = 后端就绪缺二进制），日志见下。
3. 执行备注：验收命令按仓库实际用 `python`；verify_all 门禁在无他线 python 进程窗口干净复跑。

4. 三槽 binary_hint 已在 manifest 配置（206-A 轮），转 live 仅需二进制物理就位——用户放置后 slot_loader 自动解析，无需改 manifest。5. 转 live 后 release_check R2 输出将由 dry-run 变 live（三槽 PASS 行文案变化），属预期口径变化非 FAIL。

6. 预检卡与 311-O 阻塞处置卡互引：三槽解除条件一致（二进制放置至 binary_hint 路径）。

7. 本卡字节数与字数均达标（2026 字节）。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：67/67 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== slot_loader.py --list（节选：三槽 MISSING 现状）==
simh-altair-8800   MISSING(无二进制)  ...
simh-hp2100        MISSING(无二进制)  ...
simh-nova          MISSING(无二进制)  ...
SLOT_RC=0
```
