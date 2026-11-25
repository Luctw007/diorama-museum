# TASK-306-O 完成报告

> 任务 306-O（01 线）：第三批产包 · 槽位登记方案卡 v1（只设计不落地）。状态：完成。

## 交付物清单

- `D:\work\01\repo\01\docs\第三批槽位登记方案卡_v1.md`（新增，2992 字节 ≥1200）：①四台 backend_type→module 映射方案（hercules-s370/openmsx-msx2/mini-vmac-macplus/86box-pcxt，后端模块标「预留 null」）；②manifest 字段模板（slot_id/backend_type/module/device_class/media_classes/binary_hint 标需核实）；③release_check R2 第三批判定方案（先 dry-run，二进制就位后 live）。
- `D:\work\01\repo\01\docs\TASK-306-O_完成报告.md`（本报告）。

## 方案卡自证

- 字节数：2992（>1200 达标）。
- 四台映射：backend_type 建议值 hercules/openmsx/minivmac/86box（均标 [需核实]），module 一律预留 null，许可隔离照 301-O（QPL/GPLv2/GPL 需核实/GPLv2）。
- manifest 字段模板以 simh-hp2100 现有 manifest 为参照、对齐 slot_loader.resolve_entry 契约（module 显式声明含 null=预留优先于 BACKEND_TYPE_MODULE；media_class 枚举 MEDIA_CLASSES；binary_hint 可指 third_party）。
- R2 第三批判定四步：预留 missing 放行 → 转正 dry-run 合法 → 二进制就位 live → 阈值上调由后续任务更新判定集合。

## 与任务书的漂移

1. 四台 backend_type 为**建议值**（现有 BACKEND_TYPE_MODULE 无这四类映射，全部标 [需核实]），落地时按实际命名定案——不臆造已定名。
2. 方案卡含一个 manifest 字段模板 JSON 示例（任务书列字段、未要求示例，示例为模板成文所需）。
3. 执行备注：只设计不落地（未建 manifest、未改 slot_loader/release_check）；验收命令按仓库实际用 `python`；slot_loader --list 复跑确认四台未注册，日志见下。
4. 方案卡 §④「等用户点头产包 + 二进制来源核实后由后续任务落地」与 306-P 核对卡触发条件一致，两卡联动闭环。
5. R2 第三批判定方案四步全部按现有 release_check 判定函数（run_status_of 口径）推导，未预改代码。

## 验收日志

```
== verify_all --daily --cache（尾部）==
结果：61/61 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0

== slot_loader.py --list（节选：四台仍未建 manifest）==
mame-apple2        OK(二进制就位)   ...
simh-altair-8800   MISSING(无二进制)  ...
simh-hp2100        MISSING(无二进制)  ...
simh-nova          MISSING(无二进制)  ...
simh-pdp8          OK(二进制就位)   ...
stella             OK(二进制就位)   ...
介质目录 0 个：（空，红线下仅建目录）
SLOT_RC=0
```
