# TASK-302-C 完成报告

> 任务：第四批 allocate 预案（02 线）。只改 02 目录，纯文档预案。

## 一、交付物清单
新增 `docs/第四批allocate预案_v1.md`（9 台在册 + BlackBerry 850 缺失 + 目录归属 + 执行清单）。

## 二、验收日志（原始输出 + 退出码）
1. 门禁：`verify_all --daily --cache` → 55/55 通过（rc=0）。
2. catalog_ref：REF-01~04 全 0、FAIL 0（rc=0）。
3. 自证：9 台续接序号表命中；BlackBerry 850 缺失行命中；无冲突对账声明命中；字节数 >1500。
4. 改动清单：只新增 2 份 md。

## 三、结论
第四批目录条目**已真号在册（planned）**，与第三批「占位 0xx 待 allocate」不同——第四批**无需 allocate 目录
id**，产包时直接回填 device_id + status=done；BlackBerry 850 缺失待补录。

## 四、与任务书的漂移（如实）
1. **核心漂移**：任务书假设第四批参照第三批「各前缀最大号 +1 续接 allocate」，实测第四批 9 台目录条目已
   **真号在册**（C-PC-000059 等 planned），无需 allocate；本预案按实测改写为「无需 allocate、仅回填」，
   并如实标注此差异。

## 五、红线自查
零联网零下载；目录 id 在册/缺失以实测为准；只改 02 目录、未 allocate、未改 jsonl、未产包。
