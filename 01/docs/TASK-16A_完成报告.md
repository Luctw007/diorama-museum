# TASK-16A 完成报告（docs/TASK-16A_完成报告.md）

> 01 线 · 日期：2026-11-02 · 任务：一键全量验收 + mame_apple2 后端骨架（见 任务16-A 文档）。

## 1. 交付物与规模

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/verify_all.py` | 121 | 一键全量验收门禁（m0/m1/m1b + 02 线校验器对 5 内容包），`--only/--daily` 模式，汇总表 + 退出码 |
| `gw/emulators/mame_apple2.py` | 300 | MAME apple2 后端骨架（BackendBase 子类：M2.1/2.2/2.3 三层、boot.lua 模板生成、命令文件下发通道、二进制缺失优雅降级） |
| `gw/gateway.py`（改） | +40 | 注册表新增 `mame-apple2` 条目 + `_find_mame_binary()` + spawn/start 两处二进制预检 |
| `licenses/MAME.md`、`third_party/mame/README.md` | — | 许可核实标记与放置约定（红线：不随附二进制与 ROM） |
| `docs/m2_assert_draft.md` | ≥1200 字 | 三里程碑断言清单（fake 先行 / 真实 MAME 替换双轨） |

## 2. 运行日志（原文关键段）

```text
$ python -m gw.emulators.mame_apple2 --check-binary
MAME 二进制缺失（third_party/mame/ 或环境变量 MAME_BIN）      # rc=2 ✔（任务验收要求）

$ python scripts/verify_all.py          # 初次全量（时间为迁移前）
  m0                   PASS  M0 验收全部通过 ✔
  m1                   PASS  M1 验收全部通过 ✔（断言 42 条）
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  pkg:manchester-baby  FAIL  rc=1；总计 137 条：PASS 125，FAIL 12   # 03 线当时未迁移
  pkg:eniac            FAIL  rc=1；总计 101 条：PASS 89，FAIL 12
  pkg:edsac            FAIL  rc=1；总计 141 条：PASS 126，FAIL 15
  pkg:edvac            FAIL  rc=1；总计 135 条：PASS 123，FAIL 12
  pkg:apple-ii         PASS  总计 272 条：PASS 272，FAIL 0
结果：4/8 通过（退出码 1 ✔ 门禁正确拦截）

$ python scripts/verify_all.py --only pkg   # 03 线完成 v0.2 迁移后复跑
  pkg:manchester-baby  PASS  FAIL 0（128 条）
  pkg:eniac            PASS  FAIL 0（92 条）
  pkg:edsac            PASS  FAIL 0（132 条）
  pkg:edvac            PASS  FAIL 0（126 条）
  pkg:apple-ii         PASS  FAIL 0（272 条）
结果：5/5 通过（退出码 0）

$ python scripts/verify_all.py --daily      # 最小回归集
  m0 PASS / m1b PASS / pkg 5/5 PASS
结果：7/7 通过（退出码 0）
```

## 3. 迭代记录（≥2 轮）

- **轮 1**：verify_all 首跑 —— 发现 `pkg:` 前缀步骤走了非解析分支（name=="pkg" 判断错误 → 备注显示 rc 而非 FAIL 计数）→ 改 `name.startswith("pkg")`；
- **轮 2**：复跑期间 03 线并行完成四包 v0.2 迁移（manchester-baby/eniac/edsac/edvac 由 FAIL 12/12/15/12 → 全 0），门禁先红后绿，行为符合预期（作为"迁移前拦截"证据保留于报告）；
- 网关回归：注册表改动后 m0/m1/m1b 仍全绿（fake 路径不受影响）。

## 4. 骨架设计决策（对照 05 线 14-A 映射表）

1. **下发通道**采用 14-A §八候选 1 的"命令文件轮询"（跨平台最简），`_write_cmd` 是唯一落点——将来换命名管道只需改这一处；
2. **输入回显本地化**：`on_input` 立即回 input_ack（同 fake 行为），不等待 MAME——保证客户端交互时延为 0（14-A §3.2 同款结论）；
3. **帧号竞争**复用 04 线 DEFECT-M1-ROLLBACK-01 修复结论：`_frame_id` 加锁递增；
4. **M2.1 判定**：`state:running` 以首个 `frame_done` 事件为准（14-A §3.2 推荐），非进程存活；
5. **帧编码**复用 `gw/emulators/rle.py`；Apple II 帧较大，config `frame_codec` 默认 rle。
6. 红线执行：媒体只在 config.media 透传用户路径，后端无任何下载行为。

## 5. 待验证清单（真实 MAME 到位前不可验证）

1. boot.lua 全模板（位图直读 API、JSON 库名、register_periodic 文件位偏移）—— 见 14-A §十二 [需核实]；
2. 启动参数完整表（14-A §九）中的 `-snapsize` 等逐项核对；
3. 扬声器采样流通道存在性（决定 m2 断言 d）。

## 6. 开放问题

1. `save/load` 超时兜底 watchdog 未启用（骨架期 ack 依赖 MAME 事件，若 MAME 卡死客户端需网关侧超时——记入 PROTOCOL 迭代候选）；
2. `mame-apple2` 崩溃自动重启与快照恢复（FR-E8）语义未针对其定制（MAME 存档在状态集而非 persist 文件，需在真实接线段复核）。