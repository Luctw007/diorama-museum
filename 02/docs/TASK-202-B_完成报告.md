# TASK-202-B 完成报告：第二批新包过闸实测复跑 + 镜像收口口径登记

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。

## 交付物清单

1. **双包过闸实测复跑**：univac-1、cdc-6600 各跑 validate + model_check，均 0 FAIL。
2. **镜像收口口径登记**：新增 `docs/镜像收口口径_v1.md`（待镜像清单 + 反链同步要求 + 降级口径）。

## 实测结论

- **univac-1 / cdc-6600 均已过闸**：validate 各 78 PASS / 0 FAIL；model_check 各 FAIL 0 / WARN 0；
  且**均已反链**（univac-1→C-MF-000050 done、cdc-6600→C-MF-000043 done）。
- **当前 REF-02 缺失 1 个 = cray-1**（新产包未反链，非任务书说的 cdc-6600）。
- **待镜像 3 台**：univac-1 / cdc-6600 / cray-1（共享盘 37 包 vs 镜像 34 台 ready）。

## 验收日志（原文 + 退出码）

```
# 1) 双包 validate / model_check
validate univac-1   → 总计 78 条 PASS 78 / FAIL 0
validate cdc-6600   → 总计 78 条 PASS 78 / FAIL 0
model_check univac-1 → LOD1 观察档，5 网格，FAIL 0 / WARN 0
model_check cdc-6600 → LOD1 观察档，5 网格，FAIL 0 / WARN 0

# 2) catalog_ref 复跑
内容包 37 个，目录条目 1582 行
REF-01 悬空包引用：0 条 · REF-02 反链缺失：1 个（cray-1）· REF-03 漂移：未使用 1 条（C-PC-000208）· REF-04 形态非法：0 条
FAIL 1

# 3) 门禁只读复测（verify_all --daily --cache）
结果：41/41 通过   （rc=0）
```

## 与任务书的漂移（如实）

1. **cdc-6600 已反链（非任务书说的"无反链"）**：实测目录里 cdc-6600 → C-MF-000043 done，03 线已补
   反链；当前 REF-02 缺失的是 **cray-1**（执行期间新入共享盘、未反链）。
2. **待镜像 3 台（非任务书 2 台）**：cray-1 是执行期间新产的第三台待镜像包。
3. **REF-03 漂移 1 条**：registry 1583 含刚 allocate 的 C-PC-000208（Apple IIe，202-A），目录未回填故
   "未使用 1 条"，待 05 线产包回填后归零。
4. 门禁 41/41（镜像视图基线），共享盘 catalog_ref 37 包视图下 FAIL 1（仅 cray-1 反链），已如实记录。

## 红线自查

1. 不下载 ROM/二进制 ✓；2. 不臆造结果 ✓（复跑 FAIL 1 如实记录，未写"已过闸"除非 0 FAIL——univac-1/
   cdc-6600 确实 0 FAIL，cray-1 反链缺失如实标）；3. 只改 02 目录 ✓（只读复跑 + 登记）；4. 复跑有日志、
   口径有依据 ✓；5. 无 git/代理/PAT ✓。
