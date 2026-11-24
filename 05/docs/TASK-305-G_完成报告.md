# TASK-305-G 完成报告 · Microsoft Xbox 完整产包

> 任务 305-G（05 线）· 完成日期：2026-11-25。
> 执行账号：05 游戏机线；只改 `D:\work\05\`，产包轮次豁免。

## 一、交付物清单

| 文件 | 要点 |
|---|---|
| `content/xbox/meta.json` | id=xbox / era=2001 / category=game-console / manufacturer=Microsoft / 8 assemblies + 4 components（Pentium III 级、NVIDIA 图形芯片、主内存、光盘电机） |
| `content/xbox/runtime.json` | emulator=none（保守）/ media_hint=cd_rom（DVD-ROM 无枚举降级）/ output_sinks=crt_display+speaker / input_map 8 动作 |
| `content/xbox/annotations/annotations.json` | 33 条（19 role + 12 flow + 2 anim），dvd_drive 托盘弹出、controller 手柄识别件 |
| `content/xbox/encyclopedia.md` | 2570 汉字（≥2500） |
| `content/xbox/THIRD_PARTY.md` | 三件套 + Xbox BIOS/ROM 红线 + DVD-ROM→cd_rom 代指声明 |
| 目录回填 | G-HC-000067「Xbox」status planned→done、device_id null→xbox |

assemblies 8 件 gltf 沿用 305-E，未新增/修改 gltf。

## 二、验收日志与退出码

**1. 门禁全量复测**（`verify_all.py --daily --no-ref-hard`，本机无 `py -3.7`，改用 python 3.13）：

```
===== 验收汇总（61 项） =====
结果：61/61 通过
RC=0
```

**2. 逐包 validate**（`validate.py content/xbox`）：

```
总计 92 条：PASS 92，FAIL 0
RC=0
```

**3. model_check**（`model_check.py content/xbox`）：32 条 MR 全 PASS，rc=0。

**4. verify_all pkg**（`verify_all.py --only pkg:xbox`）：

```
===== 验收汇总（1 项） =====
  pkg:xbox    PASS  FAIL 0
结果：1/1 通过
RC=0
```

**5. 反链自证**（`catalog_ref_check.py`）：

```
内容包 53 个，目录条目 1583 行
REF-01 悬空包引用：0 条
REF-02 反链缺失：0 个
REF-03 台账漂移：0 条
REF-04 关联包形态非法：0 条
FAIL 0
RC=0
```

## 三、与任务书的漂移

1. **annotations 33 条**（任务书写「16 role + 12 flow + 2 anim」即 30 条）：实际 role 拆了 19 条（多了 green_ring_role、tray_role、hard_disk_role 等细项），flow 12 条、anim 2 条，合计 33 条，满足 ≥30 下限。
2. **components 4 件**（pentium3/nvidia_gpu/ram/cd_motor）：按 40 号准备卡拆分建议，对齐 gamecube 体例。
3. **内置硬盘用 hard_drive 件表达**（不引入 storage 字段）：schema 无 storage 字段，已在 40 号准备卡显式说明。
4. **media_hint=cd_rom**：DVD-ROM 无枚举、取 cd_rom 代指，已标注。
5. 其余字段对齐 40 号准备卡与 gamecube 体例，无其它漂移。

## 四、红线自证

本任务未新增/修改 gltf（沿用 305-E）；未下载 ROM/BIOS/二进制/贴图，Xbox BIOS/ROM 只清单级引用（emulator 保守 none）；改动文件仅 meta.json、runtime.json、annotations.json、encyclopedia.md、THIRD_PARTY.md、目录 jsonl/md、本报告。
