# TASK-126 完成报告（02 线）

## 一、交付物

`docs/贡献者自测包说明_v1.1.md`。

## 二、覆盖

- 内容清单：v1 为 13 条目（4 源材料 + 1 schema + 8 校验器）；v1.1 增量 = 新增 gd_naming_check.py。
- 自测命令：validate / catalog_check / catalog_ref_check / gd_naming_check，与 CONTRIBUTING、PR 模板交叉一致。
- gd_naming_check：GN-01（方法名黑名单）/ GN-02（`:=` Variant）/ GN-03（class_name 未注册），
  与 v0.6.3 附录 A 逐字对齐，输出格式对齐 gd_symbol_check。

## 三、红线

01 线 contrib kit 与 zip 只读；gd_naming_check 仅说明不实现（实现归 01 线）。
