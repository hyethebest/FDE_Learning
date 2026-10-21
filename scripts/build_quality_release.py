#!/usr/bin/env python3
"""Join independent AI audit rows without editing original question content or history."""
import json,hashlib,collections,csv,html
from validate_bank import content_hash
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def rows(obj):
 if isinstance(obj,list):return obj
 for key in ['questions','results','items','rows','audit']:
  if isinstance(obj.get(key),list):return obj[key]
 raise ValueError('缺少逐题数组')
files=['M1-M2.json','M3.json','M4.json','M5-M6.json','M7.json']
qs=read('data/questions.json'); audits=[]
for f in files:
 obj=read('research/deep-audit/'+f)
 for x in rows(obj):
  x=dict(x);x['auditFile']='research/deep-audit/'+f;audits.append(x)
a={x['id']:x for x in audits}
assert len(audits)==len(a)==1000 and set(a)=={q['id'] for q in qs}
for q in qs:
 x=a[q['id']];assert x['status'] in ['supported','needs_revision','unverified'];assert x['examUse'] in ['eligible','learning_only','hold'];assert x.get('rationale') and isinstance(x.get('sourceEvidence'),list)
 if x['status']=='unverified':x['examUse']='hold'
 if x['status']=='needs_revision' and x['examUse']=='eligible':x['examUse']='hold'
 assert x.get('contentHash',x.get('questionHash'))==content_hash(q)==q['review']['contentHash'],q['id']+' 审计哈希不匹配'
 x['contentHash']=q['review']['contentHash']
# Cross-module exclusions are separately explained and never erase stronger holds.
exclusions=read('research/deep-audit/cross-exclusions.json')
for x in exclusions:
 q=a[x['id']]
 if q['examUse']=='eligible':q['examUse']='learning_only'
 q['crossAudit']=x
 q['rationale']+='；跨模块复核：'+x['reason']
cross=read('research/deep-audit/cross-bank.json')
conservative=[]
for pair in cross['pairReviews']:
 if pair['aiDecision']=='partial_overlap_needs_editorial_review':
  id=sorted(pair['ids'])[-1]
  conservative.append({'id':id,'reason':'部分重叠尚待编辑区分（并非已判重复）：'+pair['aiExplanation']})
for item in cross['distractorReviews']:
 if item['aiDecision']=='clear_weak_distractor':conservative.append({'id':item['id'],'reason':'明确弱干扰项：'+item['aiExplanation']})
for item in conservative:
 x=a[item['id']]
 if x['examUse']=='eligible':
  x['examUse']='learning_only'
  x['rationale']+='；跨项保守处置：'+item['reason']
 x.setdefault('additionalCautions',[]).append(item['reason'])
(R/'research/deep-audit/conservative-exclusions.json').write_text(json.dumps(conservative,ensure_ascii=False,indent=2))
counts=collections.Counter(x['examUse'] for x in a.values())
quality={'version':'2026.10.09.3','checkedAt':'2026-10-09','reviewerType':'independent AI agents, not Tencent or human experts','bankSha256':hashlib.sha256((R/'data/questions.json').read_bytes()).hexdigest(),'counts':dict(counts),'questions':[a[q['id']] for q in qs]}
(R/'data/quality.json').write_text(json.dumps(quality,ensure_ascii=False,indent=2))
man=read('data/manifest.json');man.update(version=quality['version'],retained=1000,published=1000-counts['hold'],qualityCounts=dict(counts),notes=['深度审计为独立AI复核，不是腾讯或人工专家认证。','1000个原始题目及历史保留；分为可组卷、仅学习和待修订，数量见完整证据。','尚未取得官方模拟题正文，不能证明相同题风、难度或命中率。','不再以官方来源数量、题型配额或哈希审批等同命题合格。']);(R/'data/manifest.json').write_text(json.dumps(man,ensure_ascii=False,indent=2))
mod=[]
for m in read('research/blueprint.json')['modules']:
 group=[q for q in qs if q['module']==m['id']];c=collections.Counter(a[q['id']]['examUse'] for q in group)
 mod.append({**{k:m[k] for k in ['id','name','weight','quota'] if k in m},'total':len(group),'single':sum(q['type']=='single' for q in group),'multiple':sum(q['type']=='multiple' for q in group),'eligible':c['eligible'],'learning_only':c['learning_only'],'hold':c['hold']})
el=[q for q in qs if a[q['id']]['examUse']=='eligible'];gate={'passed':len(qs)==1000 and all(a[q['id']]['contentHash']==q['review']['contentHash'] for q in qs),'version':quality['version'],'total':1000,'counts':dict(counts),'modules':mod,'eligibleSingle':sum(q['type']=='single' for q in el),'eligibleMultiple':sum(q['type']=='multiple' for q in el),'canMake60QuestionPractice':sum(q['type']=='single' for q in el)>=40 and sum(q['type']=='multiple' for q in el)>=20,'sourceCountHistorical':len({s['url'] for q in qs for s in q['sources']}),'note':'通过的是1000条分级记录完整性门禁，不是1000道合格仿真题。'}
(R/'research/deep-audit/quality-gate.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2))
with (R/'research/deep-audit/逐题证据.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['ID','模块','题干','正确答案','内容状态','用途','理由','正文支持定位','难度问题','原内容哈希'])
 for q in qs:
  x=a[q['id']];w.writerow([q['id'],q['module'],q['stem'],'/'.join(q['answer']),x['status'],x['examUse'],x['rationale'],json.dumps(x['sourceEvidence'],ensure_ascii=False),json.dumps(x.get('difficultyConcern'),ensure_ascii=False),x['contentHash']])
print(json.dumps(gate,ensure_ascii=False,indent=2))
