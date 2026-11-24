# TASK-272-B 完成报告

> 任务：B-4 co_active_max 实测口径卡（01 线实测前的口径交付）（02 线）。执行账号：02 线（规范/待办）。
> 只改 02 目录，纯文档口径卡，不产包、不改校验器代码、不替 01 线执行实测。

## 一、交付物清单

1. 新增 `docs/B4_co_active_max实测口径卡_v1.md`（4380 字节）：实测目标（场景/步骤/观察项）+ 判据（梯度测试
   + PASS 判据 + 采集数据格式）+ 数据回填口径（device_budget_check.py SKIP 转 PASS 阈值写法 + B-4 销账三条件）+
   风险与边界。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复跑

```
verify_all --daily --cache
  ...
  结果：54/54 通过（rc=0）
```

### 2.2 口径卡自证

```
字节数：4380（>2000 达标）
四节标题命中：一、实测目标 / 二、判据 / 三、数据回填口径 / 四、风险与边界
（另有五、红线自查）
```

### 2.3 改动清单自证（本任务只新增，未改任何脚本/门禁/引擎）

```
新增 docs/B4_co_active_max实测口径卡_v1.md（4380 字节）
新增 docs/TASK-272-B_完成报告.md
改动脚本/门禁/引擎/gd：0（未碰 device_budget_check.py、未碰 verify_all、未碰 exhibit_host.gd）
```

## 三、结论

B-4 实测口径已落卡：明确 01 线实测「同屏激活 N 台」梯度测试（N=1~5）+ PASS 判据（FPS ≥ 目标线、默认 3
是否成立）+ 采集数据格式 + 回填口径（device_budget_check.py 第 34 行 `CO_ACTIVE_MAX_DEFAULT` 改实测值、
B-04 SKIP 转 PASS）+ B-4 销账三条件。实测前不改脚本、不提前销账。

## 四、与任务书的漂移（如实）

1. **co_active_max 未在引擎侧实装（核心漂移）**：任务书前置第 4 条「`exhibit_host.gd` —— co_active_max
   使用处」，实测 `01/repo/01/godot/` 全目录 grep `co_active_max` **无任何命中**——该字段当前仅存在于规范层
   （默认 3）与脚本占位（`device_budget_check.py` 第 34 行），**引擎侧尚未实装**。故口径卡把「引擎实装
   co_active_max 字段」列为实测前置之一，不臆造其已在引擎生效。
2. **co_active_max ≠ max_running 语义区分**：口径卡明确二者区别（同屏激活上限 vs 同厅运行配额 ≤4），
   避免 01 线实测时混淆（exhibit_host.gd 的 `max_running` export_range 1..4 是 B-03 口径，非 B-4）。
3. 其余无实质漂移：默认 3 占位、B-04 SKIP 现状与 `F4设备实例预算表_v1.md` / `device_budget_check.py` 一致。

## 五、红线自查

零联网、零下载（纯文档口径卡）；判据可执行、未实测值标「待实测」；只改 02 目录、未改 01 线脚本/引擎、未产包。
