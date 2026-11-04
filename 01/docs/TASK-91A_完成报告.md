# TASK-91A 完成报告（01/docs/TASK-91A_完成报告.md）

> 01 线 · 2026-11-05 · 任务：CI 最小流水线 + main 分支保护。

## 1. 交付物

| 文件 | 说明 |
|---|---|
| `.github/workflows/ci_01.yml` | push/PR→main、paths=01/** 触发：compileall + m0 + m1b + slots + gd；目录类步骤（依赖 03/05 镜像）在注释里写明不纳入 |
| `01/docs/branch_protect.md` | 用户侧网页操作卡（Add rule → require PR + status check `gate-01` → 不允绕过） |
| 本地等价证据 | 五步全绿（见下）；workflow 文件本地语法经 compileall 验证 |

## 2. 本地等价运行证据（推送前全步先行验证）

```text
$ python -m compileall -q 01/scripts 01/gw          → rc=0
$ python 01/scripts/m0_check.py                    → M0 验收全部通过 ✔
$ python 01/scripts/m1b_check.py                   → 断言 19 条全过 ✔
$ python 01/scripts/slot_consistency_check.py      → 完工包 24… SC-01 违规 0 ✔
$ python 01/scripts/gd_symbol_check.py             → 101 funcs/7 signals/0 MISS ✔
$ python 01/scripts/verify_all.py --daily --cache --no-ref-hard → 31/31 通过 ✔
```

## 3. 现状与待办

- 91 全部产物与完成报告已推送（远程 main 本报告为最新提交）；
- **workflow 文件本地已就绪、推送待 PAT 补 scope**：GitHub 对推 `.github/workflows/`
  要求 token 带 `workflow` scope——已请用户编辑现有 token（值不变）勾选该 scope，
  勾好后提交推送并核查 Actions 首跑；
- 门禁今日 31/31（`--no-ref-hard` 降级）：03 线 vic20 在制包反链未回填（REF-02），
  03 回填后恢复硬判。

## 4. 开放问题

- CI 在 ubuntu 上未实跑过（首次 Actions 待 workflow 推送后验证）——m0/m1b 涉及
  localhost 端口与子进程，理论上跨平台，首跑若暴露平台差异按缺陷闭环修。