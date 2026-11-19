# TASK-182-B 完成报告：第二批新包真实过闸实测 + 分档口径反向校准

> MIT License — Copyright (c) 2026 箱庭电子博物馆项目组（Hako Electronic Museum Project）。本文档按 MIT 许可分发。

## 一、交付物清单

| # | 路径 | 状态 | 说明 |
|---|---|---|---|
| 1 | `docs/第二批包过闸实测记录_v1.md` | 新建 | 两包实测 + 对照表 + 4 校准建议，1532 汉字 |

## 二、实测结论

- **两台第二批包均真实 0 FAIL 过闸**：nokia-3310（B 档）84 PASS / 0 FAIL、altair-8800（S 档）
  84 PASS / 0 FAIL；`verify_all --only` 各自 1/1。
- **三档公共硬底线逐项实测一致**：validate 0 FAIL / REF 四查 0（32 包 1582 条）/ THIRD_PARTY 三件套 /
  id 唯一 / 反链 REF-02 全 0。
- **口径"两端"验证通过**：S 档全规格（altair-8800 含 flow 11 条 + encyclopedia 2542 字）与 B 档
  最小件（nokia-3310 emulator="none" 静态）均 0 FAIL 过闸。

## 三、4 条校准建议（只写建议，不改口径本体）

1. 补 S 档"有模拟器声明但未登记槽位"中间态（altair-8800 emulator=simh-altair8800 但 slot=None）；
2. 明确 B 档"最小件"是下限不是上限（nokia-3310 远超最小件仍 0 FAIL）；
3. encyclopedia NOTE 分支待用缺百科包验证是否真只提示；
4. assemblies 装配体数与 gltf 数一致性（7 装配体 6 gltf 是合法常态，非缺件）。

## 四、验收贴日志

### 4.1 关键字抽查（8 关键字全命中）

```
validate 6 · catalog_ref 1 · REF-02 4 · S 档 5 · B 档 7 · WIP 1 · emulator 6 · 校准建议 5
```

### 4.2 文件与字数

```
文件字节：6304（>600 ✓）
汉字(CJK)字数：1532（≥1500 ✓）
```

### 4.3 实测命令输出（节选，全文见实测记录 §一）

```
validate nokia-3310   → 总计 84 条 PASS 84 / FAIL 0
validate altair-8800  → 总计 84 条 PASS 84 / FAIL 0
catalog_ref_check     → 内容包 32 个，REF-01~04 全 0，FAIL 0
pkg_registry --list   → 共 32 包（ready 32 / wip 0）
verify_all --only pkg:nokia-3310  → 1/1
verify_all --only pkg:altair-8800 → 1/1
```

### 4.4 门禁交叉复验

```
结果：38/39 通过
```

**留底说明（偏差）**：任务未写具体基线数字，但父任务口径写"39/39"；实测 **38/39**——唯一失败步骤
`catalog`（rc=1、306 重复 id），根因 monorepo 镜像 v2/v3 并存（robocopy `/E` 只增不删），与本任务
无关，执行前后均 38/39，零回归。

## 五、红线自查结论

1. 不下载 ROM/二进制/版权文件 ✓（只跑校验器读现有包）；2. 不编造史实 ✓（只记录校验器输出）；
3. 只改 02 目录 ✓（仅新增 1 文件）；4. 不否决存量 ✓（只记录不整改）；
5. 不改分档口径文件本体 ✓（校准建议以"建议"写入实测记录）；6. 禁低质产出 ✓（贴全部命令日志 + 字数达标）。
