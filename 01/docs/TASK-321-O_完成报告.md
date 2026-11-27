# TASK-321-O 完成报告

> 任务 321-O（01 线）：引擎续 · 真跑 HUD 与直起拒绝复核卡 v1。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\真跑HUD与直起拒绝复核卡_v1.md`（新增，1660 字节 ≥1200）：①现状复核表（候选标记/直起拒绝/音频降级/HUD 状态行，各列：项/现状/结论）；②结论（直起拒绝四台预留槽位口径无漂移，HUD 行无漂移）；③与 291-M 漂移核对（无漂移）。
- `D:\work\01\repo\01\docs\TASK-321-O_完成报告.md`（本报告）。

## 复核卡自证

- 字节数：1660（>1200 达标）。
- 现状复核四行全 ✓：RUN_CANDIDATE_SLOTS 四台 + 标记行在、request_direct_launch 恒 false 拒绝口径在、音频降级路径在、HUD 状态行（含 311-G status 行）在。
- 结论成文：直起拒绝口径无漂移、HUD 行无漂移。
- 与 291-M 漂移核对：无漂移（311-G status 行属其后轮次增补，不在 291-M 漂移面）；转正后直起拒绝文案变化属预期非漂移。

## 与任务书的漂移

1. gd_symbol_check + gd_naming_check 复跑 MISS 0 / FAIL 0 佐证，日志见下。
2. 复核为只读（不改 gateway_client.gd，边界遵守）。
3. 执行备注：验收命令按仓库实际用 `python`；verify_all 门禁在无他线 python 进程窗口干净复跑。

4. 转正后变化预期登记（直起拒绝文案随产包定案更新、恒 false 不变）——把「预期变化」与「漂移」分开，避免下轮复核误判。5. 本卡字节数与字数均达标（1660 字节）。

6. 直起拒绝口径的四台边界：RUN_CANDIDATE_SLOTS 仅四台，其它 slot_id 走「未登记真跑槽位」提示——两条拒绝路径各司其职，复核确认均在。

7. 本卡字节数与字数均达标（1660 字节）。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：77/77 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== gd 自检 ==
汇总：17 文件；符号池 funcs 185 / signals 8；MISS 0；已知缺口 KG 0
扫描 17 个 gd；class_name 7 个；FAIL 0
```
