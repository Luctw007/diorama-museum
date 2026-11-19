# TASK-252-B 完成报告

> 任务：第三批首批产包验收清单（10 台逐台验收口径）（02 线）。执行账号：02 线（验收口径）。
> 只改 02 目录，纯验收清单，不产包、不 allocate id、不改目录 jsonl。

## 一、交付物清单

1. 新增 `docs/第三批产包验收清单_v1.md`（5122 字节），含：
   - ① 10 台逐台总表（目录 id 占位 / 包 id 建议 / 产包顺序 / validate 预期 / model_check / emulator 口径 /
     反链回填）——ibm-system370、msx2、macintosh-plus、ibm-pc-xt、acorn-archimedes、sinclair-zx81、
     sgi-indigo、compaq-portable、whirlwind、apple-newton 共 10 行；
   - ② 每台产包完成判据（四道验收命令 + rc=0）；
   - ③ 逐台 emulator 口径要点（4 台具体名 + 6 台 none）+ 分档（7 A + 3 B）；
   - ④ 与任务书的漂移 + 红线自查。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复测（verify_all --daily --cache）

```
== [catalog_ref] scripts/catalog_ref_ci.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
...
结果：49/49 通过
验收缓存已写 ...\01\docs\verify_last.json
退出码 rc=0
```

### 2.2 清单自检

```
10 台逐行齐（#1 ibm-system370 … #10 apple-newton，共 10 行）        — 命中
四道验收命令列齐：
  1) validate.py <包>                → 0 FAIL（rc=0）
  2) model_check.py <包>             → FAIL 0 / WARN 0（rc=0）
  3) catalog_ref_check.py            → REF-01~04 全 0、FAIL 0（rc=0）
  4) 目录反链 device_id=<包 id> + status=done → 复跑 REF-02 缺失 0    — 命中
字节数：5122（>1500 达标）
```

## 三、结论

第三批首批 10 台验收口径已成型：三档硬底线（validate 0 FAIL / REF 四查 0 / THIRD_PARTY 三件套 / id 唯一 /
反链 REF-02）不降，分档只区分生产深度（7 A + 3 B）；4 台模拟器口径明确（hercules QPL、openmsx GPLv2、
86Box GPLv2、mini-vmac GPL 需核实），6 台 none 记 THIRD_PARTY 候选、缺失作 NOTE 级提示不算缺口。

## 四、与任务书的漂移（如实）

1. **包 id 为 kebab-case 建议值（非权威）**：产包时以 02 线 id_registry allocate 的目录真 id + 内容包 meta.id
   为准（meta.id 即目录 device_id，参考第二批 `altair-8800`/`sparcstation-1`）。
2. **validate「PASS 数」为参考值（约 78/84）**：硬底线是 0 FAIL；实际 PASS 数随件清单
   （assemblies/annotations）浮动，本清单不臆造精确 PASS 数。
3. **反链第 4 道依赖定案四步**（用户点头 → 01 线登记 → 02 线 allocate 10 真实 id），本清单只给占位 `0xx`
   待换真号，不 allocate——与任务书边界一致。
4. 补充：6 台 none 中 **Whirlwind 明确「无候选」**，其余 5 台有候选（Arculator/EightyOne/MAME/86Box/Einstein），
   已逐台如实标注，不虚构模拟器。

## 五、红线自查

零联网、零下载（纯验收清单）；口径以 242-A/227-B/校验器实测为准，未臆造；只改 02 目录、不产包、不 allocate、
不改 03 线目录 jsonl、不改校验器代码。
