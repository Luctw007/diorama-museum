# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""聚合画廊（TASK-66B）：把 tour 目录的按厅帧序列合成单文件 HTML 轮播。

用法：python scripts/gen_tour_gallery.py [--tour demo_out/tour_<最新>] [--out tour_gallery.html]
"""

from __future__ import annotations

import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SCRIPT_DIR)


def find_latest_tour(base: str) -> str:
    if not os.path.isdir(base):
        return ""
    tours = [d for d in os.listdir(base)
             if d.startswith("tour_") and os.path.isdir(os.path.join(base, d))]
    if not tours:
        return ""
    return os.path.join(base, sorted(tours)[-1])


def collect(tour_dir: str) -> list[dict]:
    halls = []
    for d in sorted(os.listdir(tour_dir)):
        p = os.path.join(tour_dir, d)
        if not os.path.isdir(p):
            continue
        frames = sorted(f for f in os.listdir(p) if f.endswith(".png"))
        if frames:
            halls.append({"name": d,
                          "frames": [os.path.join(d, f).replace("\\", "/")
                                     for f in frames]})
    return halls


def gallery_html(halls: list[dict], fps: int) -> str:
    sections = []
    for hall in halls:
        frames_json = json.dumps(hall["frames"])
        sections.append("""
<section data-frames='%s'>
  <h2>%s</h2>
  <img class="stage" width="560" alt="frame">
  <div class="bar"><button class="play">暂停/播放</button>
    <span class="info"></span></div>
</section>""" % (frames_json, hall["name"]))
    body = "".join(sections)
    return """<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>五厅轮播画廊</title>
<style>
body{margin:0;background:#12151a;color:#cfd3da;font-family:system-ui;padding:24px;}
section{margin:0 0 28px 0;background:#1a1f27;border:1px solid #343b46;
border-radius:10px;padding:16px;}
h2{margin:0 0 10px 0;font-size:18px;}
.stage{image-rendering:pixelated;background:#000;display:block;}
.bar{margin-top:8px;display:flex;gap:10px;align-items:center;}
button{background:#2a303a;color:#dfe3ea;border:1px solid #4a5563;border-radius:6px;
padding:4px 12px;cursor:pointer;}
</style></head><body>
<h1>五厅轮播 · 演示帧</h1>
__BODY__
<script>
const FPS = __FPS__;
for (const sec of document.querySelectorAll("section")) {
  const frames = JSON.parse(sec.dataset.frames);
  const img = sec.querySelector(".stage");
  const info = sec.querySelector(".info");
  let i = 0, playing = true;
  const show = () => {
    img.src = frames[i];
    info.textContent = (i + 1) + " / " + frames.length;
  };
  show();
  img.onload = () => { if (playing) setTimeout(() => { i = (i + 1) % frames.length; show(); }, 1000/FPS); };
  sec.querySelector(".play").onclick = () => { playing = !playing; if (playing) show(); };
}
</script></body></html>""".replace("__BODY__", body).replace("__FPS__", str(fps))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="聚合画廊生成")
    ap.add_argument("--tour", default="")
    ap.add_argument("--out", default=os.path.join(REPO, "demo_out", "tour_gallery.html"))
    ap.add_argument("--fps", type=int, default=8)
    args = ap.parse_args(argv)
    tour = args.tour or find_latest_tour(os.path.join(REPO, "demo_out"))
    if not tour:
        print("未找到 tour 目录")
        return 1
    halls = collect(tour)
    if not halls:
        print("tour 目录无帧")
        return 1
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(gallery_html(halls, args.fps))
    print("画廊：%d 厅 → %s" % (len(halls), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())