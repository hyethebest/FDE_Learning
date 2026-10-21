#!/usr/bin/env python3
import json,html,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
q=read('data/questions.json'); quality=read('data/quality.json'); audit={x['id']:x for x in quality['questions']};gate=read('research/deep-audit/quality-gate.json');c=gate['counts']
root='.'
lines=['# 腾讯FDE题库迁移与实质证据报告','',f'版本2026.10.09.3；核验日期2026-10-09。正式位置：`{root}`。','',
'## 结论：可以证明相关，不能证明已经贴近真题','',
f'原始1000题完整保留。本轮逐题独立AI复核后，{c.get("eligible",0)}题可用于自编模拟练习，{c.get("learning_only",0)}题仅供知识学习，{c.get("hold",0)}题暂停作答与新组卷。这里的“可组卷”仍不代表腾讯认可或与正式考试等难。此前仅靠配额、文档数量与哈希批准，不能证明命题质量；本轮没有沿用“1000题都合格”的结论。','',
'有直接证据支持的是官方考试结构、大纲能力方向、逐题的部分产品事实及其版本。没有直接证据支持的是与官方题干相似、干扰项难度一致、推理步骤分布一致、命中率、通过率或真题覆盖率。没有伪造这些比例。','',
'## 官方依据与对照边界','',
'- [官方考试指南](https://cloud.tencent.com/document/product/658/137832)，2026-09-10版本，“基本信息”和“知识点占比与考核重点”：90分钟、40单选+20多选、70/100，多选漏选或错选零分。',
'- [官方认证详情](https://cloud.tencent.com/edu/training/cert/detail?type=CFD)，“理论考试”：单选1.5分、多选2分。此前本机Chrome正文已核，记录research/exam-evidence.md；本轮普通网页工具未返回此页，不能写成本轮该工具成功。',
'- [官方FDE指南文章](https://adp.tencent.com/zh/blog/adp-fde-certification-guide)，腾讯云ADP团队2026-09-17，“认证关注哪些能力”“官方学习资料与学习入口”：认证面向需求分析、方案设计、应用搭建、交付运营、安全合规，提供官方在线学习与模拟资源。',
'- [课程入口](https://cloud.tencent.com/edu/learning/course-4742-84527-84531)：公开工具本轮仅返回登录页框架，没有得到完整讲义。没有以社区作者文章替代官方认证依据。','',
'| 对照维度 | 已有证据 | 能作出的结论 |','|---|---|---|',
'| 考纲域 | 官方七域与权重 | 可以规划学习方向，不能证明每道题归类合理 |',
'| 题型、计分与时长 | 正式指南与认证详情 | 本地采用正式考试公开规则；不是25分钟官方练习卷复刻 |',
'| 腾讯术语及版本 | 对应产品正文 | 按逐题来源适用范围判断，须处理新旧页面冲突 |',
'| 场景约束与认知要求 | 官方能力描述＋自编题AI审查 | 可识别偏离交付目标、纯记忆或不充分场景，但不是官方难度标定 |',
'| 单选唯一最佳、多选完整集合 | 自编题选项检查＋正文事实 | 是内部命题检查，仍可能存在AI漏检 |',
'| 官方题干长度、推理步数、干扰合理性、难度 | 没有官方样题正文 | 无法比较，不能声称相似或命中 |','',
'## 考纲矩阵与实际可用范围','',
'七模块的100/70/220/250/150/110/100只是自定1000题训练配额，667/333也是训练库比例。官方并未说明每张60题试卷按七权重精确分配题数。软件采用尽量分配并在候选不足时补齐，不能把这一算法冒称官方出卷算法。','',
'| 模块 | 官方权重 | 原始单/多 | 原始总数 | 可组卷 | 仅学习 | 暂停 |','|---|---:|---:|---:|---:|---:|---:|']
for m,w in zip(gate['modules'],[10,7,22,25,15,11,10]):lines.append(f"| {m['id']} {m['name']} | {w}% | {m['single']}/{m['multiple']} | {m['total']} | {m['eligible']} | {m['learning_only']} | {m['hold']} |")
lines+=['',f"可组卷池含{gate['eligibleSingle']}单选、{gate['eligibleMultiple']}多选。数量是审计分类结果，不是官方正确率。",'',
'复核发现：M1部分训练格式、精调与GraphSchema操作偏离基础概念；M2部分具体购买/操作细节偏离定位与模式选择；M5若干行业页面小功能点或题干直接泄露答案，不能代替真实场景判断；M7部分CAM底层参数记忆不等于FDE安全方案能力。即使章节标签与配额相符，也不能据此宣称实质覆盖完整。逐题理由和降级记录见附表。','',
'## 本轮审计方法与完整逐题证据','',
'分工：industry_delivery审M1/M2，foundations_modes审M3，core_features审M4，solution_design审M5/M6，reviewer审M7；均非对应模块原作者。safety做跨库筛查与语义候选判别，root汇总并实现分级。这些都是同一AI系统的代理，不是人工专家或腾讯认证；结果可能仍有误判或漏检。','',
'复核逐题读取题干、选项、答案、解析与干扰理由，按官方正文核支持范围，并区分产品事实与工程推论。正文定位包含URL、标题/章节、短定位词或本次工具行号、事实释义、版本；行号随页面更新可变，不是永恒段落编号。无法重新取得正文且无充分替代证据的题标unverified/hold，不把访问失败直接判为事实错误。','',
'数据：`data/quality.json`包含1000条用途分级及当前原题哈希；`research/deep-audit/逐题证据.csv`可用表格软件筛选；M1-M2.json、M3.json、M4.json、M5-M6.json、M7.json保留分工审计原件。`data/questions.json`保留完整题干、选项、答案、解析与旧审校记录。`evidence.html`把原题和新证据逐条合并展示。','',
'程序门禁检查1000条记录完整覆盖、无重复ID、每行原题哈希一致、来源证据数组与分类字段齐备。它不能自动证明正文蕴含答案。旧发布时119个URL返回正文的访问记录保留；本轮无法复核的页面仍按hold处置，不以旧抓取成功代替新事实审查。','',
'本轮不是抽样代替全库：1000题均有分类记录。旧版固定种子20261009的21题样本、22条展示（含替代题）继续保存在题库审计报告.md，保留当时发现的重复和来源修订。','',
'## 重复、弱干扰与版本风险','',
'跨库机器规则与输入快照、所有候选和AI处置见cross_bank_scan.py、cross-bank-machine.json、cross-bank.json/md及cross-exclusions.json。比较题干/答案/来源事实词面、显式术语锚点、极端或离题干扰词；候选不是重复定论。已确认的16个实质重复次题降为仅学习；51对部分重叠尚待编辑区分，对每对按稳定ID排序的后项也采取保守降级，但不将其标成确定重复。7个明确弱干扰项同样排除新组卷；逐条见conservative-exclusions.json。没有使用全库嵌入向量语义模型，不能证明零重复；也没有将候选命中比例写成相似率。','',
'历史例子M1-060/M3-154曾被原字符阈值漏检；本轮又发现工具契约、关闭记忆不删除、MCP空工具列表、子工作流复用、JSON序列化、SkillHub更新、异步网页抓取限制等重复判断。保留所有原题和稳定ID，未通过删除失败题伪造1000道独立合格题。','',
'版本重点：Schema/知识检索Agent已停止新建而考纲仍列相关知识，旧创建教程不能当作当前操作规则；新版记忆按记忆库×终端用户隔离；标签/metadata过滤或软加权不能代替授权；平台新版高级数据权限可含应用发布开关，不能无条件套用旧权限分类描述。各题冲突与处理见逐题表。','',
'## 软件中的实际处理与进度兼容','',
'- eligible：可进入自编90分钟练习；仍显示难度未经官方样题校准。',
'- learning_only：可作概念学习，不进入新模拟卷。',
'- hold：普通学习与复习排除；错题/收藏中保留历史入口但禁用作答，不计新掌握。',
'- 未改写原1000题内容或复用退役ID；版本变化后旧作答不计新题掌握，原历史和收藏仍保存。历史试卷按开考快照保留分数，并提示旧卷可能含降级题，不能当作当前水平证据。','',
'本轮新增测试覆盖分级排除组卷与内容版本变化后掌握重置；现17项核心/保存测试、1项原子保存测试。真实浏览器迁移后验收见research/qa/browser-results.json，超时通过隔离测试截止时间触发，不声称实等90分钟。','',
'## 迁移与数据保全','',
f'新入口：`{root}/启动备考.command`。这是本地Web App，Python标准库服务仅监听127.0.0.1:8765。源码、题库、研究证据、测试和文档均在新目录；旧任务目录作为回滚副本保留，不再作为日常启动位置。', '',
'迁移前查明8765无监听、源local-data/progress.json不存在。因此没有发现可供迁移的真实磁盘学习记录；不能虚称已搬迁非空用户记录。保留原浏览器相同127.0.0.1:8765来源和应急缓存机制，不清除浏览器数据。8766仍有早期98题QA缓存页，未将其测试历史冒充用户进度，也未修改它。', '',
'迁移快照及逐文件SHA-256在research/migration/before.json、pre-migration-project.zip、snapshot-verification.json；复制与最终启动证明在copy-verification.json、final-verification.json。新服务health返回进程PID、真实ROOT和数据路径，以防旧目录服务冒充新目录。启动脚本遇到另一路径占用同端口会提示保存并关闭旧服务，不强杀。', '',
'真实进度路径：新目录local-data/progress.json（第一次保存后创建）。今后备份、错题、收藏由此文件和浏览器应急副本保护。迁移验证使用隔离临时数据实际生成错题/收藏/进度、备份去重与重启恢复；测试不写个人正式目录。','',
'回滚：先在界面导出学习备份、关闭当前终端服务；恢复pre-migration-project.zip到另一个新目录，保留/导入最新进度后再启动。不要同时启动新旧目录服务；旧质量未分级版本只用于取回数据，不建议继续用其分数备考。','',
'## 未来开源准备与尚未证实部分','',
'本任务没有推送GitHub，没有发布，也没有替你选定开源许可证。详见research/deep-audit/开源准备清单.md（若文件名不同，见open-source-readiness.md）。正式发布前须选择代码许可、核对第三方/图片来源、保留腾讯文档链接与事实引用边界，并清除个人学习记录、导出备份、浏览器缓存、绝对路径和本机运行信息。研究里有内部工具定位和AI工作稿，应筛选整理，不能把完整工作目录不经审核直接公开。','',
'最需要补足的是合法可读的官方练习样例对照与人工命题复审；本任务未取得样题正文，不能出具“非常贴近真实题目”的证明。建议以官方课程和平台实操为主，以本库经分级的题作补充，不能只凭本地70分判断已达到正式考试通过水平。','',
'## 全量审计索引','', '| ID | 用途 | 内容判断 | 复核理由 |','|---|---|---|---|']
for x in quality['questions']:lines.append('| '+ ' | '.join(str(v).replace('|','/').replace('\n',' ') for v in [x['id'],x['examUse'],x['status'],x['rationale']])+' |')
text='\n'.join(lines)+'\n';(R/'完整证据报告.md').write_text(text)
# A self-contained, searchable local evidence reader. No remote assets or requests.
h=html.escape
out=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FDE题库完整证据</title><style>body{font:16px/1.75 system-ui,sans-serif;max-width:1050px;margin:auto;padding:28px;color:#18332f;background:#f7faf8}a{color:#006b54}input{font:inherit;width:95%;padding:12px;position:sticky;top:8px}details{background:white;border:1px solid #cad8d2;padding:14px;margin:12px 0}summary{cursor:pointer;font-weight:650}.muted{color:#576963}pre{white-space:pre-wrap;overflow-wrap:anywhere}h1{font-size:30px}</style><body><a href="/">← 返回背题软件</a><h1>完整质量证据 · 2026.10.09.3</h1>']
# Keep narrative separate from 1000-row index already shown as searchable cards.
out.append('<details open><summary>结论、官方对照、考纲矩阵与迁移方法</summary><pre>'+h(text.split('## 全量审计索引')[0])+'</pre></details>')
out.append('<label>搜索题号、题干或问题原因<input id="find" placeholder="例如 M7-049、版本、干扰项"></label>')
for q0 in q:
 x=audit[q0['id']]
 out.append('<details class="question"><summary>'+h(q0['id']+' · '+x['examUse']+' · '+q0['stem'])+'</summary>')
 for k,v in q0['options'].items():out.append('<p>'+h(k+'. '+v)+'</p>')
 out.append('<p><b>原题答案：</b>'+h('、'.join(q0['answer']))+'</p><p>'+h(q0['explanation'])+'</p><p><b>本轮结论：</b>'+h(x['rationale'])+'</p><p>难度/干扰项：'+h(str(x.get('difficultyConcern','未提供')))+'</p>')
 if x.get('additionalCautions'):out.append('<p>附加风险：'+h('；'.join(x['additionalCautions']))+'</p>')
 out.append('<p><b>原题干扰项解释：</b>'+h('；'.join(k+'：'+v for k,v in q0['distractors'].items()))+'</p>')
 for e in x['sourceEvidence']:
  out.append('<p><a href="'+h(e.get('url',''))+'" target="_blank" rel="noopener">'+h(e.get('url',''))+'</a></p><pre>'+h(json.dumps({k:v for k,v in e.items() if k!='url'},ensure_ascii=False,indent=2))+'</pre>')
 out.append('<p class="muted">独立AI审计原件：'+h(x['auditFile'])+'；题目内容哈希：'+h(x['contentHash'])+'</p></details>')
out.append('<script>document.querySelector("#find").addEventListener("input",e=>{const s=e.target.value.toLowerCase();document.querySelectorAll(".question").forEach(d=>d.hidden=!d.textContent.toLowerCase().includes(s))});</script></body></html>')
(R/'evidence.html').write_text(''.join(out));print('完整证据报告.md + evidence.html')
