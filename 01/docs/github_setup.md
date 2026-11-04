# github_setup.md —— GitHub 接入手册（TASK-86A）

> 账号：Luctw007 · 仓库：`diorama-museum`（公开，MIT）
> 地址：https://github.com/Luctw007/diorama-museum
> 现状见文末"当前推进状态"。

## 1. 仓库架构（已定案：monorepo，五线已并仓）

远程 https://github.com/Luctw007/diorama-museum 根结构 = 本地 `D:\work\01\repo`：

```
diorama-museum/
  01/      工程线（网关/门禁/槽位/CI 收口）
  02/ 03/ 04/ 05/   各线 mirror（由 01 收口镜像，见 §3）
  README.md / .gitignore（根级防线：*.bin *.rom *.exe *.iso *.img *.chd、**/third_party/ 等）
```

各线仍在 `D:\work\0N\repo` 各自作业；01 线每轮例行结尾执行 §3 收口镜像 → 提交 → 推送。

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

## 3. 收口镜像与推送（01 线每轮结尾照做）

```powershell
# ① 四线镜像（注意：robocopy 禁接管道/Out-Null（会误报 rc=16），rc≤7 均为成功）
robocopy D:\work\02\repo D:\work\01\repo\02 /E /XD .git __pycache__ .workbuddy /XF *.pyc /NFL /NDL /NJH /NJS
robocopy D:\work\03\repo D:\work\01\repo\03 /E /XD .git __pycache__ .workbuddy /XF *.pyc /NFL /NDL /NJH /NJS
robocopy D:\work\04\repo D:\work\01\repo\04 /E /XD .git __pycache__ .workbuddy /XF *.pyc /NFL /NDL /NJH /NJS
robocopy D:\work\05\repo D:\work\01\repo\05 /E /XD .git __pycache__ .workbuddy /XF *.pyc /NFL /NDL /NJH /NJS
# ② 提交（红线防线在根 .gitignore 统一把关）
git -c user.name="01-工程线" -c user.email="01@diorama.local" add -A
git -c user.name=.. -c user.email=.. commit -m "chore(monorepo): NN-NN 轮收口镜像"
# ③ 推送（PAT 一次性、-c credential.helper= 空、不带 -u；网络直连失败加 -c http.proxy=http://127.0.0.1:10808）
git -c credential.helper= push "https://x-access-token:<PAT>@github.com/Luctw007/diorama-museum.git" main
```

## 3b. 各线本地 git 化（可后补，非推送前提）

各线自行 `git init` 的指引不变（docs/git_workflow.md）；GitHub 侧本体是 monorepo，
各线本地仓只是过程稿，最终以收口镜像为准。

## 4. 当前推进状态（2026-11-05）

- 仓库已建（公开）；**五线 monorepo 已重组**：99bb2b9 起全部历史含 02-05 首批镜像，
  1098 个文件；main 高位 99bb2b9，远程/本地一致；
- 红线防线：根 .gitignore 统一（*.bin/*.rom/*.exe…、**/third_party/、**/slots/_drill/），
  并借此清掉了早期误入的 `godot/content/test-device/meshes/mainboard.bin`；
- 推送线路固化：`-c http.proxy=http://127.0.0.1:10808` + 一次性令牌（§2）；
- 分支保护与 CI：91-A 任务在建。