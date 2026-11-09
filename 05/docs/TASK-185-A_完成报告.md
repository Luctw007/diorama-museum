# TASK-185-A 完成报告（Apple II 正式低模样板）

> 任务 185-A（05 线）· 完成日期：2026-11-10。

## 一、交付物

重制 `content/apple-ii/meshes/` 下 4 个 glTF（占位白模 → 低模多材质），文件名/路径/mesh_ref 不变，meta.json/annotations 未动：

| 文件 | 顶点数 | 三角面数 | 材质 | 内容 |
|---|---|---|---|---|
| case.gltf | 104 | 156 | 3 | 米色机箱+斜切顶盖+散热槽×6+格栅×4+红灯 |
| keyboard.gltf | 296 | 444 | 2 | 深棕底座+3排×12键帽 |
| disk_ii.gltf | 120 | 180 | 4 | 米色主体+槽口/把手/散热槽+红灯+灰脚垫 |
| mainboard.gltf | 144 | 216 | 4 | 绿基板+芯片×12+灰插槽条×3+红电容×2 |

材质全部用 `baseColorFactor` 数值（米色 0.86/0.82/0.70、深棕 0.25/0.22/0.20、主板绿 0.10/0.30/0.12、芯片黑、金属灰 0.5/0.5/0.52 等），无贴图、无外部文件。

## 二、验收日志

**① `verify_all.py --only pkg:apple-ii`**（全 PASS）：
```
总计 272 条：PASS 272，FAIL 0
===== 验收汇总（1 项） =====
  pkg:apple-ii         PASS  FAIL 0
结果：1/1 通过
```

**② `verify_all.py --only catalog_ref`**（无新增 FAIL）：
```
REF-01 悬空包引用：0 条
REF-02 反链缺失：0 个
REF-04 关联包形态非法：0 条
FAIL 0
结果：1/1 通过
```

**③ 顶点数自检**（POSITION accessor count）：case 104、keyboard 296、disk_ii 120、mainboard 144——均 **>100 且 <4000**，低模口径达标。

## 三、规范遵守

- glTF 节点名 = node_id（R-090 契约），mesh_ref 引用不变，装配体树未改。
- 坐标 Y 向上、面朝 -Z，模型原点在装配体原点。
- 未下载任何 ROM/二进制/贴图；尺寸比例沿用公开资料近似值，无来源标「需核实」。
