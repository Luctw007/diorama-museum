# TASK-91B 完成报告（01/docs/TASK-91B_完成报告.md）

> 01 线 · 2026-11-05 · 任务：v0.1 阻塞项处置包①（44 号 G-9 占位口播轨 + G-2 站位精调）。

## 1. 交付物

| 项 | 文件 | 结果 |
|---|---|---|
| 占位口播轨 ×2 | `01/godot/content/audio/demo/narr_hall_intro_placeholder.wav`、`narr_eniac_placeholder.wav` | 各 352,844 字节 / 8.0s / 22.05kHz 16bit 单声道 / 峰值 −18 dBFS；命名对齐 20 号 narr 系（占位语义，正式轨由 04 线配音流程替换） |
| 生成器 | `01/scripts/gen_placeholder_vo.py` | 纯 stdlib（wave+math+struct），可复跑 |
| 站位精调 | `01/godot/content/exhibit_dawn.json` | 四台按 16 号 v2 动线重排：eniac(-7,2)→edvac(-3.5,2)→edsac(0.5,3)→baby(4.5,1)；步距 3.5/4.0/4.0 m 对齐 16 号 §1 表 |
| 自检脚本 | `01/scripts/station_check.py` | S-1 厅界（±0.5 m 边距）/ S-2 两两间距 ≥3.4 m / S-3 动线顺序+scale 合法 |

## 2. 运行证据（原文）

```text
$ python 01/scripts/gen_placeholder_vo.py
已生成 …narr_hall_intro_placeholder.wav（8.0s, 22050Hz, 176400采样）
已生成 …narr_eniac_placeholder.wav（8.0s, 22050Hz, 176400采样）        → rc=0

$ python 01/scripts/station_check.py
站位自检：4 台 / 厅 20m×12m / 最小步距 3.4m
  全部通过（S-1 厅界/S-2 间距/S-3 动线顺序）                          → rc=0
```

两条 WAV 落盘 352,844 字节（可播放，节拍哔每秒 1 次便于互斥时序观察）。

## 3. 回填与说明

- G-9/G-2 已处置；44 号对应两行的状态由 04 线下轮确认（本任务未改 04 文件）；
- 音频落点说明：04 线 20 号规格未定 narr 物理目录 → 暂落 `01/godot/content/audio/demo/`
  （01 线引擎目录）；正式轨命名/目录以 04 线资产规格为准时再迁移；
- 顺带修复 monorepo 重组引入的三个跨仓路径回归（pkg_registry/catalog_ingest/m1b_check
  的 WORK_ROOT 上溯推导失效 → 锚定 `D:\work`）——这是本轮门禁一度 4/6 的直接原因，
  修复后 31/31（catalog_ref 因 03 线 vic20 在制反链按 --no-ref-hard 降级）。