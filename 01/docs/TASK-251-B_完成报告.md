# TASK-251-B 完成报告

## 交付物清单
- **四台槽位预留方案**：新增 `docs/第三批真跑候选槽位预留_v1.md`——逐台表（hercules-s370/openmsx-msx2/mini-vmac-macplus/86box-pcxt：backend_type 建议 dedicated、binary_env、binary_hint、media_classes [需核实]、许可隔离口径）+ 四条预留口径裁决（backend 家族绕过、不建 manifest 理由、许可分条款、ALIASES 后补）。
- **登记回写**：`slots/README.md` 新增「第三批真跑候选槽位预留」表（四台预留态 + 说明）。
- 边界遵守：未建 manifest、未写后端骨架、未下载/编译任何二进制。

## 预留方案自证（四台逐行表 + 许可隔离 + 字节数）
四台逐行：hercules-s370（QPL 已核实/S-370 需核实）、openmsx-msx2（GPLv2 已核实）、mini-vmac-macplus（GPL 需核实）、86box-pcxt（GPLv2 已核实）；全部「二进制不进仓」隔离；字节数 2717 > 1200（日志块 2）。README 登记表四台预留态已回写（slots/README.md 新增节）。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：53/53 全 PASS、rc=0（日志块 1）；2. 预留方案自证：四台表 + 许可口径 + 字节数（日志块 2）；3. 封版硬断言：硬断言 FAIL 0 处、rc=0（日志块 3）；4. 漂移（槽位 id/许可口径裁决）见下节。

## 与任务书的漂移
1. **不建 manifest 预留**（任务书两可，选仅登记方案）：预留 manifest（module=null）会出现在 `slot_loader --list`，无后端却可见易误导；待 03 线产包定案后按第二批 SIMH 先例一步建 manifest 转正。
2. 槽位 id 采用任务书建议四项（hercules-s370/openmsx-msx2/mini-vmac-macplus/86box-pcxt）；backend_type 统一 `dedicated`（四台均非既有家族枚举，实装经 manifest 显式 module 转正，不提前扩 BACKEND_TYPE_MODULE）。
3. media_classes 四台全部 [需核实]；mini-vmac 许可版本未定——不预写许可结论（红线遵守）。
4. 门禁日志与 241/246/251-A 共用同一次干净重跑（同批状态）。

---

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 46，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：16 文件；符号池 funcs 146 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 16 个 gd；class_name 6 个；FAIL 0
===== 验收汇总（53 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 46，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：16 文件；符号池 funcs 146 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 16 个 gd；class_name 6 个；FAIL 0
  pkg:*（46 包）        PASS  全部 FAIL 0
结果：53/53 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```

## 验收日志块 2（预留方案自检）

```
（四台逐行表命中 + 字节数）
| IBM System/370 | `hercules-s370` | dedicated（预留） | HERCULES_BIN | third_party/hercules | tape, disk（[需核实]） | QPL 已核实；S/370 支持需核实；GPL/QPL 隔离——二进制不进仓 |
| MSX2（FS-A1） | `openmsx-msx2` | dedicated（预留） | OPENMSX_BIN | third_party/openmsx | cartridge（[需核实]） | GPLv2 已核实；隔离——二进制不进仓 |
| Macintosh Plus | `mini-vmac-macplus` | dedicated（预留） | MINIVMAC_BIN | third_party/minivmac | disk（[需核实]） | GPL 许可需核实；隔离——二进制不进仓；ROM 路径需核实 |
| IBM PC XT | `86box-pcxt` | dedicated（预留） | EIGHTYSIXBOX_BIN | third_party/86box | disk（[需核实]） | GPLv2 已核实；隔离——二进制不进仓；BIOS ROM 路径需核实 |
预留方案: 2717 字节
```

## 验收日志块 3（release_check）

```
项目封版版本 0.1.0（网关版本 0.2.0 · 协议 v2，只读引用）
[PASS] R1 验收基线 53/53 通过（2026-11-20 01:26:06）
[INFO] R3 wip 清单（不计入 rc）：（无）
[PASS] R3 完工包 47 ≥ 30
[PASS] R2 槽位 mame-apple2 已登记后端 gw.emulators.mame_apple2
[PASS] R2 槽位 mame-apple2 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 simh-pdp8 已登记后端 gw.emulators.simh_pdp8
[PASS] R2 槽位 simh-pdp8 run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 槽位 stella 已登记后端 gw.emulators.stella
[PASS] R2 槽位 stella run_status=live（live/dry-run 合法；missing 判 FAIL）
[PASS] R2 第二批槽位 simh-hp2100 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-nova 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 第二批槽位 simh-altair-8800 已转正，run_status=dry-run（live/dry-run 合法）
[PASS] R2 许可记录存在 licenses/MAME.md
[PASS] R2 许可记录存在 licenses/SIMH.md
[PASS] R2 许可记录存在 licenses/Stella.md
[INFO] R4 gw\emulators\mame_apple2.py: 「占位」×1
[INFO] R4 残留扫描完成：命中 1 处（含骨架注记与新发现，只暴露不计 rc）
汇总：硬断言 FAIL 0 处 → rc=0
RELEASE_RC=0
```
