# TASK-197-A 完成报告：v0.7 正式定稿收口

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。

## 交付物清单

1. 改 `docs/v0.7_RTO项裁决记录.md`：A-1、D-2 裁决结果「转 1.x 待办」→「已落地（191-A，01 线）」，裁决
   分布统计更新（落正文 4 + 已落地 2 + 转 1.x 3），§五 后续动作标注已收口。
2. 改 `docs/规范v0.7_1.0正文修订_v2.md`：E-2 数字引用补「univac-1、cdc-6600 已产待镜像入册」标注。
3. 改 `docs/1x待办清单_v1.md`：新增「六、目录侧待办」登记 Apple IIe（`C-PC-0000xx` 待 allocate）。

## 验收日志（原文 + 退出码）

```
# 1) 门禁只读复测（verify_all --daily --cache）
结果：41/41 通过   （rc=0）

# 2) 定稿回写自证（Select-String 命中）
v0.7_RTO项裁决记录.md:
  | A-1 | ... | **已落地（191-A，01 线）** | 01 线 slot_loader.py L40-43 MEDIA_CLASSES 9 值含 none
  | D-2 | ... | **已落地（191-A，01 线）** | 01 线 release_check.py L73-100 run_status live/dry-run/missing
规范v0.7_1.0正文修订_v2.md:
  现状为 **存量 34 台包（...）、目录 1582 条、门禁 41/41**；另有 **univac-1、cdc-6600 已产待镜像入册**

# 3) Apple IIe allocate 待办登记原文
| Apple IIe（第二批第 8 台） | `C-PC-0000xx`（占位） | 产包前由 02 线 `id_registry allocate C 1 PC` 分配真实 id，03/05 线回填 | 02 线分配 / 05 线回填 |
```

## 与任务书的漂移（如实）

1. **待镜像包数**：任务书写「univac-1 待镜像 1 台」，实测共享盘还有 **cdc-6600** 也已产、同样不在
   monorepo 镜像（pkg_registry 现扫 `01/repo/03/content` 镜像，34 台 ready），故正文标注补记 2 台
   （univac-1 + cdc-6600）。
2. **pkg_registry 扫描源已变**：现扫 monorepo 镜像路径（`\DESKTOP-2IDAL09\work\01\repo\03\content\`），
   非共享盘；共享盘 03/repo/content 有 30 包目录、镜像仅 34 台 ready（含 data-general-nova/hp-2100，
   不含 univac-1/cdc-6600）。
3. A-1/D-2 落地证据引 191-A 落地记录（slot_loader.py L40-43、release_check.py L73-100），非凭经验。

## 红线自查

1. 不下载 ROM/二进制 ✓；2. 不臆造数字 ✓（以 verify_all 实测 41/41 为准，univac-1 标"待镜像"非"已入册"）；
3. 只改 02 目录 ✓；4. 不代 03 产包/不代 01 改门禁 ✓（Apple IIe 只登记待办）；5. 回写有据、数字可溯 ✓；
6. 无 git/代理/PAT ✓。
