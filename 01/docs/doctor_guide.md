# 模拟器体检向导使用说明（docs/doctor_guide.md · 终版）

> TASK-36A 交付；TASK-171-A 收口终版。`scripts/emulator_doctor.py`：把
> 「装二进制 → 真跑」压缩成一条可诊断的命令，并给出三台真跑部署就绪判定。

## 1. 用法（四种）

```powershell
python scripts/emulator_doctor.py                            # 人类可读体检表 + 部署就绪判定
python scripts/emulator_doctor.py --json                     # 机器可读（含 deploy_readiness 键）
python scripts/emulator_doctor.py --fix-check --log docs\doctor_log.txt
python scripts/emulator_doctor.py --deploy-report docs\deploy_report.json  # 落盘部署签字（恒 rc=0）
```

## 2. 三态语义表

| 状态 | 含义 | 你的动作 |
|---|---|---|
| OK | 该项就绪 | 无需动作 |
| MISSING | 二进制缺失（阻断真跑） | 按 `>>>` 指引安装并放到提示路径（唯一口径见 deploy 手册 §2） |
| FAIL | 自检失败（如网关起不来） | 检查端口残留进程（指引已给出命令） |
| HINT | 提示项（如 ROM 位置、介质目录数） | 知悉即可，不阻断 |

## 3. 体检项与人工三步对应（三台真跑）

| 人工步骤 | doctor 项 | 就绪后的下一步 |
|---|---|---|
| 自备 MAME，放 `third_party\mame\` 或设 `MAME_BIN` | `mame_binary` OK | `--fix-check` 自动跑 m2a --mame 真实轨 + m0 冒烟 |
| 自备 SIMH，放 `third_party\simh\` 或设 `SIMH_PDP8_BIN` | `simh_binary` OK | 同上（PDP-8 控制台验证） |
| 自备 Stella，放 `third_party\stella\` 或设 `STELLA_BIN` | `stella_binary` OK | 同上（2600 卡带验证） |
| 自备介质放对应目录（deploy 手册 §3） | `slot_media_dirs`（HINT 计数） | `launch_device --device <id>` 直起 |
| 槽位扫描区（slots\emulators\*） | `slot:<id>` 行（OK/MISSING） | 无「后端模块预留」即后端已接；二进制按 hint 放置 |

## 4. 部署就绪判定（TASK-171-A）

- 每次输出末尾一行：`部署就绪判定：三台真跑二进制 齐/缺 N（缺: …）· 介质目录已建 M 个`；
- `--json` 的 `deploy_readiness` 键：`{ok, missing, total, media_dirs, ready}`，
  `ready = 三台二进制（mame/simh/stella）全 OK`；
- `--deploy-report <path>` 落盘签字 JSON：`{checked_at, binaries{mame/simh/stella:
  status+detail}, media_dirs, media_count, ready}`；本参数恒 rc=0（只有 `--fix-check`
  失败才非 0），可央求用户装完回传作为部署证据。
- 完整自装流程见 `SLOT_DEPLOY-Guide-v0.1.md`。

## 5. 红线

- 本工具**永不代置、永不代取**任何二进制/ROM：只检测位置并给出手动自备指引；
- 检测是只读的：唯一副作用是网关自检的临时进程（用完即止）、fix-check 日志与
  deploy 签字 JSON 落盘。