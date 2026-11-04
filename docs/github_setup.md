# github_setup.md —— GitHub 接入手册（TASK-86A）

> 账号：Luctw007 · 仓库：`diorama-museum`（公开，MIT）
> 地址：https://github.com/Luctw007/diorama-museum
> 现状见文末"当前推进状态"。

## 1. 仓库架构（已定案：monorepo）

单仓库五线子目录方案（本轮已推 01 线为第一批）：

```
diorama-museum/
  01/   ← 工程线（当前：以 01 repo 全树推送）
  02/ 03/ 04/ 05/  ← 后续各行目录平铺进入（待各线 git 化后按轮推进）
```

## 2. 认证铁律（高于一切）

1. **PAT/密码/SSH 私钥永远不落盘**：不进 `.git/config`、不进任何 commit、
   不进任务文档与报告；
2. 推送用一次性内联 URL：`git -c credential.helper= push https://x-access-token:<PAT>@github.com/... main`
   ——`credential.helper=` 置空确保不写 Windows 凭据管理器，`push` 不带 `-u` 确保不写 config；
3. 推完即用 `git remote -v` 与 `git config` 复查无 `ghp_`/`x-access-token` 字样；
4. **直连失败时经本机代理推**（2026-11-05 实战验证）：用户本地代理客户端监听
   `127.0.0.1:10808`（HTTP）时，push 加 `-c http.proxy=http://127.0.0.1:10808`；
   `api.github.com` 常可直连、`github.com` 443 常被阻断——优先走代理线路；
5. 长期方案：用户侧配 SSH key（github.com/settings/keys），本地 remote 永远用
   `https://github.com/Luctw007/diorama-museum.git`。

## 3. 各线推送顺序（照做卡）

```powershell
$git = "C:\Program Files\Git\cmd\git.exe"   # 或直接把 Git 加入 PATH 后直接用 git
cd D:\work\NN\repo
& $git init; Copy-Item D:\work\01\repo\.gitignore .
& $git add <按三段>; & $git -c user.name="NN线" -c user.email="NN@diorama.local" commit -m "chore(NN): 首次提交-..."
& $git remote add origin https://github.com/Luctw007/diorama-museum.git
# 推送需用户新发 PAT（每次会话提供一次）：
& $git -c credential.helper= push "https://x-access-token:<PAT>@github.com/Luctw007/diorama-museum.git" main
```

## 4. 当前推进状态（2026-11-05）

- 仓库已建（公开）；01 线 main 已推 **5 个提交**（aa4aa30…5499bb7），远程/本地一致；
- 推送线路固化：`-c http.proxy=http://127.0.0.1:10808` + 一次性令牌（详见 §2）；
- 分支保护与 CI（verify_all --daily 行动）建议下轮排：main 禁止直推，走 PR。