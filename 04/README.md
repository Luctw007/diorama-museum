# 箱庭电子博物馆 — 仓库（repo）

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组。本仓库文档与代码均按 MIT 许可分发。

本仓库承载「箱庭电子博物馆」项目的各任务交付物。任务相互独立、可并行，通过本 README 合并说明，**不要互相覆盖文件**。

## 目录结构

```
repo/
├── README.md                  # 本说明（各任务合并说明）
├── docs/
│   ├── 内容包规范_v0.1.md      # TASK-02：内容包规范（权威版，九章 + 规则表 R-xxx）
│   └── TASK-02_完成报告.md     # TASK-02：完成报告
├── content/
│   ├── schema/
│   │   └── device_spec.schema.json   # TASK-02：DeviceSpec JSON Schema（draft 2020-12）
│   └── test-device/           # TASK-02：最小示例设备包「验证方块机」（假想设备）
└── tools/
    └── validate/
        ├── validate.py        # TASK-02：内容包校验器
        ├── budget_check.py    # TASK-02：资产预算检查器
        └── tests/
            └── run_tests.py   # TASK-02：校验器测试（正例 + 6 反例）
```

## 任务进度

| 任务 | 状态 | 交付物位置 |
|---|---|---|
| TASK-01（引擎骨架 + PROTOCOL.md） | 待办（并行） | `tools/`、`docs/PROTOCOL.md`（待建立） |
| TASK-02（内容包规范 + 校验工具链） | ✅ 完成 | 见上表 |
| TASK-03（内容包生产） | 待办 | — |
| TASK-04（核心交互与 UI 设计规格） | ✅ 完成 | `docs/design/`（01~05 初版 + 完成报告） |
| TASK-05 | 待办 | — |
| TASK-09（04 续线：v1.0 冻结 + 实现指引 + 测试 v2） | ✅ 完成 | `docs/design/`（01~05 升级 v1.0/v2 + 06/07 新增 + TASK-09 报告） |
| TASK-13（04 线：A 测试执行手册 + B 音效资产来源） | ✅ 完成 | `docs/design/`（08/09/10/11 + TASK-13A/13B 报告） |

## 快速上手（TASK-02）

```bash
# 校验示例包（应全绿，退出码 0）
python tools/validate/validate.py content/test-device

# 跑校验器测试套件
python tools/validate/tests/run_tests.py

# 预算自查
python tools/validate/budget_check.py content/test-device/meshes/mainboard.gltf --level L2
```

## 约定

- 各任务在 `docs/`、`content/`、`tools/` 下按需建立子目录，**不覆盖他人文件**。
- 术语以《内容包规范 v0.1》附录 A 与设计文档 v0.1 核对后为准。
- 文档与代码统一加 MIT 头注释。
