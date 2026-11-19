# TASK-207-B 完成报告：cray-1 新包过闸实测 + supercomputer 分档补记

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。

## 交付物清单

1. **cray-1 过闸实测复跑**：validate + model_check 均 0 FAIL，catalog_ref 确认 cray-1 已反链。
2. **分档口径补记**：`第二批分档验收口径_v1.md` §二 补「S 档 category=supercomputer 过闸记录」。

## 实测结论

- **cray-1 过闸**：validate 78 PASS / 0 FAIL；model_check FAIL 0 / WARN 0（LOD1，5 网格）。
- **cray-1 已反链**：目录 `C-SC-000003` done、taxonomy `["计算机","超级计算机","向量机"]`（203-A 已补）。
- **category=supercomputer 放行**：validate 对 `category=supercomputer` 已放行（78 PASS 实证），
  `emulator="none"`（无成熟模拟器，静态+原理动画）走 S 档「无 bone → none」口径。

## 验收日志（原文 + 退出码）

```
# 1) cray-1 validate / model_check
validate cray-1   → 总计 78 条 PASS 78 / FAIL 0
model_check cray-1 → LOD1 观察档，5 网格，FAIL 0 / WARN 0

# 2) catalog_ref 复跑（扫共享盘）
内容包 38 个，目录条目 1582 行
REF-01 悬空包引用：0 条 · REF-02 反链缺失：1 个（amiga-1000）· REF-03 漂移：未使用 1 条 · REF-04 形态非法：0 条
（cray-1 反链 C-SC-000003 done 已补齐，无残留 FAIL）

# 3) 分档口径补记原文（节选）
cray-1 是第二批首个 category=supercomputer 包，validate 枚举放行、S 档「无 bone → emulator=none」口径适用、
目录 taxonomy「计算机/超级计算机/向量机」对齐。

# 4) 门禁只读复测（verify_all --daily --cache）
结果：41/41 通过   （rc=0）
```

## 与任务书的漂移（如实）

1. **cray-1 反链确认**：任务书说"203-A 已补反链（C-SC-000003 done）"，实测确认——cray-1 反链已补齐。
2. **当前 REF-02 缺失是 amiga-1000**（非 cray-1）：catalog_ref 共享盘视图下 REF-02 缺失 1 个 =
   amiga-1000（执行期间新产、未反链），cray-1 已无残留 FAIL。
3. **cray-1 emulator="none"**：`category=supercomputer` 但 `emulator="none"`（无成熟 Cray-1 模拟器），
   与 UNIVAC I 同款"无成熟模拟器"口径，已在分档补记里写明。
4. 内容包 38 个（共享盘又增 amiga-1000），镜像 34 台 ready 不变，差额扩到 4 台（含 amiga-1000）。

## 红线自查

1. 不下载 ROM/二进制 ✓；2. 不臆造结果 ✓（cray-1 实测 0 FAIL 如实记录，amiga-1000 反链缺失如实标）；
3. 只改 02 目录 ✓（只读复跑 + 口径补记，未改 03 线内容包/目录）；4. 复跑有日志、补记有依据 ✓；
5. 无 git/代理/PAT ✓。
