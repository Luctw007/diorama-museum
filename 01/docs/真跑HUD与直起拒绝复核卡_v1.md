# 真跑 HUD 与直起拒绝复核卡 v1（docs/真跑HUD与直起拒绝复核卡_v1.md · TASK-321-O）

> TASK-321-O 交付。复核 gateway_client.gd 真跑 HUD 与直起拒绝现状无漂移。只改 01 目录，纯复核，
> **不改 gateway_client.gd、不实机、不启动真跑**。

## ① 现状复核表

| 项 | 现状（源码实况） | 结论 |
|---|---|---|
| 候选标记 | `RUN_CANDIDATE_SLOTS` 四台（hercules-s370/openmsx-msx2/mini-vmac-macplus/86box-pcxt）+ HUD「真跑候选」标记行（281-A 未动） | ✓ 无漂移 |
| 直起拒绝 | `request_direct_launch` 四台预留态恒 false + 「直起拒绝：…待产包定案+用户编译二进制」提示（281-A 未动） | ✓ 四台预留槽位拒绝口径无漂移 |
| 音频降级 | `_apply_audio` 占位 WAV 降级路径 + HUD 音频状态行（113 未动） | ✓ 无漂移 |
| HUD 状态行 | `_set_status`/`_set_info` 状态行 + 311-G 新增 `_handle_status` status 行 | ✓ 无漂移 |

## ② 结论

- **直起拒绝四台预留槽位口径无漂移，HUD 行无漂移**：gd_symbol_check + gd_naming_check 复跑 MISS 0 / FAIL 0（见 321-O 报告日志块）。

## ③ 与 291-M 漂移核对

- **无漂移**：291-M 真跑 HUD 收口核对口径（候选标记行/音频状态行/直起拒绝提示）与当前源码一致；311-G 的 status 行增补属其后轮次（已入 311-G 报告），不在 291-M 漂移面。
- 转正后变化预期：四台转正/二进制就位后 request_direct_launch 仍恒 false（283-A 口径「接真实启动链待 F-13 后专门轮次」），直起拒绝提示文案随产包定案更新——属预期变化非漂移。
