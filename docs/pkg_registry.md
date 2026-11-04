# 内容包注册表与门禁数据驱动化（docs/pkg_registry.md）

> TASK-41A 交付。从此包清单不再由人工在每个门禁脚本里维护——“新包入库 = 产生 meta.json，
> 门禁自动跟上”。

## 1. 语义

| 项 | 规则 |
|---|---|
| 扫描根 | `D:\work\03\repo\content`、`D:\work\05\repo\content`（内容线两仓） |
| 判定 | 子目录内含 `meta.json` 即视为规范包 |
| 排除 | `EXCLUDES = {test-device, manchester-baby-scaffold}`（fixture/示例） |
| **WIP 判据** | 缺 `THIRD_PARTY.md` / `annotations/annotations.json` / 两网格目录（`meshes/` 旧、`assemblies/` v0.4 新）合计 0 gltf；**或包内存在 `.wip` 标记文件**（内容线生产中的显式声明，交付时删除——写入 02 线协作契约） |
| NOTE | 缺 `encyclopedia.md` 不算 WIP（内容缺口，转到内容线下轮补齐） |
| 排序 | 按 device_id 字典序（门禁输出稳定） |
| 扩展 | 未来新线（如 06 手机线）只需在 `SCAN_ROOTS` 加一行 |

## 2. 消费方

- `scripts/verify_all.py`：`READY, WIP = pkg_registry.discover_packages_full()`；WIP 只提示不判定；
  `--only wip` 可单独检查生产中包；`--only pkg:<id>` 单包过滤；
- `scripts/sync_content.py`：`SOURCES` 同源；五包、十三包、十五包零手改。

## 3. 验证记录（2026-11-04）

- registry `--list`：15 包（ready 15 / wip 0），2 条百科缺口 NOTE；
- `verify_all --daily`：**17/17**（含执行窗口内 03 线新交的 bbcmicro 与 05 线 sega-md 自动入闸）；
- `--only pkg:apple-ii`：1/1；sync：15 包 0 失败。
- 实战演练：执行期间 03 线正生产 bbcmicro（结构不全→轮 3 判据过严误伤 12 包→轮 4 修正为
  "结构件+双网格目录+.wip 约定"）——数据驱动门禁在跨线并行下自动吸纳新完工包。

## 4. 边界

- 跨机部署（仓库移盘符）时 SCAN_ROOTS 需同步改（当前以 `__file__` 推导 D:\work，单机假设成立）；
- EXCLUDES 是唯一允许的手工排除点——若要临时屏蔽某包，改这里而不是删包。