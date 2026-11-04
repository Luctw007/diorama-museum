# TASK-41A 完成报告（docs/TASK-41A_完成报告.md）

> 01 线 · 2026-11-04 · 任务：门禁数据驱动化（见 任务41-A）。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/pkg_registry.py` | 78 | discover_packages()：双仓扫描 + EXCLUDES；`--list/--json` |
| `scripts/verify_all.py`（改） | — | PKGS 动态化；新增 `--only pkg:<id>` 过滤（未知 id → rc=2 + 提示） |
| `scripts/sync_content.py`（改） | — | SOURCES 动态化 |
| `docs/pkg_registry.md` | ≥800 字 | 语义/消费方/验证记录/边界 |

## 2. 运行日志（等价性证明原文）

```text
$ python scripts/pkg_registry.py --list
  共 13 包（扫描根 2 个，EXCLUDES=['manchester-baby-scaffold', 'test-device']）

$ python scripts/verify_all.py --daily
  m0 PASS / m1b PASS / 13×pkg 全部 FAIL 0
结果：15/15 通过                       ← 与手改清单时代逐项相同

$ python scripts/verify_all.py --only pkg:apple-ii
结果：1/1 通过
$ python scripts/sync_content.py → 13 包，失败 0
```

## 3. 迭代记录（4 轮，含跨线并行实战）

1. 轮 1：verify_all 的 `--only` 曾用 argparse choices 限制 → 改为自由串 + 手动校验（pkg:<id> 与非法值两分支各自返回明确提示与 rc=2）；
2. 轮 2：sync_content 导入 pkg_registry 时依赖脚本目录在 sys.path——不改脚本既有运行方式（`python scripts\...` 直跑），保留显式注释说明依赖关系；
3. 轮 3（实战暴露）：执行窗口内 03 线正生产 bbcmicro → 门禁红；初版 WIP 判据（五件套全齐）过严，把 12 个合法包误判 WIP（v0.4 网格目录改名 `assemblies/` 与老包 `meshes/` 并存所致）；
4. 轮 4（修正定稿）：WIP 判据收敛为"结构件（THIRD_PARTY/annotations）+ 双网格目录任一 ≥1 gltf + `.wip` 显式标记"；encyclopedia 缺失降级为 NOTE（baby/apple-ii 两条，转内容线补齐）。修正后 15 包 ready、17/17 全绿——且 bbcmicro/sega-md 这两个跨线并行产出被门禁**自动吸纳**，正是数据驱动化的目标形态。

## 4. 等价性证明（前后对比）

| 时点 | 清单来源 | daily 结果 |
|---|---|---|
| 改造前（13 包时代手改） | PKGS 硬编码 | 15/15 |
| 改造后（自动发现） | pkg_registry | 15/15（同 13 包时点）→ 新包入库后 17/17（零手改自动扩展） |

## 5. 开放问题

- discover 以 `__file__` 推导 D:\work，多盘符/异地部署需改 SCAN_ROOTS（docs 已注明）；
- `--only pkg:<id>` 的未知 id 返回 rc=2（区别于"跑过但有失败"的 rc=1），供 CI 区分参数错误与实际失败；
- `.wip` 标记约定需 02 线协作契约正式吸收（已写入 docs/pkg_registry.md，待 02 线 37-B 工单采纳）。