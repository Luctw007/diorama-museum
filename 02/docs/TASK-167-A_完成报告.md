# TASK-167-A 完成报告（02 线）

## 一、交付物

1. `tools/validate/tests/run_catalog_tests.py`：增量新增 3 条 CC-10 反例（默认 WARN / 严格 FAIL / 有值 PASS），不改 CC-01~08 用例；
2. `tools/index/tests/run_registry_tests.py`：新建 id_registry 黑盒测试（5 用例 A~E）；
3. `tools/index/id_registry.py`：`registry_path()` 增加 `ID_REGISTRY_PATH` 环境变量注入（默认行为不变）。

## 二、验收日志（贴证）

```
run_catalog_tests.py：结果 PASS 13，FAIL 0（含 CC-10 三条）
run_registry_tests.py：结果 PASS 5，FAIL 0（A 回填3/B 幂等/C 跳过非法2/D 防撞号000010/E verify）
台账条数：跑测试前 [report] 台账 1582 条 → 跑测试后 [report] 台账 1582 条（未污染）
run_tests.py 回归：结果 PASS 21，FAIL 0
```

## 三、关键说明

- 注入点语义：`ID_REGISTRY_PATH` 非空时 `registry_path()` 返回该绝对路径，否则回退仓库内默认路径。
- 测试覆盖矩阵：rebuild 回填/幂等/跳过非法、allocate --files 防撞号、verify 查重/格式错。

## 四、红线自查

台账条数未变（1582）；假 id 全部写入临时目录；只改 02 线 tools/；无二进制/网络。
