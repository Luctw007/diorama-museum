# 第三批 none 机型 6 台标注复核 v1

> 03 线 TASK-308-D 交付。第三批 6 台 emulator=none（Archimedes/ZX81/SGI Indigo/Compaq Portable/Whirlwind/Newton）内容侧标注复核：无模拟器声明、需核实标注、annotations 素材取用口径逐台核对。只复核不改原文、不产包。

## 一、6 台逐台复核表

| # | 设备 | 无模拟器声明 | 静态+动画口径 | 需核实标注 | THIRD_PARTY 处理 | annotations 取用 | 结论 |
|---|---|---|---|---|---|---|---|
| 1 | Acorn Archimedes | ✅ none | ✅ RISC 原理动画 | ✓ 尺寸/候选 | ✅ Arculator/ArcEm 候选记 | ✅ 命中 | 齐备 |
| 2 | Sinclair ZX81 | ✅ none | ✅ 编程入门动画 | ✓ 尺寸/候选/ROM | ✅ EightyOne/sz81 候选记 | ✅ 命中 | 齐备 |
| 3 | SGI Indigo | ✅ none | ✅ 3D 渲染动画 | ✓ 尺寸/支持度 | ✅ MAME/QEMU 候选记 | ✅ 命中 | 齐备 |
| 4 | Compaq Portable | ✅ none | ✅ BIOS 逆向动画 | ✓ 尺寸/机型支持 | ✅ 86Box/PCem 候选记 | ✅ 命中 | 齐备 |
| 5 | Whirlwind | ✅ none | ✅ 磁芯/实时动画 | ✓ 尺寸/候选 | ✅ 无候选 | ✅ 命中 | 齐备 |
| 6 | Apple Newton | ✅ none | ✅ 手写识别动画 | ✓ 尺寸/候选/ROM | ✅ Einstein 候选记 | ✅ 命中 | 齐备 |

## 二、标注缺口登记

**0 缺口**。6 台研究卡/口径卡「无模拟器声明、静态+原理动画承载、需核实标注、THIRD_PARTY 候选记、annotations 素材取用命中」五项均到位。

## 三、复核结论

第三批 none 机型 6 台**标注齐备**：`emulator="none"` 口径统一，演示走「静态 + 原理动画」，候选模拟器记 THIRD_PARTY，annotations 素材从研究卡部件分解取用（303-F 已映射）。**本复核不改原文、不产包**。

## 四、复核依据与 none 口径说明

- **none 口径来源**：预检总卡（227-B）「无 bone → emulator="none" 静态+动画」口径；6 台研究卡/口径卡均据此标 `emulator="none"`。
- **候选模拟器处理**：Archimedes（Arculator/ArcEm）、ZX81（EightyOne/sz81）、SGI Indigo（MAME/QEMU）、Compaq Portable（86Box/PCem）、Whirlwind（无候选）、Newton（Einstein）——候选均记 THIRD_PARTY 标需核实。
- **annotations 取用**：6 台部件分解已在 303-F 素材预填卡映射（L0/L1/L2/L3），产包时按卡取用。
- **红线**：只复核不改原文、不产包、不改 jsonl、不 allocate、不代产包 annotations、零联网零下载。
