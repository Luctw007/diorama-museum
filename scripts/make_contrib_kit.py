# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2026 箱庭电子博物馆（Diorama Computer Museum）项目作者
# SPDX-License-Identifier: MIT
"""贡献者自测包打包器（TASK-86B）。

打包内容（全部纯文本，无二进制/ROM/图片/凭据）：
  contrib_kit_src/ 源材料（README / 自测命令卡 / 提交清单 / 槽位样例）
  02 线校验器 tools/validate/*.py（仅顶层校验脚本；tests 与其夹具资产不打包）
  02 线 device_spec.schema.json
产出：dist/contrib_kit_v1.zip + dist/CHECKSUM.md5

安全黑名单：见 BLOCK_EXTS / BLOCK_SUBSTR，逐文件检查，命中即中止打包。
用法：python scripts/make_contrib_kit.py
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALID = r"D:\work\02\repo\tools\validate"
SCHEMA = r"D:\work\02\repo\content\schema\device_spec.schema.json"
SRC = os.path.join(REPO, "contrib_kit_src")
DIST = os.path.join(REPO, "dist")

BLOCK_EXTS = {".exe", ".bin", ".rom", ".img", ".iso", ".zip", ".7z", ".rar",
              ".pyc", ".pyo", ".dll", ".so", ".bat", ".cmd", ".jar",
              ".png", ".jpg", ".jpeg", ".gif", ".gltf", ".wav", ".mp3"}
BLOCK_SUBSTR = ("ghp_", "x-access-token", "password", "credential",
                "private key", "begin rsa")


def check_file(path: str) -> None:
    name = os.path.basename(path).lower()
    ext = os.path.splitext(name)[1].lower()
    if ext in BLOCK_EXTS:
        raise RuntimeError("黑名单扩展名拦截: %s" % path)
    for s in BLOCK_SUBSTR:
        if s in name:
            raise RuntimeError("黑名单字样拦截: %s（%s）" % (s, path))


def build() -> None:
    os.makedirs(DIST, exist_ok=True)
    zip_path = os.path.join(DIST, "contrib_kit_v1.zip")
    stage = os.path.join(DIST, "_stage")
    shutil.rmtree(stage, ignore_errors=True)
    os.makedirs(stage, exist_ok=True)

    # 1) 源材料（README/命令卡/提交清单/槽位样例）
    for f in sorted(os.listdir(SRC)):
        p = os.path.join(SRC, f)
        if os.path.isfile(p):
            check_file(p)
            shutil.copy(p, os.path.join(stage, f))

    # 2) 02 线校验器：只取 tools/validate/ 顶层 *.py（tests/ 及其夹具资产不打包；
    #    结构保持 validate.py → ../../content/schema 的相对引用成立）
    vdst = os.path.join(stage, "tools", "validate")
    os.makedirs(vdst, exist_ok=True)
    for f in sorted(os.listdir(VALID)):
        p = os.path.join(VALID, f)
        if os.path.isfile(p) and f.endswith(".py"):
            check_file(p)
            shutil.copy(p, os.path.join(vdst, f))

    # 3) schema（validate.py 的 ../../content/schema 相对引用对应位置）
    sdir = os.path.join(stage, "content", "schema")
    os.makedirs(sdir, exist_ok=True)
    check_file(SCHEMA)
    shutil.copy(SCHEMA, os.path.join(sdir, "device_spec.schema.json"))

    # 4) 打 zip（顶层 contrib_kit/ 目录）
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _dirs, files in os.walk(stage):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, stage)
                z.write(full, os.path.join("contrib_kit", rel))
                print("  + contrib_kit/%s" % rel.replace(os.sep, "/"))
    md5 = hashlib.md5(open(zip_path, "rb").read()).hexdigest()
    with open(os.path.join(DIST, "CHECKSUM.md5"), "w", encoding="utf-8") as fh:
        fh.write("%s  contrib_kit_v1.zip\n" % md5)
    shutil.rmtree(stage, ignore_errors=True)
    size = os.path.getsize(zip_path)
    print("\n已打包 %s（%.1f KB）" % (zip_path, size / 1024.0))
    print("校验和（md5）: %s" % md5)
    print("黑名单扩展名: %s" % " ".join(sorted(BLOCK_EXTS)))
    print("黑名单字样: %s" % " | ".join(BLOCK_SUBSTR))


def main() -> int:
    try:
        build()
    except RuntimeError as exc:
        print("打包中止: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())