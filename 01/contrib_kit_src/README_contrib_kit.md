# 贡献者自测包（contrib_kit v1）—— 箱庭电子博物馆

> 面向社区贡献者的离线自测工具包。本包只含**纯文本**（校验器 + 样例 + 说明），
> 不含任何模拟器二进制、ROM、介质或凭据（红线 FR-E3）。
> 完整贡献流程见项目 CONTRIBUTING.md（https://github.com/Luctw007/diorama-museum）。
> 许可：MIT（本包内全部代码与文档）。

## 包内结构

```
contrib_kit/
  README_contrib_kit.md      ← 本文件
  自测命令卡.md              ← 三行命令跑通自测（先读）
  提交清单.md                ← 内容包三件套核对 + 数据模板
  slot_manifest.sample.json  ← 模拟器槽位 manifest 样例
  tools/validate/            ← 02 线校验器（validate.py 及全部 *._check.py + tests/）
  content/schema/device_spec.schema.json  ← 内容包 schema（validate.py 引用）
```

## 最小可用流程（三步）

1. 照着 `提交清单.md` 做自己的内容包目录（`content/<device-id>/`，device-id 为
   kebab-case）；
2. 跑 `python tools/validate/validate.py <你的包路径>` → 必须 `FAIL 0`；
3. 把包与目录条目按 CONTRIBUTING 提交（目录条目须在对应大类 `.jsonl` 回填
   `device_id` 与 `status=done`）。

## 注意事项

- 校验器为**零第三方依赖**纯 Python（≥3.10）；无网络也能跑；
- 史实拿不准标「需核实」；THIRD_PARTY.md 三件套（分档+URL+日期）缺一不可；
- 主项目另有一键门禁（verify_all，含 m0/m1/引擎符号/槽位/目录引用）——本包不含
  引擎与网关，门禁全量请按仓库 README 操作。