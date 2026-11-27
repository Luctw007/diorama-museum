# TASK-323-A 完成报告

## 交付物清单

- [x] `docs/research/第三批产包开产装配口径卡_v1.md`（3217 字节，≥2500 达标）

## 执行摘要

把 318-A~D 五件备底固化为「05 线装配取用口径」：①六件套逐件字段映射表（encyclopedia 段落 / annotations role+flow / THIRD_PARTY 三件套 / meta 五字段 / runtime 四字段 / 「需核实」落点）；②10 台逐台 device_id + 目录续接预案 + 卷归属（有模拟器 4 + none 6）；③05 线装配取用指令（每件从哪份备底取、落到哪个文件）；④版本治理声明。

## 验收日志

```
verify_all --daily --cache：75/77 通过（m0/m1b 为 01 线网关运行时问题，非 03 线）
catalog_ingest --gate：摄取 5 文件 1583 行，错误 0，rc=0
```

## 与任务书的漂移

无。六件套映射表 + 10 台 device_id 表 + 「需核实」落点声明行命中。

## 红线声明

只写口径卡文本，不写 content/<id>/、不产包、不改 jsonl、不 allocate、不代点头。
