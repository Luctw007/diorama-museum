# PR 流程演练卡（启用 main 分支保护后使用）

> branch_protect.md 的配套：保护启用后 main 禁止直推，日常合入改为"分支 → PR → CI 绿灯 → merge"。
> 本卡在**未启用保护时也可预演**（普通 push 分支 + 手动开 PR）。

## 日常收口流程

```powershell
cd D:\work\01\repo
python 01\scripts\sync_monorepo.py                 # ① 镜像四线（只镜像）
git checkout -b sync/20261105                      # ② 开收口分支
git -c user.name="01-工程线" -c user.email="01@diorama.local" add -A
git -c user.name=.. -c user.email=.. commit -m "chore(monorepo): NN-NN 轮收口镜像"
git -c http.proxy=http://127.0.0.1:10808 push origin sync/20261105   # ③ 推分支
# ④ 网页：Compare & pull request → 等 CI（gate-01）全绿 → Merge
git checkout main && git pull                      # ⑤ 本地 main 同步
```

## 关键点

- push 分支不需要 PAT 直接标（若要求认证时用一次性 PAT 内联 URL：规则同 github_setup.md §2）；
- CI 绿灯 = 五步（96-B 后为全门禁）通过；黄/红一律不合并；
- 合并后本地 `git pull` 用干净 remote（无凭据残留复查：`git config --list | Select-String ghp_` 应为空）。

## 预演方式（保护未启用时）

上面前 ③ 步正常执行即可（分支推送到 GitHub 无阻碍），开 PR 后可选择直接 merge 按钮；
当日后启用保护，此卡照用不变。