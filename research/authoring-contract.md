# 冻结题库合同 v1
每个模块写 data/batches/Mn.json，数组格式。总数与单多选配额见 blueprint.json。先研究官方文档再写题。任何无法直接支持的产品能力不编入。1000题是独立学习目标，不做名词替换扩量。
每题字段：id (FDE-M1-001 形式)、module (M1)、topic (细粒度考点)、type (single/multiple)、stem、options (对象A/B/C/D)、answer (字母数组)、explanation (详细解释)、distractors (对象，为每个错误选项解释原因)、difficulty (基础/进阶/综合)、sources (数组，每项 url/title/section/fact/verifiedAt/version)、review ({status:'draft',author:'...',reviewer:null,notes:[]})。
来源必须腾讯官方精确正文链接+章节，fact写简短中文转述支持事实，不批量复制原文。版本使用页面更新时间，无日期写“2026-10-09访问版本”。每个来源页衍生总结不超过200词，保持源多样性；同一事实不无限变体。
题干必须唯一、有明确可验证答案、干扰项合理且不能引入未核规则。正确项的位置应分散。多选2-3个正确项，避免所有题选同一组合。
模块之间避免重叠：M1概念原理；M2模式/边界选型；M3具体配置功能；M4客户需求到组件方案；M5行业交付情境；M6评测/上线/运维过程；M7权限/隐私/责任AI。
额外写 research/Mn-sources.md，列已核官方来源、覆盖与不足、事实/推理区分；先提交 sources 与子考点配额，随后分批写题。勿碰其它模块文件。
