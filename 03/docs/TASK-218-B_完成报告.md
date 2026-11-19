# TASK-218-B 完成报告 · 第二批收官档案

> 03 线 · 第二批首批 11 台收官档案（只读核对 + 归档，不产包、不改目录 jsonl）。

## 一、交付物

- `docs/catalog/第二批收官档案_v1.md`：**4,264 字节**（>1500），四节齐全（11 台产包总览 / 图鉴短卡收口核对 / 需核实清单汇总 / 收官声明）。
- 总览表 **11 台逐行齐**，emulator 口径与各包 runtime.json 实测一致。

## 二、验收日志（第 4 章）

**1. 档案字节数**
```
4264 字节（>1500）
```
**2. 总览表自检**
```
总览表 11 台（grep 计数 11 行）；emulator 口径：none×5（nokia-3310/univac-1/cdc-6600/cray-1/sparcstation-1/nokia-8110）· simh×3（altair/nova/hp2100）· uae×1（amiga-1000）· mame×1（apple-iie 05 线）
```
**3. 图鉴短卡收口自检**
```
第二批首批卷 §一 9 台来源列「需核实」残留 = 0（S94–S115 / S58–S59 已回填）
Nokia 3310 短卡待补 = 1 项；Apple IIe 短卡 = 05 线管辖（不代写）
```
**4. verify_all --daily --cache（40/41 通过，rc=1）**
```
结果：40/41 通过
catalog_ref  FAIL 1  →  [REF-02] 完工包 hp-2100 无目录反链
```

## 三、跨线发现（如实记录）

`verify_all --daily --cache` 报 **catalog_ref FAIL 1**（REF-02：完工包 hp-2100 无目录反链）。根因查明：

- **01 线 monorepo 镜像**（`work/01/repo/03/docs/catalog/计算机大类_目录_v2.jsonl`）里 hp-2100 条目仍是 `status=planned, device_id=null`——**镜像目录未同步** 03 线 188-A 的目录回填（sync_content.py 滞后）。
- **03 线活跃目录**里 hp-2100 条目已是 `status=done, device_id=hp-2100, research_doc=10_HP2100.md`（正确）。
- **贴证**：02 线 `catalog_ref_check.py`（直扫 03 线活跃目录）REF-02 反链缺失 **0**、REF-03 台账漂移 0（registry 1583 = 目录 1583）、FAIL 0。

故该 FAIL 为 01 线镜像目录同步滞后导致的误报，**非 03 线真实反链缺失**；待 01 线 `sync_content.py` 同步即可消除。

## 四、需核实汇总

档案 §三 汇总 **11 台**「需核实」项（SIMH 许可 / 模拟器可行性 / 具体参数 / 销量 / 屏幕·重量·尺寸等），逐台可溯至各研究卡/完成报告。

## 五、与任务书的漂移

- 第 4.4 章要求 verify_all「全 PASS、rc=0」，实测 **40/41、rc=1**——唯一 FAIL 为 01 线镜像目录未同步（REF-02 hp-2100），非本任务新增缺陷，已用 02 线 catalog_ref_check 直扫活跃目录贴证 REF-02=0。
- 目录文件名按实际为 `通讯与移动大类_目录_v3.jsonl`（任务书简写「通讯大类」）。
- Nokia 3310 图鉴短卡缺失属实记录为「待补」1 项。
