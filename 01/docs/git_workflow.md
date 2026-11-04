# git 工作流指引（TASK-81B · 各线照做版本）

> 目标：01 线已按本指引建仓；02/03/04/05 线在**各自 repo 目录**内照此操作卡执行一遍。
> 原则：红线进 `git` 版本库的只有一个——**任何二进制、ROM、版权介质文件**。其余皆可入。

## 0. 前置（每台机器一次）

- 安装 Git for Windows（或挥便携版解压），确认 `git --version` 可执行；
- 身份：不要动全局 config。未配置身份时用每条命令前加临时身份：
  `git -c user.name="线号-线名" -c user.email="NN@diorama.local" <子命令>`，
  或在你自己的账号下 `git config user.name/user.email`（仅限本仓库 config，不动全局）。

## 1. 初始化（每线 repo 根目录一次）

```powershell
cd D:\work\NN\repo
git init
# 复制 01 线的 .gitignore（把 NN 换成自己）：
Copy-Item D:\work\01\repo\.gitignore .
```

`.gitignore` 要点（与 01 同款）：`__pycache__/`、`*.pyc`、`third_party/`、
`slots/_drill/`、`demo_out/`、`docs/doctor_log_*.txt`、`.workbuddy/`。

## 2. 首次提交（三段式，避免大杂烩）

```powershell
git add scripts gw                       # ① 代码（02/03/04/05 按自己目录结构替换）
git commit -m "chore(NN): 首次提交-代码与工具链"
git add docs slots                       # ② 文档与槽位
git commit -m "chore(NN): 首次提交-文档与槽位声明"
git add .                                # ③ 内容树（content/ 等），.gitignore 已自动挡掉红线
git commit -m "chore(NN): 首次提交-内容树"
```

读三遍再回车：`git status` 里**不应出现** `third_party/`、`_drill/`、`*.pyc`。
红线条目机器验证：`git check-ignore third_party/mame/mame` 必须有输出。

## 3. 每日一提交约定

- 完成任务后随手提交，message 格式：
  `NN线 TASK<编号>: <短述>`（例：`01线 TASK-76A: 注册表与槽位折叠`）；
- 一个逻辑改动一次 commit；禁止把别人目录/二进制塞进自己的提交；
- `git add` 用具体路径，不要 `git add -A` 一把梭。

## 4. 常用检查

```powershell
git status                 # 应干净或只有本轮的明确改动
git log --oneline -3       # 最近提交
git check-ignore <可疑文件>  # 红线命中验证
```

## 5. 禁止入版本库清单（每线固化，无例外）

1. 任何模拟器二进制（mame/pdp8/hatari/vice/stella…）；
2. 任何 ROM / BIOS / 固件 / 磁盘镜像 / 卡带镜像；
3. `third_party/` 全目录、`slots/_drill/` 假二进制件；
4. 密钥、token、个人凭据文件。