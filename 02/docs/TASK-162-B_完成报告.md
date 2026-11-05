# TASK-162-B 完成报告（02 线）

## 一、交付物

1. `tools/validate/catalog_check.py` 新增 CC-10（软落地：默认 WARN，`--require-media-class` 严格 FAIL），
   per_rule / render_report / render_json 补齐 CC-10 维度；
2. `CC-10规则草案_media_class覆盖率.md` 状态「草案」→「已实现」+ 严格模式启用交接条件。

## 二、验收日志（贴证）

```
默认模式：条目 1582，唯一 id 1582，FAIL 0，WARN 1582
  CC-01 FAIL 0 / PASS 1582　CC-02 FAIL 0 / PASS 1582　CC-10 FAIL 0 / PASS 0 / WARN 1582
严格模式 --require-media-class：条目 1582，FAIL 1582（media_class 缺失 1582 条）
```

## 三、关键说明

- **回归不新增**：CC-01~08 默认模式 FAIL 0（与落地前一致）；CC-02 台账冲突经修 `load_registry_ids`
  （只取 source_file=None 的 allocate 行）后归 0，避免 rebuild 回填目录镜像 id 被误判冲突。
- **严格模式启用交接条件**：回填完成且默认 CC-10 缺失归 0 后，方可在 verify_all 侧打开严格开关。

## 四、红线

默认模式存量不破门禁（FAIL 0）；只改 02 线文件，03/05 目录只读；置信度委托 media_infer，不重复造轮子。
