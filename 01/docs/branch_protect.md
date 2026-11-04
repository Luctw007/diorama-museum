# main 分支保护设定步骤卡（TASK-91A · 用户侧网页操作）

> 目的：main 禁止直推，一切变更走 PR + CI 绿灯。**本步骤在网页上做一次即长期生效。**

## 设置步骤（github.com → 仓库 Settings）

1. 打开 https://github.com/Luctw007/diorama-museum/settings/branches
2. 点 **Add branch protection rule**（或 Add rule）；
3. Branch name pattern 填：`main`
4. 勾选：
   - **Require a pull request before merging**（子项按默认：1 approval；如需更严可勾"Require review from Code Owners"）；
   - **Require status checks to pass before merging** → 搜并勾 `gate-01`（CI 跑一次后才会出现在搜索列表）；
   - **Do not allow bypassing the above settings**（防止绕过）；
   - 可选：Block force pushes / 对 admin 也生效；
5. 点 **Create**（或 Save changes）。

## 生效后行为

- 直接 `git push` main 会被拒绝（403 protected branch）→ 全部走 PR；
- 每个 PR 必须 CI（gate-01：compileall + m0 + m1b + slots + gd）全绿才能合并；
- 维护者（01 线）推送改为：开分支 → PR → 合并。收口镜像流程见
  `01/docs/github_setup.md §3`（PR 化后的变体：镜像提交进 `sync/YYYYMMDD` 分支 → PR）。

## 注意

- 若看不到 status checks 选项，先让 CI 跑成功一次（push 到任意分支触发）；
- 本项目是个人仓库、单维护者，1 approval 可只勾"Require approvals"为 0 或不勾，
  仅以 status check 兜底——但建议至少保留 PR 门。