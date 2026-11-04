# TASK-82B 完成报告（02 线 2/2 · 轻量）

## 一、交付物

1. `docs/catalog/registry.jsonl` 清空：50 条 C-GEN 模拟记录 → **0 条**（任务文档写
   `tools/index/registry.jsonl`，实际台账路径为 `docs/catalog/registry.jsonl`，id_registry 与
   catalog_ref_check 均读此处，按实处理）。
2. `docs/规范增补_v0.6.2.md` 追加「六、反链义务（CC-10 语义）」：完工过闸 ready 的内容包必须回填
   device_id 且 status=done；由 REF-02 拦截（编号说明：语义 CC-10，不撞 catalog_check 现有 CC-01~08）。
3. emulators_registry：mame-apple2=骨架、simh-pdp8=预留，77-A 已补正，**无需再改**（"若有"项为空）。

## 二、REF-03 复验（贴证）

```
REF-03 台账漂移：registry 0 条 / 目录使用 0 条（未使用 0 条）
```
漂移 50 → **0**。另：REF-02 反链缺失 3 → **1**（仅 pet2001，03/05 线回填进展）。

## 三、开放问题

- 反链义务当前由 REF-02 拦（CC-10 语义），是否在 catalog_check 内正式落地 CC-10，待定。
