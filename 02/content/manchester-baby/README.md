# 曼彻斯特婴儿（SSEM）（manchester-baby）

> 设备包骨架（由 `scaffold_device.py` 生成，TASK-07）。**内容填写由后续任务负责。**

## 元数据

- device-id：`manchester-baby`
- 名称：曼彻斯特婴儿（SSEM）
- 年代：1948
- 规范版本：0.2

## 待办（作者填写）

1. 在 `meta.json` 补充 `intro`/`description`/`sources`（来源 URL 示例格式见下）。
2. 在 `assemblies/`、`meshes/`、`materials/`、`sounds/` 放入真实资产。
3. 在 `annotations/annotations.json` 补充 role/flow/anim 标注（anim 可含 timeline）。
4. 在 `runtime.json` 与 `meta.json.runtime` 同步填写真实的模拟器与 sinks/input_map。
5. 更新 `THIRD_PARTY.md` 许可清册。

## sources 条目示例（填入 meta.json 的 sources 数组）

```json
{
  "type": "documentation",
  "title": "来源标题",
  "url": "https://example.com/source",
  "license": "public_domain",
  "accessed_at": "2026-10-31"
}
```

## 校验

```bash
python tools/validate/validate.py content/manchester-baby
```
