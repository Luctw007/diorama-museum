# TASK-46A 完成报告（docs/TASK-46A_完成报告.md）

> 01 线 · 2026-11-04 · 任务：模拟器插槽系统（槽位装载器 v1）。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/slot_loader.py` | 160 | manifest 扫描/解析/映射 → `apply_slots(EMULATORS)`；`slots_available()`/`media_dirs()`；backend_type→module 映射表（mame/simh/stella/mesen/mobile/dedicated/native 预留） |
| `gw/gateway.py`（改） | — | **二进制检查泛化**（`_find_binary`/`_binary_ok` 取代硬编码双分支）；list_emulators 同步泛化；启动时 `apply_slots` 自动注册（含故障降级） |
| `scripts/emulator_doctor.py`（改） | — | 新增槽位扫描区（逐槽位三态 + 介质目录提示） |
| `slots/emulators/fake-slot/manifest.json` | — | 样例槽位（native 后端零二进制） |
| `slots/README.md`、`slots/media/README.md` | — | 目录契约全文 + 使用三步 + 红线 |

## 2. 运行日志（原文关键段）

```text
$ python scripts/slot_loader.py --list
fake-slot   OK(native,无二进制要求)  样例槽位：…  [MIT（本仓库自带）]
介质目录 0 个：（空，红线下仅建目录）

# 槽位真跑证据：start_device{emulator:"fake-slot"} 全流程
FRAME frame_id=1 280x192
ACK_OK device_id=slot-demo sinks=['main']
STOPPED ok=True        → rc=0

$ python scripts/emulator_doctor.py
[OK] slot:fake-slot   native 后端，无二进制要求
[HINT] slot_media_dirs   介质目录 0 个

# 网关泛化后全量回归：m0 ✔ / m1 42 ✔ / m1b 19 ✔ / m2a 10 ✔
```

## 3. 迭代记录（3 轮）

1. 轮 1：native 槽位在 `--list` 被标"MISSING(无二进制)"——语义错误 → 三态标签改为
   OK(native)/OK(就位)/MISSING；
2. 轮 2（真实回归故障）：list_emulators 处理器仍引用已删除的 `_find_simh_binary` → NameError
   导致 m1 超时 → 改 `_binary_ok` 泛化判定，四套验收全绿；
3. 轮 3：删除旧双查找函数后确认无残留引用（grep 清零），网关注册表与槽位同名的沉淀规则
   （内置优先）写入实现并留到 02 线 v0.5 裁决。

## 4. 开放问题

1. `backend_type→module` 映射目前 simh/stella/mesen/mobile/dedicated 为 None（槽位登记但不注册）——真实后端实现后逐一落映射；
2. 多架构二进制（win/linux 双文件名）的 manifest 表达待 02 线 v0.5 定稿；
3. 槽位与内置注册同名时的优先级（当前内置优先）需 v0.5 明确。