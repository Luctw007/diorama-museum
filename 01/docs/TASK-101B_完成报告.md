# TASK-101B 完成报告（手机厅 DynaTAC 演示帧存证）

## 一、执行
python 01/scripts/launch_device.py --device dynatac-8000x --frames 3 --out 01/demo_out_cell

决策链原文：
包位置: D:\work\03\repo\content\dynatac-8000x
emulator=none  demo_mode=True  category=phone
决策: demo_mode → fake 演示直起（无需槽位）
演示启动 ok（sinks=['main', 'speaker'] 画面 240x320@15.0）
帧存证：3 张 PNG → 01/demo_out_cell

未触发 fallback：dynatac-8000x 已在完工包注册表（门禁 pkg:dynatac-8000x PASS 84 条），无需 amiga500 对照。

## 二、交付物（01/demo_out_cell/）
- dynatac-8000x_0001.png　2005 B
- dynatac-8000x_0002.png　2768 B
- dynatac-8000x_0003.png　2799 B
（demo_out 不入库，仅本地证据）

## 三、结论
手机厅首台 DynaTAC 8000X（定案表 #25、演示向无模拟器）demo 通道出帧成功，引擎侧首证成立。
备注：竖屏 240x320@15、sinks=main+speaker；竖屏帧与画廊 280x192 横屏兼容性留 04 线体验侧核对。