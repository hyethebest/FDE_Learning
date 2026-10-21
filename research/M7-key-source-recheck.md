# M7 密钥题来源追加复核（AI 执行）

复核日期：2026-10-09；作者：safety。涉及 FDE-M7-062、063、098、099。

## 初次读取证据的限制

本轮能读取的历史上下文及 M7-sources.md 没有保留 598/37140 初次读取的 tool ref 或原始正文。因而无法证明最初实际读取了完整正文，也无法确证最初仅用了搜索摘要；不能凭此前总结里的“已读”断言。旧清单的笼统声明不能作为原始访问证据。

## 本轮访问结果

- 原国内官方页 https://cloud.tencent.com/document/product/598/37140 ：直接 open（turn251view0）、从40488的下一篇链接进入（turn254view0）、从123925的禁用链接进入（turn257view1），均仅返回 1 行 Timeout 错误，无正文，不计访问成功。
- 搜索结果 turn252search1、turn255search1、turn259search1 是摘要，不能等同完整正文。
- 普通 urllib 请求失败于域名解析，未取得页面。浏览器 iab 不可用，Chrome 两次返回无法加载 request-header policy；均未得到页面，不计成功。
- 国际站官方 https://www.tencentcloud.com/zh/document/product/598/32675 通过 open 成功，turn260view0 共410行，页面版本2026-07-07 18:13:14。L337明确子账号密钥禁用拒绝所有请求；L353先禁用、L361删除不可恢复。该页是国际站文档，未作为国内站事实自动替代，未加入正式题源；其密钥前缀、访问日志延迟等细节与国内资料存在地域版本区别。

## 正式替代证据与逐题支持

| 题号 | 本轮实际打开的官方正文 | 工具证据/版本 | 直接支持的事实与改动 |
|---|---|---|---|
| 062 | https://cloud.tencent.com/document/product/598/96157 | turn253view0，66行，L19版本2023-11-28 15:41:02；L30、35 | 公告明确适用于主账号和子账号，SecretKey仅创建时查看保存。题干、答案不变，仅换源。 |
| 063 | https://cloud.tencent.com/document/product/598/40488 | turn253view1，198行，L19版本2026-05-09 14:18:52；L105—107、L48 | 禁用主账号密钥后拒绝其所有请求。为避免将主账号流程套至子账号，题干收窄为清理已有主账号密钥；保留禁用效果学习目标及答案C，并说明不建议日常新建使用主账号密钥。 |
| 098 | https://cloud.tencent.com/document/product/598/123925 | turn255view0 / turn256view0，85行，L19版本2025-10-10 14:53:52；L58—64 | 轮转子用户密钥，先切换业务，再禁用旧密钥、观察正常后删除。题干限定轮转建议，D改为完整建议；不声称API强制禁用前置条件。 |
| 098 | https://cloud.tencent.com/document/product/598/82369 | turn253view2，150行，L19版本2025-09-12 01:18:08；L40—41、59—61 | 删除访问密钥不可恢复；操作对象是指定AccessKeyId，不是删除账号资源。答案仍C、D。 |
| 099 | https://cloud.tencent.com/document/product/598/40488 | turn253view1，L36—44 | 操作场景给出API密钥通用字段职责，SecretId标识、SecretKey验证；题干、答案不变。 |

另读取国内更新访问密钥 API（turn257view0，2025-09-12 01:17:55，https://cloud.tencent.com/document/api/598/82368），仅证明 Active/Inactive 状态参数，并不直接写明全部请求拒绝，因此没有把它当作063答案的充分证据。

审查结论：以上区分了访问成功和事实支持；四题已改为本轮能实际打开且适用范围明确的国内官方正文。旧版hash和新版hash保存在 M7-key-source-recheck-hashes.json。作者不自批。foundations_modes 已实际重新打开四个国内官方页面并独立AI复审4/4通过，见 research/reviews/M7-key-source-recheck.json；四项审批hash已与当前题库核对一致，原审校文件保留。此次为AI审校，不是人工专家背书。
