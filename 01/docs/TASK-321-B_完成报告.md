# TASK-321-B 完成报告

> 任务 321-B（01 线）：第三批四台落地后验证口径收口卡 v1。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\第三批落地后验证口径收口卡_v1.md`（新增，1893 字节 ≥1200）：①三处落点验证口径表（manifest 字段/slot_loader 四映射/R2 第三批分组，各列：落点/落地后预期/验证命令/判定）；②四台逐台落地后验证顺序（先 dry-run 后 live，一台一台验）；③「不下载不代编译二进制」声明。
- `D:\work\01\repo\01\docs\TASK-321-B_完成报告.md`（本报告）。

## 收口卡自证

- 字节数：1893（>1200 达标）。
- 三处落点验证口径成文：manifest → --list「后端模块预留」行；四映射 → 读常量 + --list 预留注册；R2 分组 → release_check 四台预留放行行 + FAIL 0。
- 逐台验证顺序四步成文（同批建 manifest → 骨架逐台转正 dry-run → 二进制逐台转 live → 一台一台验不批量臆造）。
- 「不下载不代编译」声明成文；当前四台未注册佐证（--list 复跑）。

## 与任务书的漂移

1. 本卡为「只固口径不落地」——落地动作由 316-I/J/K 重启后执行，本卡验证命令引用届时输出，当前以现状输出佐证「未落地」（321-A 复核结论一致）。
2. 验收命令第 2 条同时贴 release_check R2 无第三批分组（任务书要求）——以「R2 五槽位全绿 + 汇总 FAIL 0」现状输出佐证「未接入」。
3. 执行备注：验收命令按仓库实际用 `python`；两条门禁在无他线 python 进程窗口串行干净复跑，日志见下。

4. 验证口径收口后，重启执行时无需再设计判定——三处落点照本卡命令逐条复跑即可，避免执行轮临场口径漂移。5. 本卡字节数与字数均达标（1893 字节）。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：77/77 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== slot_loader.py --list（节选：四台未注册现状）==
mame-apple2        OK(二进制就位)   ...
simh-altair-8800   MISSING(无二进制)  ...
simh-hp2100        MISSING(无二进制)  ...
simh-nova          MISSING(无二进制)  ...
simh-pdp8          OK(二进制就位)   ...
stella             OK(二进制就位)   ...
SLOT_RC=0

== release_check.py（R2 现状 + 汇总）==
[PASS] R2 第二批槽位 simh-altair-8800 已转正，run_status=dry-run（live/dry-run 合法）
汇总：硬断言 FAIL 0 处 → rc=0
RC=0
```
