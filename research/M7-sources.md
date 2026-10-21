# M7 安全合规与责任 AI — 冻结来源与配额

核实日期：2026-10-09；作者 safety；目标 100 题（67 单选、33 多选）。所有问题是原创模拟题，非真题。以下产品事实与题目中的工程判断分开：事实以页面对应章节为准；场景推理仅把事实应用到题设，不推断未声明的安全保证。

## 子考点配额

| 子考点 | 题数 |
|---|---:|
| 平台成员、功能/数据权限及企业空间边界 | 20 |
| 应用端知识隔离与外部授权 | 13 |
| 内容风险、关键词、隐私脱敏 | 13 |
| 授权凭证、密钥生命周期及签名 | 18 |
| Skills 安全审核与共享边界 | 6 |
| 浏览器/远程执行责任、AI 输出风险 | 14 |
| 临时存储权限及接口鉴权 | 6 |
| 最小权限、身份安全、审计证据 | 10 |

## 已核官方正文

以下记录出题时的来源清单；37140 的初次完整正文读取缺少可恢复工具证据，本轮访问持续超时，已撤出正式题源并补核四题，详见 M7-key-source-recheck.md。其余记录沿用原研究与独立审校；每页仅摘要独立支持事实，不复制样题。

- https://cloud.tencent.com/document/product/1759/122574 《平台端用户权限》，2026-07-10。空间级用户/角色/权限；用户和角色授权并集；功能权限与数据权限区分；高级自定义可细分操作。
- https://cloud.tencent.com/document/product/1759/119281 《应用端用户权限说明》，2026-02-26。应用隔离；角色知识范围并集；visitor_biz_id；外部系统逐切片过滤；Multi-Agent 不支持。
- https://cloud.tencent.com/document/product/1759/125070 《内容安全》，2025-11-14。输入输出风险检测、模型与关键词、不可关闭底线模型、词库匹配、应用脱敏。不采用已过时的灰度/计费预测。
- https://cloud.tencent.com/document/product/1759/122569 《企业、工作空间与权限概述》，2025-11-14。企业下独立空间、空间隔离、成员与功能/数据权限。
- https://cloud.tencent.com/document/product/1759/122570 《企业管理》，2026-07-10。企业用户与首次访问范围；默认空间或等待管理员添加。
- https://cloud.tencent.com/document/product/1759/138107 《授权凭证》，2026-09-14。个人及企业共享凭证权限；引用影响；凭证变更/撤销风险；不明文展示。
- https://cloud.tencent.com/document/product/1759/129561 《Skills 介绍》，2026-07-14。内置安全审核，自定义扫描，企业共享审批沿用安全报告。
- https://cloud.tencent.com/document/product/1759/132714 《ADP 浏览器助手插件服务协议》，2026-06-10。指令触发页面读取；凭证、AI 偏差、不可逆操作、第三方访问限制；不保证输出准确性。
- https://cloud.tencent.com/document/product/1759/128396 《Lighthouse OpenClaw Connector 插件服务协议》，2026-02-11。执行环境由用户负责；自定义模型授权/内容风险；凭证管理；必要调度日志。
- https://cloud.tencent.com/document/product/1759/116238 《操作 cos 指南》，2026-08-05。平台内置存储与临时密钥；按场景配置；禁止跨场景混参。
- https://cloud.tencent.com/document/product/1759/105050 《获取文件上传临时密钥》，2026-04-28，旧版 API 2023-11-30。参数组合决定权限；有效期与路径；试题显式注明旧版接口上下文。
- https://cloud.tencent.com/document/product/1759/105109 《签名方法 v3》，2024-12-25，旧版 API 栏目。V3 签名身份与完整性，不推断新版本接口地址。
- https://cloud.tencent.com/document/product/1759/127284 《ADP 文档解析协议》，2026-01-07，v1.0。HTTPS、Bearer Token、文件临时签名 URL。
- https://cloud.tencent.com/document/product/598/10592 《安全实践教程》，2025-04-11。CAM 最小权限、MFA、离职回收、职责分离。
- https://cloud.tencent.com/document/product/598/37140 《子账号访问密钥管理》，原记录版本2026-05-09。本轮访问失败、未取得正文；原初读取不能凭现有证据确认。四道关联题已更换来源，下列四项为实际补读正文。
- https://cloud.tencent.com/document/product/598/96157 《腾讯云 API 密钥升级公告》，2023-11-28。主账号、子账号均仅在创建时查看保存SecretKey。
- https://cloud.tencent.com/document/product/598/40488 《主账号访问密钥管理》，2026-05-09。已有主账号密钥禁用拒绝全部请求；API密钥两字段通用职责。
- https://cloud.tencent.com/document/product/598/82369 《删除访问密钥》，2025-09-12。按AccessKeyId删除密钥，删除不可恢复。
- https://cloud.tencent.com/document/product/598/19420 《角色概述》，2024-10-12。角色是虚拟身份，临时凭证，不持有固定密码。
- https://cloud.tencent.com/document/product/598/13665 《用户类型》，2023-08-25。实体子账号与消息接收人边界。
- https://cloud.tencent.com/document/product/598/14985 《新建用户组》，2024-10-12。同职能用户批量授权。
- https://cloud.tencent.com/document/product/598/38037 《限制 IP 访问》，2024-10-11。须产品支持 IP 条件，不外推 ADP 所有接口。
- https://cloud.tencent.com/document/product/598/10603 《元素参考概述》，2026-09-20。action/resource/condition/effect 各自含义。
- https://cloud.tencent.com/document/product/629/56259 《查看操作记录事件详情》，2026-07-23。请求 ID 与 CAM/API 错误字段区别；不保证覆盖全部 ADP 操作。
- https://cloud.tencent.com/document/product/598/65676 《下载安全分析报告》，2024-12-10。凭证状态报告和 MFA/登录安全字段。
- https://cloud.tencent.com/document/product/598/123925 《定期轮转访问密钥的安全建议》，2025-10-10。本轮重新打开核实正文：新子用户密钥替换业务使用后，禁用旧密钥、观察无异常再删除。M7-098明确考建议流程，不外推为所有删除API前置条件。

## 缺口/排除

隐私政策入口 104945 指向 rule.tencent.com/rule/202404080003，网页读取仅返回 JavaScript 提示，因此不编造数据留存期、不训练承诺或具体条文。课程付费内容及真实考题未获取。Schema 下架冲突不属本模块出题范围。安全实践文档为腾讯云通用实践，题干明确 CAM 上下文，不冒称 ADP 自动完成对应能力。题库作者状态保留 draft，待独立审校。
