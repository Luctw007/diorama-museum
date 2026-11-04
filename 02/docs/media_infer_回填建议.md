# 目录 → 媒体类目回填建议（自动生成，勿手改）

> 生成时间：2026-11-04 02:02:37　|　工具：`tools/index/media_infer.py`（TASK-62B）
> 共 1484 条目录推定；media_class 枚举与 v0.5 槽位契约 §3.3 对齐。

## 一、低置信度清单（confidence < 0.6，需人工复核，置顶）

- （无）

## 二、分中分类统计

| 大分类/中分类 | 条数 | media_class 分布 |
|---|---|---|
| 游戏机/街机 | 376 | cartridge×376 |
| 计算机/个人机 | 207 | disk×207 |
| 游戏机/家用机 | 186 | cartridge×186 |
| 游戏机/掌机 | 113 | cartridge×113 |
| 计算机/大型机 | 84 | tape×84 |
| 通讯与移动/手机 | 73 | firmware×73 |
| 计算机/服务器 | 55 | disk×55 |
| 计算机/工作站 | 54 | disk×54 |
| 计算机/小型机 | 48 | disk×48 |
| 通讯与移动/PDA | 36 | firmware×36 |
| 计算机/超级计算机 | 28 | disk×28 |
| 办公与计算外设/输入设备 | 22 | 无×22 |
| 办公与计算外设/磁盘驱动器 | 22 | disk×18、dvd×3、tape×1 |
| 家电影音/影音播放机 | 18 | cd×12、dvd×5、tape×1 |
| 通讯与移动/传呼机 | 17 | firmware×17 |
| 家电影音/电视 | 16 | 无×16 |
| 计算机/手持计算 | 15 | firmware×15 |
| 家电影音/随身听 | 15 | tape×15 |
| 家电影音/录像机 | 14 | tape×13、dvd×1 |
| 家电影音/音响 | 14 | cd×14 |
| 计算机/早期计算机 | 13 | tape×13 |
| 办公与计算外设/打印机 | 12 | 无×12 |
| 通讯与移动/无绳电话 | 10 | firmware×10 |
| 通讯与移动/卫星电话 | 10 | firmware×10 |
| 办公与计算外设/显示器 | 9 | 无×9 |
| 通讯与移动/车载电话 | 8 | firmware×8 |
| 办公与计算外设/调制解调器 | 5 | 无×5 |
| 办公与计算外设/扫描仪 | 4 | 无×4 |

## 三、置信度分布

- 中(0.7~0.9)：923 条
- 高(≥0.9)：547 条
- 低(<0.7)：14 条

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
