from pathlib import Path
import json,hashlib,collections
BASE=Path(__file__).resolve().parent;APP=BASE.parents[1]
def read(p):return json.loads(p.read_text())
old={q['id']:q for q in read(BASE/'before/questions.json')};bank=read(APP/'data/questions.json');new={q['id']:q for q in bank}
r=read(APP/'data/rounds.json')['rounds'][0];audit=read(APP/'data/quality.json');ledger=read(APP/'research/original400/review-ledger.json')['questions']
def h(q):return hashlib.sha256(json.dumps({k:v for k,v in q.items() if k!='review'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert len(bank)==len(new)==1000 and set(new)==set(old)
ids=set(r['recheckedOriginalIds']);assert len(ids)==400 and ids==set(r['retainedCoreIds'])=={q['id'] for q in ledger}
changed={i for i in ids if h(old[i])!=h(new[i])};assert len(changed)==118 and changed==set(r['revisedOriginalIds'])
assert all(new[i]==old[i] for i in new if i not in ids)
for q in bank:
 assert set(q['answer'])<=set(q['options']) and len(set(q['answer']))==len(q['answer']),q['id']
 assert set(q['distractors'])==set(q['options'])-set(q['answer']),q['id']
 if q['type']=='single':assert len(q['answer'])==1
 if q['id'] in ids:
  assert q['answer']==old[q['id']]['answer'] and q['type']==old[q['id']]['type']
  assert q['review']['contentHash']==h(q)
for a in audit['questions']:
 if a['id'] in ids:assert a['questionHash']==a['contentHash']==h(new[a['id']])
assert audit['bankSha256']==hashlib.sha256((APP/'data/questions.json').read_bytes()).hexdigest()
assert collections.Counter(a['examUse'] for a in audit['questions'])=={'eligible':500,'learning_only':458,'hold':42}
assert len(set(r['coreIds']))==500 and ids|set(r['revisedIds'])==set(r['coreIds'])
export=read(APP/'data/core500-export.json');assert export['questions']==[q for q in bank if q['id'] in r['coreIds']]
assert len(set(q['stem'] for q in export['questions']))==500
result={'version':export['version'],'reviewed':400,'changedContent':118,'unchangedOriginalContent':282,'otherQuestionsUnchanged':600,'sourceUrlCount':len(set(s['url'] for i in ids for s in new[i]['sources'])),'checks':['1000题号完整且不重复','400题复核记录与原集合完全对应','118题真实内容变化、282题内容哈希保留','其他600题原样保留','答案存在、单选唯一、全部干扰项逐一匹配','原400题答案字母及题型保持','内容哈希与质量文件整库哈希一致','500/458/42分级及核心导出一致','核心题无完全重复题干']}
(APP/'research/original400/data-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
