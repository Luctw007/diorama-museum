# 无引擎演示套件（docs/demo_kit.md）

> TASK-31B 交付。不起 Godot、不装任何浏览器插件，即产出一份"机器跑起来"的可分享证据。

## 1. 产物结构

```
demo_out/
  frames/
    frame_0001.png … frame_0030.png   # 280x192 RGB PNG（纯 stdlib zlib 手写）
  gallery.html                         # 单文件画廊（自动播放 + 暂停/播放 + 帧号）
```

## 2. 用法

```powershell
python scripts/demo_frames.py                     # 默认 30 帧
python scripts/demo_frames.py --frames 60 --html --txt
python scripts/demo_frames.py --port 17337        # 专用端口，避免与验收 suite 冲突
```

- `--txt`：逐帧校验摘要（帧序号/frame_id/宽高/PNG 字节数）——写报告时直接引用；
- 无 `--gif`：purpose 不用第三方库；PNG 序列可被 OBS/ffmpeg 直接合成视频。

## 3. 合成"90 秒里程碑视频"的拍摄脚本（直接照做）

1. 起演示：`python scripts/demo_frames.py --frames 300 --html`（约 12 秒素材循环用）；
2. 打开 `demo_out/gallery.html`，OBS 捕获浏览器窗口；
3. 镜头顺序（引用 05 线 17_运行演示台本）：开机色块识别（前 3 秒说明文字来自署名横幅）
   → 键注入（配合 `m2a_check.py` 的输入断言镜头）→ 存档回滚（帧号回跳特写）；
4. 旁白用 04 线 16 号台本"第一幕"解说词；时长 90 秒、1080p。
5. 归档命名：`milestone_d0_<日期>.mp4`，与 `docs/TASK-*_完成报告` 互相引用。

## 4. 边界与下一步

- 这是**网关层演示**（画面来自 fake 后端彩条），不是 Godot 渲染——两者在 D0 验收里
  分别对应"模拟器通路"与"引擎表现"两条线；
- 若后续需要自动合成 MP4：仅需在脚本内 subprocess 调 ffmpeg（不做，保持零依赖；可行性记录在案）；
- `gallery.html` 的播放帧率固定 25fps（与抓帧 FPS 一致）；改 `--fps` 需同步改 HTML 常量
  （下轮可把 fps 参数化——列为 lint 余项）。