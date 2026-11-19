# TASK-242-A 完成报告

> 任务：第三批产包顺序与过闸口径终版（10 台滚动产包准备）。执行账号：02 线。只改 02 目录，纯文档。

## 一、交付物清单

1. 新增 `docs/第三批产包顺序与口径终版_v1.md`（5882 字节），含 10 台产包顺序表 + 逐台过闸口径终版 +
   正式定案后产包验收口径 + 漂移。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复测

```
verify_all --daily --cache
  ...
  结果：49/49 通过（rc=0）
```

### 2.2 终版卡自检

```
字节：5882（>1500 达标）
10 台顺序表（System/370 → MSX2 → Macintosh Plus → IBM PC XT → Archimedes → ZX81 → SGI Indigo →
  Compaq Portable → Whirlwind → Newton）
逐台口径：hercules（QPL 已核实）/ openmsx（GPLv2 已核实）/ mini-vmac（GPL 需核实）/ 86Box（GPLv2 已核实）
  + 6 台 none（候选 Arculator/EightyOne/MAME/86Box/Einstein 记 THIRD_PARTY）
```

## 三、产包顺序结论

前 4 台（System/370、MSX2、Macintosh Plus、IBM PC XT）为「有明确模拟器」台，Hercules/openMSX/86Box 许可
已核实、先行对接 1.0 真跑矩阵；后 6 台「无成熟模拟器」按厅叙事优先级排序（个人机 → 工作站 → 便携 → 黎明厅
→ PDA）。

## 四、与任务书的漂移

1. **产包顺序采纳任务书建议**（System/370 → … → Newton），未改动。
2. **6 台 none 候选模拟器已补全**：238-B 收尾档案给出 Archimedes→Arculator/ArcEm、ZX81→EightyOne/sz81、
   SGI Indigo→MAME/QEMU、Compaq Portable→86Box/PCem、Newton→Einstein、Whirlwind→无候选，本卡逐台记入
   （227-B 预检总卡未列候选）。
3. **Macintosh Plus 许可仍需核实**（mini-vmac GPL 许可精确版本未定），与 System/370（QPL）、MSX2/PC XT
   （GPLv2）已核实区分。

## 五、红线自查

零联网、零下载（纯文档）；顺序与口径以研究卡（238-B 收尾档案）/预检总卡（227-B）为准，未臆造；只改 02 目录、
不 allocate id、不改 03 线目录 jsonl。
