import json, hashlib, pathlib, collections
root=pathlib.Path(__file__).resolve().parents[2]
base=root/'research/deep-audit'
versions={'104208':'2026-01-20','135538':'2026-08-05','104209':'2026-08-11','130990':'2026-06-30','104210':'2026-09-24','138789':'2026-09-24','112702':'2026-09-16','112703':'2026-02-06','122551':'2026-08-04','138380':'2026-09-18','138240':'2026-09-18','128202':'2026-02-12','132211':'2026-08-21','104195':'2025-05-20','97822':'2025-09-02','government-enterprise-ai-agents-practice':'2026-09-09','retail-ai-assistant-agent-solution':'2026-07-31'}
questions={q['id']:q for m in ['M5','M6'] for q in json.loads((root/f'data/batches/{m}.json').read_text())}
rows=[]
for line in (base/'M5-M6-audit-notes.tsv').read_text().splitlines():
 if not line or line.startswith('#'):continue
 m,n,use,locator,fact,rationale,difficulty,duplicate=line.split('|')
 q=questions[f'FDE-{m}-{int(n):03}']
 evidence=[]
 for s in q['sources']:
  loc=locator; f=fact
  if q['id']=='FDE-M6-107':
   if s['url'].endswith('112702'):loc='文档操作／文档状态 L296–317';f='失败或失效文档不能问答'
   else:loc='功能说明／超过有效时间的生效策略 L161–165';f='超期可配置继续参与检索'
  evidence.append({'url':s['url'],'section':loc.split(' L')[0],'locator':loc,'shortFact':f,'version':versions.get(s['url'].rsplit('/',1)[-1],'页面未标更新日；2026-10-09访问'),'verifiedAt':'2026-10-09','method':'直接阅读腾讯官方公开页面正文；非搜索摘要替代'})
 canonical={k:v for k,v in q.items() if k!='review'}
 rows.append({'id':q['id'],'status':'needs_revision' if use=='H' else 'supported','examUse':{'E':'eligible','L':'learning_only','H':'hold'}[use],'rationale':rationale,'sourceEvidence':evidence,'difficultyConcern':difficulty,'duplicateGroup':None if duplicate=='-' else duplicate,'examAlignment':{'guideUrl':'https://cloud.tencent.com/document/product/658/137832','guideVersion':'2026-09-10','guideLocator':'考试范围：行业典型痛点、方案与交付边界（M5）' if m=='M5' else '考试范围：数据准备、验收、评估、排障、迭代、培训和运营（M6）','questionTopic':q['topic'],'claimLimit':'仅证明模块层级关联；官方未公开逐题考点、难度或真题相似度。'},'reviewer':'solution_design（独立AI审校，非原作者、非腾讯官方或人工专家）','auditedAt':'2026-10-09','questionHash':hashlib.sha256(json.dumps(canonical,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
assert len(rows)==260 and len({r['id'] for r in rows})==260
assert set(questions)=={r['id'] for r in rows}
rows.sort(key=lambda r:r['id'])
(base/'M5-M6.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
counts={m:dict(collections.Counter(r['examUse'] for r in rows if r['id'].startswith('FDE-'+m))) for m in ['M5','M6']}
summary={'scope':'M5全部150题及M6全部110题','reviewer':'solution_design / 独立AI审校，非腾讯官方或人工专家','date':'2026-10-09','counts':counts,'totalByStatus':dict(collections.Counter(r['status'] for r in rows)),'totalByExamUse':dict(collections.Counter(r['examUse'] for r in rows)),'definitions':{'supported':'题干限定下的产品事实及答案可由所列官方材料支持，或解析明确为合理工程推理；不代表题目质量通过。','needs_revision':'当前题干/答案/证据范围不一致，需要修改并重新审阅。','unverified':'未取得足够官方直接证据；本批未使用该标签。','eligible':'本次AI审计认为可作为模块内基础模拟候选；不是官方真题或难度认证。','learning_only':'事实可学，但弱干扰、原词泄题、非核心细节或重复判断使其不应计入有效模拟题配额。','hold':'在修订前不纳入考试及可信题数。','duplicateGroup':'审阅发现同目标或组合重复的关联记录；不表示组内任意两题完全相同，请结合各题rationale判断。'},'method':['逐题阅读题干、全部选项、正确答案、解析与干扰项说明。','直接重新打开题目涉及的23个腾讯官方公开来源，并核对2026-09-10版FDE指南的模块范围。','未用题目原有review标签作为证据；sourceEvidence由本次读到正文定位填写。','审计只产出研究报告，未修改题库。','未登录课程、运行腾讯真实应用或接触真题；无官方/人工专家认定，也未做考生实测区分度统计。'],'sourceCount':len({e['url'] for r in rows for e in r['sourceEvidence']}),'inputFileSha256':{m:hashlib.sha256((root/f'data/batches/{m}.json').read_bytes()).hexdigest() for m in ['M5','M6']},'questionHashAlgorithm':'SHA256(JSON of question excluding review; UTF-8, ensure_ascii=False, sort_keys=True, separators=(comma,colon))','holdItems':[r['id'] for r in rows if r['examUse']=='hold'],'followUp':['优先重写弱干扰为同一业务阶段的可比较方案，并加真实限制条件。','将案例品牌、产品宣传页小细节和当前建设中状态移入阅读补充，不用其数量补齐模拟题。','重复题组保留一个代表性判断，后续题必须增加实质不同的根因或配置约束。','重新设计题目后再核事实、答案唯一性及整体考纲配额；不能因初审有来源而恢复为有效题。']}
(base/'M5-M6-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
