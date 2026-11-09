# TASK-177-B 完成报告：第二批设备包 31-60 分档验收口径

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。

## 一、交付物清单

| # | 路径 | 状态 | 说明 |
|---|---|---|---|
| 1 | `docs/第二批分档验收口径_v1.md` | 新建 | 六区块 + FAQ + 边界，2109 汉字 |

## 二、三档口径与 WIP 升档结论

- **S 档（8 台）**：全规格件清单（meta/runtime + assemblies 全 + annotations 含 flow + encyclopedia +
  THIRD_PARTY），`pkg:*` 进 ready 全绿 + 反链 done；模拟器 bone 可接则登记槽位，否则静态+动画。
- **A 档（12 台）**：近似 S，允许更多「需核实」、annotations 以 role 为主 flow 可减、百科字数下限
  略低；validate 0 FAIL 硬底线不变。
- **B 档（10 台）**：最小可展示（meta/runtime + ≥1 gltf + THIRD_PARTY + emulator="none" 静态+动画），
  encyclopedia 可存缺口（NOTE 转补），目录走 planned→researching→package→done。
- **WIP 升档**：`.wip` 标记 / 缺 THIRD_PARTY 或 annotations / 0 gltf 三选一判 WIP；`.wip → 补件 →
  ready → done` 逐态迁移路径 + 样板走查（nokia-3310 五步过闸）。

## 三、分档与 173-A 名单对齐

口径明确写"三档档位与 173-A 名单一致：S 档 8 / A 档 12 / B 档 10，共 30 台（31-60）"，并以
nokia-3310 为已产样板举例说明过闸路径；未篡改名单档位、未把名单外设备写进口径。

## 四、验收贴日志

### 4.1 Select-String 抽查（10 关键字）

```
S 档 8 · A 档 5 · B 档 7 · WIP 6 · 升档 4 · validate 8 · REF-02 6 · THIRD_PARTY 8 · 反链 11 · 门禁 10
```

### 4.2 字数

```
汉字(CJK)字数：2109（≥2000 达标）
```

### 4.3 分档对齐

```
S 档 8 ×1 · A 档 12 ×1 · B 档 10 ×1 · 31-60 ×3 · nokia-3310 ×5
```

### 4.4 门禁机制佐证（registry + 样板）

```
python pkg_registry.py --list
  共 31 包（ready 31 / wip 0 / EXCLUDES=['manchester-baby-scaffold','test-device']）
  （nokia-3310 已在 ready，无 NOTE）

python validate.py D:\work\03\repo\content\nokia-3310
  总计 84 条：PASS 84，FAIL 0
```

### 4.5 门禁只读复测

```
结果：37/38 通过
```

**留底说明（偏差）**：任务写"基线 38/38"，实测 **37/38**——唯一失败步骤 `catalog`（rc=1、306 重复
id），根因 monorepo 镜像 v2/v3 并存（robocopy `/E` 只增不删）。此失败与本任务无关（本任务仅新增
1 份 02 线文档），执行前后均 37/38，零回归。

## 五、红线自查结论

1. 不下载 ROM/二进制/版权文件 ✓；2. 不编造史实 ✓（仅门禁/件清单/升档机制，无新年代/参数/许可断言）；
3. 只改 02 线目录 ✓（仅新增 1 文件，未分配/登记 id、未改 03 目录 jsonl、未碰 01 脚本）；
4. 口径不定案、不否决存量 ✓；5. 禁止低质产出 ✓（2109 汉字、六区块齐全、三档各有实质口径表）。

## 六、开放问题

- 真跑矩阵阈值（≥5 台）与 `run_status` 落点转 v0.7 章 D + 01 线 release_check 后续任务；
- 家电影音类第二批（05 线）不在本口径覆盖内。
