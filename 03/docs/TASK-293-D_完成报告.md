# TASK-293-D 完成报告

> 03 线 TASK-293-D「第四批候选产包口径卡预研·卷四（Manchester Mark 1 + IBM 701）」完成报告。执行账号：03 内容线。只改 `D:\work\03\` 目录，纯文档口径卡，不产包、不改 jsonl、不 allocate id。

## 一、交付物清单

| 路径 | 状态 | 说明 |
|---|---|---|
| `docs/research/hall-mainframe/20_ManchesterMark1产包口径卡.md` | 新增 | 3944 字节，六节齐备 |
| `docs/research/hall-mainframe/21_IBM701产包口径卡.md` | 新增 | 3814 字节，六节齐备 |
| `docs/TASK-293-D_完成报告.md` | 新增 | 本报告 |

Manchester Mark 1 按黎明厅口径（category=early-computer，对齐 Whirlwind 先例）；IBM 701 按大型机厅口径（category=mainframe）。两张均 emulator=`none`（教学模拟器候选/无候选），标注第四批候选性质。

## 二、验收日志与退出码

### 1. 门禁只读复测
```
py -3.7 D:\work\01\repo\01\scripts\verify_all.py --daily --cache
...（55 项逐项 PASS）...
结果：55/55 通过
EXIT_CODE=0
```

### 2. 口径卡自证
```
20_ManchesterMark1 3944 字节（>2500 ✔）六节命中；需核实 2 类（尺寸/候选）
21_IBM701 3814 字节（>2500 ✔）六节命中；需核实 2 类（尺寸/候选）
```

### 3. 改动清单自证
本任务仅新增 3 份 md（两张口径卡 + 完成报告）；未碰 jsonl、未产包、未 allocate、未改 01/02/04/05 线。

## 三、与任务书的漂移

1. **category 口径校正（关键）**：任务书要求「category 按研究卡口径——黎明厅 early-computer 或大型机厅 mainframe，以研究卡为准」。实际：Manchester Mark 1 研究卡 17 号明确「计算机黎明厅，目录占位 C-EC」，故 `early-computer`；IBM 701 研究卡 18 号明确「大型机，目录占位 C-MF」，故 `mainframe`。两厅分列，均已按研究卡口径落地。
2. **Manchester Mark 1 manufacturer**：研究卡写「研制方 曼彻斯特大学」，本卡取 `University of Manchester`（英文全称，对齐 meta.json 惯例）。
3. 其余路径、红线、边界均与任务书一致，无其他漂移。

## 四、红线自查

零联网、零下载、零二进制；系统软件红线只清单级引用；史实以研究卡为准；第四批候选性质如实标注；只改 03 目录。
