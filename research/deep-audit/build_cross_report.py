#!/usr/bin/env python3
"""Join deterministic candidates with explicit AI decisions; no bank mutations."""
import json,hashlib,collections,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from scripts.validate_bank import content_hash
P=Path(__file__).resolve().parent
m=json.loads((P/'cross-bank-machine.json').read_text());qs=json.loads((P/'cross-bank-snapshot.json').read_text());by={x['id']:x for x in qs}
dec={}
for line in (P/'pair-ai-decisions.tsv').read_text().splitlines():
 i,code,note=line.split('\t',2);dec[int(i)]=(code,note)
labels={'D':'substantive_duplicate','O':'partial_overlap_needs_editorial_review','N':'distinct_judgment_despite_overlap'}
assert len(dec)==len(m['pairCandidates'])
rows=[]
for i,c in enumerate(m['pairCandidates'],1):
 code,note=dec[i];r=dict(c);r.update(candidateNumber=i,aiDecision=labels[code],aiExplanation=note,reviewer='safety',reviewMethod='AI阅读候选双方题干、正确选项与来源事实后判断认知任务；非人工专家；不代替各模块事实复核',contentHashes={id:content_hash(by[id]) for id in c['ids']},stems={id:by[id]['stem'] for id in c['ids']});rows.append(r)
weak_notes={
 'FDE-M2-034':'错误项A仅改名即成为企业共享、B同名知识库即共享，均与Skill审批链缺少合理关系；建议用审批状态与作用域易混项替代。',
 'FDE-M3-206':'D仅改旧文档名作为新版问答来源，不形成文档差异生成机制，属于容易排除的动作。',
 'FDE-M4-011':'B改名让旧功能自动成为新功能，明显不成立，与产品版本边界无合理竞争。',
 'FDE-M4-016':'C文件上传者头像与制度有效时间无关，是明确离题干扰。',
 'FDE-M4-145':'D把原文件改名为结果文件明显不等于数据清洗；B/C也直接违背题设产物要求，且本题另有跨模块重复。',
 'FDE-M6-069':'C只给源文档改名与生成问答采纳无关；B下载即采纳也较弱，宜改为待校验列表操作误区。',
 'FDE-M6-087':'C二维码替代所有API鉴权易排除，D公开AppKey也是基础禁忌，两个正确项几乎可凭常识筛出。'
}
lex_false={
 'FDE-M5-065':'题设本身是分类重命名期间的元数据更新，改名词是有效主题线索，不能按离题词剔除。',
 'FDE-M6-047':'昵称能否作为跨渠道身份线索与去重主题有关，D1为误报；三个错误项宽泛措辞仍需难度复核。',
 'FDE-M7-013':'展示昵称、会话ID与visitor_biz_id属于可混淆标识维度，昵称非离题。',
 'FDE-M7-016':'题目直接考唯一用户ID和重复昵称，昵称必须出现，词表误报。',
 'FDE-M7-099':'昵称作为公开展示值的对照仍与标识/秘密分工有关；偏基础但并非改头像式无关动作。'
}
priority={
 'FDE-M1-021':'干扰跨越训练权重、Token精确概率与事实性保证，正确项明显温和，应增强真实提示词误区。',
 'FDE-M1-025':'必须输出每个字、复制全部数据库与子Agent职责描述脱节，易排除。',
 'FDE-M1-064':'所有模型强制训练、替代全部文本、永久写权重三项过度承诺，与参考图生成并不接近。',
 'FDE-M2-005':'三干扰分别任意套餐/任意模型/免评测，正确项是唯一带条件的表述，存在措辞线索。',
 'FDE-M2-008':'三干扰均夸张绝对或授权豁免，不能据此模拟官方难度。',
 'FDE-M2-045':'名字/PU余额/自动升级三个对照均弱于真实套餐权益判断。',
 'FDE-M5-017':'全部贷款额度与替代风控等对照明显越界，缺少知识助手任务内的合理竞争。',
 'FDE-M5-018':'保证获利与自动改评级均可不依赖官方案例直接排除。',
 'FDE-M5-021':'反思越多永远最快和无需检查引用是显然错误，应换成成本/时延真实取舍。',
 'FDE-M5-028':'永久政策豁免、所有申请批准、无需再审三项极端；基础边界题难度不足。',
 'FDE-M5-029':'全市规则不明、完全无法衡量、无接口自动划拨皆明显违背有限试点，缺乏取舍。',
 'FDE-M5-045':'自动替全部部门批准、保证无人参与过于显眼，清单多选难度较低。',
 'FDE-M5-064':'只看文件名、自动维修全部车辆、无车型保证诊断三项脱离知识支持能力。',
 'FDE-M5-107':'药品审批和临床诊断与会议纪要场景相距较大，干扰可信度不足。',
 'FDE-M5-111':'保证注册、单批次代表全部、平均掩盖超标皆明显不合科学处理；建议加报告口径误区。',
 'FDE-M5-114':'无边界自由执行、替医生开处方与专业营销Agent矩阵不相近。',
 'FDE-M5-121':'自动全校开放、永久不可能等极端选项使建设状态识别偏易。',
 'FDE-M5-135':'未接入任意系统自动可用、未建设功能提示词交付，是通用夸张干扰。',
 'FDE-M5-141':'AI意见等同法院裁判、最终批准明显不合理，人工复核答案几乎只靠常识。',
 'FDE-M7-044':'所有任务成功、全部终端备份、全部模型合规三干扰职责跨度很大，建议更贴近调度认证边界。'
}
distractors=[]
for c in m['distractorCandidates']:
 id=c['id'];q=by[id]
 if id in weak_notes:status='clear_weak_distractor';note=weak_notes[id]
 elif id in lex_false:status='off_topic_lexicon_false_positive';note=lex_false[id]
 elif id in priority:status='difficulty_review_priority';note=priority[id]
 else:
  status='wording_candidate_not_automatic_failure'
  note='AI已阅读该候选选项：主题为“'+q['topic']+'”。所列绝对化词出现在错误选项，但主题内的权限、参数、版本边界本身可能是绝对规则；词命中不足以判该题无效，应结合模块复核及真实试答区分合理误区与送分干扰。'
 distractors.append(dict(c,aiDecision=status,aiExplanation=note,contentHash=content_hash(q),correctOptions={k:q['options'][k] for k in q['answer']},reviewer='safety'))
ex=json.loads((P/'cross-exclusions.json').read_text())
current=json.loads((ROOT/'data/questions.json').read_text());cur={q['id']:content_hash(q) for q in current}
changed=[q['id'] for q in qs if cur.get(q['id'])!=content_hash(q)]
report={
 'checkedAt':'2026-10-09','reviewer':'safety','method':'全1000题确定性候选扫描+AI逐候选认知任务判读；不调用模型/Embedding收费API；未修改题库。',
 'snapshot':{'file':'research/deep-audit/cross-bank-snapshot.json','sha256':m['snapshotSha256'],'questions':1000,'pairComparisons':m['pairComparisons'],'currentPublishedContentChangedIdsAtReport':changed},
 'artifactHashes':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['cross_bank_scan.py','pair-ai-decisions.tsv','cross-bank-machine.json']},
 'rules':{
 'R1':'标点归一化题干三字集合Jaccard>=0.26。',
 'R2':'正确选项合并文本二字集合Jaccard>=0.42；答案字母不参与。',
 'R3':'短考点二字集合Jaccard>=0.50且每方至少3个二字单元。',
 'R4':'至少共用一个来源URL，事实二字集合Jaccard>=0.40，或包含系数>=0.70且较短方至少8个单元。',
 'R5':'考点+题干+正确答案+支持事实的二字presence TF-IDF余弦>=0.44，idf=log((1001)/(df+1))+1。',
 'R6':'跨模块综合TF-IDF前50对补充检索，不设及格线。',
 'R7':'归一化题干最后8字相同且至少3题，仅提示同句式。',
 'R8':'12组公开语义术语锚点，每组须同时满足多组同义词条件；详见扫描脚本ANCHORS。按已知记忆改绑漏检加此召回通道，不能推断其对其他改写完备。',
 'D1':'错误选项含头像/背景色/二维码/改名/昵称/皮肤/主题色/字体/换颜色/深色模式/壁纸/浏览器缩放/桌面图标。',
 'D2':'至少2个错误选项含永远/永久/保证/必然/任何/全部/所有/自动/无需/不需/只需/完全/零成本/无限/100%/绝对。'
 },
 'summary':{'pairCandidates':len(rows),'crossModuleCandidates':sum(x['crossModule'] for x in rows),'pairAiDecisions':dict(collections.Counter(x['aiDecision'] for x in rows)),'distinctSecondaryIdsRecommendedLearningOnly':len(ex),'distractorCandidates':len(distractors),'distractorAiDecisions':dict(collections.Counter(x['aiDecision'] for x in distractors)),'templateCandidateGroups':len(m['templateCandidates'])},
 'knownRetiredRegression':m['knownRetiredRegression'],'blindCueProbe':m['blindCueProbe'],'templateCandidates':m['templateCandidates'],
 'pairReviews':rows,'distractorReviews':distractors,'exclusions':ex,
 'limits':[
 '没有公开或登录后实际可见的官方题干供对照；官方模拟仅说明页，未开始且未消耗机会。不能报告贴题率、官方题风接近程度或难度一致性。',
 '内部词面检索分数只用于挑候选，不是题目相似率、重复率或质量百分比。',
 '241对有AI说明，其余499259对只经过规则扫描，未逐对AI阅读；不能证明全库无其余语义重复。',
 'R8用已知漏检校准，只证明该回归样本能被捕获；跨语言、因果改写和未列术语仍可能漏检。',
 '203题为用词候选，不等于203道无效题。31题盲选探针中24题正确仅体现当前词表的措辞线索，不代表真实考生正确率。',
 'D类为AI确认认知任务相同的16对；O类只提出部分包含/近邻复核，不自动降级；N类只判该对不重复，不等于通过事实审校。',
 '本次跨库审计者也是M7及M4尾批作者，已披露此角色；各模块事实复核由其他代理承担，这不是人工专家或腾讯官方审核。',
 '报告绑定冻结快照；后续改题必须按ID内容hash重新核查。原题和历史不删除，排除仅建议影响新组卷。'
 ]}
(P/'cross-bank.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# 全库跨模块重复与干扰项审计','',f"日期：2026-10-09。冻结发布题库1000题，比较499500对；快照 SHA-256：`{m['snapshotSha256']}`。仅审计，没有改题。",'',
 '全库规则产生241对候选（102对跨模块），逐候选AI判读后：'+str(report['summary']['pairAiDecisions'])+'。明确16个次题建议降为仅学习，原题/ID/历史保留，见 `cross-exclusions.json`。部分重叠不自动视为重复。','',
 '规则、原始候选与每对解释在 `cross-bank.json` / `cross-bank-machine.json`；全文输入快照和 `pair-ai-decisions.tsv` 保留。此为AI审计，非人工专家审校。', '',
 '## 明确重复的次题建议','', '| 次题（仅学习） | 保留参照 | 判断依据 |','|---|---|---|']
for x in ex:lines.append(f"| {x['id']} | {x['duplicateOf']} | {x['reason']} |")
lines+=['','## 规则及可复现性','', '在项目根运行：','','```sh','python3 research/deep-audit/cross_bank_scan.py','python3 research/deep-audit/build_cross_report.py','```','', '扫描固定 `cross-bank-snapshot.json`，不会偷偷换成后续修订题库；需要新版本审计时另存快照并重新人工判断候选映射。决策TSV行号绑定本快照/规则，不得直接用于改动后的规则。','']
for k,v in report['rules'].items():lines.append(f'- **{k}**：{v}')
lines+=['','旧M1-060与M3-154的题干、答案、事实词面规则均漏掉；新R8记忆改绑术语锚点捕获该已知对照。这个反例说明，把近重复列表为空写成“无重复”不成立。旧060未算入本轮1000题。', '',
 '## 干扰项与题目难度','', f"203题命中用词候选；AI分级：{dict(collections.Counter(x['aiDecision'] for x in distractors))}。7题有明确弱干扰，20题建议优先难度复查，5题的离题词命中是主题相关误报；其余171题不因绝对词自动判失败。", '',
 '明确弱干扰：'+ '、'.join(weak_notes)+ '。例如M4-016用上传者头像干扰制度有效时间、M6-069用源文档改名干扰问答采纳。', '',
 '为检验措辞线索，另做不读题干的确定性探针：单选题只有一个选项完全不含D2词时选它，否则弃答。全库31题可选，24题答案吻合。这里只是词表触发后的内部探针，不能当真实考生表现，也不能据此给全库打难度分。', '',
 'R7仅找到1组末8字同句式，句式相同不等于目标重复；更有价值的是R8锚点及逐对检查。例如M4-223同时维护知识授权与记忆停用，和M1-058单问开关效果不同，未因共享来源降级。','',
 '## 覆盖边界','']
lines += ['- '+x for x in report['limits']]
lines+=['', '官方模拟访问说明见 `official-mock-visible.md`；未读取或辅助作答官方模拟题。本报告无官方题风/难度接近结论。开源准备清单见 `open-source-readiness.md`。','']
(P/'cross-bank.md').write_text('\n'.join(lines))
print(report['summary']);print('content changes since snapshot',changed)
