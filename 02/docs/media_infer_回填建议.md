# 目录 → 媒体类目回填建议（自动生成，勿手改）

> 生成时间：2026-11-08 22:17:11　|　工具：`tools/index/media_infer.py`（TASK-62B）
> 共 1582 条目录推定；media_class 枚举与 v0.5 槽位契约 §3.3 对齐。

## 一、低置信度清单（confidence < 0.6，需人工复核，置顶）

- （无）

## 二、分中分类统计

| 大分类/中分类 | 条数 | media_class 分布 |
|---|---|---|
| 游戏机/街机 | 250 | cartridge×250 |
| 计算机/个人机 | 207 | disk×207 |
| 通讯与移动/手机 | 171 | firmware×171 |
| 游戏机/家用机 | 95 | cartridge×95 |
| 计算机/大型机 | 84 | tape×84 |
| 游戏机/掌机 | 76 | cartridge×76 |
| 办公与计算外设/键鼠/输入 | 75 | 无×75 |
| 通讯与移动/PDA | 69 | firmware×69 |
| 家电影音/音响 | 62 | cd×49、tape×13 |
| 办公与计算外设/存储外设 | 60 | disk×50、dvd×6、tape×4 |
| 计算机/服务器 | 55 | disk×55 |
| 计算机/工作站 | 54 | disk×54 |
| 计算机/小型机 | 48 | disk×48 |
| 通讯与移动/寻呼机 | 40 | firmware×40 |
| 家电影音/影碟播放 | 34 | cd×21、dvd×11、tape×2 |
| 办公与计算外设/打印机 | 33 | 无×33 |
| 计算机/超级计算机 | 28 | disk×28 |
| 家电影音/电视 | 28 | 无×28 |
| 通讯与移动/固定电话 | 26 | 无×26 |
| 家电影音/录像机 | 24 | tape×23、dvd×1 |
| 办公与计算外设/显示器 | 23 | 无×23 |
| 计算机/手持计算 | 15 | firmware×15 |
| 计算机/早期计算机 | 13 | tape×13 |
| 办公与计算外设/计算器 | 12 | 无×12 |

## 三、置信度分布

- 中(0.7~0.9)：1106 条
- 高(≥0.9)：427 条
- 低(<0.7)：49 条

## 四、全量建议表（截前 100 条）

| catalog_id | 名称 | media_class | 规则 | 置信度 |
|---|---|---|---|---|
| C-EC-000001 | ENIAC | tape | R13 | 0.80 |
| C-EC-000002 | EDVAC | tape | R13 | 0.80 |
| C-EC-000003 | EDSAC | tape | R13 | 0.80 |
| C-EC-000004 | Manchester Baby | tape | R13 | 0.80 |
| C-EC-000005 | Colossus | tape | R13 | 0.80 |
| C-EC-000006 | Z3 | tape | R13 | 0.80 |
| C-EC-000007 | Z4 | tape | R13 | 0.80 |
| C-EC-000008 | Harvard Mark I | tape | R13 | 0.80 |
| C-EC-000009 | ABC | tape | R13 | 0.80 |
| C-EC-000010 | IBM SSEC | tape | R13 | 0.80 |
| C-EC-000011 | Manchester Mark 1 | tape | R13 | 0.80 |
| C-EC-000012 | IAS Machine | tape | R13 | 0.80 |
| C-EC-000013 | Whirlwind | tape | R13 | 0.80 |
| C-MF-000001 | IBM 701 | tape | R12 | 0.80 |
| C-MF-000002 | IBM 650 | tape | R12 | 0.80 |
| C-MF-000003 | IBM 704 | tape | R12 | 0.80 |
| C-MF-000004 | IBM 709 | tape | R12 | 0.80 |
| C-MF-000005 | IBM 1401 | tape | R12 | 0.80 |
| C-MF-000006 | IBM 1620 | tape | R12 | 0.80 |
| C-MF-000007 | IBM 7090 | tape | R12 | 0.80 |
| C-MF-000008 | IBM 7094 | tape | R12 | 0.80 |
| C-MF-000009 | IBM 7030 Stretch | tape | R12 | 0.80 |
| C-MF-000010 | IBM 7070 | tape | R12 | 0.80 |
| C-MF-000011 | IBM 7080 | tape | R12 | 0.80 |
| C-MF-000012 | IBM 1410 | tape | R12 | 0.80 |
| C-MF-000013 | IBM 1440 | tape | R12 | 0.80 |
| C-MF-000014 | IBM 305 RAMAC | tape | R12 | 0.80 |
| C-MF-000015 | IBM System/360 Model 30 | tape | R12 | 0.80 |
| C-MF-000016 | IBM System/360 Model 40 | tape | R12 | 0.80 |
| C-MF-000017 | IBM System/360 Model 50 | tape | R12 | 0.80 |
| C-MF-000018 | IBM System/360 Model 65 | tape | R12 | 0.80 |
| C-MF-000019 | IBM System/360 Model 91 | tape | R12 | 0.80 |
| C-MF-000020 | IBM System/360 Model 20 | tape | R12 | 0.80 |
| C-MF-000021 | IBM System/360 Model 67 | tape | R12 | 0.80 |
| C-MF-000022 | IBM System/370 Model 145 | tape | R12 | 0.80 |
| C-MF-000023 | IBM System/370 Model 168 | tape | R12 | 0.80 |
| C-MF-000024 | IBM System/370 Model 115 | tape | R12 | 0.80 |
| C-MF-000025 | IBM 3033 | tape | R12 | 0.80 |
| C-MF-000026 | IBM 3031 | tape | R12 | 0.80 |
| C-MF-000027 | IBM 3081 | tape | R12 | 0.80 |
| C-MF-000028 | IBM 4341 | tape | R12 | 0.80 |
| C-MF-000029 | IBM 4381 | tape | R12 | 0.80 |
| C-MF-000030 | IBM 3090 | tape | R12 | 0.80 |
| C-MF-000031 | IBM System/390 | tape | R12 | 0.80 |
| C-MF-000032 | IBM 9020 | tape | R12 | 0.80 |
| C-MF-000033 | IBM zSeries z900 | tape | R12 | 0.80 |
| C-MF-000034 | Amdahl 470V/6 | tape | R12 | 0.80 |
| C-MF-000035 | Hitachi M-180 | tape | R12 | 0.80 |
| C-MF-000036 | Fujitsu FACOM M-190 | tape | R12 | 0.80 |
| C-MF-000037 | EC 1030 | tape | R12 | 0.80 |
| C-MF-000038 | EC 1045 | tape | R12 | 0.80 |
| C-MF-000039 | EC 1060 | tape | R12 | 0.80 |
| C-MF-000040 | CDC 1604 | tape | R12 | 0.80 |
| C-MF-000041 | CDC 160 | tape | R12 | 0.80 |
| C-MF-000042 | CDC 3600 | tape | R12 | 0.80 |
| C-MF-000043 | CDC 6600 | tape | R12 | 0.80 |
| C-MF-000044 | CDC 6400 | tape | R12 | 0.80 |
| C-MF-000045 | CDC 7600 | tape | R12 | 0.80 |
| C-MF-000046 | CDC CYBER 70 | tape | R12 | 0.80 |
| C-MF-000047 | CDC CYBER 170 | tape | R12 | 0.80 |
| C-MF-000048 | CDC 3400 | tape | R12 | 0.80 |
| C-MF-000049 | CDC 3300 | tape | R12 | 0.80 |
| C-MF-000050 | UNIVAC I | tape | R12 | 0.80 |
| C-MF-000051 | UNIVAC 1101 | tape | R12 | 0.80 |
| C-MF-000052 | UNIVAC 1103 | tape | R12 | 0.80 |
| C-MF-000053 | UNIVAC 1107 | tape | R12 | 0.80 |
| C-MF-000054 | UNIVAC 1108 | tape | R12 | 0.80 |
| C-MF-000055 | UNIVAC 494 | tape | R12 | 0.80 |
| C-MF-000056 | UNIVAC 1110 | tape | R12 | 0.80 |
| C-MF-000057 | UNIVAC 1100/80 | tape | R12 | 0.80 |
| C-MF-000058 | UNIVAC 90/70 | tape | R12 | 0.80 |
| C-MF-000059 | UNIVAC 90/60 | tape | R12 | 0.80 |
| C-MF-000060 | UNIVAC LARC | tape | R12 | 0.80 |
| C-MF-000061 | RCA 501 | tape | R12 | 0.80 |
| C-MF-000062 | RCA 301 | tape | R12 | 0.80 |
| C-MF-000063 | RCA Spectra 70 | tape | R12 | 0.80 |
| C-MF-000064 | Burroughs B5000 | tape | R12 | 0.80 |
| C-MF-000065 | Burroughs B5500 | tape | R12 | 0.80 |
| C-MF-000066 | Burroughs B2500 | tape | R12 | 0.80 |
| C-MF-000067 | Burroughs B3500 | tape | R12 | 0.80 |
| C-MF-000068 | Burroughs B6500 | tape | R12 | 0.80 |
| C-MF-000069 | Burroughs B6700 | tape | R12 | 0.80 |
| C-MF-000070 | Burroughs B1700 | tape | R12 | 0.80 |
| C-MF-000071 | Burroughs B7700 | tape | R12 | 0.80 |
| C-MF-000072 | Burroughs B7900 | tape | R12 | 0.80 |
| C-MF-000073 | GE-645 | tape | R12 | 0.80 |
| C-MF-000074 | GE-635 | tape | R12 | 0.80 |
| C-MF-000075 | GE-225 | tape | R12 | 0.80 |
| C-MF-000076 | Honeywell 200 | tape | R12 | 0.80 |
| C-MF-000077 | Honeywell 800 | tape | R12 | 0.80 |
| C-MF-000078 | Honeywell 6000 | tape | R12 | 0.80 |
| C-MF-000079 | NCR 304 | tape | R12 | 0.80 |
| C-MF-000080 | NCR 315 | tape | R12 | 0.80 |
| C-MF-000081 | ICL 1900 | tape | R12 | 0.80 |
| C-MF-000082 | ICL 2900 | tape | R12 | 0.80 |
| C-MF-000083 | ICL System 4 | tape | R12 | 0.80 |
| C-MF-000084 | Ferranti Atlas | tape | R12 | 0.80 |
| C-MC-000001 | PDP-1 | disk | R11 | 0.80 |
| C-MC-000002 | PDP-4 | disk | R11 | 0.80 |
| C-MC-000003 | PDP-5 | disk | R11 | 0.80 |
