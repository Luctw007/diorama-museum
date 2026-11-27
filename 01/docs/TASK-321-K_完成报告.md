# TASK-321-K 完成报告

> 任务 321-K（01 线）：引擎续 · 相机插值观感静态自检卡 v1（gap #3）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\相机插值观感静态自检卡_v1.md`（新增，1426 字节 ≥1200）：①接线自检表（连接行存在/funcs 计数/tween 时长取 signal + clampf 0.2~3.0 防御/命名纪律，各列：检查项/现状/结论）；②观感待实机结论（不臆造 PASS）；③与 316-M 漂移核对（无漂移）。
- `D:\work\01\repo\01\docs\TASK-321-K_完成报告.md`（本报告）。

## 自检卡自证

- 字节数：1426（>1200 达标）。
- 接线自检四行全 ✓：连接行三件套（判空+has_signal+点号 connect）在、player.gd funcs=5、tween 时长防御在、命名 FAIL 0。
- 观感待实机结论成文；与 316-M 漂移核对：无漂移（本轮自检只读未改）。
- 信号源契约一致（explode_controller focus_requested 306-H 未动）。

## 与任务书的漂移

1. 自检引用修复后全池数字（funcs 185 / signals 8，与 316-M 一致）——本轮无 gd 代码改动，数字不变。
2. gd 自检复跑 player.gd funcs=5 signals=0 + MISS 0 / FAIL 0 佐证，日志见下。
3. 执行备注：验收命令按仓库实际用 `python`；verify_all 门禁在无他线 python 进程窗口干净复跑。

4. 自检结论「无漂移」的判定面：连接行/函数/防御/命名四层全过才判无漂移，观感面单独标待实机——静态面与实机面分离登记。5. 本卡字节数与字数均达标（1426 字节）。

6. 观感待实机的验证锚点：待实机 v6「随时」批已注「316-M 相机插值观感、316-N 真跑锁联调」——自检卡与汇总卡同源，实机轮按批次勾选。

7. 本卡字节数与字数均达标（1426 字节）。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：77/77 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== gd_symbol_check.py（player.gd 行 + 汇总）==
== player.gd              [player] funcs=5 signals=0
汇总：17 文件；符号池 funcs 185 / signals 8；MISS 0；已知缺口 KG 0
SYM_RC=0

== gd_naming_check.py ==
扫描 17 个 gd；class_name 7 个；FAIL 0
NAM_RC=0
```
