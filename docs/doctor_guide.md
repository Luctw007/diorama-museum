# 模拟器体检向导使用说明（docs/doctor_guide.md）

> TASK-36A 交付。`scripts/emulator_doctor.py`：把"装二进制 → 真跑"压缩成一条可诊断的命令。

## 1. 三种用法

```powershell
python scripts/emulator_doctor.py                # 人类可读体检表
python scripts/emulator_doctor.py --json         # 机器可读（供 04 线回归引用）
python scripts/emulator_doctor.py --fix-check --log docs/doctor_log.txt
```

## 2. 三态语义表

| 状态 | 含义 | 你的动作 |
|---|---|---|
| OK | 该项就绪 | 无需动作 |
| MISSING | 二进制缺失（阻断真跑） | 按 `>>>` 指引安装并放到提示路径 |
| FAIL | 自检失败（如网关起不来） | 检查端口残留进程（指引已给出命令） |
| HINT | 提示项（如 ROM 位置、端口占用） | 知悉即可，不阻断 |

## 3. 与你人工三步的对应关系

| 人工步骤 | doctor 项 | 就绪后的下一步 |
|---|---|---|
| 下载 MAME，放 `third_party/mame/` | `mame_binary` OK | `--fix-check` 自动跑 m2a --mame 真实轨 + m0 冒烟 |
| 下载 SIMH，放 `third_party/simh/` | `simh_binary` OK | 同上（PDP-8 控制台验证） |
| （可选）自备 ROM 放 `third_party/roms/` | `rom_location_hint` | MAME apple2 启动到引导画面 |

## 4. 红线

- 本工具**永不下载**任何二进制/ROM：只检测位置并给出手动安装指引；
- 检测是只读的：唯一副作用是网关自检的临时进程（用完即止）与 fix-check 日志落盘。