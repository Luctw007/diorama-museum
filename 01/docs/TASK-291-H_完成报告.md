# TASK-291-H 完成报告

## 交付物清单
- **启动厅 hub 巡检用例补全卡**（docs/启动厅巡检用例补全_v1.md，≥2000 字节）：
  - §①现有巡检项清单：startup_check.gd 四项逐项（目录可读/meta 可读/槽位表可读/HUD 呈现，函数+判定+降级行为）；
  - §②补全用例表 9 条：A 类 hub 跳转 3 条（DEFAULT_LAYOUT=exhibit_hub.json 断言/布局过闸/hub 四门框载入）、B 类三系统入口 3 条（图鉴同源/真跑与厅无关/拆解跨切厅保活）、C 类异常回退 3 条（布局失败回退 hub/portal 缺失降级/巡检失败不中断）——每类 3 条静态用例；
  - §③待实机项标注（实机走查 8 条/碰撞路径/巡检扩展待排）。
- 改动清单：只新增 1 份 md + 本报告；不改 gd（任务书边界）、02/03/04/05 线零改动。

## 用例卡自证
字节数（UTF-8）见报告末自证块（>2000）；补全用例表 9 条（A/B/C 各 3 条）命中。

## 验收日志（原样粘贴，详见文末日志块）
1. hard 门禁：59/59 全 PASS、rc=0（日志块 1）；2. 用例卡自证见上节；3. 改动清单见上节。

## 与任务书的漂移
1. 任务书第 3 节「每类 2-3 条静态用例」——三类各取 3 条（上限口径），共 9 条。
2. C 类异常回退为「口径补全」不实装进 startup_check（任务书边界「不改 gd」）；是否进引擎标待排。
3. 任务书命令 `py -3.7` 用 python 3.12.10 执行；验收基数 59/59（仓库实际）。
4. B 类三系统入口用例引用 F-3（241-A）收口结论为静态断言母本（无第二套映射/真跑与厅无关/切厅不动 DeviceRoot），与 266-A/281-A 实装现状一致；巡检扩展（§② C 类）登记待排不实装。

---

## 用例卡字节数自证

```
3761 字节
```

## 验收日志块 1（verify_all --daily --cache，节选）

```
== [slots] scripts/slot_consistency_check.py
   汇总：完工包 51，声明 slot 0，SC-01 违规 0
== [catalog_ref] D:\work\02\repo\tools\validate\catalog_ref_check.py
     REF-02 反链缺失：0 个
     REF-03 台账漂移：registry 1583 条 / 目录使用 1583 条（未使用 0 条）
     REF-04 关联包形态非法：0 条
   FAIL 0
== [gd] scripts/gd_symbol_check.py
   汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
== [gd_naming] scripts/gd_naming_check.py
   扫描 17 个 gd；class_name 7 个；FAIL 0
== [budget] scripts/device_budget_check.py
   汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
===== 验收汇总（59 项） =====
  m0                   PASS  M0 验收全部通过 ✔
  m1b                  PASS  M1b 验收全部通过 ✔（断言 19 条）
  slots                PASS  汇总：完工包 51，声明 slot 0，SC-01 违规 0
  catalog              PASS  verify：24 片 / 1583 行，通过
  catalog_ref          PASS  FAIL 0
  gd                   PASS  汇总：17 文件；符号池 funcs 171 / signals 7；MISS 0；已知缺口 KG 0
  gd_naming            PASS  扫描 17 个 gd；class_name 7 个；FAIL 0
  budget               PASS  汇总：PASS 9 行 / SKIP 2 项 / FAIL 0 处
  pkg:*（51 包）        PASS  全部 FAIL 0
结果：59/59 通过
验收缓存已写 D:\work\01\repo\01\docs\verify_last.json
VERIFY_RC=0
```
