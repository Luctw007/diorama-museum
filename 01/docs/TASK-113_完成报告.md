# TASK-113 完成报告（网关音频通道 HUD 接线）

## 交付物
- `gateway_client.gd`：
  - `_apply_audio(data)`：`audio_chunk` → `Marshalls.base64_to_raw` 解 s16le PCM → `AudioStreamWAV`（FORMAT_16_BITS / mix_rate / channels）→ `AudioStreamPlayer.play()`；PCM 为空/非法时**降级**播放磁盘占位 WAV（`res://content/audio/demo/narr_hall_intro_placeholder.wav`），不崩溃；
  - HUD 新增音频状态行（左下角、绿色）：`音频：chunk N seq=S（8kHz/1ch · 共 N · 播放中）` 与降级字样；计数 `_audio_chunks/_audio_degraded`；
  - `01/gw/` 协议与网关实现未动（无上游反馈项）。
- `main.tscn`：AudioStreamPlayer 节点由脚本动态创建（add_child），无需改场景接线。

## 验收证据
- `python 01/scripts/m0_check.py`（音频通道证据）
```text
[PASS] 收到音频块：seq=1, format=s16le
[PASS] 网关在端口 17331 就绪 …（22 条断言，含快照回滚）
M0 验收全部通过 ✔
```
- Godot 输出面板 HUD 音频状态日志：静态交付（本机无引擎），预期时序——收 chunk → 状态行"播放中"计数递增 → PCM 非法时"（降级:占位 wav）"，待实机对照。

## 备注
音频块每 chunk 重建 AudioStreamWAV（M0 量级可接受；连续流化播放列入后续迭代）。降级 WAV 复用占位口播轨资源（同属 godot/content/audio/demo，仅本地播放、不下载）。