# TASK-212-B 完成报告

> 任务：第二批全量过闸实测终测 + 过闸总表。执行账号：02 线。只改 02 目录，纯复跑 + 总表。

## 一、交付物清单

1. 新增 `docs/第二批过闸总表_v1.md`（11 台逐行：目录 id / 包 id / 分档 / validate / model_check / 反链 /
   emulator / 状态）。

## 二、验收日志（原始输出 + 退出码）

已产 10 台逐台 validate：

```
nokia-3310         总计 84 条：PASS 84，FAIL 0
altair-8800        总计 84 条：PASS 84，FAIL 0
data-general-nova  总计 84 条：PASS 84，FAIL 0
hp-2100            总计 84 条：PASS 84，FAIL 0
univac-1           总计 78 条：PASS 78，FAIL 0
cdc-6600           总计 78 条：PASS 78，FAIL 0
cray-1             总计 78 条：PASS 78，FAIL 0
apple-iie          总计 80 条：PASS 80，FAIL 0
amiga-1000         总计 84 条：PASS 84，FAIL 0
sparcstation-1     总计 84 条：PASS 84，FAIL 0
```

model_check（10 台均 LOD1 观察档，FAIL 0 / WARN 0）：

```
nokia-3310 / altair-8800 / data-general-nova / hp-2100 / amiga-1000 / sparcstation-1 / apple-iie  各 6 网格
univac-1 / cdc-6600 / cray-1  各 5 网格
```

全量 catalog_ref 复跑：

```
内容包 40 个，目录条目 1583 行
REF-01 悬空包引用：0 条
REF-02 反链缺失：1 个（sparcstation-1 无目录反链）
REF-03 台账漂移：registry 1583 / 目录使用 1583（未使用 0）
REF-04 关联包形态非法：0 条
FAIL 1
```

门禁只读复测：

```
verify_all --daily --cache
  结果：41/41 通过（rc=0）
```

## 三、过闸总表结论

**11 台 = 已产 10 台（9 台过闸 + 1 台 SPARCstation 1 反链待回填）+ 待产 1 台（Nokia 8110，口径卡已出）**。
validate 已产 10 台全部 0 FAIL，model_check 全部 0 FAIL/0 WARN。

## 四、与任务书的漂移

1. **已产 10 台（非 9 台）**：SPARCstation 1 已产（84 PASS/0 FAIL），是执行期间新入共享盘的第 10 台。
2. **待产仅 Nokia 8110 1 台**（非 2 台收尾）。
3. **REF-02 缺失对象 = sparcstation-1**（反链缺失随新产包滚动，前几轮 cdc-6600/cray-1/amiga-1000 均已补）。
4. **目录条目 1583 行**（Apple IIe `C-PC-000208` 已回填，REF-03 台账漂移归 0）。

## 五、红线自查

零联网、零下载（纯校验复跑）；未改 03/05 线内容包/目录（只读复跑）；复跑 FAIL 如实记录并标归属（仅
sparcstation-1 反链待回填，属 03 线职责，非校验器缺陷）。
