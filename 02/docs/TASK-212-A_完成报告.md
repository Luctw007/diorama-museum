# TASK-212-A 完成报告

> 任务：第二批收尾两台过闸口径卡（SPARCstation 1 + Nokia 8110）。执行账号：02 线。只改 02 目录，纯口径卡。

## 一、交付物清单

1. 新增 `docs/第二批收尾两台过闸口径卡_v1.md`（9335 字节，两台三问三答 + 建议写法 + 落地清单 + 漂移）。
2. 改 `docs/第二批分档验收口径_v1.md` §二补记「S 档第二批收尾两台口径登记（TASK-212-A 引用）」（§二已覆盖
   S 档无成熟模拟器形态，故只登记引用、不另立档位）。

## 二、验收日志（原始输出 + 退出码）

口径卡字节数自检：

```
9335（>600 达标）
```

门禁只读复测（预期全 PASS、rc=0）：

```
verify_all --daily --cache
  结果：41/41 通过（rc=0）
```

## 三、两台三问三答结论（摘要）

| 台 | emulator 写法 | 分档 | 校验器放行 |
|---|---|---|---|
| SPARCstation 1 | `emulator="none"`（QEMU sparc 需核实、无 bone 不写 qemu） | S 档 | 已放行 none，无需改码 |
| Nokia 8110 | `emulator="none"`（无成熟模拟器，静态+滑盖动画） | S 档 | 已放行 none，无需改码 |

## 四、与任务书的漂移

1. **SPARCstation 1 已产**（非「待产」）：`03/repo/content/sparcstation-1/` 已存在，`emulator="none"`、
   `media_hint="disk"`、6 件 gltf、validate 84 PASS/0 FAIL 已过闸，但**缺 encyclopedia.md** 且**目录反链
   未回填**（catalog_ref REF-02 缺失对象）。本卡口径与已产实况一致，仅补记两处待办。
2. **Nokia 8110 仍待产**，本卡为其产包前口径卡。
3. **media 口径澄清**：任务书「media 无介质形态」实为物理形态描述，落地 `media_hint="firmware"`
   （参照 nokia-3310 先例），不取 `media_class="none"`。

## 五、红线自查

- 零联网、零下载（纯口径卡）；未改 03/05 线文件、未改校验器代码；结论以 208-B 裁决/研究卡/schema 实测为依据。
