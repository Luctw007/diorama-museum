# migrate_package.py — 内容包 v0.1 → v0.2 迁移助手（TASK-17A）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本文档与配套代码按 MIT 许可分发。

本工具把内容包 `meta.json` 中"可安全机械转换"的本地化字段从 v0.1 结构迁到 v0.2 结构，
不依赖任何第三方库（纯标准库）。

## 1. 用法

```bash
# dry-run（默认）：只看 diff，不写盘
python tools/migrate/migrate_package.py content/<device-id>

# 落盘写入
python tools/migrate/migrate_package.py content/<device-id> --apply

# 写入后自动调用 validate.py 并打印最后 1 行（总计/FAIL 数）
python tools/migrate/migrate_package.py content/<device-id> --apply --validate

# 指定 validate.py 路径（默认相对本脚本定位 tools/validate/validate.py）
python tools/migrate/migrate_package.py content/<device-id> --apply --validate \
    --validate-script /abs/path/validate.py
```

- 参数 `<device-id>` 可以是一个内容包目录（含 `meta.json`），也可以是一个上级目录——
  后者会扫描其下所有含 `meta.json` 的子目录，逐个处理。
- 退出码：所有包处理成功为 `0`；任一包出错为 `2`。
- **幂等**：已迁移（或本就不需迁移）的包再次运行会报告 `无需迁移（已是 v0.2 结构）`，退出码 `0`。

## 2. 转换对照表

| 位置 | v0.1 | v0.2 | 迁移动作 |
|---|---|---|---|
| `meta.name` | string | localized `{zh, en}` | `zh = 原值`；若存在 `name_en` 则 `en = name_en` |
| `meta.name_en` | string（正常字段） | deprecated | 并入 `name.en` 后**删除**（R-088） |
| `meta.spec_version` | `"0.1"` | `"0.2"` | 直接升版本（R-071） |
| `meta.version` | SemVer | SemVer | **保持不变**，仅提示作者可考虑迁移性小版本（如 `1.1.0`） |
| `assemblies[].role` | string | localized `{zh}` | `zh = 原文`（缺 en 由 R-087 仅警告，不阻塞） |
| `components[].role` | string | localized `{zh}` | `zh = 原文` |

## 3. 边界（哪些**不做**）

本工具只做上表列出的"可安全机械转换"字段，以下内容一律**进报告不改写**，交作者/对应内容线人工处理：

| 项目 | 处理方式 |
|---|---|
| `meta.intro` / `meta.era` / `meta.manufacturer` 缺失 | 提示，不自动补写（涉及文案/事实，无法机械生成） |
| `meta.version` 是否升小版本 | 提示（建议 `1.1.0`），不自动改 |
| `runtime.output_sinks[].surface` 非法枚举（如 edsac 的 `indicator_led`） | 不自动改（R-084，数据语义判断） |
| `runtime.input_map` 值 legacy 字符串 → 结构化 `{map,key}` | 不自动改（legacy 仍合法，见规范 v0.2.1 §11.2） |
| glTF 节点名与 `node_id` 不符（R-090，如 edsac 的 `console.gltf`） | 不自动改（需改动二进制/JSON 网格资产，见完成报告 §4） |
| `assemblies[].role` / `components[].role` 缺失 | 提示必填缺失，不自动造文案 |

## 4. 设计说明

- **目标版本硬编码为 `"0.2"`**：取自 v0.2 规范 schema 的 `$defs/meta/properties/spec_version.const`。
  即便某个包仍带 v0.1 schema（`const == "0.1"`），迁移目标仍是规范最新版 `"0.2"`，不读取旧
  schema 常量来"降级"目标。
- **只改 `meta.json`**：不触碰 `runtime.json` / `annotations` / `THIRD_PARTY.md` / 网格资产，
  因此不会破坏 `runtime.json 与 meta.json.runtime 逐字节等价`（R-004）。
- **先分析后写盘**：`build_plan` 只读 `meta.json` 产出变更计划；`apply_plan` 才写盘，二者逻辑
  保持一致，且 apply 后立即复检幂等。
- **写入风格**：`json.dump(..., ensure_ascii=False, indent=2)` + 末尾换行，与脚手架一致。

## 5. 演练（demo/）

`demo/` 下为四个 03 线包的副本演练（manchester-baby / eniac / edsac / edvac）。完整
dry-run → apply → validate 闭环日志与幂等性测试见《docs/TASK-17A_完成报告.md》§2。
