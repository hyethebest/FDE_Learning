# M3 来源与细粒度配额（冻结草案，2026-10-09）

目标 220 题（147 单选、73 多选）。作者 core_features。逐题标记 draft，独立审校前不算已通过。

|分区|目标|来源与已核章节|
|---|---:|---|
|知识库建立、文档与网页、问答、标签、切分、引用|50|123551 创建/删除；112702 导入/导入设置；112703 问答；112704 检索设置；由正文链接继续核切分、范围、问答生成|
|工作流节点与变量配置|70|112963 大模型；115747 意图识别；112964 知识问答；112965 标签提取；112966 检索；115756 选项卡；115750 循环；后续核参数/条件/代码/批处理等|
|MCP、API 与工具参数|30|117855 新建工具；115873 新建连接器；117856 使用工具；115748 连接器与工具节点|
|Skills 创建、打包、使用|25|129561 Skills 介绍；134602 文件规范；129562 新建；129563 使用|
|模型与变量、长期记忆|25|104206 应用设置；122458 长期记忆；138162 记忆库；后续核变量/模型页|
|发布、接入、版本边界、Agentic RAG|20|104209 发布；132211 Agentic RAG；123555 Schema（限存量历史语境）|

所有 URL 前缀为 https://cloud.tencent.com/document/product/1759/ ，正文精确 URL 和章节逐题保存。范围依据：https://cloud.tencent.com/document/product/658/137832 （2026-09-10）。

版本冲突：123555（2026-09-16）声明知识库 Schema 与检索 Agent 于 2026-08-27 下架，存量用户继续使用。不得把 Schema 写成新建应用必选步骤。112702 的知识生效范围规则较 104209 发布概述更新，题目不把知识变更一概写成必须发布。

事实与推理：配置字段、类型、状态来自正文；原创故障/配置选择题仅将这些事实应用到给定输入，不虚构产品保证。具体数额、容量只在正文一致且明确时使用；存在互相冲突的表格上限不出题。每页避免无穷变体，不抄课程或样题。

## 最终来源清单与作者自检

220题，147单选/73多选，220个独立题干与题号，全部仍为draft。下列37篇官方正文已联网核对。初稿无关干扰项已逐题人工改为同概念配置误区；106/107分别检查独立片段与累计全文的不同SSE解析，并改为不同任务表述。

- [什么是知识库？](https://cloud.tencent.com/document/product/1759/123551)：创建、管理与删除知识库；版本2026-10-09访问版本；5题。
- [文档概述](https://cloud.tencent.com/document/product/1759/112702)：导入文档与文档导入设置；版本2026-09-16；7题。
- [问答](https://cloud.tencent.com/document/product/1759/112703)：新建问答与问答操作；版本2026-02-06；7题。
- [知识检索相关设置](https://cloud.tencent.com/document/product/1759/112704)：且或关系与API参数映射；版本2026-02-26；6题。
- [文档切分设置](https://cloud.tencent.com/document/product/1759/122551)：文档切分功能介绍；版本2026-08-04；6题。
- [大模型节点](https://cloud.tencent.com/document/product/1759/112963)：操作说明；版本2026-08-18；6题。
- [大模型意图识别节点](https://cloud.tencent.com/document/product/1759/115747)：意图模式、意图与输出变量；版本2026-02-10；6题。
- [大模型标签提取节点](https://cloud.tencent.com/document/product/1759/112965)：标签、提示词与输出变量；版本2025-12-04；6题。
- [大模型知识问答节点](https://cloud.tencent.com/document/product/1759/112964)：知识问答与知识设置；版本2026-03-31；6题。
- [知识检索节点](https://cloud.tencent.com/document/product/1759/112966)：知识检索；版本2026-03-31；6题。
- [选项卡节点](https://cloud.tencent.com/document/product/1759/115756)：选择设置方式与用户交互形式；版本2026-01-13；6题。
- [循环节点](https://cloud.tencent.com/document/product/1759/115750)：循环体、循环方式与输出变量；版本2026-04-28；6题。
- [批处理节点](https://cloud.tencent.com/document/product/1759/119290)：批处理设置、输入与输出；版本2026-01-26；6题。
- [代码节点](https://cloud.tencent.com/document/product/1759/112967)：代码与输出变量；版本2026-06-01；6题。
- [条件判断节点](https://cloud.tencent.com/document/product/1759/112970)：设置条件与条件配置；版本2026-01-16；6题。
- [工作流节点](https://cloud.tencent.com/document/product/1759/115749)：引用工作流与常见问题；版本2026-01-29；6题。
- [连接器与工具节点](https://cloud.tencent.com/document/product/1759/115748)：输入参数与异常处理；版本2026-05-27；6题。
- [工具节点](https://cloud.tencent.com/document/product/1759/112968)：基础信息与调用方式；版本2026-01-06；6题。
- [新建连接器](https://cloud.tencent.com/document/product/1759/115873)：接入自定义连接器；版本2026-05-27；6题。
- [新建工具](https://cloud.tencent.com/document/product/1759/117855)：校验工具、基于已发布的应用创建；版本2026-08-20；6题。
- [使用工具](https://cloud.tencent.com/document/product/1759/117856)：调整工具、工作流；版本2026-10-09访问版本；6题。
- [Skills介绍](https://cloud.tencent.com/document/product/1759/129561)：Skills的三种类别；版本2026-07-14；6题。
- [新建Skills](https://cloud.tencent.com/document/product/1759/129562)：新建与管理自定义Skills；版本2026-07-20；6题。
- [Skills文件规范](https://cloud.tencent.com/document/product/1759/134602)：ZIP包基础约束与SKILL.md规范；版本2026-07-20；6题。
- [使用Skills](https://cloud.tencent.com/document/product/1759/129563)：智能工作台使用与Claw应用挂载；版本2026-09-10；6题。
- [记忆库](https://cloud.tencent.com/document/product/1759/138162)：记忆库类型与绑定规则；版本2026-09-15；6题。
- [应用发布概述](https://cloud.tencent.com/document/product/1759/104209)：发布历史、服务状态与发布渠道；版本2026-08-11；6题。
- [Agentic RAG](https://cloud.tencent.com/document/product/1759/132211)：操作步骤；版本2026-08-21；6题。
- [知识库Schema](https://cloud.tencent.com/document/product/1759/123555)：下架提示与创建方式；版本2026-09-16；3题。
- [模型介绍](https://cloud.tencent.com/document/product/1759/112876)：标准模式；版本2026-05-06；6题。
- [应用设置概述](https://cloud.tencent.com/document/product/1759/104206)：编辑应用与高级设置；版本2026-07-21；6题。
- [变量说明](https://cloud.tencent.com/document/product/1759/122457)：变量类型；版本2025-11-18；6题。
- [知识库标签设置](https://cloud.tencent.com/document/product/1759/112956)：相关名词解释与标签管理；版本2026-01-13；6题。
- [知识图谱GraphRAG](https://cloud.tencent.com/document/product/1759/128202)：知识图谱构建、查看与更新；版本2026-02-12；6题。
- [文档对比任务](https://cloud.tencent.com/document/product/1759/116451)：处理文档对比任务；版本2025-12-29；6题。
- [变量聚合节点](https://cloud.tencent.com/document/product/1759/117358)：聚合与输出变量；版本2025-08-17；6题。
- [参数提取节点](https://cloud.tencent.com/document/product/1759/112962)：收集参数与异常处理；版本2026-01-26；6题。

新增版本注意：新版138162将长期记忆改为记忆库×终端用户，并支持兼容模式应用共享；不采用122458的旧应用唯一隔离说法。GraphSchema与旧知识库Schema明确区分。标签修改发布规则与新知识生效范围存在潜在跨页差异，未出相关发布时序题。文档对比题不采用旧页的文档待发布状态要求，仅测试对比任务本身的行为。Skills文件规范FAQ与主规范的嵌套目录说明可能不一致，题目采用根目录入口的明确推荐结构，不出嵌套包一定拒绝之题。

覆盖缺口：未声称完全覆盖全部产品参数。发布渠道专门接入细节、数据库连接及高级运维配额较少；权限/合规与上线运维主要留给M7/M6。本模块以具体配置和数据流为主，未调用真实云API。独立审核前不可计入已通过数。

### 独立审校后新增目标（2026-10-09）
- 005：可下载文档 FileUrl/CosUrl 的二选一与优先级（112702）。
- 009：逐条/批量网页URL入口限制（112702）。
- 013/014/016：问答来源不可修改、审核中不可编辑、分类最多10层（112703）。
- 128/129：Skills场景分类中的平台构建运维与OCR字段提取（129561）。
- 158–163：触发受理实例与GET查询、不推送行为、立即运行不改调度、频率配置、触发器管理后果（104209）。
- 165：两类重排模型官方定位（132211）。
- 214：新增第38篇官方来源[变量赋值节点](https://cloud.tencent.com/document/product/1759/122550)，2025-08-17版本，2026-10-09核验；输出isSuccess与Error，区别业务值与赋值成功标志。
- 修订脚本分层：先M3-author.py，再M3-revise-root-001.py，再M3-revise-duplicates.py；勿在冻结审校后单独重跑旧作者脚本。


## 末轮独立审校修订记录（2026-10-09）
- `M3-revise-industry-final.py`：14题合理干扰及独立考点修订。117改为117855 OpenAPI的servers字段，166改为132211默认反思轮数与允许范围。
- `M3-revise-cross-final.py`：133改129562申请人审批进度与取消入口；164改104206意图达成优先级。均先联网读取精确章节，保留稳定ID与题型。
- 若需重建，须按M3-author.py → M3-revise-root-001.py → M3-revise-duplicates.py → M3-revise-industry-final.py → M3-revise-cross-final.py顺序；任何重建后独立审校hash须重新验证。正常升级请直接维护JSON，不重跑初始作者脚本。
