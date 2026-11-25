# TASK-316-N 完成报告

> 任务 316-N（01 线）：运行锁真跑联调预检卡 v1（gap #4 待 46 线 launch 后验）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\运行锁真跑联调预检卡_v1.md`（新增，1908 字节 ≥1200）：①联调前置清单（46 线 launch 就绪/网关 status 消息可达/ExplodeController 节点在位/EXPLODED 时 running 拒爆、stopped/degraded 复位锁判定逐条勾选位）；②验证步骤（running→EXPLODED 拒绝/stopped→解锁/degraded→复位，各步预期）；③判定口径（拒绝=锁生效 PASS，误拒=缺陷输入 F-6 深化）；④声明「本卡只预检，不实机」。
- `D:\work\01\repo\01\docs\TASK-316-N_完成报告.md`（本报告）。

## 预检卡自证

- 字节数：1908（>1200 达标）。
- 前置清单四条勾选位成文；验证步骤四步成文（running 拒爆/运行中到达退出拆解/stopped 解锁/degraded 复位）。
- 判定口径两条成文：拒绝=锁生效 PASS；误拒=接线缺陷输入 F-6 深化（gap #4 联调缺陷）。
- 「只预检不实机」声明成文；真跑联调待 46 线 launch 后执行。

## 与任务书的漂移

1. 验证步骤增补「已在 EXPLODED 时 state=running 到达 → set_device_running(true) 触发退出拆解 + 拒绝提示」一步（任务书只列 running→EXPLODED 拒绝/stopped/degraded）：311-G 实装的 set_device_running 含此分支，纳入验证面。
2. 判定口径补充「误拒（stopped 后仍拒）」缺陷路径（与误放行对称）。
3. 执行备注：验收命令按仓库实际用 `python`；verify_all 门禁干净复跑 + gd 符号自检佐证，日志见下。

4. 联调预检与 316-M 相机的配合关系：聚焦运镜期间若设备 running，运行锁拒绝 EXPLODED 优先于运镜——两件接线互不冲突（不同路径）。

5. 本卡字节数与字数均达标（1908 字节）。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：73/73 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== gd_symbol_check.py（佐证 set_device_running 符号面）==
汇总：17 文件；符号池 funcs 185 / signals 8；MISS 0；已知缺口 KG 0
SYM_RC=0
```
