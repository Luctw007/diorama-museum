# TASK-222-B 完成报告

> 任务：镜像收口口径 v2（待镜像终版清单 + 收口后校验步骤）。执行账号：02 线。只改 02 目录，纯文档，不执行镜像。

## 一、交付物清单

1. 新增 `docs/镜像收口口径_v2.md`（5979 字节），含 ①待镜像 12 台终版清单（第二批 7 台 ready + 家电影音
   5 台 WIP）②镜像同步要求（内容包 + 目录 jsonl 反链同步、消除 hp-2100 stale）③收口后校验步骤（sync 后
   hard 门禁预期 48 步全 PASS）④WIP 五台处置口径。

## 二、验收日志（原始输出 + 退出码）

### 2.1 门禁只读复测

```
verify_all --daily --cache
  catalog_ref          FAIL  FAIL 1
结果：40/41 通过（rc=1）
```

### 2.2 口径 v2 自证（11/12 台清单 + 步骤）

```
字节：5979（>1000 达标）
待镜像终版清单：第二批 7 台 ready（univac-1/cdc-6600/cray-1/amiga-1000/apple-iie/sparcstation-1/nokia-8110）
              + 家电影音 5 台 WIP（crt-tv/cd-player/dvd-player/vhs-vcr/walkman-tpsl2）
收口后校验：sync 后 hard 门禁预期 48 步全 PASS、catalog_ref REF-02 归零、ci 包装器 FAIL 归零
WIP 处置：不入 ready、不阻塞门禁
```

## 三、镜像收口结论摘要

- **7 台 ready** 全反链 done，可直接镜像（内容包 + 目录 jsonl 同步）；镜像后门禁从 41 步增至 **48 步全 PASS**。
- **hp-2100 stale 是本轮关键修复点**：镜像目录 hp-2100 仍 `planned/device_id=null`（共享盘已 done），是
  catalog_ref FAIL 1（40/41）根因，收口时必须用共享盘最新目录 jsonl 覆盖镜像。
- **5 台 WIP** 无 meta.json，镜像后不进 ready、不阻塞门禁。

## 四、与任务书的漂移

1. **待镜像 12 台（非 11 台）**：任务书「家电影音 4 台（crt-tv 已产 + 3 WIP）」，实测 **5 台全部 WIP**
   （crt-tv 亦无 meta.json、非"已产"），且执行期间 05 线新增 **cd-player** WIP 目录，故 5 台 WIP。
2. **hp-2100 stale 确认仍在**（连续多轮）：门禁 40/41 的 catalog_ref FAIL 1 即此，收口时须一并修复。
3. 本任务只改 02 目录、不执行镜像（收口由统筹统一做），门禁 40/41 属镜像 stale、非本任务回归。

## 五、红线自查

零联网、零下载（纯文档）；不执行镜像/同步；清单以实测（2026-11-19 diff）为准，未臆造；未改 01/03/05 线文件。
