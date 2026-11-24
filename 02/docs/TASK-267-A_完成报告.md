# TASK-267-A 完成报告

> 任务：第三批 allocate 预案卡（id 分配预案，待用户点头后执行）（02 线）。执行账号：02 线（规范/台账）。
> 只改 02 目录，纯文档预案，不 allocate、不改目录 jsonl、不产包。

## 一、交付物清单

1. 新增 `docs/第三批allocate预案_v1.md`（5876 字节）：10 台 device_id + 目录 id 分配预案表（10 行）+
   id 命名规则核对 + 无冲突核对 + 目录归属预案 + allocate 执行清单 + 待点头依赖声明 + 红线自查。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复跑

```
verify_all --daily --cache
  ...
  结果：54/54 通过
验收缓存已写 ...\01\docs\verify_last.json
退出码 rc=0
```

### 2.2 预案卡自证

```
字节数：5876（>3000 达标）
分配预案表 10 行命中（#1 System/370 … #10 Apple Newton）
id 无冲突核对：现有 ready 包 47 个；10 个新 device_id 冲突 0；全部 kebab-case slug ✔
```

### 2.3 改动清单自证（本任务只新增，未改任何目录 jsonl）

```
新增 docs/第三批allocate预案_v1.md（5876 字节）
新增 docs/TASK-267-A_完成报告.md
改动目录 jsonl：0（未 allocate、未回填、未碰 03/05 线目录）
```

## 三、结论

第三批 allocate 预案已出：10 台 device_id（kebab-case）+ 目录 id（C-MF/C-PC/C-WS/C-EC/M-PD 五组续接序号）
+ 目录归属（9 台计算机 v2 + 1 台通讯 v3）+ allocate 执行清单（用户点头后 6 步）。10 个 device_id 与现有
47 包无冲突。**点头前不执行**，待用户点头后按预案落地。

## 四、与任务书的漂移（如实）

1. **续接序号为「预案值」非「最终值」**：预案按 registry 各前缀最大序号 +1 起算（C-MF-000085 / C-PC-000209~214 /
   C-WS-000055 / C-EC-000014 / M-PD-000070），实际 allocate 时由 id_registry 按「台账 ∪ 目录已用 id」续号，
   若目录已用 id 超出本预案序号会自动跳过，**以 allocate 实算为准**——预案卡已声明，不算臆造。
2. **任务书「现有 47 包无冲突核对」实测吻合**：门禁 47 ready 包，10 个新 device_id 无重复；并额外区分
   易混项（system360≠ibm-system370、macintosh128k≠macintosh-plus、ibm5150≠ibm-pc-xt）。
3. 其余无实质漂移：device_id 与 03 线口径卡/252-B 建议 id 完全对齐。

## 五、红线自查

零联网、零下载（纯文档预案）；id 命名以 id_registry ID_RE + 47 包实账为准，未臆造；只改 02 目录、未 allocate、
未改任何目录 jsonl、未改 01/03/04/05 线、未产包。
