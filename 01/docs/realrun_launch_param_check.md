# 三台真跑启动器前置参数核对卡（realrun_launch_param_check）

> TASK-181-B · 免 ROM / 零介质 / 零下载 / 零联网；**不启动任何真实模拟器进程**。
> 每项标 `[已对齐]`（源码+实测一致）或 `[需核实]`（标出处，不臆造）。
> 源码引用：`gw/emulators/{mame_apple2,simh_pdp8,stella}.py`、`scripts/launch_lib.py`、
> `slots/emulators/*/manifest.json`、`licenses/*.md`。

## 一、apple-ii → mame-apple2（gw/emulators/mame_apple2.py）

| 项 | 状态 | 核对结果 |
|---|---|---|
| 启动参数 | [已对齐] | `cmd = [binary, machine, "-video", "none", "-console", "-autoboot_script", <lua>]`（L106-107），media 追加 `-flop1`（L110）；与任务书第 3 章一致 |
| 工作目录 | [已对齐] | `cwd=os.path.dirname(binary)`（L113） |
| 键码注入参数 | [已对齐（代码口径）] | keymap 三级回退（config.keymap → `gw/emulators/keys/keymap_apple2.json` → 旧路径）+ `natkeyboard:post` 注入（见该文件 `_handle_input`/docstring）；**键码值本身** [需核实]（realrun_drill_v3 §二 #1-4） |
| ROM/介质缺失提示 | [已对齐] | `EMULATOR_BINARY_MISSING` 文案（L93）+ `binary_env=MAME_BIN` + `third_party\mame` + `licenses/MAME.md`；decision_chain 缺失态文案「把二进制放入 third_party\mame\mame 或设环境变量 MAME_BIN」（launch_lib.py:74-77） |
| 实测 | — | 176-A presmoke：`-version` → `0.289 (mame0289)` rc=0（约 33s）；`-createconfig`（cwd=临时目录）生成 mame.ini |

## 二、pdp8 → simh-pdp8（gw/emulators/simh_pdp8.py）

| 项 | 状态 | 核对结果 |
|---|---|---|
| 启动参数 | [已对齐] + [需核实] | `cmd = [binary, <start.ini>]`（L87）与任务书一致；**start.ini 内命令名/语法** [需核实]（骨架注释，L 见 `_write_script`） |
| 工作目录 | [已对齐] | `cwd=os.path.dirname(binary)`（L90） |
| 键码注入参数 | [已对齐（口径）] + [需核实] | TTY 文本注入（docstring：无 keymap 三级回退，与 mame_apple2 差异点）；**注入通道**（命令文件轮询 vs stdin 直写）[需核实] |
| ROM/介质缺失提示 | [已对齐] | `EMULATOR_BINARY_MISSING`（L75）+ `SIMH_PDP8_BIN` + `licenses/SIMH.md` |
| 实测 | — | 176-A presmoke：横幅 `PDP-8 simulator Open SIMH V4.1-0 Current`；stdin `quit` 退出 rc=0（**核销**退出命令与横幅两项） |

## 三、atari-2600 → stella（gw/emulators/stella.py）

| 项 | 状态 | 核对结果 |
|---|---|---|
| 启动参数 | [需核实] | `cmd = [binary]` + media 卡带路径追加（L81）；**无头/抓帧开关** [需核实]（L80 注释：以 `stella --help` 与版本为准） |
| 工作目录 | [已对齐] | `cwd=os.path.dirname(binary)`（L86） |
| 键码注入参数 | [需核实] | `input_map` 语义直传（joystick axis/btn、keyboard KEY_*，docstring）；**注入通道** [需核实]；明确**不用** `keymap_atari-2600.json`（MAME 语义遗留）作翻译层 |
| ROM/介质缺失提示 | [已对齐] | `EMULATOR_BINARY_MISSING`（L71）+ `STELLA_BIN` + `licenses/Stella.md` |
| 实测 | — | 176-A presmoke：`-help` 无输出、无参 rc=0xC0000135（**缺运行库 DLL**，目录无 SDL2.dll）→ 转用户补全，Stella 侧全部参数待其能启动后再验 |

## 四、need_verify 续清单（续 realrun_presmoke §③；186-B 轮更新）

**已核销（此前轮次）**：三台决策链「二进制就位 → 真实后端」实测（181-B）；三后端 `--check-binary` rc=0 路径打印；SIMH 退出命令 `quit` 与就绪横幅（176-A presmoke）；MAME `-version`/`-createconfig` 行为（176-A）。

**本轮（186-B）静态核销**：
1. MAME boot.lua 通道——路径生成与命令拼接：`mame_apple2.py` L101 运行时生成 `%TEMP%\diorama_boot_apple2.lua`、L106-107 以 `-autoboot_script <lua>` 传参 → **已核销（静态）**；lua 内容生效（抓帧）仍需介质实跑 → 续挂；
2. MAME natkeyboard 键码表——`gw/emulators/keys/keymap_apple2.json` 存在，`key_repeat`（REPT）/`key_reset`（RESET）已登记 `verify:true` 且自带 [需核实] 注记 → **已核销（表与登记存在）**；实际键码回显/组合行为 → 续挂。

**续挂 [需核实]（转交对象）**：
1. MAME：boot.lua 抓帧生效、REPT/RESET 键码回显、组合复位——转用户装 ROM 后按 m2a 断言核对（v3 §二 #1-4）；
2. SIMH：start.ini 命令名/语法、TTY 注入通道、快照 SAVE/LOAD 命令名——转 05 线预研/用户实跑核对；
3. Stella：**运行库 DLL 先补全（用户侧）**；无头/抓帧开关、帧 rgba8/音频 pcm16 直读 API、注入通道——转 05 线/用户核对。
   **绕行/替代方案（191-B 补）**：①用户补全运行库 DLL（如 SDL2.dll 与 stella.exe 同目录）后按本卡 §三 逐项验；②若用户共享盘已有完整版 stella 发行目录，可设 `STELLA_BIN` 指向其 stella.exe 后再验；③「无头抓帧」验证路径降级为需用户确认项——不能无介质凭空验，不得臆造「就绪」。

> 判定口径：只记实测与源码行；三后端骨架代码不做「貌似能跑」改动，核销一条、移除一条。

## 五、本轮预检结论（TASK-221-B 终版）

- need_verify 分布**终版定稿**：**核销 5 / 续挂 6**——MAME boot.lua 抓帧生效与键码回显（2 项）、
  SIMH start.ini 命令名 / TTY 注入 / SAVE·LOAD（3 项）、Stella 无头开关与直读 API（1 项，缺运行库
  DLL 保持续挂 + 191-B 绕行方案）；
- 第二批 SIMH 待核项合并口径：hp2100/nova/altair-8800 三台的 start.ini 命令名 / 横幅 / SAVE·LOAD
  （3×3 项）并入上述 SIMH 续挂组，同一转交对象（05 线预研 / 用户编译后实跑），不重复计数；
- 用户侧待办清单（终版，三件）：
  ① 放介质真跑三台（ROM/卡带自备，need_verify 打勾）；
  ② 补 Stella 运行库 DLL（或 STELLA_BIN 指向完整发行版）；
  ③ 编译第二批 SIMH 二进制（pdp8 已就位；hp2100/nova/altair8800 待用户编译入 third_party\simh\）；
- 真跑矩阵 dry-run 终检（221-B 实测）：三台真跑均「二进制就位 → 真实后端」（apple-ii/pdp8/atari-2600，
  rc=0）；第二批 SIMH 三台均「未就位 → EMULATOR_BINARY_MISSING + third_party 指引」（rc=0）——
  七台决策链口径一致，无异常分支；
- R2 断言口径不变：三台真跑 run_status ∈ {live, dry-run}；第二批槽位转正后同口径（现均 dry-run）。

## 六、第二批 SIMH presmoke 适配结论（TASK-206-A）

- 四台 check-binary 实测（realrun_smoke.py 矩阵段，全部 PASS）：
  simh-pdp8 **rc=0 就位**（third_party\simh\pdp8.exe）；simh-hp2100 / simh-nova /
  simh-altair-8800 均 **rc=2 缺失**，提示指向 `third_party\simh\<hp2100|nova|altair8800>`
  与 `SIMH_HP2100_BIN / SIMH_NOVA_BIN / SIMH_ALTAIR_BIN`；
- 三台新槽位决策链缺失态文案实测：`决策: 二进制未就位 → EMULATOR_BINARY_MISSING +
  doctor 指引: 把二进制放入 third_party/simh/<target> 或设环境变量 SIMH_*_BIN`（206-A
  已补 manifest binary_hint，提示路径与部署手册 §2 一致）；
- 二进制名 [需核实] 清单：hp2100 / nova / altair8800（Open SIMH 实际可执行文件名以
  用户编译产物为准）；altair 包 runtime 语义名 `simh-altair8800` 已由 slot_loader
  ALIASES 归一（建议 03 线后续统一命名）；
- 结论口径：四台均为「骨架已接、二进制待用户侧编译」，**未臆造就绪**。

## 七、第二批 SIMH 启动器参数核对卡 v2（TASK-211-A · hp2100 / nova / altair 三台）

三台后端与 simh_pdp8 母本逐字同构（201-A/B 转正），逐项状态一致；差异仅 machine/binary_env/binary_hint。
每项标 [已对齐（代码口径）]=源码可查证；[需核实]=无实测支撑，标出处不臆造。

| 项 | hp2100（simh_hp2100.py） | nova（simh_nova.py） | altair（simh_altair_8800.py） |
|---|---|---|---|
| 启动参数 | [已对齐（代码口径）] `cmd=[binary, <start.ini>]`（L87 同构行）；start.ini 内命令名/语法 [需核实] | 同左 | 同左 |
| 工作目录 | [已对齐（代码口径）] `cwd=os.path.dirname(binary)` | 同左 | 同左 |
| 键码/TTY 注入 | [已对齐（代码口径）] TTY 文本注入、无 keymap 三级回退；注入通道 [需核实] | 同左 | 同左 |
| ROM/介质缺失提示 | [已对齐] `EMULATOR_BINARY_MISSING` + `SIMH_HP2100_BIN` + `third_party/simh/hp2100` + licenses/SIMH.md | `SIMH_NOVA_BIN` + third_party/simh/nova | `SIMH_ALTAIR_BIN` + third_party/simh/altair8800 |
| 就绪横幅 | [需核实] `HP2100 simulator` | `NOVA simulator` | `ALTAIR simulator` |
| 快照 SAVE/LOAD | [需核实] 命令名（骨架仅落命令文件+时间戳） | 同左 | 同左 |
| presmoke 实测（206-A） | check-binary **rc=2 缺失**；决策链「未就位 → EMULATOR_BINARY_MISSING → third_party/simh/hp2100」 | rc=2；→ third_party/simh/nova | rc=2；→ third_party/simh/altair8800 |

need_verify 关联：三台新槽位待核项（start.ini 命令名 / 横幅 / TTY 注入通道 / SAVE·LOAD，
共 3×4 项）并入既有续挂清单同一转交口径（05 线预研 / 用户编译后实跑），不单列计数膨胀；
altair 包 runtime 语义名 `simh-altair8800` 已由 slot_loader ALIASES 归一（[需核实] 建议 03 线统一）。
