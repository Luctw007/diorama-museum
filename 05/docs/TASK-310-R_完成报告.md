# TASK-310-R 完成报告 · Pac-Man 街机框体完整产包

> 任务 310-R（05 线）· 完成日期：2026-11-25。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，产包轮次豁免。

## 一、交付物清单

`content/pac-man-arcade/` 完整产包（8 件低模 + 5 文件）：

| 文件 | 要点 |
|---|---|
| assemblies/ 8 件 gltf + MESHES.md | cabinet(120) / control_panel(104) / coin_door(104) / crt_display(104) / joystick(104) / button(104) / mainboard(104) / speaker(112)；识别件 coin_door（投币门）、joystick（摇杆） |
| meta.json | id=pac-man-arcade / era=1980 / category=arcade / manufacturer=Namco / 8 assemblies + 4 components（Z80/图形芯片/音源芯片/投币机构） |
| runtime.json | emulator=none / media_hint=none / output_sinks=crt_display+speaker / input_map 8 动作含投币 |
| annotations.json | 30 条（16 role + 12 flow + 2 anim） |
| encyclopedia.md | 2503 汉字（≥2500） |
| THIRD_PARTY.md | 三件套 + 街机 ROM 红线（FR-E3） |
| 目录回填 | G-AC-000005 status planned→done、device_id→pac-man-arcade |

## 二、验收日志与退出码

**1. 低模自证**（8 件，顶点 100-4000，纯色 0–1）：cabinet 120 / control_panel 104 / coin_door 104 / crt_display 104 / joystick 104 / button 104 / mainboard 104 / speaker 112，全部达标。

**2. 逐包 validate**（`validate.py content/pac-man-arcade`）：

```
总计 92 条：PASS 92，FAIL 0
RC=0
```

**3. 门禁全量复测**（`verify_all.py --daily --no-ref-hard`）：本轮产包统一复核 rc=0。

**4. 改动清单自证**：本任务新增 pac-man-arcade 8 件 gltf + 5 文件 + 目录 jsonl/md + 本报告。

## 三、与任务书的漂移

1. **role 文案「在框体」→「在整机」**（R-061 红线）：validate 初跑 FAIL 1（R-061 要求 role 文案含「在整机」），已批量替换 26 处「在框体」→「在整机」，复跑 92/92。
2. **annotations 30 条**（16 role + 12 flow + 2 anim）：满足 ≥30 下限。
3. 其余字段对齐 305-N 准备卡，无其它漂移。

## 四、红线自证

未下载 ROM/BIOS/二进制/贴图，街机 ROM 只清单级引用（FR-E3，emulator 保守 none、media_hint=none）；框体尺寸/参数无来源标 [需核实]；只改 05 目录，未动 01/02/03/04 线。
