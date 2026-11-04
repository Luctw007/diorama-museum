# media_class 回填工作表（2026-11-05）

> 生成工具：`tools/index/media_infer.py`（TASK-62B）规则表　|　任务：TASK-92B（02 线 2/2 · 轻量）
> **只出表、不改他线文件**（红线）。本表是把 media_infer 的"建议"转成 03/05 线可照抄执行的
> 行级清单；执行由 03/05 线各自在其目录文件上进行。

## 〇、总览与执行约定

**执行范围**：03/05 两仓现有 6 个目录 jsonl 中，取 4 个 **v2 权威文件**为回填执行目标；
2 个 v1 文件（`家电影音与外设大类_目录_v1.jsonl` 151 条、`游戏机与手持大类_目录_v1.jsonl` 274 条）
为 legacy 旧版，按「全量文件替代制」应删除，**不纳入回填**（见 §四）。

**执行约定**：
1. 03 线只改 `03/repo/docs/catalog/` 下自己的两个 v2 文件；05 线只改 `05/repo/docs/catalog/` 下自己的两个 v2 文件，**不得互改**；
2. 每条回填 = 在该目录条目的 `runtime.slot.media_class`（或目录行 `media_class` 字段）写入建议值；
3. 高置信度节可直接照抄执行；低置信度节须该线逐条复核后再写；
4. 执行完在对应行打勾（勾选列随线自建，本表不落勾）；
5. 回填后重跑 `catalog_check` 与 `catalog_ref_check`，确认无新增 FAIL。

## 一、计数小节

- **media_class 建议总数（v2 执行目标）**：1562 条（高置信度 1270 条 / 低置信度 292 条）。
- **media_class 分布**：disk×442、cartridge×401、firmware×295、无×197、tape×139、cd×70、dvd×18。
- **CC-08 违规数（device_id 未回填）**：当前 **0**（复跑原文见下）；回填前 18 条（86-B 自测暴露，03 线目录）→ 预期后 0。

```
== 目录校验（文件 4 个，条目 1562 行，唯一 id 1562，FAIL 0，WARN 0）==
  CC-08  FAIL 0 / PASS 24
```

> 说明：CC-08 是 device_id 存在性校验（package/wip/done 必须带真实 device_id），与 media_class 回填是两条独立
> 回填项；此处一并记录，供 03/05 线"回填前 18 → 预期 0"对照。

## 二、高置信度（≥0.8，可直接照抄执行）

| 文件 | 条目 id | 机型名 | 建议 media_class | 置信度 | 执行线 |
|---|---|---|---|---|---|
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000001 | VCD 播放机 | cd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000002 | DVD 播放机 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000006 | DVD 录像一体机 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000007 | 便携式 DVD 播放机 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000010 | VHS/DVD 一体机 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000018 | VCD 便携机 | cd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000019 | DVD 高清机 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000022 | 录像机 DVD 一体 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000028 | DVD 刻录机 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000029 | VCD 影碟（介质） | cd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000030 | DVD 影碟（介质） | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000007 | DVD 光驱 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000019 | DVD-R 光盘 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000031 | DVD-RW 光驱 | dvd | 0.95 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000003 | 蓝光播放机 | dvd | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000020 | 蓝光 3D 机 | dvd | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000031 | 蓝光影碟（介质） | dvd | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000001 | VHS 录像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000002 | Betamax 录像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000003 | VHS-C 摄像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000004 | 8mm 摄像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000005 | Hi8 摄像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000006 | MiniDV 摄像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000007 | 硬盘摄像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000008 | 蓝光录像机 | dvd | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000009 | 幻灯机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000010 | 8mm 放映机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000011 | 16mm 放映机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000012 | 随身录像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000013 | 录像带倒带机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000014 | S-VHS 录像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000015 | D-VHS 录像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000016 | Betamovie 摄像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000017 | VHS-C 一体机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000018 | Digital8 摄像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000019 | DV 摄像机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000020 | VHS 录放一体 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000021 | 幻灯机（自动） | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000022 | 8mm 摄影机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000023 | 16mm 摄影机 | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VR-000024 | 录像带（VHS 介质） | tape | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000002 | 5.25 英寸软驱 | disk | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000003 | 3.5 英寸软驱 | disk | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000020 | 蓝光光盘 | dvd | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000023 | 5.25 软驱（半高） | disk | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000024 | 3.5 软驱（1.44M） | disk | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000032 | 蓝光光驱 | dvd | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000045 | 软驱（外置 USB） | disk | 0.90 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000058 | 光驱（蓝光刻录） | dvd | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000001 | Magnavox Odyssey | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000002 | Pong（家用专用机） | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000003 | Coleco Telstar | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000004 | Fairchild Channel F | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000005 | RCA Studio II | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000006 | Atari 2600 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000007 | Bally Astrocade | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000008 | Interton VC 4000 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000009 | Magnavox Odyssey² | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000010 | APF Imagination Machine | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000011 | Intellivision | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000012 | Epoch Cassette Vision | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000013 | ColecoVision | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000014 | Atari 5200 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000015 | Vectrex | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000016 | Emerson Arcadia 2001 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000017 | Sord M5 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000018 | Tomy Tutor | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000019 | Bandai Super Vision 8000 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000020 | Coleco Gemini | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000021 | Casio PV-1000 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000022 | Nichibutsu My Vision | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000023 | Gakken TV Boy | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000024 | Atari 2800 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000025 | Color TV-Game 6 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000026 | Color TV-Game 15 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000027 | Famicom | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000028 | SG-1000 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000029 | Sega SG-1000 II | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000030 | Epoch Super Cassette Vision | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000031 | Sega Master System | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000032 | Atari 7800 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000033 | Famicom Disk System | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000034 | Atari XEGS | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000035 | PC Engine | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000036 | PC Engine CD-ROM² | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000037 | Sega Mega Drive | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000038 | SuperGrafx | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000039 | Super Famicom | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000040 | Neo Geo AES | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000041 | Amstrad GX4000 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000042 | Commodore 64 Games System | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000043 | Sega Master System II | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000044 | Sega Mega-CD | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000045 | Philips CD-i | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000046 | Commodore CDTV | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000047 | FM Towns Marty | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000048 | Sega Pico | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000049 | 3DO Interactive Multiplayer | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000050 | Atari Jaguar | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000051 | Amiga CD32 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000052 | Pioneer LaserActive | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000053 | Family Computer AV | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000054 | Sega 32X | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000055 | Sega Saturn | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000056 | PlayStation | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000057 | Neo Geo CD | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000058 | PC-FX | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000059 | Bandai Playdia | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000060 | Casio Loopy | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000061 | Virtual Boy | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000062 | Nintendo 64 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000063 | Apple Pippin | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000064 | Sega Dreamcast | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000065 | PlayStation 2 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000066 | GameCube | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000067 | Xbox | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000068 | Panasonic Q | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000069 | PSX | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000070 | PlayStation 2 Slim | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000071 | VTech V.Smile | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000072 | Atari Flashback | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000073 | Xbox 360 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000074 | Wii | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000075 | PlayStation 3 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000076 | HyperScan | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000077 | Xbox 360 S | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000078 | Wii U | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000079 | Wii Mini | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000080 | Neo Geo X | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000081 | PlayStation 4 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000082 | Xbox One | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000083 | NES Classic Edition | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000084 | Nintendo Switch | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000085 | SNES Classic Edition | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000086 | PlayStation Classic | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000087 | Sega Genesis Mini | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000088 | PlayStation 5 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000089 | Xbox Series X | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000090 | Xbox Series S | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000091 | Nintendo Switch OLED | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000092 | Sega TeraDrive | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000093 | Atari 2600 Jr. | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000094 | SC-3000 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HC-000095 | Sega Master System（游戏电脑版） | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000001 | Game & Watch Ball | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000002 | Game & Watch Donkey Kong | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000003 | Game & Watch Fire | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000004 | Game & Watch Octopus | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000005 | Game & Watch Oil Panic | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000006 | Game & Watch Mario Bros | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000007 | Game Boy | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000008 | Atari Lynx | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000009 | Game Gear | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000010 | PC Engine GT | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000011 | Atari Lynx II | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000012 | Watara Supervision | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000013 | Sega Game Gear（Kids Gear） | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000014 | Tiger R-Zone | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000015 | Sega Nomad | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000016 | Game Boy Pocket | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000017 | Tamagotchi | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000018 | Digimon | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000019 | Game.com | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000020 | Game Boy Light | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000021 | Game Boy Color | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000022 | Neo Geo Pocket | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000023 | Neo Geo Pocket Color | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000024 | WonderSwan | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000025 | WonderSwan Color | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000026 | Cybiko | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000027 | Game Boy Advance | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000028 | GP32 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000029 | Pokémon Mini | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000030 | SwanCrystal | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000031 | Game Boy Advance SP | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000032 | N-Gage | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000033 | Nintendo DS | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000034 | PlayStation Portable | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000035 | GP2X | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000036 | Game Boy Micro | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000037 | Game Boy Advance SP（AGS-101） | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000038 | Nintendo DS Lite | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000039 | PSP-2000 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000040 | Nintendo DSi | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000041 | PSP-3000 | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000042 | Nintendo DS XL | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000043 | PSP Go | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000044 | Pandora | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000045 | Nintendo 3DS | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000046 | PlayStation Vita | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000047 | Nintendo 3DS XL | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000048 | Nintendo 2DS | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000049 | PS Vita Slim | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000050 | New Nintendo 3DS | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000051 | New Nintendo 3DS XL | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000052 | Game Boy Color（透明紫） | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000053 | Game & Watch Multi Screen | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000054 | Game & Watch Donkey Kong Jr. | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000055 | Game & Watch Manhole | cartridge | 0.90 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-HH-000056 | Game & Watch Mickey Mouse | cartridge | 0.90 | 05 |
| 计算机大类_目录_v2.jsonl | C-PC-000001 | Apple I | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000002 | Apple II | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000003 | Apple II Plus | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000004 | Apple IIc | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000005 | Apple III | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000006 | Apple Lisa | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000007 | Macintosh 128K | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000008 | Macintosh Plus | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000009 | Macintosh SE | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000010 | Macintosh II | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000011 | Macintosh Classic | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000012 | Macintosh LC | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000013 | PowerBook 100 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000014 | Macintosh Portable | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000015 | Commodore PET 2001 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000016 | Commodore VIC-20 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000017 | Commodore 64 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000018 | Commodore 128 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000019 | Commodore 16 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000020 | Commodore Plus/4 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000021 | Commodore Amiga 1000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000022 | Commodore Amiga 500 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000023 | Commodore Amiga 2000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000024 | Commodore Amiga 3000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000025 | Commodore Amiga 600 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000026 | Atari 400 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000027 | Atari 800 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000028 | Atari 600XL | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000029 | Atari 800XL | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000030 | Atari ST | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000031 | Atari 1040ST | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000032 | Atari Falcon | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000033 | TRS-80 Model I | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000034 | TRS-80 Model III | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000035 | TRS-80 Model 4 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000036 | TRS-80 Color Computer | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000037 | TRS-80 Model II | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000038 | TRS-80 Model 100 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000039 | Tandy 1000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000040 | Sinclair ZX80 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000041 | Sinclair ZX81 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000042 | ZX Spectrum | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000043 | Sinclair QL | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000044 | Acorn Atom | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000045 | BBC Micro | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000046 | Acorn Electron | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000047 | Acorn Archimedes | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000048 | Acorn Risc PC | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000049 | Acorn BBC Master | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000050 | IBM PC 5150 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000051 | IBM PC XT 5160 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000052 | IBM PC AT 5170 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000053 | IBM PCjr | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000054 | IBM PS/2 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000055 | Compaq Portable | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000056 | Compaq Deskpro 386 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000057 | Compaq Portable II | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000058 | Dell 210 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000059 | Amstrad CPC 464 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000060 | Amstrad CPC 6128 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000061 | Dragon 32 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000062 | Oric-1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000063 | TI-99/4A | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000064 | Sharp MZ-80K | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000065 | Sharp MZ-700 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000066 | Sharp MZ-800 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000067 | Sharp MZ-80B | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000068 | Sharp MZ-2000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000069 | Sharp MZ-2500 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000070 | Sharp X1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000071 | Sharp X1 turbo | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000072 | Sharp X1 turbo Z | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000073 | Sharp X68000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000074 | Sharp X68000 Expert | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000075 | Sharp X68000 XVI | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000076 | Sharp X68030 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000077 | Sharp PC-6000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000078 | Sharp PC-7000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000079 | NEC PC-8001 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000080 | NEC PC-6001 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000081 | NEC PC-8801 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000082 | NEC PC-8801mkII | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000083 | NEC PC-8801FA | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000084 | NEC PC-9801 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000085 | NEC PC-9801VM | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000086 | NEC PC-9801VX | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000087 | NEC PC-9801RA | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000088 | NEC PC-6601 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000089 | NEC PC-100 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000090 | NEC PC-9821 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000091 | Fujitsu FM-8 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000092 | Fujitsu FM-7 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000093 | Fujitsu FM-77 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000094 | Fujitsu FM-77AV | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000095 | Fujitsu FM-16β | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000096 | Fujitsu FM Towns | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000097 | Fujitsu FM-11 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000098 | MSX | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000099 | Sony HB-75 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000100 | Sony HB-101 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000101 | Toshiba HX-10 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000102 | Hitachi MB-H1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000103 | Sanyo MPC-100 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000104 | Panasonic CF-2000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000105 | Yashica YC-64 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000106 | Canon V-20 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000107 | Toshiba Pasopia | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000108 | Toshiba Pasopia 5 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000109 | Sony SMC-70 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000110 | Hitachi S1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000111 | Sord M23 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000112 | Seiko 9500 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000113 | Mitsubishi MULTI8 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000114 | Casio FP-1000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000115 | Osborne 1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000116 | Kaypro II | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000117 | GRiD Compass 1101 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000118 | Epson HX-20 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000119 | Toshiba T1100 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000120 | Toshiba T1000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000121 | Compaq SLT/286 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000122 | Altair 8800 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000123 | Altair 8800b | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000124 | IMSAI 8080 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000125 | Processor Technology Sol-20 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000126 | NorthStar Horizon | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000127 | Cromemco Z-1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000128 | SWTPC 6800 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000129 | Ohio Scientific Challenger | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000130 | 长城 0520 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000131 | 浪潮 0520 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000132 | 联想汉卡 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000133 | 四通打字机 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000134 | 紫金-II | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000135 | Agat | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000136 | Pravetz 82 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000137 | Pravetz 8M | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000138 | Homelab 2 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000139 | ZX Spectrum 128K | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000140 | ZX Spectrum +2 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000141 | Dragon 64 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000142 | Jupiter Ace | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000143 | Memotech MTX512 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000144 | Oric Atmos | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000145 | Grundy NewBrain | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000146 | Camputers Lynx | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000147 | NEC PC-8801mkII SR | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000148 | NEC PC-9801UV | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000149 | NEC PC-9801BX | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000150 | NEC PC-9801DA | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000151 | NEC PC-9821Ce | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000152 | Sharp X68000 ACE | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000153 | Sharp X68000 Pro | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000154 | Fujitsu FM Towns II | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000155 | Fujitsu FM-7 II | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000156 | Sharp MZ-1200 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000157 | Sony MSX2 HB-F1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000158 | Panasonic MSX2 FS-A1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000159 | Toshiba Pasopia 7 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000160 | NEC PC-8201 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000161 | Sharp PC-1500 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000162 | Casio FP-1100 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000163 | Sord M5 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000164 | Hitachi MB-6890 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000165 | Epson QX-10 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000166 | ES-1840 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000167 | Agat-7 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000168 | Iskra 1030 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000169 | Pravetz 8A | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000170 | Pravetz 16 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000171 | Videoton TVC | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000172 | Robotron KC 85 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000173 | Robotron KC 87 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000174 | Didaktik Gama | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000175 | Elwro 800 Junior | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000176 | 长城 0520CH | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000177 | 长城 286 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000178 | 浪潮 0530 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000179 | 联想 1+1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000180 | 四通 MS-2403 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000181 | 中华学习机 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000182 | 长江 0520 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000183 | MITS Altair 680 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000184 | Sphere 1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000185 | Poly-88 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000186 | Ohio Scientific Superboard II | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000187 | Exidy Sorcerer | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000188 | Zenith Z-89 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000189 | IBM PS/2 Model 30 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000190 | IBM PS/1 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000191 | Compaq Deskpro | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000192 | Compaq Portable III | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000193 | Compaq LTE | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000194 | Gateway 2000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000195 | Packard Bell | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000196 | Dell 486 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000197 | AST Bravo | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000198 | Acer 1000 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000199 | Zenith Data Systems | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000200 | Leading Edge Model D | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000201 | Epson Equity | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000202 | IBM PC Convertible | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000203 | Toshiba T3200 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000204 | Apple IIGS | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000205 | Atari XEGS | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000206 | Amstrad PCW 8256 | disk | 0.90 | 03 |
| 计算机大类_目录_v2.jsonl | C-PC-000207 | Sharp PC-8801 | disk | 0.90 | 03 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000053 | 磁带录音座（三磁头） | tape | 0.85 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000014 | 磁带录音机 | tape | 0.85 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000009 | 磁带驱动器 | tape | 0.85 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000033 | 磁带机（DLT） | tape | 0.85 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000034 | 磁带机（LTO） | tape | 0.85 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000052 | 磁带机（DAT） | tape | 0.85 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000001 | Walkman 磁带机 | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000002 | CD Walkman | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000003 | MD Walkman | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000027 | Walkman II | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000028 | Walkman Professional | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000029 | Walkman Sports | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000030 | Walkman 数字 | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000035 | 磁带随身听（国产） | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000047 | CD 随身听（运动） | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000049 | 磁带随身听（自动反转） | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000056 | MD 随身听（录放） | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000057 | Walkman（卡带收藏版） | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000021 | CD 随身听 | tape | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000001 | 软盘驱动器 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000004 | 硬盘驱动器 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000005 | SCSI 硬盘 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000006 | 光盘驱动器 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000008 | 刻录机 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000010 | Zip 驱动器 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000011 | 固态硬盘 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000012 | USB 闪存盘 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000013 | 磁光驱动器 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000014 | 光驱（外置） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000015 | 网络硬盘 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000016 | 软盘（5.25 英寸） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000017 | 软盘（3.5 英寸） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000018 | CD-R 光盘 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000021 | 内存卡 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000022 | UPS 不间断电源 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000025 | 硬盘（10MB） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000026 | 硬盘（IDE） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000027 | 硬盘（SATA） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000028 | SSD（SATA） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000029 | SSD（NVMe） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000030 | CD-ROM 光驱（倍速） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000035 | MO 磁光驱 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000036 | Zip 驱动器（100MB） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000037 | Jaz 驱动器 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000038 | USB 闪存盘（1GB） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000039 | 内存卡（SD） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000040 | 内存卡（CF） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000041 | NAS（家用） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000042 | 外置硬盘 | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000043 | UPS（在线式） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000044 | UPS（后备式） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000046 | 光驱（吸入式） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000047 | 硬盘（外置 USB 2.0） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000048 | 移动硬盘（2.5 寸） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000049 | U盘（金属防水） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000050 | UPS（在线双变换） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000051 | 光驱（刻录 CD-RW） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000053 | 软盘驱动器（8 寸） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000054 | 硬盘（MFM 接口） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000055 | 内存条（SIMM） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000056 | 内存条（DIMM） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000057 | 读卡器（多合一） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000059 | 硬盘（监控级） | disk | 0.80 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-ST-000060 | U盘（加密） | disk | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000001 | Pong（街机） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000002 | Space Invaders | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000003 | Galaxian | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000004 | Asteroids | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000005 | Pac-Man | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000006 | Centipede | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000007 | Missile Command | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000008 | Defender | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000009 | Donkey Kong | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000010 | Frogger | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000011 | Tempest | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000012 | Galaga | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000013 | Joust | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000014 | Robotron: 2084 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000015 | Dig Dug | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000016 | Ms. Pac-Man | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000017 | Q*bert | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000018 | BurgerTime | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000019 | Zaxxon | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000020 | Donkey Kong Jr. | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000021 | Popeye | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000022 | Dragon's Lair | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000023 | Mario Bros. | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000024 | Elevator Action | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000025 | Track & Field | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000026 | Xevious | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000027 | 1942 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000028 | Punch-Out!! | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000029 | Space Ace | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000030 | Gauntlet | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000031 | Gradius | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000032 | Space Harrier | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000033 | TwinBee | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000034 | Ghosts 'n Goblins | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000035 | Out Run | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000036 | Bubble Bobble | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000037 | Arkanoid | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000038 | Salamander | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000039 | Wonder Boy | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000040 | After Burner | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000041 | Double Dragon | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000042 | R-Type | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000043 | Shinobi | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000044 | 1943: The Battle of Midway | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000045 | Altered Beast | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000046 | Ghouls 'n Ghosts | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000047 | Golden Axe | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000048 | Galaxian3 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000049 | Street Fighter II | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000050 | Fatal Fury | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000051 | Mortal Kombat | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000052 | Street Fighter II Turbo | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000053 | Virtua Racing | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000054 | Virtua Fighter | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000055 | Samurai Shodown | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000056 | Super Street Fighter II | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000057 | Mortal Kombat II | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000058 | Ridge Racer | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000059 | Sonic the Hedgehog（街机） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000060 | Daytona USA | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000061 | Tekken | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000062 | The King of Fighters '94 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000063 | Puzzle Bobble | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000064 | Street Fighter Alpha | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000065 | Time Crisis | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000066 | Cyber Troopers Virtual-On | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000067 | Metal Slug | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000068 | House of the Dead | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000069 | Beatmania | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000070 | Dance Dance Revolution | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000071 | Guitar Freaks | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000072 | Pump It Up | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000073 | Initial D Arcade Stage | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000074 | F-Zero AX | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000075 | Mario Kart Arcade GP | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000076 | Neo Geo MVS | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000077 | Capcom CPS-1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000078 | Capcom CPS-2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000079 | Capcom CPS-3 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000080 | Sega System 16 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000081 | Sega System 18 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000082 | Sega System 24 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000083 | Sega System 32 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000084 | Sega Model 1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000085 | Sega Model 2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000086 | Sega Model 3 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000087 | Sega Naomi | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000088 | Sega Naomi 2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000089 | Sega Atomiswave | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000090 | Sega System 1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000091 | Sega System 2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000092 | Sega System 14 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000093 | Sega System C | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000094 | Namco System 1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000095 | Namco System 2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000096 | Namco System 21 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000097 | Namco System 86 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000098 | Namco System 11 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000099 | Namco System 12 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000100 | Namco System 22 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000101 | Namco System 23 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000102 | Namco NA-1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000103 | Namco NB-1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000104 | Taito F3 System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000105 | Taito Z System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000106 | Taito B System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000107 | Taito Type X | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000108 | Midway Y Unit | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000109 | Midway T Unit | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000110 | Irem M72 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000111 | Irem M92 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000112 | Konami GX | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000113 | Konami System 573 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000114 | Capcom ZN-1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000115 | Capcom ZN-2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000116 | Capcom CPS Changer | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000117 | SNK Neo Geo 64 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000118 | Cave CV1000 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000119 | PGM | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000120 | Vs. System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000121 | PlayChoice-10 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000122 | Super System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000123 | Toaplan V1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000124 | Raizing CP System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000125 | Psikyo SH-2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000126 | Namco System 246 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000127 | System 256 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000128 | Triforce | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000129 | Sega Lindbergh | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000130 | Taito Type X2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000131 | Cave CV1000B | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000132 | Seibu SPI System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000133 | Kaneko Super Nova | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000134 | Jaleco Mega System 32 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000135 | Data East MEC-M1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000136 | Seta Aleck64 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000137 | Atomiswave 强化 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000138 | Cave PGM2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000139 | Konami e-Amusement | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000140 | Sega Chihiro | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000141 | Neo Geo MVS MV-1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000142 | Neo Geo MVS MV-4 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000143 | Neo Geo Pocket Color 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000144 | Capcom CPS-1.5 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000145 | Capcom Mitchell | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000146 | Sega System E | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000147 | Sega System 16B | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000148 | Sega Mega-Tech | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000149 | Sega Mega-Play | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000150 | Sega Titan Video | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000151 | Sega Hikaru | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000152 | Sega Aurora | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000153 | Namco System FL | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000154 | Namco System 10 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000155 | Namco System 147 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000156 | Namco System 357 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000157 | Taito F2 System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000158 | Taito H System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000159 | Taito L System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000160 | Taito FX-1A System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000161 | Taito G-NET | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000162 | Konami Nemesis | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000163 | Konami Twin 16 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000164 | Konami System GX | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000165 | Konami Viper | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000166 | Konami Bemani PC | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000167 | Konami FireBeat | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000168 | Irem M62 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000169 | Irem M82 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000170 | Irem M107 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000171 | Data East DECO Cassette | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000172 | Data East MEC-M1（复） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000173 | Technos System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000174 | Jaleco Mega System 1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000175 | Seibu SPI | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000176 | Toaplan Version 2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000177 | Raizing Battle Garegga 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000178 | Psikyo SH-1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000179 | Cave 68000 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000180 | Kaneko AX System | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000181 | Nichibutsu 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000182 | UPL 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000183 | Atari System 1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000184 | Atari System 2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000185 | Atari G1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000186 | Atari GT | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000187 | Midway Wolf Unit | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000188 | Midway Seattle | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000189 | Midway Zeus | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000190 | Williams 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000191 | Cinematronics 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000192 | Gottlieb 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000193 | Exidy 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000194 | Universal 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000195 | Stern 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000196 | Nintendo Vs. 复基 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000197 | Nintendo PlayChoice 复基 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000198 | Sammy System 32 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000199 | Sammy Atomiswave 复基 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000200 | Seta ST-0016 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000201 | Banpresto 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000202 | Video System 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000203 | NMK 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000204 | Allumer 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000205 | Arika 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000206 | Triangle Service 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000207 | G-mode 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000208 | Milestone 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000209 | Warashi 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000210 | Eighting Raizing 复基 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000211 | SemiCom 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000212 | Andamiro 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000213 | IGS PGM2 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000214 | IGS PGM3 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000215 | Nintendo Triforce 复基 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000216 | Sega Lindbergh 复基 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000217 | Sega RingEdge | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000218 | Sega RingWide | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000219 | Sega Nu | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000220 | Taito Type X Zero | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000221 | Taito Type X3 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000222 | Namco System ES1 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000223 | Namco System ES3 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000224 | Konami PC 基板 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000225 | SNK NEOGEO 复基 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000226 | Capcom CPS 复基 | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000227 | 光枪框体（Time Crisis） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000228 | 光枪框体（House of the Dead） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000229 | 体感框体（DDR 跳舞机） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000230 | 体感框体（Virtual-On） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000231 | 体感框体（Sega R360） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000232 | 体感框体（After Burner 液压） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000233 | 体感框体（Galaxian3） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000234 | 体感框体（Sega G-LOC） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000235 | 体感框体（Namco Starblade） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000236 | 体感框体（Sega Virtua Cop） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000237 | 体感框体（Konami Police 911） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000238 | 体感框体（Sega OutRun 液压） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000239 | 体感框体（Namco Ridge Racer 框体） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000240 | 体感框体（Sega Daytona 框体） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000241 | 体感框体（Konami Beatmania 台） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000242 | 体感框体（Guitar Freaks 台） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000243 | 体感框体（DrumMania 台） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000244 | 体感框体（Sega Samba De Amigo） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000245 | 体感框体（Namco Taiko no Tatsujin） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000246 | 体感框体（Konami Dance Evolution） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000247 | 体感框体（Sega Initial D 框体） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000248 | 体感框体（Sega Wangan Midnight） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000249 | 体感框体（Namco Mario Kart Arcade） | cartridge | 0.80 | 05 |
| 游戏机与手持大类_目录_v2.jsonl | G-AC-000250 | 体感框体（Sega Sega Racing Classic） | cartridge | 0.80 | 05 |
| 计算机大类_目录_v2.jsonl | C-EC-000001 | ENIAC | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000002 | EDVAC | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000003 | EDSAC | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000004 | Manchester Baby | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000005 | Colossus | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000006 | Z3 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000007 | Z4 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000008 | Harvard Mark I | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000009 | ABC | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000010 | IBM SSEC | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000011 | Manchester Mark 1 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000012 | IAS Machine | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-EC-000013 | Whirlwind | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000001 | Psion Organiser | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000002 | Psion Series 3 | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000003 | Psion Series 3a | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000004 | Psion Series 5 | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000005 | Psion Series 5mx | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000006 | Psion Series 7 | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000007 | Psion Revo | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000008 | HP 95LX | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000009 | HP 100LX | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000010 | HP 200LX | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000011 | HP OmniGo 100 | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000012 | Atari Portfolio | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000013 | Poqet PC | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000014 | Sharp PC-3000 | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-HC-000015 | Casio PB-100 | firmware | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000001 | PDP-1 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000002 | PDP-4 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000003 | PDP-5 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000004 | PDP-7 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000005 | PDP-8 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000006 | PDP-8/I | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000007 | PDP-9 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000008 | PDP-10 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000009 | PDP-12 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000010 | PDP-11/20 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000011 | PDP-11/45 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000012 | PDP-11/70 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000013 | PDP-11/34 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000014 | PDP-11/40 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000015 | PDP-11/03 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000016 | PDP-11/60 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000017 | VAX-11/780 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000018 | VAX-11/750 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000019 | VAX-11/730 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000020 | VAX-11/782 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000021 | MicroVAX II | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000022 | MicroVAX 3100 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000023 | VAX 8200 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000024 | VAXstation | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000025 | VAX 8600 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000026 | VAX 9000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000027 | Data General Nova | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000028 | Data General SuperNova | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000029 | Data General Nova 2 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000030 | Data General Nova 3 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000031 | Data General Eclipse | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000032 | Data General Eclipse S/130 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000033 | Data General MV/8000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000034 | Prime 300 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000035 | Prime 750 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000036 | Wang 2200 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000037 | Wang VS | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000038 | Interdata 7/32 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000039 | Honeywell DPS-6 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000040 | SEL 32 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000041 | Texas Instruments 990 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000042 | Modular One | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000043 | DJS-130 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000044 | DJS-100 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000045 | HP 2116 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000046 | HP 2100 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000047 | HP 1000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MC-000048 | HP 3000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000001 | IBM 701 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000002 | IBM 650 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000003 | IBM 704 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000004 | IBM 709 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000005 | IBM 1401 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000006 | IBM 1620 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000007 | IBM 7090 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000008 | IBM 7094 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000009 | IBM 7030 Stretch | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000010 | IBM 7070 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000011 | IBM 7080 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000012 | IBM 1410 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000013 | IBM 1440 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000014 | IBM 305 RAMAC | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000015 | IBM System/360 Model 30 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000016 | IBM System/360 Model 40 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000017 | IBM System/360 Model 50 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000018 | IBM System/360 Model 65 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000019 | IBM System/360 Model 91 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000020 | IBM System/360 Model 20 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000021 | IBM System/360 Model 67 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000022 | IBM System/370 Model 145 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000023 | IBM System/370 Model 168 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000024 | IBM System/370 Model 115 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000025 | IBM 3033 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000026 | IBM 3031 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000027 | IBM 3081 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000028 | IBM 4341 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000029 | IBM 4381 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000030 | IBM 3090 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000031 | IBM System/390 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000032 | IBM 9020 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000033 | IBM zSeries z900 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000034 | Amdahl 470V/6 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000035 | Hitachi M-180 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000036 | Fujitsu FACOM M-190 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000037 | EC 1030 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000038 | EC 1045 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000039 | EC 1060 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000040 | CDC 1604 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000041 | CDC 160 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000042 | CDC 3600 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000043 | CDC 6600 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000044 | CDC 6400 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000045 | CDC 7600 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000046 | CDC CYBER 70 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000047 | CDC CYBER 170 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000048 | CDC 3400 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000049 | CDC 3300 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000050 | UNIVAC I | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000051 | UNIVAC 1101 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000052 | UNIVAC 1103 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000053 | UNIVAC 1107 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000054 | UNIVAC 1108 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000055 | UNIVAC 494 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000056 | UNIVAC 1110 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000057 | UNIVAC 1100/80 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000058 | UNIVAC 90/70 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000059 | UNIVAC 90/60 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000060 | UNIVAC LARC | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000061 | RCA 501 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000062 | RCA 301 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000063 | RCA Spectra 70 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000064 | Burroughs B5000 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000065 | Burroughs B5500 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000066 | Burroughs B2500 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000067 | Burroughs B3500 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000068 | Burroughs B6500 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000069 | Burroughs B6700 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000070 | Burroughs B1700 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000071 | Burroughs B7700 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000072 | Burroughs B7900 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000073 | GE-645 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000074 | GE-635 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000075 | GE-225 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000076 | Honeywell 200 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000077 | Honeywell 800 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000078 | Honeywell 6000 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000079 | NCR 304 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000080 | NCR 315 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000081 | ICL 1900 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000082 | ICL 2900 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000083 | ICL System 4 | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-MF-000084 | Ferranti Atlas | tape | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000001 | IBM AS/400 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000002 | IBM System/3 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000003 | IBM System/32 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000004 | IBM System/34 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000005 | IBM System/36 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000006 | IBM System/38 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000007 | Compaq SystemPro | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000008 | IBM PC Server 500 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000009 | HP NetServer LH | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000010 | Sun Enterprise 450 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000011 | Dell PowerEdge 2100 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000012 | IBM Netfinity 3000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000013 | Compaq ProLiant | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000014 | Compaq ProLiant 1500 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000015 | Compaq ProLiant DL380 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000016 | Dell PowerEdge | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000017 | Dell PowerEdge 4100 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000018 | Dell PowerEdge 1950 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000019 | Dell PowerEdge 2950 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000020 | IBM Netfinity | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000021 | IBM xSeries | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000022 | HP ProLiant DL360 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000023 | HP ProLiant DL380 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000024 | Sun Fire V880 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000025 | Sun SPARCserver 1000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000026 | Sun Enterprise 4500 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000027 | IBM RS/6000 SP | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000028 | SGI Challenge | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000029 | DEC AlphaServer 8400 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000030 | HP Superdome | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000031 | IBM pSeries p690 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000032 | Google Server | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000033 | IBM BladeCenter HS20 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000034 | IBM BladeCenter H | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000035 | HP ProLiant BL20p | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000036 | HP BladeSystem c7000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000037 | Dell PowerEdge M600 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000038 | Dell PowerEdge M1000e | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000039 | Cisco UCS B200 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000040 | IBM iSeries 400 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000041 | Compaq ProLiant ML370 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000042 | Dell PowerEdge 1300 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000043 | Acer Altos | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000044 | HP ProLiant ML150 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000045 | HP 9000 K系列 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000046 | Sun Fire V210 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000047 | Sun Netra | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000048 | IBM xSeries 346 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000049 | HP ProLiant DL580 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000050 | Dell PowerEdge R710 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000051 | 曙光一号 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000052 | HP ProLiant BL460c | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000053 | IBM BladeCenter HS21 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000054 | IBM pSeries 690 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-SV-000055 | HP 9000 E 系列 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000001 | Sun-1 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000002 | Sun-2 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000003 | Sun-3 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000004 | Sun-4 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000005 | SPARCstation 1 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000006 | SPARCstation 1+ | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000007 | SPARCstation 2 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000008 | SPARCstation 5 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000009 | SPARCstation 10 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000010 | SPARCstation 20 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000011 | Sun Ultra 1 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000012 | Sun Ultra 2 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000013 | Sun Ultra 5 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000014 | Sun Ultra 10 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000015 | SGI IRIS 1000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000016 | SGI IRIS 4D | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000017 | SGI Indigo | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000018 | SGI Indigo2 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000019 | SGI Indy | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000020 | SGI O2 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000021 | SGI Octane | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000022 | SGI Octane2 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000023 | SGI Onyx | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000024 | SGI Onyx2 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000025 | SGI Crimson | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000026 | SGI Fuel | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000027 | Apollo DN100 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000028 | Apollo DN300 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000029 | Apollo DN4000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000030 | Apollo DN5500 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000031 | Apollo DN10000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000032 | NeXT Computer | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000033 | NeXTcube | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000034 | NeXTstation | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000035 | HP 9000 Series 300 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000036 | HP 9000 Series 400 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000037 | HP 9000 Series 700 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000038 | HP 9000 715 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000039 | HP 9000 735 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000040 | DECstation 3100 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000041 | DECstation 5000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000042 | VAXstation 2000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000043 | VAXstation 3100 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000044 | AlphaStation | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000045 | AlphaStation 500 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000046 | IBM RT PC | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000047 | IBM RS/6000 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000048 | Sony NEWS | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000049 | Intergraph Clipper | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000050 | Tadpole SPARCbook | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000051 | SPARCstation 4 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000052 | Sun Ultra 30 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000053 | HP 9000 712 | disk | 0.80 | 03 |
| 计算机大类_目录_v2.jsonl | C-WS-000054 | SGI Iris Indigo R4000 | disk | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000001 | Motorola DynaTAC 8000X | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000002 | Motorola DynaTAC 8500X | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000003 | Motorola DynaTAC 8800X | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000004 | Motorola 9800X | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000005 | Motorola MicroTAC 9800X | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000006 | Motorola MicroTAC Lite | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000007 | Nokia Mobira Senator | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000008 | Nokia Mobira Talkman | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000009 | Nokia Mobira Cityman 450 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000010 | Ericsson HotLine Pocket | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000011 | Nokia 1011 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000012 | Nokia 2110 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000013 | Nokia 6110 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000014 | Nokia 8110 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000015 | Nokia 3310 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000016 | Nokia 5110 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000017 | Nokia 3210 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000018 | Nokia 8210 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000019 | Nokia 1100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000020 | Nokia 6150 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000021 | Nokia 6210 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000022 | Nokia 6310 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000023 | Nokia 6600 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000024 | Nokia 7110 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000025 | Nokia 8850 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000026 | Nokia 7600 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000027 | Motorola StarTAC | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000028 | Motorola cd928 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000029 | Motorola V8088 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000030 | Ericsson GA628 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000031 | Ericsson T18 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000032 | Ericsson T28 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000033 | Ericsson T39 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000034 | Siemens S10 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000035 | Siemens S25 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000036 | Siemens S35 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000037 | Siemens C35 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000038 | Siemens S55 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000039 | Samsung SGH-600 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000040 | Samsung SGH-A100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000041 | Motorola RAZR V3 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000042 | Motorola V70 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000043 | Samsung SGH-D500 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000044 | Samsung SGH-E700 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000045 | Samsung U600 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000046 | Sony Ericsson T610 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000047 | Sony Ericsson K750i | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000048 | Siemens SX1 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000049 | LG Chocolate KG800 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000050 | Iridium 9500 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000051 | Iridium 9505 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000052 | Iridium 9555 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000053 | Iridium 9575 Extreme | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000054 | Inmarsat IsatPhone | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000055 | Inmarsat IsatPhone 2 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000056 | Globalstar GSP-1600 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000057 | Globalstar GSP-1700 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000058 | Thuraya SO-2510 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000059 | Thuraya XT | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000060 | Iridium 9505A | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000061 | Inmarsat IsatPhone Pro | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000062 | Motorola IMTS 车载电话 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000063 | Motorola TLD-1100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000064 | Nokia Actionman 320 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000065 | Nokia Talkman 320F | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000066 | Ericsson Car Phone | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000067 | NEC Car Phone | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000068 | Panasonic Car Phone | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000069 | Siemens Car Phone | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000070 | Motorola 8000X 车载套件 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000071 | Nokia Mobira Quattro | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000072 | Motorola HT220 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000073 | Motorola GP300 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000074 | Motorola Talkabout | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000075 | Kenwood TK 系列 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000076 | Yaesu FT 系列 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000077 | 波导 S1000 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000078 | TCL 3188 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000079 | 夏新 A8 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000080 | 康佳 5238 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000081 | 科健 K100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000082 | 首信 C200 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000083 | 熊猫 GM100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000084 | 中兴 ZTE A100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000085 | 华为 A616 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000086 | 天语 A615 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000087 | 金立 GN205 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000088 | 长虹 C100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000089 | 小灵通 UT-Starcom 618 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000090 | UT斯达康 X30 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000091 | 中兴小灵通 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000092 | IBM Simon | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000093 | Nokia 9000 Communicator | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000094 | Nokia 9210 Communicator | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000095 | Ericsson R380 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000096 | Nokia 7650 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000097 | Nokia 3650 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000098 | Nokia N95 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000099 | Nokia N73 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000100 | Nokia 6260 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000101 | Sony Ericsson P800 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000102 | Sony Ericsson W800 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000103 | Motorola A1200 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000104 | BlackBerry 5810 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000105 | BlackBerry 6230 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000106 | BlackBerry 8700 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000107 | Palm Treo 180 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000108 | Palm Treo 650 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000109 | HTC Wallaby | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000110 | Motorola MPx200 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000111 | iPhone | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000112 | iPhone 3G | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000113 | HTC Dream | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000114 | Palm Pre | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000115 | Samsung Galaxy S | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000116 | Nokia 9500 Communicator | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000117 | Nokia 6630 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000118 | Nokia 6680 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000119 | Nokia N70 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000120 | Nokia N80 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000121 | Nokia E61 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000122 | Nokia E71 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000123 | Sony Ericsson P900 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000124 | Sony Ericsson P990 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000125 | Sony Ericsson M600 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000126 | Motorola A780 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000127 | Motorola E680 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000128 | Samsung SGH-i300 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000129 | HTC Wizard | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000130 | HTC TyTN | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000131 | HTC Touch | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000132 | Palm Treo 700w | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000133 | BlackBerry 7230 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000134 | BlackBerry 7100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000135 | BlackBerry Pearl 8100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000136 | BlackBerry Curve 8300 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000137 | BlackBerry Bold 9000 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000138 | Motorola Q | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000139 | Samsung BlackJack | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000140 | LG Prada | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000141 | 魅族 M8 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000142 | 联想 LePhone | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000143 | 华为 U8220 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000144 | 中兴 Blade | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000145 | 酷派 6260 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000146 | 小米 1 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000147 | OPPO Find | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000148 | vivo X1 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000149 | 天语 W700 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000150 | 华为 Ascend P1 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000151 | Nokia 6100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000152 | Nokia 6230 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000153 | Nokia 5300 XpressMusic | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000154 | Nokia 6300 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000155 | Nokia 6500 Classic | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000156 | Motorola C350 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000157 | Motorola L7 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000158 | Motorola V3i | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000159 | Samsung SGH-U700 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000160 | Samsung SGH-E250 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000161 | Sony Ericsson K800 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000162 | Sony Ericsson W910 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000163 | Philips Xenium 9@9 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000164 | Siemens SL55 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000165 | NEC N8 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000166 | Alcatel OT 511 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000167 | LG KG270 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000168 | Pantech PG-3500 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000169 | LG Chocolate BL40 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000170 | HTC Hero | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-MP-000171 | Motorola Droid | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000001 | Palm Pilot 1000 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000002 | Palm Pilot 5000 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000003 | PalmPilot Personal | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000004 | PalmPilot Professional | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000005 | Palm III | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000006 | Palm IIIe | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000007 | Palm IIIc | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000008 | Palm V | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000009 | Palm Vx | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000010 | Palm VII | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000011 | Palm IIIxe | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000012 | Palm m100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000013 | Palm m105 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000014 | Palm m500 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000015 | Palm m515 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000016 | Palm Tungsten T | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000017 | Palm Tungsten T2 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000018 | Palm Tungsten T3 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000019 | Palm Tungsten E | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000020 | Palm Zire | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000021 | Palm Zire 72 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000022 | Palm TX | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000023 | Palm LifeDrive | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000024 | Handspring Visor | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000025 | Handspring Visor Edge | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000026 | Handspring Treo 90 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000027 | Sony CLIÉ PEG-S300 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000028 | Sony CLIÉ PEG-NR70 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000029 | Sony CLIÉ PEG-T615C | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000030 | Sony CLIÉ PEG-NX70V | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000031 | Apple Newton MessagePad | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000032 | Apple Newton MessagePad 120 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000033 | Apple Newton MessagePad 2000 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000034 | Compaq iPAQ H3100 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000035 | Compaq iPAQ H3600 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000036 | Compaq iPAQ H3900 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000037 | Compaq iPAQ 3630 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000038 | HP iPAQ 1910 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000039 | HP iPAQ h5400 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000040 | HP iPAQ 4150 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000041 | HP iPAQ hx4700 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000042 | HP iPAQ rx1950 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000043 | HP iPAQ 2210 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000044 | Dell Axim X5 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000045 | Dell Axim X50 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000046 | Dell Axim X51 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000047 | Toshiba e740 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000048 | Casio Cassiopeia | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000049 | Casio Cassiopeia E-125 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000050 | Compaq Aero 1500 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000051 | HP Jornada 720 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000052 | HP Jornada 568 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000053 | HP Jornada 928 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000054 | Sharp Zaurus PI-3000 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000055 | Sharp Zaurus MI-10 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000056 | Sharp Zaurus SL-5500 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000057 | Sharp Zaurus SL-5600 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000058 | Sharp Zaurus SL-C750 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000059 | Sharp Zaurus SL-C1000 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000060 | Garmin iQue 3600 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000061 | Psion netBook | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000062 | Palm Tungsten C | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000063 | Palm Tungsten E2 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000064 | Palm Z22 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000065 | Palm m125 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000066 | Palm m130 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000067 | HP iPAQ h1940 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000068 | Toshiba Genio e550 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PD-000069 | Palm Tungsten W | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000001 | Motorola PageBoy | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000002 | Motorola PageBoy II | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000003 | Motorola Bravo | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000004 | Motorola Bravo Plus | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000005 | Motorola Spirit | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000006 | Motorola Ultra Express | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000007 | Motorola Memo Express | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000008 | Motorola KeyNote | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000009 | Motorola Jazz | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000010 | NEC Pager | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000011 | Panasonic Pager | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000012 | Philips Pager | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000013 | Sony Pager | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000014 | Sanyo Pager | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000015 | Panasonic EK-2098 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000016 | Philips PRC 系列 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000017 | POCSAG 寻呼机 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000018 | 摩托罗拉 大顾问 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000019 | 摩托罗拉 精英王 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000020 | 摩托罗拉 火凤凰 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000021 | 摩托罗拉 进取 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000022 | 波导寻呼机 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000023 | 国脉寻呼机 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000024 | 中北寻呼机 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000025 | Motorola Advisor | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000026 | Motorola Tango | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000027 | Motorola Director | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000028 | Motorola Wordline FLX | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000029 | Motorola Gold Line | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000030 | 摩托罗拉汉显寻呼机（中国） | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000031 | Motorola PageWriter 2000 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000032 | Motorola PageWriter 2000X | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000033 | Motorola Timeport P935 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000034 | RIM Inter@ctive Pager 950 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000035 | Motorola Pronto | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000036 | Motorola Confidant | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000037 | Motorola LS550 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000038 | 摩托罗拉 中文寻呼机 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000039 | NEC 汉字寻呼机 | firmware | 0.80 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-PG-000040 | Motorola Advisor Gold | firmware | 0.80 | 03 |

## 三、低置信度（<0.8，须该线逐条复核）

| 文件 | 条目 id | 机型名 | 建议 media_class | 置信度 | 执行线 |
|---|---|---|---|---|---|
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000004 | MP3 播放器 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000005 | iPod | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000006 | iPod Nano | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000007 | iPod Shuffle | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000008 | iPod Touch | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000009 | 便携收音机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000010 | 录音笔 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000011 | 电子词典 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000012 | 电子宠物机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000013 | 组合音响 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000014 | 立体声功放 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000015 | 黑胶唱机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000016 | 收音机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000017 | 收录机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000018 | CD 音响 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000019 | 家庭影院系统 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000020 | 蓝牙音箱 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000021 | 留声机（手摇） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000022 | 电子琴 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000023 | 车载音响 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000024 | 电唱收音一体机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000025 | 有源音箱 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000026 | Soundbar 回音壁 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000031 | MD 录音机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000032 | MD 台式机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000033 | iPod mini | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000034 | MP3 播放器（闪存） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000036 | 收音机（晶体管） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000037 | 双卡收录机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000038 | 功放（AV） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000039 | 黑胶唱机（直驱） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000040 | CD 转盘 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000041 | DAC 解码器 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000042 | 耳机（大耳） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000043 | 留声机（电唱） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000044 | 组合音响（带 MD） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000045 | 收音机（电子管） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000046 | 电唱机（便携） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000048 | MP3 播放器（硬盘） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000050 | 收音机（闹钟） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000051 | CD 组合（书架） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000052 | 黑胶唱机（自动） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000054 | 均衡器 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000055 | CD 播放机（便携防震） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000058 | 蓝牙耳机 | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000059 | 组合音响（落地） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000060 | 收音机（车用） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000061 | 黑胶唱片（LP） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-AU-000062 | MD 光盘（介质） | cd | 0.60 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000001 | 早期 CRT 电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000002 | 黑白电视机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000003 | 彩色电视机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000004 | 晶体管电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000005 | 特丽珑电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000006 | 投影电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000007 | 液晶电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000008 | 等离子电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000009 | OLED 电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000010 | 智能电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000011 | 便携电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000012 | 车载电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000013 | 背投电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000014 | 曲面电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000015 | 4K 电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000016 | 8K 电视 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000017 | 投影机（DLP） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000018 | 投影机（LCD） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000019 | 电视（壁挂） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000020 | 电视（画中画） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000021 | 电视（宽屏 CRT） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000022 | 电视（黑白便携） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000023 | 电视（卫星接收） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000024 | 电视（游戏专用） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000025 | 电视（CRT 彩监） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000026 | 电视（手持黑白） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000027 | 电视（投影背投） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-TV-000028 | 电视（OLED 曲面） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000004 | 激光影碟机 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000005 | CD 播放机 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000008 | 高清媒体播放器 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000009 | CD-i 播放机 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000011 | 数字机顶盒 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000012 | 卡拉 OK 机 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000013 | 留声机 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000015 | 电子书阅读器 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000016 | 数码相框 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000017 | 投影仪 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000023 | MP4 播放器 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000024 | 移动影院 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000025 | 唱机（留声） | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000026 | 开盘录音机 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000027 | 盒式录音机 | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000032 | LD 影碟（介质） | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000033 | 录音带（盒式介质） | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | A-VP-000034 | CD 光盘（介质） | cd | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000001 | 电子计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000002 | 可编程计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000003 | HP-65 计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000004 | 图形计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000005 | 科学计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000006 | HP-35 计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000007 | TI-84 图形计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000008 | Casio fx 计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000009 | 财务计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000010 | 打印计算器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000011 | 计算器（太阳能） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-CA-000012 | 计算器（编程） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000001 | 鼠标 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000002 | 光学鼠标 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000003 | 无线鼠标 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000004 | 游戏鼠标 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000005 | 机械键盘 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000006 | IBM PC 键盘 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000007 | 轨迹球 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000008 | 游戏手柄 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000009 | 绘图板 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000010 | 扫描枪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000011 | 触控板 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000012 | 指点杆 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000013 | 摇杆 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000014 | 方向盘 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000015 | 跳舞毯 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000016 | 手写板 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000017 | 光笔 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000018 | 扫描仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000019 | 网络摄像头 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000020 | 指纹识别器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000021 | 调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000022 | 平板扫描仪（家用） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000023 | 高速文档扫描仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000024 | 胶片扫描仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000025 | 手持扫描仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000026 | 一体机扫描模块 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000027 | 书籍扫描仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000028 | 3D 扫描仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000029 | 名片扫描仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000030 | 声学耦合器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000031 | 300 波特调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000032 | 1200 波特调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000033 | 2400 波特调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000034 | 9600 波特调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000035 | 14.4K 调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000036 | 28.8K 调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000037 | 33.6K 调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000038 | 56K 调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000039 | ISDN 终端适配器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000040 | ADSL 调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000041 | 电缆调制解调器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000042 | 光纤 ONU | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000043 | 无线路由器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000044 | 调制解调器（外置） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000045 | 滚球鼠标 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000046 | 串口鼠标 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000047 | USB 鼠标 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000048 | 人体工学键盘 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000049 | 薄膜键盘 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000050 | 无线键盘 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000051 | 轨迹球（拇指） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000052 | 游戏手柄（USB） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000053 | 数位板（影拓） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000054 | 触摸屏（外接） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000055 | 麦克风 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000056 | 摄像头（模拟） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000057 | 光笔（CRT） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000058 | 光笔（图形） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000059 | 键盘（机械青轴） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000060 | 鼠标（轨迹球老式） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000061 | 数位屏（绘图） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000062 | 条码扫描仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000063 | 二维码扫描枪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000064 | RFID 读卡器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000065 | 蓝牙适配器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000066 | WiFi 网卡 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000067 | 以太网卡 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000068 | 声卡 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000069 | 显卡 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000070 | 主板（PC 扩展） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000071 | 键盘（折叠便携） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000072 | 鼠标（垂直人体工学） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000073 | 绘图板（入门） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000074 | 扫描仪（便携） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-IN-000075 | 调制解调器（56K 内置） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000001 | CRT 显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000002 | 单色显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000003 | LCD 显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000004 | 彩色显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000005 | 宽屏显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000006 | 专业显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000007 | 竖屏显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000008 | 触摸显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000009 | 超宽显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000010 | 高刷新显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000011 | CRT 显示器（17 寸） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000012 | CRT 显示器（21 寸） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000013 | LCD 显示器（15 寸） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000014 | LCD 显示器（19 寸） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000015 | LCD 显示器（22 寸） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000016 | LED 显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000017 | 4K 显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000018 | 电竞显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000019 | 便携显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000020 | 专业色彩显示器 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000021 | 显示器（CRT 三枪） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000022 | 显示器（液晶电视两用） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-MO-000023 | 显示器（带音箱） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000001 | 点阵打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000002 | 喷墨打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000003 | 激光打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000004 | 热敏打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000005 | 3D 打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000006 | 多功能一体机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000007 | 照片打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000008 | 彩色激光打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000009 | 票据打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000010 | 标签打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000011 | 大幅面打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000012 | 绘图仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000013 | 针式打印机（高速） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000014 | 喷墨照片打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000015 | 激光一体机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000016 | 针式打印机（24 针） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000017 | 喷墨打印机（彩色） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000018 | 激光打印机（网络） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000019 | 热敏票据打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000020 | 热转印标签机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000021 | 喷墨一体机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000022 | 大幅面绘图仪 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000023 | 3D 打印机（桌面） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000024 | 照片打印机（热升华） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000025 | 激光彩色一体机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000026 | 针式打印机（票据） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000027 | 便携照片打印机 | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000028 | 绘图仪（滚筒） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000029 | 绘图仪（平板） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000030 | 打印机（针式 9 针） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000031 | 打印机（喷墨连续供墨） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000032 | 打印机（激光黑白） | 无 | 0.70 | 05 |
| 家电影音与外设大类_目录_v2.jsonl | P-PR-000033 | 打印机（针式平推） | 无 | 0.70 | 05 |
| 计算机大类_目录_v2.jsonl | C-SC-000001 | CDC STAR-100 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000002 | CDC CYBER 205 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000003 | Cray-1 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000004 | Cray-1S | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000005 | Cray X-MP | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000006 | Cray-2 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000007 | Cray Y-MP | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000008 | Cray C90 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000009 | Cray T90 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000010 | NEC SX-2 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000011 | NEC SX-3 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000012 | Fujitsu VP-200 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000013 | Thinking Machines CM-1 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000014 | Thinking Machines CM-2 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000015 | Thinking Machines CM-5 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000016 | Cray T3D | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000017 | Cray T3E | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000018 | IBM Blue Gene/L | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000019 | SGI Origin 2000 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000020 | nCUBE 2 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000021 | Intel Paragon | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000022 | IBM SP2 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000023 | MasPar MP-1 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000024 | Elbrus-1 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000025 | Elbrus-2 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000026 | Cray J90 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000027 | Hitachi S-820 | disk | 0.70 | 03 |
| 计算机大类_目录_v2.jsonl | C-SC-000028 | Fujitsu VPP500 | disk | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000001 | Western Electric 302 型 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000002 | Western Electric 500 型 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000003 | GPO 拨盘电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000004 | 拨盘电话（中国） | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000005 | 拨盘电话（日本） | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000006 | Western Electric 2500 型 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000007 | AT&T Trimline | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000008 | 早期 49MHz 无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000009 | Sony SPP 系列无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000010 | Panasonic KX-T 系列无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000011 | AT&T 无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000012 | GE 无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000013 | DECT 标准无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000014 | Siemens Gigaset | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000015 | Panasonic DECT 无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000016 | Uniden DECT 无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000017 | Philips DECT 无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000018 | Motorola 无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000019 | VTech 无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000020 | BT 无绳电话 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000021 | Panasonic KX-TG 系列 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000022 | 公用投币电话机 | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000023 | 磁卡电话机（中国） | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000024 | IC 卡电话机（中国） | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000025 | 按键电话代表（中国） | 无 | 0.70 | 03 |
| 通讯与移动大类_目录_v2.jsonl | M-TL-000026 | 按键电话（日本） | 无 | 0.70 | 03 |

## 四、v1 legacy 文件（待删除，不执行回填）

| 文件 | 条数 | 处置 |
|---|---|---|
| 家电影音与外设大类_目录_v1.jsonl | 151 | 删除（已被 v2 351 条替代） |
| 游戏机与手持大类_目录_v1.jsonl | 274 | 删除（已被 v2 401 条替代） |

> 删除前请 03/05 线确认 v2 确为 v1 超集（全量文件替代制），避免误删存量条目。
