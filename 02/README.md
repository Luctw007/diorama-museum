# 箱庭电子博物馆 — 仓库（repo）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本仓库文档与代码均按 MIT 许可分发。

本仓库承载「箱庭电子博物馆」项目的各任务交付物。任务相互独立、可并行，通过本 README 合并说明，**不要互相覆盖文件**。

## 目录结构

```
repo/
├── README.md                  # 本说明（各任务合并说明）
├── docs/
│   ├── 内容包规范_v0.1.md      # TASK-02：内容包规范 v0.1（九章）
│   ├── 内容包规范_v0.2.md      # TASK-07：内容包规范 v0.2（12 章 + 迁移表）
│   ├── TASK-02_完成报告.md     # TASK-02：完成报告
│   ├── TASK-07_完成报告.md     # TASK-07：完成报告
│   └── design/                # TASK-04/09：UI 设计规格（01~07 + 报告）
├── content/
│   ├── schema/
│   │   └── device_spec.schema.json   # TASK-07：DeviceSpec JSON Schema v0.2（draft 2020-12）
│   ├── test-device/           # 最小示例设备包「验证方块机」（假想设备，v0.2 增强）
│   └── manchester-baby/       # TASK-07：Manchester Baby 骨架（仅骨架，内容由 08 线填写）
└── tools/
    └── validate/
        ├── validate.py        # TASK-07：内容包校验器 v0.2（54 规则）
        ├── budget_check.py    # TASK-07：资产预算检查器（glTF 精确统计 + PNG/JPEG 纹理解析）
        ├── scaffold_device.py # TASK-07：设备包脚手架生成器
        └── tests/
            ├── run_tests.py   # TASK-07：校验器测试（正例 + 19 反例）
            └── tex_sample/    # 纹理解析夹具
```

## 任务进度

| 任务 | 状态 | 交付物位置 |
|---|---|---|
| TASK-01（引擎骨架 + PROTOCOL.md） | 待办（并行） | `tools/`、`docs/PROTOCOL.md`（待建立） |
| TASK-02（内容包规范 v0.1 + 校验工具链） | ✅ 完成 | 见上表 |
| TASK-07（规范 v0.2 + 工具链强化） | ✅ 完成 | 见上表 |
| TASK-03（内容包生产） | 待办 | — |
| TASK-04（核心交互与 UI 设计规格） | ✅ 完成 | `docs/design/`（01~05 初版 + 完成报告） |
| TASK-05 | 待办 | — |
| TASK-08（Baby 设备包与黎明厅展呈内容） | 待办（填 manchester-baby 内容） | `content/manchester-baby/` |
| TASK-09（04 续线：v1.0 冻结 + 实现指引 + 测试 v2） | ✅ 完成 | `docs/design/`（01~05 升级 v1.0/v2 + 06/07 新增 + TASK-09 报告） |

## 快速上手（TASK-07，v0.2）

```bash
# 校验示例包（应全绿，退出码 0）
python tools/validate/validate.py content/test-device
python tools/validate/validate.py content/manchester-baby

# 跑校验器测试套件（正例 + 19 反例）
python tools/validate/tests/run_tests.py

# 预算自查（glTF 精确统计 + 纹理解析）
python tools/validate/budget_check.py content/test-device/meshes/mainboard.gltf --level L2

# 生成新设备包骨架
python tools/validate/scaffold_device.py content/<device-id> --name "名称" --era 1977 --category placeholder
```

## 约定

- 各任务在 `docs/`、`content/`、`tools/` 下按需建立子目录，**不覆盖他人文件**。
- 术语以《内容包规范 v0.2》附录 A 与设计文档 v0.1 核对后为准。
- 文档与代码统一加 MIT 头注释。
