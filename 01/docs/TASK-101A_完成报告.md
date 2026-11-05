# TASK-101A 完成报告（01 线接棒认知装载）

## 一、认知装载摘要（5 份 ×3 行）

1. 00_项目总览
- 开源箱庭电子设备博物馆：Godot4 主引擎 + Python 网关，MIT；五线流水线，用户只审代码。
- 基线：设备包 27 ready、目录 1484 条、门禁 --daily 全绿；Godot 实机与真模拟器是用户侧闭环。
- 决策：GitHub monorepo 已接；01 线移交新账号（本账号）、原账号转统筹。

2. github_setup
- monorepo 本地根 D:\work\01\repo，02-05 由 01 每轮收口镜像并入；根 .gitignore 是红线防线。
- 铁律：PAT 永不落盘；一次性内联 URL + credential.helper 空 + 不带 -u；断连走 127.0.0.1:10808 代理。

3. git_workflow
- 身份 -c「01-工程线」覆盖、不动全局；每日一提交「01线 TASK<编号>: 短述」。
- 唯一入仓禁令：二进制/ROM/版权介质 + third_party/、_drill/、密钥。

4. realrun_drill_v2
- 真跑三步放：下载→槽位→manifest 照抄；doctor --fix-check 体检+冒烟。
- 假二进制预演修掉网关 _spawn 缺 module 缺陷；demo 通道免二进制直出帧存证。

5. 规范 v0.6
- 13 键统一英文；taxonomy_path 允许两级（补「未细分」）。
- catalog_check 裁判与 _adapt 归一层互补；存量迁移完前归一层不收紧。

## 二、门禁实跑
python 01/scripts/verify_all.py --daily --cache → **33/33 全绿**（任务书 32/32 已漂移：03 线新增 atari-st 包）

## 三、收口镜像例行
sync_monorepo.py 四线：02=151、03=348、04=116、05=177 文件，rc=1 均成功；git add -A + commit（-c 身份，未 push），commit hash：ae12de4

## 四、接棒确认
红线三条：①不下载/入库 ROM·二进制·版权介质（只清单级引用）；②不编造史实，无来源标「需核实」；③各线只改自己目录，门禁是唯一判定口径。
风险三条：①验收基线数字漂移（32→33），任务书需随轮次同步；②本会话执行机与 D:\work 宿主分离，python/git 需本机便携安装，嵌入式 Python 会破坏 m0/m1b/catalog 模块路由；③sync_monorepo 锚定 D:\work 本地盘路径，跨共享盘执行依赖驱动器映射，宿主直跑更稳。