# M2 来源与冻结配额
核实：2026-10-09；作者 foundations_modes；目标70题（47单选/23多选）。

## 独立目标配额
- 平台定位与生产能力边界 10
- 四模式核心选择原则 16
- 模式切换与工作流关系 8
- Claw自主执行边界 8
- 知识库/连接器/工具/Skills之间关系 15
- 智能工作台与应用开发关系 7
- 开放生态、模型与套餐边界 6

## 已核官方来源
- https://cloud.tencent.com/document/product/1759/104193 产品概述，2026-06-15，企业应用平台、开放集成、全生命周期。
- https://cloud.tencent.com/document/product/1759/122549 智能体应用及其四种模式，2026-08-04，四模式、切换边界。
- https://cloud.tencent.com/document/product/1759/134194 什么是Claw模式，2026-07-15，独立执行空间、代码与Skills、工作流工具。
- https://cloud.tencent.com/document/product/1759/126433 使用流程，2026-07-03，轻量原型到生产、模式场景。
- https://cloud.tencent.com/document/product/1759/115872 连接器与工具介绍，2026-07-16，组件关系与扩展。
- https://cloud.tencent.com/document/product/1759/129561 Skills介绍，2026-07-14，专业能力及三种来源。
- https://cloud.tencent.com/document/product/1759/130637 对话功能概述，2026-06-22，工作台即用助手及产物。
- https://cloud.tencent.com/document/product/1759/123551 什么是知识库，2025-09-22，知识载体与应用关系。
- https://cloud.tencent.com/document/product/1759/132211 Agentic RAG，2026-08-21，使用边界。
- https://cloud.tencent.com/document/product/1759/122573 Multi-Agent示例，模式分工。
- https://cloud.tencent.com/document/product/1759/122572 单工作流示例，固定执行。
- https://cloud.tencent.com/document/product/1759/129200 套餐版本说明，功能与权益边界。
- https://cloud.tencent.com/document/product/1759/137902 对话式应用开发与调优，工作台与开发联动。
- https://cloud.tencent.com/document/product/1759/133868 动态配置概览，模型/插件/工具关系。

## 原则与不足
不将传统Chatbot一律描述为没有工具或没有记忆；只比较题设明确的固定问答机器人。默认模型、数字额度、套餐价格不是本模块重点，避免用易变数值扩题。旧三模式文档不代表当前模式全集。选型题是根据机制做的原创应用推理，不冒称考试原题。

## 最终修订清单（2026-10-09）

共70题；结构检查无错误、模块内题干近重复检测无命中。独立审校由 safety 完成，审校记录绑定内容哈希。

实际引用来源：

- [产品概述](https://cloud.tencent.com/document/product/1759/104193)；页面版本 2026-06-15
- [连接器与工具介绍](https://cloud.tencent.com/document/product/1759/115872)；页面版本 2026-07-16
- [套餐版本说明](https://cloud.tencent.com/document/product/1759/129200)；页面版本 2026-06-30
- [智能体应用及其四种模式](https://cloud.tencent.com/document/product/1759/122549)；页面版本 2026-08-04
- [使用流程](https://cloud.tencent.com/document/product/1759/126433)；页面版本 2026-07-03
- [什么是Claw模式？](https://cloud.tencent.com/document/product/1759/134194)；页面版本 2026-07-15
- [概览](https://cloud.tencent.com/document/product/1759/133868)；页面版本 2026-07-13
- [Skills介绍](https://cloud.tencent.com/document/product/1759/129561)；页面版本 2026-07-14
- [什么是知识库？](https://cloud.tencent.com/document/product/1759/123551)；页面版本 2025-09-22
- [对话功能概述](https://cloud.tencent.com/document/product/1759/130637)；页面版本 2026-06-22
- [对话式应用开发与调优](https://cloud.tencent.com/document/product/1759/137902)；页面版本 2026-09-21
- [基于Multi-Agent模式创建脱口秀素材创作助手](https://cloud.tencent.com/document/product/1759/122573)；页面版本 2026-06-30
- [基于单工作流模式创建网页内容总结助手](https://cloud.tencent.com/document/product/1759/122572)；页面版本 2026-06-30

最终独立考点：

- FDE-M2-001：定位/平台类别
- FDE-M2-002：定位/使用者范围
- FDE-M2-003：定位/业务系统集成
- FDE-M2-004：定位/从聊天到任务
- FDE-M2-005：定位/模型开放性
- FDE-M2-006：定位/端到端价值
- FDE-M2-007：定位/知识效果来源
- FDE-M2-008：定位/低代码边界
- FDE-M2-009：标准模式/双模型核心
- FDE-M2-010：标准模式/轻量起步
- FDE-M2-011：单工作流/全对话入口
- FDE-M2-012：单工作流/目标条件
- FDE-M2-013：MultiAgent/主动权
- FDE-M2-014：MultiAgent/团队分工
- FDE-M2-015：Claw/独立执行环境
- FDE-M2-016：模式/当前全集
- FDE-M2-017：模式切换/Claw迁出
- FDE-M2-018：模式切换/Claw迁入
- FDE-M2-019：模式切换/非Claw互转
- FDE-M2-020：模式切换/配置独立性
- FDE-M2-021：模式切换/资产范围
- FDE-M2-022：Claw/Skills区别
- FDE-M2-023：Claw/工具配额计数
- FDE-M2-024：Claw/工作流组合
- FDE-M2-025：Claw/创建入口
- FDE-M2-026：Claw/模型与成员
- FDE-M2-027：组件/插件与工具
- FDE-M2-028：组件/自定义扩展入口
- FDE-M2-029：组件/API封装
- FDE-M2-030：组件/代码工具
- FDE-M2-031：组件/应用工具调用边界
- FDE-M2-032：Skills/三类来源
- FDE-M2-033：Skills/自定义范围
- FDE-M2-034：Skills/企业共享关系
- FDE-M2-035：知识库/组件定位
- FDE-M2-036：知识库/三类知识
- FDE-M2-037：知识库/默认与共享
- FDE-M2-038：工作台/即用定位
- FDE-M2-039：工作台/历史任务
- FDE-M2-040：工作台/工作区
- FDE-M2-041：工作台/应用构建关系
- FDE-M2-042：工作台/开发模式覆盖
- FDE-M2-043：接入/API与界面
- FDE-M2-044：接入/应用与Agent
- FDE-M2-045：套餐/能力与权益
- FDE-M2-046：套餐/SkillPlan边界
- FDE-M2-047：套餐/Claw模式与ClawPro
- FDE-M2-048：模式/MultiAgent工作流编排边界
- FDE-M2-049：模式/标准与单工作流取舍
- FDE-M2-050：MultiAgent/转交关系生效
- FDE-M2-051：单工作流/结束与回复职责
- FDE-M2-052：Claw/动态配置作用域
- FDE-M2-053：模式/切换保留项
- FDE-M2-054：模式/知识消费路径
- FDE-M2-055：Claw/智能辅助配置与调试
- FDE-M2-056：工具/可调用契约
- FDE-M2-057：组件/MCP与API关系
- FDE-M2-058：工具/第三方服务评估责任
- FDE-M2-059：Skills/能力复用范围
- FDE-M2-060：Skills/场景与来源两个维度
- FDE-M2-061：定位/运行监控指标
- FDE-M2-062：定位/试点路径
- FDE-M2-063：工作台/产物边界
- FDE-M2-064：工作台/输入和资源
- FDE-M2-065：工作台/开发闭环范围
- FDE-M2-066：工作台/草稿线上边界
- FDE-M2-067：接入/开发与使用角色
- FDE-M2-068：接入/可视化与代码
- FDE-M2-069：套餐/有效期内PU用尽
- FDE-M2-070：套餐/升级与到期时间
