# TASK-227-A 完成报告

> 任务：layout schema 扩展规格（portals / hall_group / lod_scale 落规范）。执行账号：02 线。只改 02 目录，纯规范文档。

## 一、交付物清单

1. 新增 `docs/layout扩展规格_v1.md`（5136 字节），含三字段定义（portals/hall_group/lod_scale）、兼容迁移
   口径、01 线 F-1~F-3 实装引用与验收口径（L-11~L-13）。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复测

```
verify_all --daily --cache
  catalog_ref          FAIL  FAIL 1
结果：40/41 通过（rc=1）
```

> 40/41 唯一 FAIL = catalog_ref「完工包 hp-2100 无目录反链」（镜像 hp-2100 反链 stale），与本任务纯规范
> 文档改动无关（详见 `镜像收口口径_v2.md` §二.2）。

### 2.2 规格自检

```
字节：5136（>1200 达标）
三字段定义表：portals（数组，元素 target/position/rotation）、hall_group（string，hub/dawn/mainframe/personal/console）、lod_scale（数值，缺省 1.0）
JSON 示例：portals 传送点示例
兼容口径：存量 layout 不受影响（三字段均可选，L-01~L-04 不变）
L-11/L-12/L-13 验收判据：portal 解析 / hall_group 归属 / lod_scale 生效
```

## 三、三字段定义摘要

| 字段 | 类型 | 必填 | 语义 |
|---|---|---|---|
| portals | 数组 | 可选 | 大厅↔子厅传送点（target/position/rotation，沿用 L-03 + 朝向角转换） |
| hall_group | string | 可选 | hub / dawn / mainframe / personal / console 分组 |
| lod_scale | 数值 | 可选 | 厅级 LOD 距离缩放系数（缺省 1.0） |

## 四、与任务书的漂移

1. **226-A 提案未产出**：`layout传送点提案_v1.md` 执行时不存在（01 线 226-A 未交付），本规格以 221-A §②
   口径为准，未对 226-A 的 JSON 提案格式逐字段对齐（留待 226-A 交付后回填）。
2. **hall_group 枚举取值**：221-A 未给枚举值，本规格按 02 线目录「厅归属」口径补五项（hub/dawn/mainframe/
   personal/console），并注明以 04 线定案为准。

## 五、红线自查

零联网、零下载（纯规范）；字段以 221-A 提案 + 01 线既有 layout 实际为准，未臆造；只改 02 目录、未改
01 线 layout 文件、未改校验器代码。
