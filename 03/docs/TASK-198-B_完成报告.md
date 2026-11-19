# TASK-198-B 完成报告

> 第二批第 8 台 Apple IIe 单独研究卡（产包备料，不产包/不改目录 jsonl/不 allocate id）。

## 交付物

| 件 | 路径 | 规模 |
|---|---|---|
| 研究卡 | `docs/research/hall-personal-batch2/11_AppleIIe.md` | 4,989 字节，七节齐全（证据 S116–S118） |
| 证据索引回填 | `hall-personal-batch2/05_证据包索引.md` | 追加 S116–S118 |

## 验收日志

- **研究卡字节数**：11_AppleIIe.md = 4,989 字节（>1200）。
- **五要素自检**：史实（§一）/ 尺寸依据（§二）/ 部件分解草图（§三）/ 模拟器行（§五）/ 出处清单（§六）齐备，另含 L1-L3 拆解（§四）与展呈叙事建议（§七）。
- **门禁只读复测**：`catalog_ingest.py --from-work --gate` → **摄取 5 文件 1582 行，错误 0**（本任务不改 jsonl，零回归）。

## 目录 id 占位说明

Apple IIe 在 03 线计算机目录 v2 中**无单独条目**（仅有 Apple II / II Plus / IIc / III / IIGS），本卡目录 id 为占位 **`C-PC-0000xx`**，正式生产时由 02 线 id_registry `allocate` 分配真实 id。本任务不产包、不改目录 jsonl、不 allocate id。

## 模拟器行结论

MAME 驱动（apple2e）为候选模拟后端，许可「需核实」，槽位 dedicated 预留，不下发二进制。**红线**：Apple IIe 的 ROM（Monitor ROM + Applesoft BASIC）受版权保护，不入库、不下载，只清单级引用。

## 需核实清单

尺寸、主频、内存规格、销量、MAME 驱动许可均已标「需核实」。
