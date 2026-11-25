# TASK-311-K 完成报告

> 任务 311-K（01 线）：第三批四台槽位落地预案卡 v1（只设计）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\第三批槽位落地预案卡_v1.md`（新增，2282 字节 ≥1200）：①落地步骤预案（manifest 字段定稿 → slot_loader 注册 → release_check R2 第三批判定接入 → 转正 → 转 live，各步落点+触发条件）；②四台逐台落地顺序（先 dry-run 后 live）；③阈值上调留白说明；④声明「用户点头前不落地，不建 manifest」。
- `D:\work\01\repo\01\docs\TASK-311-K_完成报告.md`（本报告）。

## 预案卡自证

- 字节数：2282（>1200 达标）。
- 落地步骤五步成文（manifest 定稿/注册/判定接入/转正/转 live），触发条件逐条引用 306-P 两项（用户点头产包 + 二进制来源核实关闭 301-O 需核实项）。
- 四台落地顺序：同批建 manifest（module=null 预留）→ 后端骨架逐台（复用 simh 母本复制法，201-A 经验）→ 二进制逐台就位，一台一台验不批量臆造。
- 阈值上调留白（66 号 ≥5 由当时任务更新判定集合）+ 「不落地」声明成文。

## 与任务书的漂移

1. 落地步骤比任务书三段（manifest 定稿/注册/判定接入）扩展为五步（增「转正」「转 live」两步）：三段为登记态，转正/转 live 是 306-O §③ dry-run→live 判定的落地后半程，补齐闭环。
2. slot_loader --list 复跑确认四台仍未注册（八槽位无第三批四台）——「未落地」佐证，日志见下。
3. 执行备注：不建 manifest、不改 slot_loader/release_check（边界遵守）；验收命令按仓库实际用 `python`。

4. 五步预案与 306-O/P 三卡构成完整闭环（方案→预登记→落地预案），执行轮次条件成文，避免用户点头后临时设计。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：67/67 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== slot_loader.py --list（节选：四台仍未注册）==
mame-apple2        OK(二进制就位)   ...
simh-altair-8800   MISSING(无二进制)  ...
simh-hp2100        MISSING(无二进制)  ...
simh-nova          MISSING(无二进制)  ...
simh-pdp8          OK(二进制就位)   ...
stella             OK(二进制就位)   ...
介质目录 0 个：（空，红线下仅建目录）
SLOT_RC=0
```
