# 第三批 none 6 台装配口径与闸口基线 v1

> 03 线 TASK-323-C 交付。把 none 6 台（Acorn Archimedes、Sinclair ZX81、SGI Indigo、Compaq Portable、Whirlwind、Apple Newton）的 meta/runtime/annotations 口径逐台固化（emulator 全 none、静态演示向），并做「开产闸口基线快照」。只改 03 目录，纯文本，不产包、不 allocate。

## 一、6 台逐台 meta/runtime 字段固化

| 设备 | emulator | media_hint | bios_required | 静态演示向声明 |
|---|---|---|---|---|
| Acorn Archimedes | none | floppy | false | 静态 + ARM2 RISC 原理动画 |
| Sinclair ZX81 | none | tape | false | 静态 + ULA 合一芯片动画 |
| SGI Indigo | none | disk | false | 静态 + 3D 渲染管线动画 |
| Compaq Portable | none | floppy | false | 静态 + 净室逆向 BIOS 叙事 |
| Whirlwind | none | tape | false | 静态 + 磁芯内存/实时计算动画 |
| Apple Newton | none | firmware | false | 静态 + 手写识别/触控动画 |

> meta 五字段（name/intro/era/manufacturer/category/description）与 sources 照 318-C 备底母本，此处不重复罗列。

## 二、6 台 annotations 口径

- role 文案含「在整机」（照 318-A 落地备底逐台草案）；flow 叙事锚点 ≥10。
- R-060：「需核实」只进 encyclopedia / MESHES / THIRD_PARTY，**不进 role/flow**。

## 三、开产闸口基线快照

- 第三批 10 台五件备底状态：encyclopedia 四卷 ✅ + annotations 318-A ✅ + THIRD_PARTY 318-B ✅ + meta/runtime 318-C ✅，总检 0 缺口（318-D）。
- 待点头 3 项（照抄 318-D）：①顺序维持；②模拟器合规路径（mini-vmac 需核实）；③BIOS-ROM 红线。
- 闸口：**用户点头前不产包、不 allocate、不代点头**。

## 四、版本治理声明

目录只改活跃版本（计算机 v2 + 通讯 v3），不新建版本；本卡只固化口径与快照，不写 content/<id>/、不改 jsonl。

## 五、none 6 台 sources 映射（补充）

- Acorn Archimedes=[S125][S126]；Sinclair ZX81=[S127][S128]；SGI Indigo=[S129][S130]；Compaq Portable=[S131][S132]；Whirlwind=[S133][S134]；Apple Newton=[S135][S136]。
- 候选模拟器记 THIRD_PARTY（Arculator/ArcEm、EightyOne/sz81、MAME/QEMU MIPS、86Box/PCem、Einstein），均「需核实」、不下载。

## 六、闸口基线结论

第三批 10 台内容侧五件备料 + 装配口径（323-A/B/C）完整闭环，**0 缺口**；闸口状态固化：待用户点头 3 项照抄 318-D，点头前不产包、不 allocate、不代点头。

---

> 本卡只写口径 + 快照文本，不写 content/<id>/、不产包、不改 jsonl、不 allocate、不代点头。
