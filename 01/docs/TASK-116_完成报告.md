# TASK-116 完成报告（占位口播轨播放接线）

## 交付物
- `narr_player.gd`（新增）：
  - `play_narr(id)`：加载 narr 系占位轨播放；**切换时停旧播新（单口播互斥）**；同一轨已在播时幂等不重启；未知 id 降级 FALLBACK_NARR；
  - `stop_narr()/current_narr()`；HUD 状态行（`口播：narr_hall_intro（playing/stopped）` 与降级字样）；
  - 触发点仅作接线（NarrPlayer 节点挂 Main 下），正式触发由 04 线导览台本驱动。
- `main.tscn`：挂载 NarrPlayer（ext_resource 10_narr，load_steps 14→16，scene_check 通过）。

## 验收证据
- `python 01/scripts/gen_placeholder_vo.py`
```text
已生成 …narr_hall_intro_placeholder.wav（8.0s, 22050Hz, 176400采样）
已生成 …narr_eniac_placeholder.wav（8.0s, 22050Hz, 176400采样）  rc=0
```
（两文件各 352844 B，22.05kHz/16bit/单声道/-18dBFS 峰值）
- Godot 输出面板日志：静态交付。预期时序：`play_narr("narr_hall_intro")` → HUD "narr_hall_intro（playing）" → `play_narr("narr_eniac")` → hall_intro 被 stop（互斥成立）+ HUD "narr_eniac（playing）"。待实机对照。

## 备注
互斥语义与 04 线 20 号规格 narr 系"播新停旧"一致；on-finish 自动清空状态未做（占位轨无结束回调需求，正式轨接入时补 `finished` 信号清理，列入后续）。占位轨为本地生成（纯正弦+节拍），无真实语音素材下载。