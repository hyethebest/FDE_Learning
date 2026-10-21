# M1 来源与冻结配额
核实：2026-10-09；作者 foundations_modes；目标100题（67单选/33多选）。

## 独立目标配额
- 大模型、生成与训练：10；Token与上下文：10；提示词：15；Embedding/召回/重排：15；RAG与图谱：15；Agent与工具：10；记忆与会话：10；多模态：10；幻觉与认知边界：5。
- 仅考概念机制，不考控制台配置或行业方案。场景推理标明由文档机制推导，不能当作腾讯逐字结论。

## 已核官方来源
- https://cloud.tencent.com/document/product/658/137832 考试指南，2026-09-10，限定模块范围。
- https://cloud.tencent.com/document/product/1759/104495 词汇表，2026-10-09，Token、AI Agent；词汇表包括其他产品，不将其中其他产品能力冒充ADP。
- https://cloud.tencent.com/document/product/851/109354 大模型广场，预训练与指令微调模型、垂直场景精调。
- https://cloud.tencent.com/document/product/851/123443 内置大模型训练数据格式，监督微调/预训练。
- https://cloud.tencent.com/document/product/1759/112963 大模型节点，2026-08-18，温度、Top_P、长度、系统/用户提示词、多模态。
- https://cloud.tencent.com/document/product/1759/106206 原子能力，2025-05-20，Embedding、指代消解、语义拆分、重排序。
- https://cloud.tencent.com/document/product/1772/115343 获取特征向量，输入文本与向量输出。
- https://cloud.tencent.com/document/product/1729/101838 数据结构，Usage区分输入与输出Token。
- https://cloud.tencent.com/document/product/1729/111007 兼容接口调用示例，上下文和图生文概念。
- https://cloud.tencent.com/document/product/1759/123551 什么是知识库，2025-09-22，RAG三个环节及知识类型。
- https://cloud.tencent.com/document/product/1759/132211 Agentic RAG，2026-08-21，反思与迭代检索、质量成本权衡。
- https://cloud.tencent.com/document/product/1759/128202 知识图谱，2026-02-12，实体属性关系与三元组。
- https://cloud.tencent.com/document/product/1759/135538 召回测试，2026-08-05，召回与答案生成区别。
- https://cloud.tencent.com/document/product/1759/115872 连接器与工具介绍，2026-07-16，外部工具与MCP。
- https://cloud.tencent.com/document/product/1759/134193 多Agent协同，角色、执行规则、协作规则。
- https://cloud.tencent.com/document/product/1759/134719 智能工作台长期记忆，2026-08-13，历史信息沉淀与上下文。
- https://cloud.tencent.com/document/product/1759/138162 记忆库，当前隔离维度。
- https://cloud.tencent.com/document/product/1729/106530 生图Prompt指南，文生图。
- https://cloud.tencent.com/document/product/1759/138789 调优准则，待完整展开支撑提示词与幻觉。

## 冲突和缺口
旧长期记忆122458称应用×用户隔离，新138162改为记忆库×用户；不依据旧文档编当前隔离题。暂不考未经官方页面支撑的Transformer结构、模型内部训练算法及概率数学。细粒度100目标将在题目topic唯一值中留存，无法证实的目标宁可报告缺口。

## 最终修订清单（2026-10-09）

共100题；结构检查无错误、模块内题干近重复检测无命中。独立审校由 safety 完成，审校记录绑定内容哈希。

实际引用来源：

- [大模型广场](https://cloud.tencent.com/document/product/851/109354)；页面版本 2026-06-04
- [内置大模型训练数据格式说明](https://cloud.tencent.com/document/product/851/123443)；页面版本 2025-11-19
- [什么是知识库？](https://cloud.tencent.com/document/product/1759/123551)；页面版本 2025-09-22
- [词汇表](https://cloud.tencent.com/document/product/1759/104495)；页面版本 2026-10-09
- [数据结构](https://cloud.tencent.com/document/product/1729/101838)；页面版本 2026-02-12
- [混元OpenAI兼容接口相关调用示例](https://cloud.tencent.com/document/product/1729/111007)；页面版本 2026-04-27
- [大模型节点](https://cloud.tencent.com/document/product/1759/112963)；页面版本 2026-08-18
- [Agentic RAG](https://cloud.tencent.com/document/product/1759/132211)；页面版本 2026-08-21
- [获取特征向量](https://cloud.tencent.com/document/product/1772/115343)；页面版本 2026-05-25
- [调优准则](https://cloud.tencent.com/document/product/1759/138789)；页面版本 2026-09-24
- [多Agent协同](https://cloud.tencent.com/document/product/1759/134193)；页面版本 2026-08-14
- [混元生图Prompt指南](https://cloud.tencent.com/document/product/1729/106530)；页面版本 2026-04-27
- [连接器与工具介绍](https://cloud.tencent.com/document/product/1759/115872)；页面版本 2026-07-16
- [原子能力](https://cloud.tencent.com/document/product/1759/106206)；页面版本 2025-05-20
- [知识库召回测试](https://cloud.tencent.com/document/product/1759/135538)；页面版本 2026-08-05
- [知识图谱GraphRAG](https://cloud.tencent.com/document/product/1759/128202)；页面版本 2026-02-12
- [智能工作台的长期记忆](https://cloud.tencent.com/document/product/1759/134719)；页面版本 2026-08-13
- [记忆库](https://cloud.tencent.com/document/product/1759/138162)；页面版本 2026-09-15
- [智能体应用及其四种模式](https://cloud.tencent.com/document/product/1759/122549)；页面版本 2026-08-04
- [变量说明](https://cloud.tencent.com/document/product/1759/122457)；页面版本 2025-11-18

最终独立考点：

- FDE-M1-001：大模型/部署与精调
- FDE-M1-002：大模型/垂直任务优化
- FDE-M1-003：大模型/下游任务
- FDE-M1-004：大模型/监督样本
- FDE-M1-005：大模型/角色设定
- FDE-M1-006：大模型/多轮样本
- FDE-M1-007：大模型/模型选择维度
- FDE-M1-008：大模型/训练与上下文
- FDE-M1-009：Token/基本单位
- FDE-M1-010：Token/中文切分
- FDE-M1-011：Token/输入输出
- FDE-M1-012：Token/历史开销
- FDE-M1-013：Token/上下文窗口
- FDE-M1-014：Token/最大回复
- FDE-M1-015：Token/输入输出口径
- FDE-M1-016：Token/额度与事实性
- FDE-M1-017：Token/推理开销
- FDE-M1-018：Token/向量化也有消耗
- FDE-M1-019：提示词/系统角色
- FDE-M1-020：提示词/用户请求
- FDE-M1-021：提示词/明确性
- FDE-M1-022：提示词/行为规则可复用
- FDE-M1-023：提示词/依据缺失
- FDE-M1-024：提示词/角色与协作
- FDE-M1-025：提示词/成员描述
- FDE-M1-026：提示词/产物规范
- FDE-M1-027：提示词/生图输入
- FDE-M1-028：提示词/任务输入与角色
- FDE-M1-029：提示词/工具描述
- FDE-M1-030：提示词/适用范围
- FDE-M1-031：Embedding/数值表示
- FDE-M1-032：Embedding/检索输入角色
- FDE-M1-033：Embedding/对称任务
- FDE-M1-034：检索/重排序作用
- FDE-M1-035：检索/指代消解
- FDE-M1-036：检索/文档解析
- FDE-M1-037：检索/语义拆分
- FDE-M1-038：检索/召回定义
- FDE-M1-039：检索/召回与生成分离
- FDE-M1-040：检索/结果可观察性
- FDE-M1-041：检索/关键词与语义
- FDE-M1-042：检索/向量与应用范围
- FDE-M1-043：RAG/基本含义
- FDE-M1-044：RAG/执行顺序
- FDE-M1-045：RAG/Agentic反思
- FDE-M1-046：RAG/成本速度权衡
- FDE-M1-047：RAG/知识图谱特色
- FDE-M1-048：知识图谱/实体
- FDE-M1-049：知识图谱/属性
- FDE-M1-050：知识图谱/关系
- FDE-M1-051：知识图谱/三元组
- FDE-M1-052：知识图谱/节点和边
- FDE-M1-053：记忆/个性化用途
- FDE-M1-054：记忆/当前关注
- FDE-M1-055：记忆/摘要可校准
- FDE-M1-056：记忆/新隔离维度
- FDE-M1-057：记忆/共享条件
- FDE-M1-058：记忆/关闭与删除
- FDE-M1-059：记忆/历史和记忆区别
- FDE-M1-060：记忆/更换存储范围
- FDE-M1-061：多模态/图生文
- FDE-M1-062：多模态/文生图
- FDE-M1-063：多模态/输入能力依赖
- FDE-M1-064：多模态/视觉理解与生成
- FDE-M1-065：多模态/音频任务差异
- FDE-M1-066：多模态/生成与检索
- FDE-M1-067：多模态/图片传递形式
- FDE-M1-068：Agent/能力构成
- FDE-M1-069：Agent/语言与行动
- FDE-M1-070：Agent/MCP定位
- FDE-M1-071：Agent/工具与连接器
- FDE-M1-072：Agent/主从分工
- FDE-M1-073：Agent/并行与协作
- FDE-M1-074：Agent/协调成本
- FDE-M1-075：Agent/成员选择信号
- FDE-M1-076：Agent/可调用契约
- FDE-M1-077：Agent/工作流关系
- FDE-M1-078：生成/温度方向
- FDE-M1-079：生成/TopP方向
- FDE-M1-080：训练/预训练与监督数据
- FDE-M1-081：生成/训练数据任务区分
- FDE-M1-082：Agent/调用与结果消息
- FDE-M1-083：提示词/要求拆分
- FDE-M1-084：提示词/要求冲突检查
- FDE-M1-085：提示词/视觉描述要素
- FDE-M1-086：检索/模型链路分工
- FDE-M1-087：检索/索引准备
- FDE-M1-088：RAG/反思与重排区别
- FDE-M1-089：RAG/适合迭代的问题
- FDE-M1-090：图谱/两类三元组
- FDE-M1-091：图谱/属性建模边界
- FDE-M1-092：记忆/摘要演进
- FDE-M1-093：上下文/当前问题与历史
- FDE-M1-094：记忆/冷启动与校准
- FDE-M1-095：多模态/理解任务分类
- FDE-M1-096：Embedding/正负样本
- FDE-M1-097：检索/证据获取故障
- FDE-M1-098：幻觉/相关性与真实性
- FDE-M1-099：幻觉/自动化反馈边界
- FDE-M1-100：RAG/零轮反思

## 固定种子审计后的题目退役与补充

2026-10-09：FDE-M1-060 因与 FDE-M3-154 重复考查改绑记忆库不迁移数据而退役。原题及旧内容哈希完整保存在 `research/retired-questions.json`，不复用其 ID。补充 FDE-M1-101（单选）考查 STS 句子对监督分数的含义，来源为 [内置大模型训练数据格式说明](https://cloud.tencent.com/document/product/851/123443) 的“语义文本相似度（STS）任务数据”，页面版本 2025-11-19，于 2026-10-09 联网核实。M1-081只考训练任务分类，本题考监督信号含义。独立审校记录：`research/reviews/M1-audit-replacement.json`，审校由 AI 完成，非人工专家审校。其余 99 题内容哈希保持不变。
