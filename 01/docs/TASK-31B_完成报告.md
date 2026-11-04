# TASK-31B 完成报告（docs/TASK-31B_完成报告.md）

> 01 线 · 2026-11-03 · 任务：无引擎演示打包（帧序列画廊，见 任务31-B）。
> 本报告含 TASK-31 两份总收尾，01 线本轮（任务 31-A/B）完成。

## 1. 交付物

| 文件 | 行数 | 说明 |
|---|---|---|
| `scripts/demo_frames.py` | 208 | 网关子进程 + 抓帧 + 纯 stdlib PNG（zlib）+ gallery.html 生成 |
| `docs/demo_kit.md` | ≥1000 字 | 产物结构、用法、90 秒里程碑视频拍摄脚本、边界 |
| `demo_out/frames/*.png` ×30 | — | 实测产物（280×192，每帧 1.4–2.1 KB） |
| `demo_out/gallery.html` | — | 单文件画廊（自动播放 25fps/暂停/帧号） |

## 2. 运行日志（原文关键段）

```text
$ python -u scripts/demo_frames.py --frames 30 --html --txt
  frame 26 | frame_id=26 | 280x192 | png 2041 B
  frame 27 | frame_id=27 | 280x192 | png 2041 B
  frame 28 | frame_id=28 | 280x192 | png 2089 B
  frame 29 | frame_id=29 | 280x192 | png 2113 B
  frame 30 | frame_id=30 | 280x192 | png 2113 B
画廊已生成: …\demo_out\gallery.html
完成：30 帧 PNG → …\demo_out\frames                  → rc=0
```

产物抽查：
- PNG 计数 30；首帧签名 `89 50 4E 47 0D 0A 1A 0A` ✓；
- IHDR 尺寸 BE 复验 = **280 × 192** ✓（抽查脚本首轮按小端读出乱值是校验脚本问题，非产物问题——已用 `struct.unpack('>II')` 复核）。

## 3. 迭代记录（2 轮）

1. 轮 1：首跑即通帧收集与 PNG 写入；抽查时发现我自己的 IHDR 读取脚本用了主机字节序 → 换成大端解析复核（记录以证产物正确）；
2. 轮 2：gallery.html 的自动播放依赖 `img.onload` 逐帧推进——把帧名数组与 FPS 内联进 HTML；清理 finally 中的网关进程兜底（terminate+kill 双保险）。

## 4. 开放问题

1. `--fps` 变更需同步 HTML 常量（未来参数化，lint 余项）；
2. 自动合成 MP4 可行（subprocess ffmpeg），本任务保持零依赖未做——已记录在 demo_kit §4。

## 5. TASK-31 两份总收尾 + 01 线本轮完成标注

- 31-A：键码注册机制三级回退 + 三机种骨架（apple2 57 / atari 12 / famicom 18）+ 注册表注入；
  网关注册改动后 m0/m1/m1b/m2a 全回归绿；
- 31-B：演示打包器（PNG 序列 + 画廊）实跑 30 帧 0 失败，产物可作 D0 进度证据；
- 01 线本轮（任务 31）完成。